from flask import request, jsonify, abort, current_app
from app import app, db, socketio
from models import User, Auction, Bid
from flask_login import current_user, login_required
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone
from flask_socketio import join_room, leave_room  # Import these functions
import pytz
from sqlalchemy import text
from werkzeug.security import check_password_hash
from flask_cors import cross_origin

# Route to get auctions with optional filtering
@app.route('/api/auctions', methods=['GET'])
def get_auctions():
    try:
        print("\n=== DEBUG: Starting auction fetch ===")
        
        # Get all auctions
        auctions = Auction.query.filter_by(status='ongoing').all()
        print(f"Found {len(auctions)} ongoing auctions")
        
        auction_list = []
        for auction in auctions:
            auction_data = {
                'id': auction.id,
                'item_name': auction.item_name,
                'description': auction.description,
                'current_price': float(auction.current_price),
                'start_price': float(auction.start_price),
                'end_time': auction.end_time.isoformat() if auction.end_time else None,
                'seller_id': auction.seller_id,
                'status': auction.status
            }
            auction_list.append(auction_data)
            print(f"Added auction: {auction_data}")
        
        return jsonify({
            'auctions': auction_list,
            'message': f'Found {len(auction_list)} active auctions'
        })

    except Exception as e:
        print(f"Error in get_auctions: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Route to place a bid
@app.route('/bids', methods=['POST'])
@login_required
def place_bid():
    if current_user.role != 'buyer':
        return jsonify({"error": "Only buyers can place bids"}), 403

    data = request.json

    # Validate auction
    auction = Auction.query.get(data.get('auction_id'))
    if not auction or auction.end_time <= datetime.utcnow():
        return jsonify({"error": "Auction not available or has ended"}), 400

    if data.get('bid_amount') <= auction.current_price:
        return jsonify({"error": "Bid must be higher than the current price"}), 400

    # Create a new bid
    bid = Bid(
        auction_id=auction.id,
        bidder_id=current_user.id,
        bid_amount=data.get('bid_amount')
    )
    auction.current_price = data.get('bid_amount')
    db.session.add(bid)
    db.session.commit()

    # Emit real-time update to the specific auction room
    socketio.emit('new_bid', {
        "auction_id": auction.id,
        "current_price": auction.current_price
    }, room=f"auction_{auction.id}")

    return jsonify({"message": "Bid placed successfully!"})

# Route to join an auction room (for WebSocket clients)
@socketio.on('join')
def on_join(data):
    auction_id = data.get('auction_id')
    if auction_id:
        room = f"auction_{auction_id}"
        join_room(room)

# Route to leave an auction room (for WebSocket clients)
@socketio.on('leave')
def on_leave(data):
    auction_id = data.get('auction_id')
    if auction_id:
        room = f"auction_{auction_id}"
        leave_room(room)

# Route to get bid history for an auction
@app.route('/auction/<int:auction_id>/bids', methods=['GET'])
def get_bid_history(auction_id):
    bids = Bid.query.filter_by(auction_id=auction_id).order_by(Bid.bid_amount.desc()).all()
    if not bids:
        return jsonify({"message": "No bids for this auction"}), 404

    return jsonify([{
        "bid_id": bid.id,
        "bid_amount": bid.bid_amount,
        "bidder_id": bid.bidder_id,
        "timestamp": bid.timestamp
    } for bid in bids])

@app.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        # Try to create a test auction
        test_auction = Auction(
            item_name="Test Item",
            description="Test Description",
            start_price=100.00,
            current_price=100.00,
            seller_id=3,  # Make sure this matches an existing user ID
            end_time=datetime(2024, 12, 31, 23, 59, 59),
            status='ongoing'
        )
        
        # Add and commit the test auction
        db.session.add(test_auction)
        db.session.commit()
        
        # Query all auctions
        all_auctions = Auction.query.all()
        
        # Format the results
        auctions_data = [{
            'id': auction.id,
            'item_name': auction.item_name,
            'current_price': float(auction.current_price),
            'end_time': auction.end_time.isoformat() if auction.end_time else None,
            'status': auction.status
        } for auction in all_auctions]
        
        return jsonify({
            'message': 'Database test successful',
            'test_auction_created': True,
            'all_auctions': auctions_data
        })
        
    except Exception as e:
        current_app.logger.error(f"Database test error: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'Database test failed'
        }), 500

@app.route('/api/debug', methods=['GET'])
def debug_database():
    try:
        # Try raw SQL query
        result = db.session.execute('SELECT * FROM auction').fetchall()
        auctions_raw = [{
            'id': row[0],
            'item_name': row[1],
            'description': row[2],
            'current_price': float(row[4]),
            'status': row[9]
        } for row in result]
        
        # Try ORM query
        auctions_orm = Auction.query.all()
        auctions_orm_data = [{
            'id': a.id,
            'item_name': a.item_name,
            'description': a.description,
            'current_price': float(a.current_price),
            'status': a.status
        } for a in auctions_orm]
        
        return jsonify({
            'database_connection': 'success',
            'raw_sql_count': len(auctions_raw),
            'raw_sql_results': auctions_raw,
            'orm_count': len(auctions_orm_data),
            'orm_results': auctions_orm_data,
            'table_name': Auction.__table__.name,
            'db_uri': db.engine.url.render_as_string(hide_password=True)
        })
    except Exception as e:
        import traceback
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

# Add an error handler for unauthorized access
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error': 'Unauthorized access',
        'message': 'Please log in to access this resource'
    }), 401

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.get_json()
        print("Received login data:", data)
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing email or password'}), 400

        user = User.query.filter_by(email=data['email']).first()
        print(f"Found user: ID: {user.id if user else None}, Email: {data['email']}")

        if user and user.password == data['password']:
            print(f"Login successful for user: {user.email}")
            return jsonify({
                'message': 'Login successful',
                'redirect_url': '/auctions'
            })
        else:
            print("Login failed: Invalid credentials")
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500