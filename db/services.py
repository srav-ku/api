
from sqlalchemy.orm import Session
from db.models_v3 import ApiKey, User, generate_api_key
from datetime import datetime
from typing import List, Optional

class ApiKeyService:
    """Service class for API key operations."""
    
    @staticmethod
    def get_all_api_keys(db: Session) -> List[ApiKey]:
        """Get all API keys with owner information."""
        return db.query(ApiKey).join(User).all()
    
    @staticmethod
    def create_api_key(
        db: Session,
        owner_name: str,
        plan: str = "free",
        monthly_limit: int = 1000
    ) -> ApiKey:
        """Create a new API key."""
        # Check if user exists
        user = db.query(User).filter(User.name == owner_name).first()
        if not user:
            # Create new user
            user = User(
                name=owner_name,
                email=f"{owner_name.lower().replace(' ', '.')}@example.com",
                hashed_password="temp_hash",
                is_verified=True,
                is_admin=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create API key
        api_key = ApiKey(
            owner_id=user.id,
            key=generate_api_key(),
            plan=plan,
            monthly_limit=monthly_limit
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        return api_key
    
    @staticmethod
    def reset_usage(db: Session, api_key: str) -> bool:
        """Reset usage count for an API key."""
        db_api_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
        if not db_api_key:
            return False
        
        db_api_key.usage_count = 0
        db_api_key.last_reset = datetime.now()
        db.commit()
        return True
    
    @staticmethod
    def suspend_api_key(db: Session, api_key_id: int) -> bool:
        """Suspend an API key."""
        db_api_key = db.query(ApiKey).filter(ApiKey.id == api_key_id).first()
        if not db_api_key:
            return False
        
        db_api_key.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def activate_api_key(db: Session, api_key_id: int) -> bool:
        """Activate an API key."""
        db_api_key = db.query(ApiKey).filter(ApiKey.id == api_key_id).first()
        if not db_api_key:
            return False
        
        db_api_key.is_active = True
        db.commit()
        return True
