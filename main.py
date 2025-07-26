# Automated Phishing Email & Campaign Generator (Educational/Training Tool)

import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_phishing_email(sender_email, sender_password, recipient_email, subject, body_content, is_html=False):
    """
    Sends a customizable email, simulating a phishing attempt for educational use only.

   sender_email (str): The email address from which to send the email.
        sender_password (str): The password for the sender's email account.
                                (WARNING: Storing passwords directly in code is INSECURE for production.
                                For this educational project, we'll use it, but be aware of the risk.)
        recipient_email (str): The email address to which the email will be sent.
        subject (str): The subject line of the email.
        body_content (str): The main content of the email.
        is_html (bool): Set to True if the body_content is HTML, False for plain text.
    """

    try:
        #make a multipart message and set headers
        msg = MIMEMultipart()  # <-- FIXED: added parentheses
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['subject'] = subject

        # Adding the body content
        if is_html:
            msg.attach(MIMEText(body_content, 'html'))
        else:
            msg.attach(MIMEText(body_content, 'plain'))

           
        # Just like Vegeta always strives to be stronger, this tool will strive to be more realistic!
        # This is where we'd add attachments or more complex headers if needed.

        # Connect to the SMTP server (e.g., Gmail's SMTP server)
        # For Gmail, use 'smtp.gmail.com' and port 587 (TLS)
        # You might need to enable "Less secure app access" in your Gmail settings
        # or use an App Password if you have 2FA enabled.

        print("Attempting to connect to SMTP server ...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password) #log into the email account

        # Send the email 
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print(f"Email successfully sent to {recipient_email}!")

    except Exception as e:
        print("An error occurred while sending the email")
        print(f"Error details: {e}")  # <-- Add this line to show the actual error
    finally:
        if 'server' in locals() and server:
            server.quit() # close the SMTP connection

if __name__ == "__main__":
    print("Phishing email generator (Educational Tool)")
    print("WARNING: This tool is for ethical training ONLY. Use responsibly.")
    print("WITH GREAT POWER COMES GREAT RESPONSIBILITY!")

    # User inputs
    # NEVER USE YOUR MAIN EMAIL ACCOUNT OR PASSWORD FOR THIS!
    sender_email = input("Enter your email address: ")
    sender_password = input("Enter your email password: ")

    recipient_email = input("Enter the recipient's email address: ")
    email_subject = input("Enter the email subject: ")
    

    # Example Email Body (text)
    # this is a simple phishing email body for educational purposes
    email_body_plain = """   
    Dear valued user,

    We have detected unusual activity on your account. To prevent unauthorized access,
    please verify your account details immediately by clicking the link below:

    {phishing_link}  # This will be our simulated login page later!

    Failure to do so will result in account suspension.

    Sincerely,
    Your Account Security Team

    ---
    (This is an educational test email. No action required.)
    (NEVER click a link from an unknown source! If you are unsure go to the main website directly and verify your account status.)
"""

# Example of HTML Email Body
# (you can uncomment this part to use HTML instead of plain text)
email_body_html = """
 <html>
     <body style="font-family: Arial, sans-serif;">
            <p>Dear valued user,</p>
            <p>We have detected unusual activity on your account. To prevent unauthorized access,
            please verify your account details immediately by clicking the link below:</p>
            <p><a href="{phishing_link}" style="color: #1a73e8; text-decoration: none;">Verify Your Account Now</a></p>
            <p>Failure to do so will result in account suspension.</p>
            <p>Sincerely,<br>Your Account Security Team</p>
            <hr>
            <p style="font-size: 0.8em; color: #888;">(This is an educational test email. No action required. Just like Piccolo training, we're building strength through practice!)</p>
     </body>
 </html>
 """   
 # Choose which body to use and whether it's HTML
use_html_body = True # Set to True to send HTML email, False for plain text
if use_html_body:
    email_content = email_body_html
else:
    email_content = email_body_plain

# Send the phishing email
sender_phishing_email = send_phishing_email(
    sender_email=sender_email,
    sender_password=sender_password,
    recipient_email=recipient_email,
    subject=email_subject,
    body_content=email_content,
    is_html=use_html_body
)

