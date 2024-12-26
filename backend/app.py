from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify, make_response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from models import User, Auction, Bid
from forms import RegistrationForm, LoginForm
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime
from dateutil.relativedelta import relativedelta
from database import db
from werkzeug.security import check_password_hash
import os
from werkzeug.utils import secure_filename
from config import Config

# Initialize Flask app
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    
    # Use a consistent secret key
    app.secret_key = 'your-secret-key-here'  # Replace with a real secret key in production

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ian:ian@localhost/auction_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Update CORS configuration
    CORS(app, 
         resources={
             r"/*": {  # Match all routes
                 "origins": ["http://localhost:3000"],  # Your React app's URL
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })
    
    # Session configuration
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="http://localhost:3000")

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

app = create_app()

# Socket.IO event handler
@socketio.on('connect')
def handle_connect():
    print("A client has connected!")

# Register routes
from routes import *

# Register routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'All fields are required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password.decode('utf-8'),
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 201

# Login route
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
        
    try:
        data = request.get_json()
        print("Received login data:", data)  # Debug print
        
        if not data or 'email' not in data or 'password' not in data:
            print("Missing email or password in request")  # Debug print
            return jsonify({'message': 'Email and password are required'}), 400

        user = User.query.filter_by(email=data['email']).first()
        print("Found user:", user)  # Debug print
        
        if user and bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            print("Login successful for user:", user.email)  # Debug print
            response = jsonify({
                'message': 'Login successful',
                'redirect_url': '/seller_dashboard' if user.role == 'seller' else '/auctions'
            })
            return response, 200
        else:
            print("Invalid credentials for email:", data['email'])  # Debug print
            return jsonify({'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print("Login error:", str(e))  # Debug print
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

# Logout route
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Admin dashboard route
@app.route('/api/admin_dashboard', methods=['GET'])
def admin_dashboard():
    # Ensure only admins can access this page
    if not current_user.is_authenticated or current_user.role != 'admin':
        return redirect(url_for('login'))
    # Display admin options like managing everything
    return jsonify({'message': 'Welcome to the admin dashboard', 'data': {}})

# Seller dashboard route
@app.route('/api/seller_dashboard', methods=['GET'])
def seller_dashboard():
    # Ensure only sellers can access this page
    if not current_user.is_authenticated or current_user.role != 'seller':
        return redirect(url_for('login'))
    # Display seller-specific options like adding items for auction
    return jsonify({'message': 'Welcome to the seller dashboard', 'data': {}})

# Buyer dashboard route
@app.route('/api/auctions', methods=['GET'])
def get_auctions():
    try:
        auctions = Auction.query.filter_by(status='ongoing').all()
        auction_list = []
        for auction in auctions:
            auction_list.append({
                'id': auction.id,
                'item_name': auction.item_name,
                'description': auction.description,
                'current_price': float(auction.current_price),
                'start_price': float(auction.start_price),
                'end_time': auction.end_time.isoformat() if auction.end_time else None,
                'seller_id': auction.seller_id,
                'status': auction.status
            })
        
        return jsonify({
            'auctions': auction_list,
            'message': 'Welcome to the Buyer Dashboard'
        })

    except Exception as e:
        print(f"Error in get_auctions: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/add-auctions', methods=['POST'])
@login_required
def add_auctions():
    try:
        data = request.get_json()
        
        # Create new auction
        new_auction = Auction(
            item_name=data['item_name'],
            description=data['description'],
            start_price=float(data['start_price']),
            current_price=float(data['start_price']),  # Set current price to start price initially
            end_time=datetime.fromisoformat(data['end_time']),
            seller_id=current_user.id,  # Add the seller's ID
            status='ongoing'
        )
        
        db.session.add(new_auction)
        db.session.commit()
        
        return jsonify({"message": "Auction added successfully", "auction_id": new_auction.id}), 200
    except Exception as e:
        print(f"Error adding auction: {str(e)}")  # Add logging for debugging
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/api/test-auth', methods=['GET'])
@login_required
def test_auth():
    return jsonify({
        'authenticated': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'role': current_user.role
        }
    })

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    