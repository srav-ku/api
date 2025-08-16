# Movie API Backend v2

## Overview

A production-ready FastAPI-based movie search and listing API with PostgreSQL database integration and API key authentication system. The system provides secure RESTful endpoints for movie discovery, search functionality, and detailed movie information retrieval with rate limiting and usage analytics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **FastAPI v2**: Enhanced with API key authentication middleware and CORS support
- **PostgreSQL**: Production database with SQLAlchemy ORM for data persistence
- **Pydantic Models**: Used for data validation and serialization, ensuring consistent API responses
- **API Key Authentication**: UUID-based keys with rate limiting and usage tracking

### Data Management
- **PostgreSQL Database**: Production-grade database with optimized indexes for fast queries
- **SQLAlchemy ORM**: Type-safe database operations with relationship management
- **Database Tables**:
  - `movies`: Core movie data with indexed title, year, and genre fields
  - `api_keys`: API key management with usage tracking and plan limits
  - `usage_logs`: Detailed request logging for analytics and monitoring
- **CSV Migration**: Automated migration from CSV to database with duplicate handling

### API Design
- **RESTful Endpoints**: Clean URL structure following REST conventions
- **API Key Authentication**: All movie endpoints require X-API-KEY header
- **Rate Limiting**: 1000 requests/month for free plan, 10000 for premium
- **Usage Tracking**: Real-time usage analytics and endpoint breakdown
- **Pagination Support**: Built-in pagination with configurable page size limits
- **Search Functionality**: Multi-criteria search by title, year, and genre
- **Admin Endpoints**: API key management and usage statistics
- **Response Models**: Structured JSON responses with consistent formatting
- **Error Handling**: Proper HTTP status codes and detailed error messages

### Data Models
- **Database Models**: SQLAlchemy models for movies, API keys, and usage logs
- **Response Models**: Specialized models for different API endpoints (single movie, paginated lists, search results)
- **Authentication Models**: API key response and usage statistics models
- **Admin Models**: API key management and analytics response models
- **Data Transformation**: Converts string fields (genre, actors) to arrays in API responses

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for building APIs with authentication middleware
- **SQLAlchemy**: ORM for PostgreSQL database operations
- **PostgreSQL**: Production database (via Replit's managed PostgreSQL service)
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for running FastAPI applications
- **bcrypt**: Password hashing for security (future user authentication)
- **python-multipart**: For form data handling

### Security & Authentication
- **UUID-based API Keys**: Cryptographically secure API key generation
- **Rate Limiting**: Built-in request throttling per API key
- **Usage Analytics**: Comprehensive tracking of API usage patterns
- **Environment Variables**: Secure database connection management

### Database Schema
- **Indexed Queries**: Optimized search performance on title, year, genre
- **Relationship Management**: Foreign key constraints between tables
- **Migration Support**: Automated CSV-to-database migration
- **Data Integrity**: Duplicate prevention and validation

## Recent Changes (Phase 2)
- ✅ Migrated from CSV to PostgreSQL database
- ✅ Added API key authentication system
- ✅ Implemented rate limiting (1000 requests/month free plan)
- ✅ Added usage tracking and analytics
- ✅ Created admin endpoints for API key management
- ✅ Enhanced error handling and security
- ✅ Added CORS support for web applications