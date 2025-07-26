# app.py
import os
import csv
import smtplib
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from flask import (Flask, render_template, request, flash, redirect, url_for,
                   g, abort)
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(
    filename='dazzlo_emailer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Flask App Initialization & Configuration ---
app = Flask(__name__)
app.config.from_pyfile('config.py')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Global App Context ---
@app.context_processor
def inject_global_vars():
    return {
        'config': app.config,
        'now': datetime.now(timezone.utc)
    }

# --- Helper Functions ---
def allowed_file(filename, file_type):
    """Checks if the uploaded file has an allowed extension."""
    if file_type == 'csv':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'
    elif file_type == 'document':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'doc', 'docx']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# --- MODIFIED: This function now accepts credentials as arguments ---
def send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, logo_data=None, cv_data=None, cv_filename=None):
    """Sends a single email using Zoho SMTP with error handling."""
    
    if not sender_email or not sender_password:
        return False, "Email or Password was not provided."

    try:
        msg = MIMEMultipart('related')
        msg['From'] = f"{app.config['COMPANY_NAME']} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        if logo_data:
            img = MIMEImage(logo_data)
            img.add_header('Content-ID', f"<{app.config['LOGO_CID']}>")
            msg.attach(img)

        if cv_data:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(cv_data)
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {cv_filename}'
            )
            msg.attach(part)

        with smtplib.SMTP_SSL("smtp.zoho.in", 465, timeout=20) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logging.info(f"Email sent successfully to {recipient_email}")
        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError:
        logging.error(f"SMTP Auth Error for {recipient_email}. Check credentials.")
        return False, "Authentication Failed. Please check your email and App Password."
    except Exception as e:
        logging.error(f"Failed to send to {recipient_email}: {e}")
        return False, f"An unexpected error occurred: {e}"

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview/<template_name>')
def preview_email(template_name):
    if template_name not in ['interview', 'congratulations', 'partnership']:
        abort(404)
    preview_data = {
        'name': "Alex Doe",
        'role': "Lead Product Designer",
        'slot': "October 25, 2025, at 11:00 AM",
        'company': "Sample Company Ltd"
    }
    
    # Add sample sender information for partnership template
    if template_name == 'partnership':
        preview_data.update({
            'sender_name': "John Smith",
            'sender_designation': "Senior Business Development Manager",
            'sender_email': "john.smith@dazzlo.co.in"
        })
    
    return render_template(f"emails/{template_name}.html", **preview_data)

@app.route('/send_emails', methods=['POST'])
def send_emails_route():
    """Handles form submission, processes the CSV, and sends emails."""
    
    # --- MODIFIED: Get credentials from the form (NOT RECOMMENDED) ---
    sender_email = request.form.get('email')
    sender_password = request.form.get('password')
    template_type = request.form.get('template_type', 'interview')
    
    # Get sender information for partnership template
    sender_name = request.form.get('sender_name', '')
    sender_designation = request.form.get('sender_designation', '')

    if not sender_email or not sender_password:
        flash('Email and App Password are required.', 'danger')
        return redirect(url_for('index'))

    # --- File Handling & Validation ---
    if 'csv_file' not in request.files:
        flash('No CSV file part in the request.', 'danger')
        return redirect(url_for('index'))
    
    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        flash('No CSV file selected.', 'danger')
        return redirect(url_for('index'))

    if not (csv_file and allowed_file(csv_file.filename, 'csv')):
        flash('Invalid file type. Please upload a .csv file.', 'danger')
        return redirect(url_for('index'))

    csv_filename = secure_filename(csv_file.filename)
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
    csv_file.save(csv_path)

    logo_data = None
    logo_file = request.files.get('logo_file')
    if logo_file and logo_file.filename != '' and allowed_file(logo_file.filename, 'image'):
        logo_data = logo_file.read()

    cv_data = None
    cv_filename = None
    cv_file = request.files.get('cv_file')
    if cv_file and cv_file.filename != '' and allowed_file(cv_file.filename, 'document'):
        cv_data = cv_file.read()
        cv_filename = secure_filename(cv_file.filename)

    # --- CSV Processing & Email Sending ---
    results = []
    sent_count, failed_count = 0, 0
    
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            required_columns = {
                'interview': ['email', 'name', 'role', 'slot'],
                'congratulations': ['email', 'name', 'role', 'company'],
                'partnership': ['email', 'company']
            }.get(template_type)

            if not all(col in reader.fieldnames for col in required_columns):
                flash(f"CSV file is missing required columns. It needs: {', '.join(required_columns)}", 'danger')
                return redirect(url_for('index'))

            for row in reader:
                recipient_email = row.get('email', '').strip()
                if not recipient_email:
                    continue

                email_data = {key: row.get(key, '').strip() for key in required_columns}

                subject = f"🎉 Congratulations! You're Selected for the {email_data['role']} Role at {email_data['company']}" if template_type == 'congratulations' else f"Strategic Partnership Opportunity - DazzloHR Solutions" if template_type == 'partnership' else f"Interview for {email_data['role']} at {app.config['COMPANY_NAME']}"
                
                # Add sender information for partnership template
                if template_type == 'partnership':
                    email_data.update({
                        'sender_name': sender_name,
                        'sender_designation': sender_designation,
                        'sender_email': sender_email
                    })
                
                html_body = render_template(f"emails/{template_type}.html", **email_data)

                # --- MODIFIED: Pass credentials to the sending function ---
                success, message = send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, logo_data, cv_data, cv_filename)
                
                results.append({'email': recipient_email, 'status': 'Success' if success else 'Failed', 'message': message})
                if success:
                    sent_count += 1
                else:
                    failed_count += 1

    except Exception as e:
        logging.error(f"Error processing CSV file '{csv_filename}': {e}")
        flash(f"An error occurred while processing the CSV file: {e}", 'danger')
        return redirect(url_for('index'))
    finally:
        if os.path.exists(csv_path):
            os.remove(csv_path)

    return render_template('results.html', results=results, sent_count=sent_count, failed_count=failed_count)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')