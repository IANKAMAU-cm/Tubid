from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from config import Config

# Create a test app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)

def test_connection():
    try:
        # Test the connection
        with app.app_context():
            # Try to execute a simple query
            result = db.session.execute(text('SELECT 1')).scalar()
            print("Database connection successful!")
            
            # Check auction table
            result = db.session.execute(text('SELECT COUNT(*) FROM auction')).scalar()
            print(f"Found {result} auctions in database")
            
            # Get all auctions
            auctions = db.session.execute(text('SELECT * FROM auction')).fetchall()
            print("\nAuctions in database:")
            for auction in auctions:
                print(f"- ID: {auction[0]}, Name: {auction[1]}, Status: {auction[9]}")
            
            # Get table details
            tables = db.session.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'auction_db'")
            ).fetchall()
            print("\nAvailable tables:")
            for table in tables:
                print(f"- {table[0]}")
                
    except Exception as e:
        print(f"Error connecting to database: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_connection() 