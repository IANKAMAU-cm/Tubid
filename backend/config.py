import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Change this to a secure secret key
    SQLALCHEMY_DATABASE_URI = 'mysql://ian:ian@localhost/auction_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Add debug settings
    DEBUG = True
    SQLALCHEMY_ECHO = True  # This will log all database operations 