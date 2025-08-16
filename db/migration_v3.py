import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal, create_tables, Base, engine
from .models_v3 import Movie, ApiKey, User, EmailVerification, UsageLog, AdminSession
from .models_v3 import generate_api_key, generate_verification_token
from auth.security import get_password_hash
import os

def migrate_to_v3_schema():
    """Migrate to Phase 3 database schema with users and email verification."""
    
    print("Migrating to Phase 3 database schema...")
    
    # Import new models to ensure they're registered
    from .models_v3 import User, EmailVerification, Movie, ApiKey, UsageLog, AdminSession
    
    db = SessionLocal()
    
    try:
        # Check if Phase 3 tables exist, if not create them
        try:
            # Try to query users table - if it fails, we need full migration
            db.execute("SELECT 1 FROM users LIMIT 1")
            print("Phase 3 tables already exist, checking data...")
        except:
            print("Creating Phase 3 database schema...")
            # Create all tables with new schema
            Base.metadata.create_all(bind=engine)
            print("Database tables created successfully!")
        
        # Check existing data
        try:
            existing_movies = db.query(Movie).count()
        except:
            # If movies query fails due to schema differences, recreate
            print("Schema mismatch detected, recreating tables...")
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            existing_movies = 0
        if existing_movies == 0:
            # Load movies from CSV if no movies exist
            csv_path = "data/movies.csv"
            if os.path.exists(csv_path):
                print(f"Loading movies from {csv_path}")
                df = pd.read_csv(csv_path)
                
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
                print(f"Successfully loaded {len(df)} movies")
        
        # Create admin user if doesn't exist
        admin_user = db.query(User).filter(User.email == "admin@movieapi.com").first()
        if not admin_user:
            admin_user = User(
                name="Admin User",
                email="admin@movieapi.com",
                hashed_password=get_password_hash("admin123"),  # Change in production
                is_verified=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("Created admin user: admin@movieapi.com / admin123")
        
        # Create test developer users if they don't exist
        test_users = [
            {"name": "Test Developer 1", "email": "dev1@gmail.com", "password": "password123"},
            {"name": "Test Developer 2", "email": "dev2@yahoo.com", "password": "password123"},
            {"name": "Premium User", "email": "premium@outlook.com", "password": "password123", "plan": "premium"}
        ]
        
        for user_data in test_users:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    name=user_data["name"],
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_verified=True,  # Auto-verify test users
                    is_admin=False
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                
                # Create API key for user
                plan = user_data.get("plan", "free")
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
        
        print("Phase 3 migration completed successfully!")
        
        # Print summary
        total_users = db.query(User).count()
        total_movies = db.query(Movie).count()
        total_api_keys = db.query(ApiKey).count()
        
        print(f"\nDatabase Summary:")
        print(f"- Users: {total_users}")
        print(f"- Movies: {total_movies}")
        print(f"- API Keys: {total_api_keys}")
        
        # Print test credentials
        print(f"\nTest Credentials:")
        print(f"Admin: admin@movieapi.com / admin123")
        for user_data in test_users:
            user = db.query(User).filter(User.email == user_data["email"]).first()
            if user and user.api_keys:
                api_key = user.api_keys[0]
                print(f"Developer: {user.email} / {user_data['password']} (API Key: {api_key.key})")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate_to_v3_schema()