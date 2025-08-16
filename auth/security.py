from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None

def is_valid_email_domain(email: str) -> bool:
    """Check if email domain is allowed (Gmail, Yahoo, Outlook)."""
    allowed_domains = [
        'gmail.com', 'googlemail.com',
        'yahoo.com', 'yahoo.co.uk', 'yahoo.ca', 'yahoo.au',
        'outlook.com', 'hotmail.com', 'live.com', 'msn.com'
    ]
    
    domain = email.split('@')[-1].lower()
    return domain in allowed_domains

def is_disposable_email(email: str) -> bool:
    """Check if email is from a disposable email service."""
    disposable_domains = [
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'yopmail.com', 'temp-mail.org',
        'throwaway.email', 'getnada.com', 'maildrop.cc'
    ]
    
    domain = email.split('@')[-1].lower()
    return domain in disposable_domains