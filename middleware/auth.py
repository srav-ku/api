from fastapi import HTTPException, Request, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from sqlalchemy.orm import Session
from db.database import get_database
from db.models_v3 import ApiKey, UsageLog
from datetime import datetime, timedelta
from typing import Optional
import calendar

security = HTTPBearer(auto_error=False)

class APIKeyAuth:
    """API Key authentication and rate limiting middleware."""
    
    @staticmethod
    def get_api_key_from_header(request: Request) -> str:
        """Extract API key from X-API-KEY header."""
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="API key required. Please provide X-API-KEY header."
            )
        return api_key
    
    @staticmethod
    def validate_api_key(
        api_key: str,
        db: Session,
        endpoint: str,
        request: Request
    ) -> ApiKey:
        """Validate API key and check rate limits."""
        
        # Find API key in database
        db_api_key = db.query(ApiKey).filter(ApiKey.key == api_key).first()
        if not db_api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key."
            )
        
        # Check if API key is active
        if not db_api_key.is_active:
            raise HTTPException(
                status_code=403,
                detail="API key is suspended."
            )
        
        # Check rate limit
        current_time = datetime.now()
        
        # Reset monthly usage if it's a new month
        if APIKeyAuth._should_reset_monthly_usage(db_api_key.last_reset, current_time):
            db_api_key.usage_count = 0
            db_api_key.last_reset = current_time
            db.commit()
        
        # Check if usage limit exceeded
        if db_api_key.usage_count >= db_api_key.monthly_limit:
            raise HTTPException(
                status_code=429,
                detail=f"Monthly usage limit ({db_api_key.monthly_limit}) exceeded. Please upgrade your plan."
            )
        
        # Log the usage
        usage_log = UsageLog(
            api_key_id=db_api_key.id,
            endpoint=endpoint,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        db.add(usage_log)
        
        # Increment usage count
        db_api_key.usage_count += 1
        db.commit()
        
        return db_api_key
    
    @staticmethod
    def _should_reset_monthly_usage(last_reset: datetime, current_time: datetime) -> bool:
        """Check if monthly usage should be reset."""
        if last_reset is None:
            return True
        if last_reset.month != current_time.month or last_reset.year != current_time.year:
            return True
        return False

# API Key header for Swagger UI integration
api_key_header_auth = APIKeyHeader(name="X-API-KEY", auto_error=False)

def require_api_key(
    request: Request,
    api_key: str = Security(api_key_header_auth),
    db: Session = Depends(get_database)
) -> ApiKey:
    """Dependency to require and validate API key for protected endpoints."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required. Please provide X-API-KEY header."
        )
    endpoint = str(request.url.path)
    return APIKeyAuth.validate_api_key(api_key, db, endpoint, request)

def get_optional_api_key(
    request: Request,
    db: Session = Depends(get_database)
) -> Optional[ApiKey]:
    """Dependency to optionally validate API key (for admin endpoints)."""
    try:
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return None
        endpoint = str(request.url.path)
        return APIKeyAuth.validate_api_key(api_key, db, endpoint, request)
    except HTTPException:
        return None