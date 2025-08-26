from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
import secrets
import string
from datetime import datetime, timedelta

Base = declarative_base()

def generate_api_key():
    """Generate a secure API key."""
    return 'mapi_' + ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

def generate_verification_token():
    """Generate a verification token."""
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

class User(Base):
    """User model for admin and developer accounts."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    email_verifications = relationship("EmailVerification", back_populates="user")
    api_keys = relationship("ApiKey", back_populates="owner")
    admin_sessions = relationship("AdminSession", back_populates="user")

class EmailVerification(Base):
    """Email verification tokens."""
    __tablename__ = "email_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_used = Column(Boolean, default=False)
    
    # Relationship
    user = relationship("User", back_populates="email_verifications")

class ApiKey(Base):
    """API Key database model."""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(255), unique=True, nullable=False, index=True)
    plan = Column(String(50), nullable=False, default="free")
    usage_count = Column(Integer, default=0)
    monthly_limit = Column(Integer, default=1000)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_reset = Column(DateTime(timezone=True), server_default=func.now())
    last_used = Column(DateTime(timezone=True))
    
    # Relationships
    owner = relationship("User", back_populates="api_keys")
    usage_logs = relationship("UsageLog", back_populates="api_key")

class Movie(Base):
    """Movie database model."""
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    genre = Column(String(500), nullable=False, index=True)
    director = Column(String(255), nullable=False)
    actors = Column(Text, nullable=False)
    plot = Column(Text, nullable=False)
    poster_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Create compound index for unique title+year constraint
    __table_args__ = (
        Index('idx_title_year_unique', 'title', 'year', unique=True),
        Index('idx_genre_search', 'genre'),
        Index('idx_title_search', 'title'),
    )

class UsageLog(Base):
    """Usage logging database model."""
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    response_code = Column(Integer)
    response_time_ms = Column(Integer)
    
    # Relationship
    api_key = relationship("ApiKey", back_populates="usage_logs")
    
    __table_args__ = (
        Index('idx_api_key_timestamp', 'api_key_id', 'timestamp'),
        Index('idx_endpoint_timestamp', 'endpoint', 'timestamp'),
    )

class AdminSession(Base):
    """Admin session management."""
    __tablename__ = "admin_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Relationship
    user = relationship("User", back_populates="admin_sessions")

def generate_api_key():
    """Generate a new UUID v4 API key."""
    return str(uuid.uuid4())

def generate_verification_token():
    """Generate a secure verification token."""
    return str(uuid.uuid4())

def generate_session_token():
    """Generate a secure session token."""
    return str(uuid.uuid4())