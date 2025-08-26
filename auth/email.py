
import smtplib
import os
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import Optional

class EmailService:
    """Email service using SMTP for sending verification emails."""
    
    def __init__(self):
        # Brevo SMTP configuration
        self.smtp_server = "smtp-relay.brevo.com"
        self.smtp_port = 587
        self.smtp_username = os.getenv("BREVO_SMTP_USERNAME")  # Your Brevo login email
        self.smtp_password = os.getenv("BREVO_SMTP_PASSWORD")  # Your Brevo SMTP password
        self.from_email = os.getenv("FROM_EMAIL", "noreply@movieapi.com")
        self.from_name = "Movie API"
    
    def send_verification_email(self, to_email: str, otp: str, user_name: str) -> bool:
        """Send email verification OTP."""
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = "Movie API - Email Verification"
            
            # HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
                    .header {{ background-color: #000000; color: #ffffff; padding: 30px; text-align: center; }}
                    .content {{ padding: 40px 30px; }}
                    .otp-box {{ background-color: #f8f9fa; border: 2px solid #000000; border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .otp-code {{ font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #000000; }}
                    .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #6c757d; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🎬 Movie API</h1>
                        <p>Email Verification Required</p>
                    </div>
                    <div class="content">
                        <h2>Hello {user_name}!</h2>
                        <p>Thank you for registering with Movie API. To complete your registration, please verify your email address using the verification code below:</p>
                        
                        <div class="otp-box">
                            <p>Your verification code is:</p>
                            <div class="otp-code">{otp}</div>
                        </div>
                        
                        <p><strong>Important:</strong></p>
                        <ul>
                            <li>This code will expire in 15 minutes</li>
                            <li>Enter this code on the verification page to activate your account</li>
                            <li>If you didn't request this verification, please ignore this email</li>
                        </ul>
                        
                        <p>Once verified, you'll be able to:</p>
                        <ul>
                            <li>Generate API keys for your applications</li>
                            <li>Access comprehensive movie database</li>
                            <li>Monitor your API usage and analytics</li>
                        </ul>
                    </div>
                    <div class="footer">
                        <p>This is an automated email from Movie API. Please do not reply to this email.</p>
                        <p>If you have any questions, contact our support team.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MimeText(html_body, 'html'))
            
            # If SMTP credentials are not configured, log to console (development mode)
            if not self.smtp_username or not self.smtp_password:
                print(f"\n{'='*50}")
                print(f"EMAIL VERIFICATION OTP (Development Mode)")
                print(f"{'='*50}")
                print(f"To: {to_email}")
                print(f"Name: {user_name}")
                print(f"OTP: {otp}")
                print(f"{'='*50}\n")
                return True
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"Verification email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send email to {to_email}: {str(e)}")
            # In development, still show OTP in console even if email fails
            print(f"\n{'='*50}")
            print(f"EMAIL VERIFICATION OTP (Fallback)")
            print(f"{'='*50}")
            print(f"To: {to_email}")
            print(f"Name: {user_name}")
            print(f"OTP: {otp}")
            print(f"{'='*50}\n")
            return False
    
    def send_password_reset_email(self, to_email: str, reset_token: str, user_name: str) -> bool:
        """Send password reset email."""
        try:
            # Create message
            msg = MimeMultipart()
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = "Movie API - Password Reset"
            
            # HTML email body
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: #ffffff; }}
                    .header {{ background-color: #dc3545; color: #ffffff; padding: 30px; text-align: center; }}
                    .content {{ padding: 40px 30px; }}
                    .reset-box {{ background-color: #f8f9fa; border: 2px solid #dc3545; border-radius: 10px; padding: 20px; text-align: center; margin: 20px 0; }}
                    .reset-code {{ font-size: 24px; font-weight: bold; letter-spacing: 4px; color: #dc3545; }}
                    .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; font-size: 14px; color: #6c757d; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Movie API</h1>
                        <p>Password Reset Request</p>
                    </div>
                    <div class="content">
                        <h2>Hello {user_name}!</h2>
                        <p>We received a request to reset your Movie API account password. Use the reset token below:</p>
                        
                        <div class="reset-box">
                            <p>Your password reset token is:</p>
                            <div class="reset-code">{reset_token}</div>
                        </div>
                        
                        <p><strong>Security Notice:</strong></p>
                        <ul>
                            <li>This token will expire in 30 minutes</li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Never share this token with anyone</li>
                        </ul>
                    </div>
                    <div class="footer">
                        <p>This is an automated email from Movie API. Please do not reply to this email.</p>
                        <p>If you have any questions, contact our support team.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MimeText(html_body, 'html'))
            
            # If SMTP credentials are not configured, log to console
            if not self.smtp_username or not self.smtp_password:
                print(f"\n{'='*50}")
                print(f"PASSWORD RESET TOKEN (Development Mode)")
                print(f"{'='*50}")
                print(f"To: {to_email}")
                print(f"Name: {user_name}")
                print(f"Reset Token: {reset_token}")
                print(f"{'='*50}\n")
                return True
            
            # Send email via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            print(f"Password reset email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"Failed to send password reset email to {to_email}: {str(e)}")
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
