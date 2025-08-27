
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

class EmailService:
    """Email service using Brevo SMTP for sending verification emails."""
    
    def __init__(self):
        # Brevo SMTP configuration
        self.smtp_server = "smtp-relay.brevo.com"
        self.smtp_port = 587
        self.smtp_username = "94d9a9001@smtp-brevo.com"
        self.smtp_password = "J7at81pWEdFrYc5f"
        self.from_email = "noreply@movieapi.dev"
        self.from_name = "Movie API"
    
    def send_verification_email(self, to_email: str, otp: str, user_name: str) -> bool:
        """Send email verification OTP."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = "🎬 Welcome to Movie API - Verify Your Email"
            
            # Modern HTML email template
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                        color: #ffffff;
                    }}
                    .container {{ 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #000000;
                        border-radius: 16px;
                        overflow: hidden;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    }}
                    .header {{ 
                        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                        padding: 40px 30px; 
                        text-align: center; 
                        position: relative;
                    }}
                    .logo {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                        background: #0a0a0a;
                    }}
                    .otp-box {{ 
                        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                        border: 2px solid #6366f1; 
                        border-radius: 12px; 
                        padding: 30px; 
                        text-align: center; 
                        margin: 30px 0; 
                    }}
                    .otp-code {{ 
                        font-size: 36px; 
                        font-weight: bold; 
                        letter-spacing: 8px; 
                        color: #6366f1;
                        margin: 20px 0;
                        font-family: 'Courier New', monospace;
                    }}
                    .button {{
                        display: inline-block;
                        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                        color: white;
                        padding: 12px 24px;
                        text-decoration: none;
                        border-radius: 8px;
                        font-weight: 600;
                        margin: 20px 0;
                    }}
                    .features {{
                        background: #111111;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                    }}
                    .footer {{ 
                        background: #111111; 
                        padding: 20px; 
                        text-align: center; 
                        color: #888888;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="logo">🎬 Movie API</div>
                        <h1 style="margin: 0; font-size: 28px;">Welcome to the Future of Movie Data</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">Your developer journey starts here</p>
                    </div>
                    <div class="content">
                        <h2 style="color: #6366f1;">Hello {user_name}! 👋</h2>
                        <p>Welcome to Movie API - the most comprehensive movie database API for developers. You're one step away from accessing thousands of movies with lightning-fast queries.</p>
                        
                        <div class="otp-box">
                            <p style="margin: 0; font-size: 18px;">Your verification code:</p>
                            <div class="otp-code">{otp}</div>
                            <p style="margin: 0; color: #888;">Valid for 15 minutes</p>
                        </div>
                        
                        <div class="features">
                            <h3 style="color: #6366f1; margin-top: 0;">🚀 What you'll get:</h3>
                            <ul style="list-style: none; padding: 0;">
                                <li style="margin: 10px 0;">✨ Instant API key generation</li>
                                <li style="margin: 10px 0;">📊 Real-time usage analytics</li>
                                <li style="margin: 10px 0;">🎬 10,000+ movies database</li>
                                <li style="margin: 10px 0;">⚡ Lightning-fast responses</li>
                                <li style="margin: 10px 0;">🔒 Secure authentication</li>
                            </ul>
                        </div>
                        
                        <p><strong>Security Notice:</strong> If you didn't create this account, please ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>Movie API - Empowering developers worldwide</p>
                        <p>This is an automated email. Please don't reply to this message.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email via Brevo SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Verification email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {str(e)}")
            # Fallback - show OTP in console for development
            print(f"\n{'='*50}")
            print(f"EMAIL VERIFICATION OTP")
            print(f"{'='*50}")
            print(f"To: {to_email}")
            print(f"Name: {user_name}")
            print(f"OTP: {otp}")
            print(f"{'='*50}\n")
            return False
    
    def send_password_reset_email(self, to_email: str, reset_token: str, user_name: str) -> bool:
        """Send password reset email."""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = "🔐 Movie API - Password Reset Request"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ 
                        margin: 0; 
                        padding: 0; 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
                        color: #ffffff;
                    }}
                    .container {{ 
                        max-width: 600px; 
                        margin: 0 auto; 
                        background: #000000;
                        border-radius: 16px;
                        overflow: hidden;
                        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
                    }}
                    .header {{ 
                        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
                        padding: 40px 30px; 
                        text-align: center; 
                    }}
                    .content {{ 
                        padding: 40px 30px; 
                        background: #0a0a0a;
                    }}
                    .reset-box {{ 
                        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                        border: 2px solid #ef4444; 
                        border-radius: 12px; 
                        padding: 30px; 
                        text-align: center; 
                        margin: 30px 0; 
                    }}
                    .reset-code {{ 
                        font-size: 28px; 
                        font-weight: bold; 
                        letter-spacing: 4px; 
                        color: #ef4444;
                        margin: 20px 0;
                        font-family: 'Courier New', monospace;
                    }}
                    .footer {{ 
                        background: #111111; 
                        padding: 20px; 
                        text-align: center; 
                        color: #888888;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1 style="margin: 0; font-size: 28px;">🔐 Password Reset</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">Secure your Movie API account</p>
                    </div>
                    <div class="content">
                        <h2 style="color: #ef4444;">Hello {user_name},</h2>
                        <p>We received a request to reset your Movie API account password. Use the reset code below to create a new password:</p>
                        
                        <div class="reset-box">
                            <p style="margin: 0; font-size: 18px;">Your reset code:</p>
                            <div class="reset-code">{reset_token}</div>
                            <p style="margin: 0; color: #888;">Valid for 30 minutes</p>
                        </div>
                        
                        <p><strong>Security Notice:</strong></p>
                        <ul>
                            <li>This code expires in 30 minutes</li>
                            <li>If you didn't request this reset, ignore this email</li>
                            <li>Never share this code with anyone</li>
                        </ul>
                    </div>
                    <div class="footer">
                        <p>Movie API - Keeping your account secure</p>
                        <p>This is an automated email. Please don't reply to this message.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"✅ Password reset email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send password reset email to {to_email}: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()

# Helper functions
def send_verification_email(to_email: str, otp: str, user_name: str) -> bool:
    """Send verification email using the global email service."""
    return email_service.send_verification_email(to_email, otp, user_name)

def send_password_reset_email(to_email: str, reset_token: str, user_name: str) -> bool:
    """Send password reset email using the global email service."""
    return email_service.send_password_reset_email(to_email, reset_token, user_name)
