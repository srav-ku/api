from fastapi import APIRouter, HTTPException, Depends, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_database
from db.models_v3 import User, ApiKey, Movie, UsageLog, AdminSession, generate_api_key
from auth.security import verify_password, get_password_hash, create_access_token
from datetime import datetime, timedelta
import pandas as pd
import io
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Admin session management
def get_admin_session(request: Request, db: Session = Depends(get_database)) -> Optional[User]:
    """Get current admin user from session."""
    session_token = request.cookies.get("admin_session")
    if not session_token:
        return None
    
    session = db.query(AdminSession).filter(
        AdminSession.session_token == session_token,
        AdminSession.expires_at > datetime.now()
    ).first()
    
    if not session:
        return None
    
    return session.user

def require_admin(request: Request, db: Session = Depends(get_database)) -> User:
    """Require admin authentication."""
    user = get_admin_session(request, db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=401, detail="Admin authentication required")
    return user

@router.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Admin login page."""
    return templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/admin/login")
async def admin_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_database)
):
    """Process admin login."""
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not user.is_admin or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "admin/login.html", 
            {"request": request, "error": "Invalid credentials"}
        )
    
    # Create admin session
    session_token = create_access_token({"sub": user.email, "admin": True})
    expires_at = datetime.now() + timedelta(hours=8)
    
    admin_session = AdminSession(
        user_id=user.id,
        session_token=session_token,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    db.add(admin_session)
    db.commit()
    
    response = RedirectResponse(url="/admin/dashboard", status_code=302)
    response.set_cookie(key="admin_session", value=session_token, httponly=True, max_age=28800)
    return response

@router.get("/admin/logout")
async def admin_logout(request: Request, db: Session = Depends(get_database)):
    """Admin logout."""
    session_token = request.cookies.get("admin_session")
    if session_token:
        # Delete session from database
        session = db.query(AdminSession).filter(AdminSession.session_token == session_token).first()
        if session:
            db.delete(session)
            db.commit()
    
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie(key="admin_session")
    return response

@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Admin dashboard."""
    # Get statistics
    total_users = db.query(User).filter(User.is_admin == False).count()
    total_movies = db.query(Movie).count()
    total_api_keys = db.query(ApiKey).count()
    active_api_keys = db.query(ApiKey).filter(ApiKey.is_active == True).count()
    
    # Recent usage logs
    recent_logs = db.query(UsageLog).join(ApiKey).join(User).order_by(
        UsageLog.timestamp.desc()
    ).limit(10).all()
    
    # Top endpoints
    from sqlalchemy import func
    top_endpoints = db.query(
        UsageLog.endpoint,
        func.count(UsageLog.endpoint).label('count')
    ).group_by(UsageLog.endpoint).order_by(
        func.count(UsageLog.endpoint).desc()
    ).limit(5).all()
    
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "user": current_user,
        "stats": {
            "total_users": total_users,
            "total_movies": total_movies,
            "total_api_keys": total_api_keys,
            "active_api_keys": active_api_keys
        },
        "recent_logs": recent_logs,
        "top_endpoints": top_endpoints
    })

@router.get("/admin/movies", response_class=HTMLResponse)
async def admin_movies(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Movies management page."""
    movies = db.query(Movie).order_by(Movie.created_at.desc()).all()
    return templates.TemplateResponse("admin/movies.html", {
        "request": request,
        "user": current_user,
        "movies": movies
    })

@router.post("/admin/movies/upload")
async def upload_movies_csv(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Upload and process movies CSV file."""
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Validate CSV structure
        required_columns = ['id', 'title', 'year', 'genre', 'director', 'actors', 'plot', 'poster_url']
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"CSV must contain columns: {', '.join(required_columns)}"
            )
        
        # Process each row
        added_count = 0
        updated_count = 0
        
        for _, row in df.iterrows():
            # Check for existing movie by title + year
            existing_movie = db.query(Movie).filter(
                Movie.title == str(row['title']),
                Movie.year == int(row['year'])
            ).first()
            
            if existing_movie:
                # Update existing movie
                existing_movie.genre = str(row['genre'])
                existing_movie.director = str(row['director'])
                existing_movie.actors = str(row['actors'])
                existing_movie.plot = str(row['plot'])
                existing_movie.poster_url = str(row['poster_url'])
                existing_movie.updated_at = datetime.now()
                updated_count += 1
            else:
                # Add new movie
                movie = Movie(
                    title=str(row['title']),
                    year=int(row['year']),
                    genre=str(row['genre']),
                    director=str(row['director']),
                    actors=str(row['actors']),
                    plot=str(row['plot']),
                    poster_url=str(row['poster_url'])
                )
                db.add(movie)
                added_count += 1
        
        db.commit()
        
        return templates.TemplateResponse("admin/movies.html", {
            "request": request,
            "user": current_user,
            "movies": db.query(Movie).order_by(Movie.created_at.desc()).all(),
            "success": f"Successfully processed CSV: {added_count} movies added, {updated_count} movies updated"
        })
        
    except Exception as e:
        return templates.TemplateResponse("admin/movies.html", {
            "request": request,
            "user": current_user,
            "movies": db.query(Movie).order_by(Movie.created_at.desc()).all(),
            "error": f"Error processing CSV: {str(e)}"
        })

@router.get("/admin/api-keys", response_class=HTMLResponse)
async def admin_api_keys(
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """API keys management page."""
    api_keys = db.query(ApiKey).join(User).order_by(ApiKey.created_at.desc()).all()
    return templates.TemplateResponse("admin/api_keys.html", {
        "request": request,
        "user": current_user,
        "api_keys": api_keys
    })

@router.post("/admin/api-keys/create")
async def create_api_key(
    request: Request,
    owner_name: str = Form(...),
    owner_email: str = Form(...),
    plan: str = Form(...),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Create new API key."""
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == owner_email).first()
        if not user:
            # Create new user
            user = User(
                name=owner_name,
                email=owner_email,
                hashed_password=get_password_hash("temp123"),  # Temporary password
                is_verified=False,
                is_admin=False
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create API key
        monthly_limit = 10000 if plan == "premium" else 1000
        api_key = ApiKey(
            owner_id=user.id,
            key=generate_api_key(),
            plan=plan,
            monthly_limit=monthly_limit
        )
        db.add(api_key)
        db.commit()
        
        return RedirectResponse(url="/admin/api-keys?success=API key created successfully", status_code=302)
        
    except Exception as e:
        return RedirectResponse(url=f"/admin/api-keys?error={str(e)}", status_code=302)

@router.post("/admin/api-keys/{api_key_id}/toggle")
async def toggle_api_key(
    api_key_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Toggle API key active status."""
    api_key = db.query(ApiKey).filter(ApiKey.id == api_key_id).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    api_key.is_active = not api_key.is_active
    db.commit()
    
    return RedirectResponse(url="/admin/api-keys", status_code=302)

@router.post("/admin/api-keys/{api_key_id}/reset")
async def reset_api_key_usage(
    api_key_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_database)
):
    """Reset API key usage count."""
    api_key = db.query(ApiKey).filter(ApiKey.id == api_key_id).first()
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    api_key.usage_count = 0
    api_key.last_reset = datetime.now()
    db.commit()
    
    return RedirectResponse(url="/admin/api-keys", status_code=302)