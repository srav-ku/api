from fastapi import FastAPI, HTTPException, Query, Depends, Request, Security
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from typing import Optional, List
import math
import os
from datetime import datetime, timedelta

# Database imports
from db.database import get_database, create_tables
from db.models_v3 import ApiKey, Movie, User, UsageLog  # Use v3 models
from middleware.auth import require_api_key, get_optional_api_key
from models import (
    MovieResponse, PaginatedMoviesResponse, SearchResponse,
    ApiKeyResponse, UsageStatsResponse, AdminStatsResponse,
    CreateApiKeyRequest, ResetUsageRequest
)

# Import route modules
from api.admin_routes import router as admin_router
from api.dev_routes import router as dev_router
from db.services import ApiKeyService

# Import for email configuration
import smtplib
from email.mime.text import MIMEText

# Load email credentials from environment variables or Replit Secrets
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))


# Initialize FastAPI app
app = FastAPI(
    title="Movie API",
    description="A comprehensive movie database API with user authentication and API key management",
    version="1.0.0"
)

# Define API Key header for Swagger UI
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_router, tags=["admin"])
app.include_router(dev_router, tags=["developer"])

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup."""
    try:
        create_tables()
        print("Database tables created successfully!")

        # Load sample data if no movies exist
        from data_loader import load_movies_from_csv
        load_movies_from_csv()

        # Create admin user if doesn't exist
        from create_admin import create_admin_user
        create_admin_user()

    except Exception as e:
        print(f"Failed to create database tables: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Homepage with landing page."""
    templates = Jinja2Templates(directory="templates")
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/movies", response_model=PaginatedMoviesResponse)
async def get_movies(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    per_page: int = Query(10, ge=1, le=50, description="Number of movies per page"),
    current_user: ApiKey = Depends(require_api_key),
    db: Session = Depends(get_database)
):
    """
    Get all movies with pagination.

    Requires API key authentication via X-API-KEY header.

    - **page**: Page number (default: 1)
    - **per_page**: Number of movies per page (default: 10, max: 50)
    """
    try:
        total_movies = db.query(Movie).count()

        if total_movies == 0:
            return PaginatedMoviesResponse(
                movies=[],
                page=page,
                per_page=per_page,
                total_movies=0,
                total_pages=0
            )

        total_pages = math.ceil(total_movies / per_page)

        # Validate page number
        if page > total_pages:
            raise HTTPException(
                status_code=404,
                detail=f"Page {page} not found. Total pages: {total_pages}"
            )

        # Calculate skip value for pagination
        skip = (page - 1) * per_page

        # Get movies for current page
        movies = db.query(Movie).offset(skip).limit(per_page).all()

        # Convert to response format
        def movie_to_response(movie: Movie) -> MovieResponse:
            return MovieResponse(
                id=movie.id,
                title=movie.title,
                year=movie.year,
                genre=movie.genre.split('|') if movie.genre else [],
                director=movie.director,
                actors=movie.actors.split('|') if movie.actors else [],
                plot=movie.plot,
                poster_url=movie.poster_url or ""
            )

        movie_responses = [movie_to_response(movie) for movie in movies]

        return PaginatedMoviesResponse(
            movies=movie_responses,
            page=page,
            per_page=per_page,
            total_movies=total_movies,
            total_pages=total_pages
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/search", response_model=SearchResponse)
async def search_movies(
    title: Optional[str] = Query(None, description="Search by movie title"),
    year: Optional[int] = Query(None, description="Search by release year"),
    genre: Optional[str] = Query(None, description="Search by genre"),
    current_user: ApiKey = Depends(require_api_key),
    db: Session = Depends(get_database)
):
    """
    Search movies by title, year, and/or genre.

    Requires API key authentication via X-API-KEY header.

    - **title**: Search in movie titles (case-insensitive, partial match)
    - **year**: Search by exact release year
    - **genre**: Search in genres (case-insensitive, partial match)

    You can combine multiple search parameters.
    """
    try:
        # Validate that at least one search parameter is provided
        if not any([title, year, genre]):
            raise HTTPException(
                status_code=400,
                detail="At least one search parameter (title, year, or genre) must be provided"
            )

        # Perform search
        query = db.query(Movie)

        if title:
            query = query.filter(Movie.title.ilike(f"%{title}%"))

        if year:
            query = query.filter(Movie.year == year)

        if genre:
            query = query.filter(Movie.genre.ilike(f"%{genre}%"))

        search_results = query.all()

        # Convert to response format
        def movie_to_response(movie: Movie) -> MovieResponse:
            return MovieResponse(
                id=movie.id,
                title=movie.title,
                year=movie.year,
                genre=movie.genre.split('|') if movie.genre else [],
                director=movie.director,
                actors=movie.actors.split('|') if movie.actors else [],
                plot=movie.plot,
                poster_url=movie.poster_url or ""
            )

        movie_responses = [movie_to_response(movie) for movie in search_results]

        # Prepare query information for response
        query_info = {}
        if title:
            query_info["title"] = title
        if year:
            query_info["year"] = year
        if genre:
            query_info["genre"] = genre

        return SearchResponse(
            movies=movie_responses,
            query=query_info,
            total_results=len(movie_responses)
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/movies/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(
    movie_id: int,
    current_user: ApiKey = Depends(require_api_key),
    db: Session = Depends(get_database)
):
    """
    Get full movie details by ID.

    Requires API key authentication via X-API-KEY header.

    - **movie_id**: The unique identifier of the movie
    """
    try:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()

        if not movie:
            raise HTTPException(
                status_code=404,
                detail=f"Movie with ID {movie_id} not found"
            )

        def movie_to_response(movie: Movie) -> MovieResponse:
            return MovieResponse(
                id=movie.id,
                title=movie.title,
                year=movie.year,
                genre=movie.genre.split('|') if movie.genre else [],
                director=movie.director,
                actors=movie.actors.split('|') if movie.actors else [],
                plot=movie.plot,
                poster_url=movie.poster_url or ""
            )

        return movie_to_response(movie)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# API Key Management Endpoints
@app.get("/api-key/stats", response_model=UsageStatsResponse)
async def get_api_key_stats(
    current_user: ApiKey = Depends(require_api_key),
    db: Session = Depends(get_database)
):
    """
    Get usage statistics for the current API key.

    Requires API key authentication via X-API-KEY header.
    """
    try:
        # Get usage stats for current API key
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=30)

        usage_logs = db.query(UsageLog).filter(
            UsageLog.api_key_id == current_user.id,
            UsageLog.timestamp >= start_date
        ).all()

        # Group by endpoint
        endpoint_stats = {}
        for log in usage_logs:
            if log.endpoint not in endpoint_stats:
                endpoint_stats[log.endpoint] = 0
            endpoint_stats[log.endpoint] += 1

        usage_percentage = (current_user.usage_count / current_user.monthly_limit) * 100

        return UsageStatsResponse(
            api_key=current_user.key,
            owner_name=current_user.owner.name if current_user.owner else "Unknown",
            plan=current_user.plan,
            usage_count=current_user.usage_count,
            monthly_limit=current_user.monthly_limit,
            usage_percentage=round(usage_percentage, 2),
            endpoint_breakdown=endpoint_stats,
            period_days=30
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Admin Endpoints
@app.get("/admin/stats", response_model=AdminStatsResponse)
async def get_admin_stats(db: Session = Depends(get_database)):
    """
    Get admin statistics (no authentication required for demo).
    """
    try:
        from sqlalchemy import func

        # Get API key statistics
        total_api_keys = db.query(ApiKey).count()
        active_api_keys = db.query(ApiKey).filter(ApiKey.is_active == "active").count()
        suspended_api_keys = db.query(ApiKey).filter(ApiKey.is_active == "suspended").count()

        # Get movie count
        total_movies = db.query(Movie).count()

        # Get today's requests
        today = datetime.now().date()
        total_requests_today = db.query(UsageLog).filter(
            func.date(UsageLog.timestamp) == today
        ).count()

        # Get top endpoints
        endpoint_counts = db.query(
            UsageLog.endpoint,
            func.count(UsageLog.endpoint).label('count')
        ).group_by(UsageLog.endpoint).order_by(
            func.count(UsageLog.endpoint).desc()
        ).limit(5).all()

        top_endpoints = {endpoint: count for endpoint, count in endpoint_counts}

        return AdminStatsResponse(
            total_api_keys=total_api_keys,
            active_api_keys=active_api_keys,
            suspended_api_keys=suspended_api_keys,
            total_movies=total_movies,
            total_requests_today=total_requests_today,
            top_endpoints=top_endpoints
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/admin/api-keys", response_model=List[ApiKeyResponse])
async def get_all_api_keys(db: Session = Depends(get_database)):
    """
    Get all API keys (admin endpoint, no authentication for demo).
    """
    try:
        api_keys = ApiKeyService.get_all_api_keys(db)
        return [
            ApiKeyResponse(
                id=key.id,
                owner_name=key.owner_name,
                key=key.key,
                plan=key.plan,
                usage_count=key.usage_count,
                monthly_limit=key.monthly_limit,
                is_active=key.is_active,
                created_at=key.created_at.isoformat()
            )
            for key in api_keys
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/admin/api-keys", response_model=ApiKeyResponse)
async def create_api_key(
    request: CreateApiKeyRequest,
    db: Session = Depends(get_database)
):
    """
    Create a new API key (admin endpoint, no authentication for demo).
    """
    try:
        api_key = ApiKeyService.create_api_key(
            db,
            owner_name=request.owner_name,
            plan=request.plan,
            monthly_limit=request.monthly_limit
        )

        return ApiKeyResponse(
            id=api_key.id,
            owner_name=api_key.owner_name,
            key=api_key.key,
            plan=api_key.plan,
            usage_count=api_key.usage_count,
            monthly_limit=api_key.monthly_limit,
            is_active=api_key.is_active,
            created_at=api_key.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/admin/reset-usage")
async def reset_api_key_usage(
    request: ResetUsageRequest,
    db: Session = Depends(get_database)
):
    """
    Reset usage count for an API key (admin endpoint, no authentication for demo).
    """
    try:
        success = ApiKeyService.reset_usage(db, request.api_key)
        if success:
            return {"message": "Usage count reset successfully", "api_key": request.api_key}
        else:
            raise HTTPException(status_code=404, detail="API key not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# --- OTP Verification ---

def send_otp_email(email: str, otp: str):
    """Sends OTP to the given email address."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials not configured. Skipping OTP email.")
        return False

    msg = MIMEText(f"Your OTP for verification is: {otp}")
    msg['Subject'] = "Movie API OTP Verification"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        print(f"OTP email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        return False

# Global OTP storage (in production, use Redis or database)
otp_storage = {}

@app.post("/verify/request-otp")
async def request_otp(request: Request, email: str = Query(..., description="User's email address")):
    """Requests an OTP for email verification."""
    import random
    otp = str(random.randint(100000, 999999))

    # Store OTP with expiry (15 minutes)
    from datetime import datetime, timedelta
    expiry = datetime.now() + timedelta(minutes=15)
    otp_storage[email] = {"otp": otp, "expiry": expiry}

    print(f"=== OTP VERIFICATION ===")
    print(f"Email: {email}")
    print(f"OTP Code: {otp}")
    print(f"Expires: {expiry}")
    print(f"========================")

    # Try to send email, but continue even if it fails
    try:
        send_otp_email(email, otp)
    except Exception as e:
        print(f"Email sending failed: {e}")

    return {"message": "OTP generated successfully. Check console for OTP (email sending may not work without SMTP config)."}

@app.post("/verify/verify-otp")
async def verify_otp(request: Request, email: str = Query(..., description="User's email address"), otp: str = Query(..., description="The OTP received")):
    """Verifies the provided OTP for the given email."""
    stored_data = otp_storage.get(email)

    if not stored_data:
        raise HTTPException(status_code=400, detail="No OTP found for this email.")

    # Check if OTP has expired
    if datetime.now() > stored_data["expiry"]:
        del otp_storage[email]
        raise HTTPException(status_code=400, detail="OTP has expired.")

    # Check if OTP matches
    if stored_data["otp"] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP.")

    # OTP is valid, clear it from storage
    del otp_storage[email]

    return {"message": "Email verified successfully!"}


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"detail": "The requested resource was not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)