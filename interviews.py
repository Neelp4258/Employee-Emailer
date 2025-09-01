import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage # Import MIMEImage
import os
import base64
import ssl
import json

# --- Configuration ---
# CSV file containing recipient data (email, name, role, slot)
CSV_FILE = "recipients.csv"

# JSON file for credentials
CREDS_FILE = "creds.json"

# Path to your company logo (optional)
LOGO_PATH = "logo.png"
# Define a Content-ID for the logo image
LOGO_CID = "dazzlo_logo"

# --- Helper Functions ---

def load_credentials(creds_file):
    """Loads sender email and password from a JSON file."""
    if not os.path.exists(creds_file):
        print(f"Error: Credentials file '{creds_file}' not found.")
        print("Please create a 'creds.json' file with your Zoho email and password:")
        print('Example: {"email": "your_email@zoho.com", "password": "your_app_password_or_regular_password"}')
        return None, None
    try:
        with open(creds_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
            email = creds.get('email')
            password = creds.get('password')
            if not email or not password:
                print(f"Error: '{creds_file}' must contain 'email' and 'password' fields.")
                return None, None
            return email, password
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{creds_file}'. Please check its format.")
        return None, None
    except Exception as e:
        print(f"Error loading credentials from '{creds_file}': {e}")
        return None, None

def get_logo_data(logo_path):
    """Reads the logo image file in binary mode."""
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as img_file:
                logo_data = img_file.read()
                print(f"Info: Logo file '{logo_path}' found and read. Size: {len(logo_data)} bytes.")
                return logo_data
        except Exception as e:
            print(f"Warning: Could not read logo file '{logo_path}'. Error: {e}")
            return None
    else:
        print(f"Warning: Logo file '{logo_path}' not found at '{os.path.abspath(logo_path)}'. Using a placeholder.")
        return None

def create_html_email_body(name, role, slot, has_logo=False):
    """
    Generates the full HTML body for the email, including the letterhead.
    This recreates the visual elements from the letterhead.py in HTML/CSS.
    The logo is now referenced via Content-ID if available.
    """
    # Define the logo HTML based on whether the logo will be attached (has_logo)
    logo_src = f"cid:{LOGO_CID}" if has_logo else ""
    logo_html = ""
    if has_logo:
        logo_html = f"""
        <img src="{logo_src}" alt="Company Logo" style="width: 50px; height: 50px; vertical-align: middle; border-radius: 8px;">
        """
    else:
        logo_html = """
        <div style="width: 50px; height: 50px; background-color: #f0f0f0; border: 1px solid #ccc; display: inline-block; vertical-align: middle; text-align: center; line-height: 50px; font-size: 8px; color: #666; border-radius: 8px;">LOGO</div>
        """

    # HTML structure and inline CSS for the letterhead and email body
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interview Shortlisting - Dazzlo Enterprises Pvt Ltd</title>
        <style>
            body {{
                font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .container {{
                max-width: 700px;
                margin: 20px auto;
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                border: 1px solid #e0e0e0;
            }}
            .header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding-bottom: 20px;
                border-bottom: 2px solid #e0e0e0; /* Placeholder for golden lines */
                margin-bottom: 20px;
                flex-wrap: wrap; /* Allow items to wrap on smaller screens */
            }}
            .header-left {{
                display: flex;
                align-items: center;
                flex-basis: 60%; /* Take up more space on wider screens */
                min-width: 250px; /* Ensure it doesn't get too small */
            }}
            .company-info {{
                margin-left: 15px;
            }}
            .company-name {{
                font-family: 'Times New Roman', serif; /* Fallback for Playfair Display */
                font-size: 24px;
                font-weight: bold;
                color: #222;
                margin: 0;
            }}
            .tagline {{
                font-style: italic;
                font-size: 11px;
                color: #666;
                margin-top: 5px;
            }}
            .contact-info {{
                text-align: right;
                font-size: 10px;
                color: #444;
                font-weight: bold;
                flex-basis: 35%; /* Take up less space on wider screens */
                min-width: 180px; /* Ensure it doesn't get too small */
            }}
            .contact-info p {{
                margin: 2px 0;
            }}
            .golden-lines {{
                border-bottom: 1.5px solid #D4AF37; /* Golden color */
                padding-bottom: 4px;
                margin-bottom: 15px;
            }}
            .golden-lines::after {{
                content: '';
                display: block;
                border-bottom: 0.8px solid #D4AF37; /* Second thinner golden line */
                margin-top: 4px;
            }}
            .content {{
                font-size: 14px;
                color: #333;
            }}
            .content p {{
                margin-bottom: 10px;
            }}
            .instructions ul {{
                list-style-type: disc;
                margin-left: 20px;
                padding-left: 0;
            }}
            .instructions li {{
                margin-bottom: 5px;
            }}
            .footer {{
                text-align: center;
                font-size: 10px;
                color: #666;
                margin-top: 30px;
                padding-top: 15px;
                border-top: 1px solid #e0e0e0;
            }}
            .footer-website {{
                text-align: right;
                font-weight: bold;
                margin-top: 5px;
            }}
            strong {{
                font-weight: bold;
            }}

            /* --- Mobile Responsiveness --- */
            @media screen and (max-width: 600px) {{
                .container {{
                    padding: 8px; /* Further reduced padding */
                    margin: 3px auto; /* Further reduced margin */
                }}
                .header {{
                    flex-direction: column; /* Stack items vertically */
                    align-items: flex-start; /* Align items to the start */
                    padding-bottom: 5px; /* Further reduced padding */
                    margin-bottom: 5px; /* Further reduced margin */
                }}
                .header-left, .contact-info {{
                    flex-basis: 100%; /* Take full width */
                    min-width: unset; /* Remove min-width constraint */
                    width: 100%; /* Ensure full width */
                }}
                .header-left {{
                    margin-bottom: 8px; /* Further reduced space between stacked sections */
                }}
                .company-info {{
                    margin-left: 8px; /* Further reduced margin */
                }}
                .contact-info {{
                    text-align: left; /* Align contact info to left on mobile */
                    margin-top: 3px; /* Further reduced space from company info */
                }}
                .company-name {{
                    font-size: 15px; /* Reduced font size for mobile */
                }}
                .tagline {{
                    font-size: 8px; /* Even smaller font size for mobile */
                }}
                .contact-info p {{
                    font-size: 7px; /* Even smaller font size for mobile */
                }}
                .content {{
                    font-size: 11px; /* Slightly smaller content font */
                }}
                .footer, .footer-website {{
                    text-align: center; /* Center footer elements */
                    font-size: 7px; /* Smaller footer font */
                }}
                img[alt="Company Logo"] {{
                    width: 35px !important; /* Even smaller logo */
                    height: 35px !important;
                }}
                .golden-lines {{
                    margin-bottom: 8px; /* Reduced margin */
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-left">
                    {logo_html}
                    <div class="company-info">
                        <h1 class="company-name">Dazzlo Enterprises Pvt Ltd</h1>
                        <p class="tagline">Redefining lifestyle with Innovations and Dreams</p>
                    </div>
                </div>
                <div class="contact-info">
                    <p>Tel: +91 9373015503</p>
                    <p>Email: <a href="mailto:info@dazzlo.co.in" style="color: #007bff; text-decoration: none;">info@dazzlo.co.in</a></p>
                    <p>Location: Kalyan, Maharashtra 421301</p>
                </div>
            </div>
            <div class="golden-lines"></div>

            <div class="content">
                <p>Hello {name},</p>
                <p>We are pleased to inform you that your application has been shortlisted by our Hiring Team for the role of <strong>{role}</strong>.</p>
                <p>An Interview has been scheduled on <strong>{slot}</strong>.</p>
                <p>Instructions for the Interview-</p>
                <div class="instructions">
                    <ul>
                        <li>Please ensure your phone is fully charged and reachable at the scheduled time.</li>
                        <li>Keep a copy of your updated resume handy for reference.</li>
                        <li>Be in a quiet environment to avoid any background disturbance.</li>
                        <li>Make sure your network connection is stable to avoid call drops.</li>
                        <li>The call will be made from our end, so kindly stay available and attentive.</li>
                    </ul>
                </div>
                <p>If you have any questions or need to reschedule, feel free to reply to this email.</p>
                <p>Looking forward to speaking with you.</p>
                <p>Best regards,<br>HR Team<br>DazzloHR<br>9373015503</p>
            </div>

            <div class="footer">
                <p>&copy; 2025 Dazzlo Enterprises Pvt Ltd. All rights reserved.</p>
                <p class="footer-website">www.dazzlo.co.in</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def send_email(sender_email, sender_password, recipient_email, subject, html_body, logo_data=None):
    """
    Sends a single email using the known working Zoho SMTP server and port (smtp.zoho.in:465 SSL).
    Now includes the logo as a CID attachment.
    """
    current_server = "smtp.zoho.in"
    current_port = 465
    current_method = "SSL"

    print(f"Attempting to send email to {recipient_email} via {current_server}:{current_port} ({current_method})...")

    try:
        msg = MIMEMultipart('related') # Use 'related' to allow inline images
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach HTML body
        msg.attach(MIMEText(html_body, 'html'))

        # Attach logo if data is provided
        if logo_data:
            img = MIMEImage(logo_data, 'png') # Assuming it's a PNG
            img.add_header('Content-ID', f'<{LOGO_CID}>') # Important: angle brackets for Content-ID
            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(LOGO_PATH))
            msg.attach(img)
            print(f"Info: Attached logo '{os.path.basename(LOGO_PATH)}' with Content-ID '{LOGO_CID}'.")
        else:
            print("Info: No logo data provided, sending email without inline logo attachment.")

        # Use SMTP_SSL for direct SSL connection
        with smtplib.SMTP_SSL(current_server, current_port, timeout=15) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {recipient_email} via {current_server}:{current_port}.")
        return True
    except smtplib.SMTPAuthenticationError:
        print(f"❌ Authentication Error for {recipient_email} on {current_server}:{current_port}. Check your email and password (especially for App-specific passwords if 2FA is enabled).")
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection Error for {recipient_email} on {current_server}:{current_port}: {e}. Check server address, port, and network connectivity.")
    except smtplib.SMTPServerDisconnected:
        print(f"❌ Server Disconnected Error for {recipient_email} on {current_server}:{current_port}. This can happen if the server closes the connection unexpectedly.")
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error for {recipient_email} on {current_server}:{current_port}: {e}. A general SMTP error occurred.")
    except Exception as e:
        print(f"❌ An unexpected error occurred for {recipient_email} on {current_server}:{current_port}: {e}")

    print(f"❌ Failed to send email to {recipient_email}.")
    return False

# --- Main Execution ---
def main():
    # Load credentials
    sender_email, sender_password = load_credentials(CREDS_FILE)
    if not sender_email or not sender_password:
        return # Exit if credentials are not loaded

    # Check if CSV file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file '{CSV_FILE}' not found.")
        print("Please create a CSV file named 'recipients.csv' with columns: email,name,role,slot")
        print("Example content:")
        print("test@example.com,John Doe,Software Engineer,Monday 10:00 AM")
        return

    # Get logo data (binary)
    logo_data = get_logo_data(LOGO_PATH)
    has_logo = logo_data is not None

    sent_count = 0
    failed_count = 0

    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        if not all(col in reader.fieldnames for col in ['email', 'name', 'role', 'slot']):
            print(f"Error: CSV file must contain 'email', 'name', 'role', 'slot' columns. Found: {reader.fieldnames}")
            return

        print(f"\n--- Starting bulk email sending from {CSV_FILE} ---")
        for row in reader:
            recipient_email = row['email'].strip() if row['email'] else ''
            name = row['name'].strip() if row['name'] else ''
            role = row['role'].strip() if row['role'] else ''
            slot = row['slot'].strip() if row['slot'] else ''

            print(f"Preparing email for {name} ({recipient_email})...")

            subject = f"Interview Shortlisting - {role} - DazzloHR"
            # Pass has_logo to create_html_email_body
            html_body = create_html_email_body(name, role, slot, has_logo)

            # Pass logo_data to send_email
            if send_email(sender_email, sender_password, recipient_email, subject, html_body, logo_data):
                sent_count += 1
            else:
                failed_count += 1

    print("\n--- Email sending complete ---")
    print(f"Total emails attempted: {sent_count + failed_count}")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed to send: {failed_count}")
    print("Please check the console for any specific error messages.")

if __name__ == "__main__":
    main()
