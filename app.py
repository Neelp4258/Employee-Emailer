# app.py
# Main file for the DazzloGo Bulk Emailer web application.

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from werkzeug.utils import secure_filename

# --- Flask App Configuration ---
app = Flask(__name__)
app.secret_key = 'a_very_secret_key_for_flash_messages' # Necessary for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# --- Email Sending Logic ---

LOGO_CID = "dazzlogo_logo"

def create_html_email_body(name, role, slot, has_logo=False):
    """
    Generates a professional, mobile-friendly HTML body for the email.
    The logo is referenced via Content-ID if available.
    """
    logo_src = f"cid:{LOGO_CID}" if has_logo else ""
    logo_html = f'<img src="{logo_src}" alt="DazzloGo Logo" style="width: 50px; height: 50px; vertical-align: middle; border-radius: 8px;">' if has_logo else '<div style="width: 50px; height: 50px; background-color: #f0f0f0; border: 1px solid #ccc; display: inline-block; vertical-align: middle; text-align: center; line-height: 50px; font-size: 8px; color: #666; border-radius: 8px;">LOGO</div>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interview Shortlisting - DazzloGo</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #f4f4f7; }}
            .email-container {{ max-width: 600px; margin: 20px auto; background-color: #ffffff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.07); }}
            .header {{ display: flex; align-items: center; justify-content: space-between; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0; margin-bottom: 20px; flex-wrap: wrap; gap: 15px; }}
            .header-left {{ display: flex; align-items: center; }}
            .company-info {{ margin-left: 15px; }}
            .company-name {{ font-size: 22px; font-weight: 600; color: #1a202c; margin: 0; }}
            .tagline {{ font-size: 12px; color: #718096; margin-top: 4px; }}
            .contact-info {{ text-align: right; font-size: 11px; color: #4a5568; }}
            .contact-info p {{ margin: 2px 0; }}
            .content {{ font-size: 15px; color: #2d3748; }}
            .content p {{ margin-bottom: 15px; }}
            .instructions ul {{ list-style-type: disc; margin-left: 20px; padding-left: 5px; color: #4a5568; }}
            .instructions li {{ margin-bottom: 8px; }}
            .footer {{ text-align: center; font-size: 12px; color: #a0aec0; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
            strong {{ font-weight: 600; color: #2d3748; }}
            a {{ color: #4299e1; text-decoration: none; }}
            @media screen and (max-width: 600px) {{
                .email-container {{ padding: 15px; }}
                .header {{ flex-direction: column; align-items: flex-start; }}
                .contact-info {{ text-align: left; margin-top: 15px; }}
                .company-name {{ font-size: 20px; }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="header-left">
                    {logo_html}
                    <div class="company-info">
                        <h1 class="company-name">DazzloGo</h1>
                        <p class="tagline">Innovate. Integrate. Inspire.</p>
                    </div>
                </div>
                <div class="contact-info">
                    <p>+91 9373015503</p>
                    <p><a href="mailto:info@dazzlo.co.in">info@dazzlo.co.in</a></p>
                </div>
            </div>
            <div class="content">
                <p>Hello {name},</p>
                <p>We are pleased to inform you that your application has been shortlisted by our Hiring Team for the role of <strong>{role}</strong>.</p>
                <p>A telephonic interview has been scheduled for you in the following time slot: <strong>{slot}</strong>.</p>
                <p>Please be prepared for the interview and follow the instructions below:</p>
                <div class="instructions">
                    <ul>
                        <li>Ensure your phone is fully charged and you are in a quiet location.</li>
                        <li>Have a copy of your updated resume ready for your reference.</li>
                        <li>Our HR representative will call you during the scheduled time.</li>
                    </ul>
                </div>
                <p>If you have any questions or need to reschedule, please reply to this email at your earliest convenience.</p>
                <p>We look forward to speaking with you.</p>
                <p>Best regards,<br><strong>The DazzloGo HR Team</strong></p>
            </div>
            <div class="footer">
                <p>&copy; 2025 DazzloGo. All rights reserved.</p>
                <p><a href="http://www.dazzlo.co.in">www.dazzlo.co.in</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, logo_data=None):
    """Sends a single email using Zoho SMTP."""
    try:
        msg = MIMEMultipart('related')
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        if logo_data:
            img = MIMEImage(logo_data, 'png')
            img.add_header('Content-ID', f'<{LOGO_CID}>')
            img.add_header('Content-Disposition', 'inline', filename="logo.png")
            msg.attach(img)

        with smtplib.SMTP_SSL("smtp.zoho.in", 465, timeout=15) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True, f"Email sent successfully to {recipient_email}"
    except Exception as e:
        return False, f"Failed to send to {recipient_email}: {e}"


# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main page with the form."""
    return render_template('index.html')

@app.route('/send_emails', methods=['POST'])
def send_emails_route():
    """Handles form submission and sends emails."""
    sender_email = request.form.get('email')
    sender_password = request.form.get('password')
    
    if not sender_email or not sender_password:
        flash('Email and Password are required.', 'danger')
        return redirect(url_for('index'))

    # Handle CSV file
    csv_file = request.files.get('csv_file')
    if not csv_file or csv_file.filename == '':
        flash('CSV file is required.', 'danger')
        return redirect(url_for('index'))
    
    csv_filename = secure_filename(csv_file.filename)
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
    csv_file.save(csv_path)

    # Load logo data from the static folder
    logo_data = None
    logo_path = os.path.join('static', 'logo.png')
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            logo_data = f.read()

    # Process and send emails
    results = []
    sent_count = 0
    failed_count = 0
    
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            required_columns = ['email', 'name', 'role', 'slot']
            if not all(col in reader.fieldnames for col in required_columns):
                flash(f"CSV file must contain columns: {', '.join(required_columns)}", 'danger')
                return redirect(url_for('index'))

            for row in reader:
                recipient_email = row['email'].strip()
                name = row['name'].strip()
                role = row['role'].strip()
                slot = row['slot'].strip()
                
                subject = f"Interview Invitation for {role} at DazzloGo"
                html_body = create_html_email_body(name, role, slot, has_logo=bool(logo_data))
                
                success, message = send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, logo_data)
                
                results.append({'email': recipient_email, 'status': 'Success' if success else 'Failed', 'message': message})
                if success:
                    sent_count += 1
                else:
                    failed_count += 1
    except Exception as e:
        flash(f"An error occurred while processing the CSV file: {e}", 'danger')
        return redirect(url_for('index'))
    finally:
        # Clean up uploaded file
        if os.path.exists(csv_path):
            os.remove(csv_path)

    return render_template('results.html', results=results, sent_count=sent_count, failed_count=failed_count)


if __name__ == '__main__':
    # Use host='0.0.0.0' to make it accessible on your local network
    app.run(debug=True, host='0.0.0.0')
