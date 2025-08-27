
from db.database import engine, Base
from db.models_v3 import User, ApiKey, Movie, UsageLog, EmailVerification

def create_all_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_all_tables()
