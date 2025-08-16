import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal, create_tables
from .models import Movie, ApiKey, generate_api_key
import os

def migrate_csv_to_database(csv_path: str = "data/movies.csv"):
    """Migrate CSV data to PostgreSQL database."""
    
    # Create tables if they don't exist
    create_tables()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if movies already exist
        existing_count = db.query(Movie).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} movies. Skipping migration.")
            return
        
        # Load CSV data
        if not os.path.exists(csv_path):
            print(f"CSV file not found at {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        print(f"Loading {len(df)} movies from {csv_path}")
        
        # Insert movies into database
        for _, row in df.iterrows():
            # Check for duplicates by title + year
            existing_movie = db.query(Movie).filter(
                Movie.title == str(row['title']),
                Movie.year == int(row['year'])
            ).first()
            
            if existing_movie:
                print(f"Skipping duplicate: {row['title']} ({row['year']})")
                continue
            
            movie = Movie(
                id=int(row['id']),
                title=str(row['title']),
                year=int(row['year']),
                genre=str(row['genre']),
                director=str(row['director']),
                actors=str(row['actors']),
                plot=str(row['plot']),
                poster_url=str(row['poster_url'])
            )
            db.add(movie)
        
        db.commit()
        print(f"Successfully migrated {len(df)} movies to database")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_test_api_keys():
    """Create test API keys for development."""
    db = SessionLocal()
    
    try:
        # Check if API keys already exist
        existing_count = db.query(ApiKey).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} API keys.")
            return
        
        # Create test API keys
        test_keys = [
            {"owner_name": "Test Developer 1", "plan": "free", "monthly_limit": 1000},
            {"owner_name": "Test Developer 2", "plan": "free", "monthly_limit": 1000},
            {"owner_name": "Admin User", "plan": "premium", "monthly_limit": 10000},
        ]
        
        for key_data in test_keys:
            api_key = ApiKey(
                owner_name=key_data["owner_name"],
                key=generate_api_key(),
                plan=key_data["plan"],
                monthly_limit=key_data["monthly_limit"]
            )
            db.add(api_key)
        
        db.commit()
        
        # Print created keys for testing
        all_keys = db.query(ApiKey).all()
        print("\nTest API Keys created:")
        for key in all_keys:
            print(f"Owner: {key.owner_name}")
            print(f"Key: {key.key}")
            print(f"Plan: {key.plan} ({key.monthly_limit} requests/month)")
            print("---")
        
    except Exception as e:
        print(f"Error creating test API keys: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def run_migration():
    """Run complete migration process."""
    print("Starting database migration...")
    migrate_csv_to_database()
    create_test_api_keys()
    print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()