from database import db
from datetime import datetime
from flask_login import UserMixin
import pytz

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='buyer')  # 'seller', 'buyer', 'admin'

    # Relationships
    auctions = db.relationship('Auction', backref='seller', lazy=True)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def __repr__(self):
        return f'<User {self.username} - {self.role}>'

    def __str__(self):
        return f"ID: {self.id}, Username: {self.username}, Email: {self.email}, Role: {self.role}"


# Auction Model
class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_price = db.Column(db.Numeric(10, 2), nullable=False)
    current_price = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(200))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='ongoing')

    # Relationships
    bids = db.relationship('Bid', backref='auction', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Auction {self.item_name} - {self.status}>'
    
    def __str__(self):
        return (
            f"ID: {self.id}, Item: {self.item_name}, Start Price: {self.start_price}, "
            f"Current Price: {self.current_price}, Status: {self.status}, "
            f"Start Time: {self.start_time}, End Time: {self.end_time}"
        )

    def to_dict(self):
        eat_tz = pytz.timezone('Africa/Nairobi')
        end_time_aware = eat_tz.localize(self.end_time) if self.end_time else None
        
        return {
            'id': self.id,
            'item_name': self.item_name,
            'description': self.description,
            'current_price': float(self.current_price),
            'start_price': float(self.start_price),
            'end_time': end_time_aware.isoformat() if end_time_aware else None,
            'seller_id': self.seller_id,
            'status': self.status
        }


# Bid Model
class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'), nullable=False)  # Link to the auction
    bidder_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the bidder
    bid_amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Bid {self.id} - Auction {self.auction_id} - Amount {self.bid_amount}>'

    def __str__(self):
        return f"ID: {self.id}, Auction ID: {self.auction_id}, Bidder ID: {self.bidder_id}, Amount: {self.bid_amount}, Timestamp: {self.timestamp}"