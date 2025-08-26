
import os
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models_v3 import User
from auth.security import get_password_hash

def create_admin_user():
    """Create default admin user if it doesn't exist."""
    try:
        db = SessionLocal()
        
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@movieapi.com").first()
        
        if not admin:
            # Create admin user
            admin_user = User(
                name="Admin",
                email="admin@movieapi.com",
                hashed_password=get_password_hash("admin123"),
                is_verified=True,
                is_admin=True
            )
            
            db.add(admin_user)
            db.commit()
            
            print("Admin user created successfully!")
            print("Email: admin@movieapi.com")
            print("Password: admin123")
            print("Please change the password after first login.")
        else:
            print("Admin user already exists.")
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
