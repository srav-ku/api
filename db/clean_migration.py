import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models_v3 import Base, Movie, ApiKey, User, EmailVerification, UsageLog, AdminSession
from .models_v3 import generate_api_key
from auth.security import get_password_hash
import os

def clean_migration():
    """Clean migration to Phase 3 schema."""
    
    print("Starting clean migration to Phase 3...")
    
    try:
        # Drop all existing tables and recreate
        print("Dropping existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Creating new Phase 3 tables...")
        Base.metadata.create_all(bind=engine)
        
        print("Phase 3 database schema created successfully!")
        
        # Now populate with data
        populate_initial_data()
        
        print("Clean migration completed successfully!")
        
    except Exception as e:
        print(f"Error during clean migration: {e}")
        raise

def populate_initial_data():
    """Populate database with initial data."""
    
    db = SessionLocal()
    
    try:
        # Load movies from CSV
        csv_path = "data/movies.csv"
        if os.path.exists(csv_path):
            print(f"Loading movies from {csv_path}")
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
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
            print(f"Successfully loaded {len(df)} movies")
        
        # Create admin user
        admin_user = User(
            name="Admin User",
            email="admin@movieapi.com",
            hashed_password=get_password_hash("admin123"),
            is_verified=True,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Created admin user: admin@movieapi.com / admin123")
        
        # Create test developer users
        test_users = [
            {"name": "Test Developer 1", "email": "dev1@gmail.com", "password": "password123", "plan": "free"},
            {"name": "Test Developer 2", "email": "dev2@yahoo.com", "password": "password123", "plan": "free"},
            {"name": "Premium User", "email": "premium@outlook.com", "password": "password123", "plan": "premium"}
        ]
        
        for user_data in test_users:
            user = User(
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                is_verified=True,
                is_admin=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Create API key for user
            plan = user_data["plan"]
            monthly_limit = 10000 if plan == "premium" else 1000
            
            api_key = ApiKey(
                owner_id=user.id,
                key=generate_api_key(),
                plan=plan,
                monthly_limit=monthly_limit
            )
            db.add(api_key)
            db.commit()
            
            print(f"Created user: {user.email} with API key: {api_key.key}")
        
        # Print summary
        total_users = db.query(User).count()
        total_movies = db.query(Movie).count()
        total_api_keys = db.query(ApiKey).count()
        
        print(f"\nDatabase Summary:")
        print(f"- Users: {total_users}")
        print(f"- Movies: {total_movies}")
        print(f"- API Keys: {total_api_keys}")
        
        # Print credentials
        print(f"\nTest Credentials:")
        print(f"Admin: admin@movieapi.com / admin123")
        
        # Get API keys for display
        api_keys = db.query(ApiKey).join(User).all()
        for api_key in api_keys:
            if not api_key.owner.is_admin:
                print(f"Developer: {api_key.owner.email} / password123 (API Key: {api_key.key})")
        
    except Exception as e:
        print(f"Error populating data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clean_migration()