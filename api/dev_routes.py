
from fastapi import APIRouter, HTTPException, Depends, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_database
from db.models_v3 import User, ApiKey, EmailVerification, generate_api_key, generate_verification_token
from auth.security import verify_password, get_password_hash, is_valid_email_domain, is_disposable_email
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

def generate_otp():
    """Generate 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email: str, otp: str, name: str):
    """Send verification email with OTP."""
    try:
        # For testing purposes, we'll print the OTP to console
        # In production, you should configure SMTP_EMAIL and SMTP_PASSWORD in Replit Secrets
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = os.getenv("SMTP_EMAIL", "")
        sender_password = os.getenv("SMTP_PASSWORD", "")
        
        print(f"=== EMAIL VERIFICATION ===")
        print(f"To: {email}")
        print(f"Name: {name}")
        print(f"OTP Code: {otp}")
        print(f"========================")
        
        if not sender_email or not sender_password:
            print("Warning: SMTP credentials not set. Using console output for OTP.")
            print(f"Your verification code is: {otp}")
            return
        
        subject = "Movie API - Email Verification"
        body = f"""
        Hi {name},

        Thank you for registering with Movie API!

        Your verification code is: {otp}

        This code will expire in 15 minutes. Please enter this code on the verification page to complete your registration.

        If you didn't create this account, please ignore this email.

        Best regards,
        Movie API Team
        """

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        print(f"Your verification code is: {otp}")

@router.get("/dev/register", response_class=HTMLResponse)
async def dev_register_page(request: Request):
    """Developer registration page."""
    return templates.TemplateResponse("dev/register.html", {"request": request})

@router.post("/dev/register")
async def dev_register(
    request: Request,
    background_tasks: BackgroundTasks,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_database)
):
    """Process developer registration."""
    try:
        # Validate input
        if password != confirm_password:
            return templates.TemplateResponse("dev/register.html", {
                "request": request,
                "error": "Passwords do not match"
            })
        
        if len(password) < 8:
            return templates.TemplateResponse("dev/register.html", {
                "request": request,
                "error": "Password must be at least 8 characters long"
            })
        
        if not is_valid_email_domain(email):
            return templates.TemplateResponse("dev/register.html", {
                "request": request,
                "error": "Please use Gmail, Yahoo, or Outlook email"
            })
        
        if is_disposable_email(email):
            return templates.TemplateResponse("dev/register.html", {
                "request": request,
                "error": "Disposable email addresses are not allowed"
            })
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return templates.TemplateResponse("dev/register.html", {
                "request": request,
                "error": "Email already registered"
            })
        
        # Create user
        user = User(
            name=name,
            email=email,
            hashed_password=get_password_hash(password),
            is_verified=False,
            is_admin=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generate OTP and create verification record
        otp = generate_otp()
        verification = EmailVerification(
            user_id=user.id,
            token=otp,
            expires_at=datetime.now() + timedelta(minutes=15)
        )
        db.add(verification)
        db.commit()
        
        # Send verification email
        from auth.email import send_verification_email
        background_tasks.add_task(send_verification_email, email, otp, name)
        
        # Redirect to verification page
        response = RedirectResponse(url=f"/dev/verify?email={email}", status_code=302)
        return response
        
    except Exception as e:
        return templates.TemplateResponse("dev/register.html", {
            "request": request,
            "error": f"Registration failed: {str(e)}"
        })

@router.get("/dev/verify", response_class=HTMLResponse)
async def dev_verify_page(request: Request, email: str = None):
    """Email verification page."""
    return templates.TemplateResponse("dev/verify.html", {
        "request": request,
        "email": email
    })

@router.post("/dev/verify")
async def dev_verify(
    request: Request,
    email: str = Form(...),
    otp: str = Form(...),
    db: Session = Depends(get_database)
):
    """Process email verification."""
    try:
        # Find user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return templates.TemplateResponse("dev/verify.html", {
                "request": request,
                "email": email,
                "error": "User not found"
            })
        
        # Check verification token
        verification = db.query(EmailVerification).filter(
            EmailVerification.user_id == user.id,
            EmailVerification.token == otp,
            EmailVerification.expires_at > datetime.now(),
            EmailVerification.is_used == False
        ).first()
        
        if not verification:
            return templates.TemplateResponse("dev/verify.html", {
                "request": request,
                "email": email,
                "error": "Invalid or expired verification code"
            })
        
        # Mark user as verified
        user.is_verified = True
        verification.is_used = True
        
        # Create default API key
        api_key = ApiKey(
            owner_id=user.id,
            key=generate_api_key(),
            plan="free",
            monthly_limit=1000
        )
        db.add(api_key)
        db.commit()
        
        return templates.TemplateResponse("dev/verify.html", {
            "request": request,
            "success": "Email verified successfully! You can now sign in."
        })
        
    except Exception as e:
        return templates.TemplateResponse("dev/verify.html", {
            "request": request,
            "email": email,
            "error": f"Verification failed: {str(e)}"
        })

@router.get("/dev/login", response_class=HTMLResponse)
async def dev_login_page(request: Request):
    """Developer login page."""
    return templates.TemplateResponse("dev/login.html", {"request": request})

@router.post("/dev/login")
async def dev_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_database)
):
    """Process developer login."""
    user = db.query(User).filter(User.email == email).first()
    
    if not user or user.is_admin or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("dev/login.html", {
            "request": request,
            "error": "Invalid email or password"
        })
    
    if not user.is_verified:
        return templates.TemplateResponse("dev/login.html", {
            "request": request,
            "error": "Please verify your email before signing in"
        })
    
    # Create session (simple cookie-based session)
    response = RedirectResponse(url="/dev/dashboard", status_code=302)
    response.set_cookie(key="dev_session", value=f"{user.id}:{user.email}", httponly=True, max_age=86400)
    return response

@router.get("/dev/dashboard", response_class=HTMLResponse)
async def dev_dashboard(request: Request, db: Session = Depends(get_database)):
    """Developer dashboard."""
    # Get user from session
    session_cookie = request.cookies.get("dev_session")
    if not session_cookie:
        return RedirectResponse(url="/dev/login")
    
    try:
        user_id, email = session_cookie.split(":")
        user = db.query(User).filter(User.id == int(user_id), User.email == email).first()
        
        if not user or not user.is_verified:
            response = RedirectResponse(url="/dev/login")
            response.delete_cookie("dev_session")
            return response
        
        # Get user's API keys
        api_keys = db.query(ApiKey).filter(ApiKey.owner_id == user.id).all()
        
        # Get usage statistics
        from sqlalchemy import func
        usage_stats = []
        for api_key in api_keys:
            from db.models_v3 import UsageLog
            total_requests = db.query(func.count(UsageLog.id)).filter(UsageLog.api_key_id == api_key.id).scalar()
            usage_stats.append({
                'api_key': api_key,
                'total_requests': total_requests or 0
            })
        
        return templates.TemplateResponse("dev/dashboard.html", {
            "request": request,
            "user": user,
            "api_keys": api_keys,
            "usage_stats": usage_stats
        })
        
    except Exception as e:
        response = RedirectResponse(url="/dev/login")
        response.delete_cookie("dev_session")
        return response

@router.post("/dev/api-key/generate")
async def generate_new_api_key(request: Request, db: Session = Depends(get_database)):
    """Generate new API key for developer."""
    session_cookie = request.cookies.get("dev_session")
    if not session_cookie:
        return RedirectResponse(url="/dev/login")
    
    try:
        user_id, email = session_cookie.split(":")
        user = db.query(User).filter(User.id == int(user_id), User.email == email).first()
        
        if not user or not user.is_verified:
            return RedirectResponse(url="/dev/login")
        
        # Check if user already has 3 API keys (limit)
        existing_keys = db.query(ApiKey).filter(ApiKey.owner_id == user.id).count()
        if existing_keys >= 3:
            return RedirectResponse(url="/dev/dashboard?error=Maximum 3 API keys allowed")
        
        # Create new API key
        api_key = ApiKey(
            owner_id=user.id,
            key=generate_api_key(),
            plan="free",
            monthly_limit=1000
        )
        db.add(api_key)
        db.commit()
        
        return RedirectResponse(url="/dev/dashboard?success=New API key generated")
        
    except Exception as e:
        return RedirectResponse(url="/dev/login")

@router.get("/dev/logout")
async def dev_logout():
    """Developer logout."""
    response = RedirectResponse(url="/")
    response.delete_cookie("dev_session")
    return response
