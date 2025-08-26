# app.py
import os
import csv
import smtplib
import logging
import time
import json
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from flask import (Flask, render_template, request, flash, redirect, url_for,
                   g, abort, jsonify)
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
    elif file_type == 'attachment':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar']
    elif file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg']
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def format_date_for_email():
    """Formats the current date for email templates."""
    now = datetime.now()
    day = now.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return now.strftime(f"%d{suffix} %B %Y")

def validate_email_credentials(email, password):
    """Validates email credentials by attempting to connect to Zoho SMTP."""
    try:
        with smtplib.SMTP_SSL("smtp.zoho.in", 465, timeout=10) as server:
            server.login(email, password)
        return True, "Credentials are valid"
    except smtplib.SMTPAuthenticationError:
        return False, "Invalid email or app password"
    except smtplib.SMTPException as e:
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def get_logo_for_template(template_type):
    """Returns the appropriate logo data and CID for the given template type."""
    try:
        if template_type in ['interview', 'congratulations', 'partnership_hr']:
            # Use HR.png for HR-related templates
            logo_path = os.path.join(app.root_path, 'static', 'images', 'HR.png')
            logo_cid = 'hr_logo'
        elif template_type == 'partnership_enterprises':
            # Use Primary.png for Dazzlo Enterprises template
            logo_path = os.path.join(app.root_path, 'static', 'images', 'Primary.png')
            logo_cid = 'enterprises_logo'
        elif template_type == 'trivantaedge':
            # Use Trivanta Edge logo
            logo_path = os.path.join(app.root_path, 'static', 'images', 'trivanta.png')
            logo_cid = 'trivanta_logo'
        else:
            # Default to HR logo
            logo_path = os.path.join(app.root_path, 'static', 'images', 'HR.png')
            logo_cid = 'hr_logo'
        
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                return f.read(), logo_cid
        else:
            logging.warning(f"Logo file not found: {logo_path}")
            return None, None
    except Exception as e:
        logging.error(f"Error loading logo for template {template_type}: {e}")
        return None, None

# --- MODIFIED: This function now accepts credentials as arguments and multiple attachments ---
def send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, template_type, attachments=None):
    """Sends a single email using Zoho SMTP with error handling and multiple attachments support.
    
    Args:
        sender_email: Sender's email address
        sender_password: Sender's password
        recipient_email: Recipient's email address
        subject: Email subject
        html_body: Email HTML body
        template_type: Template type for logo selection
        attachments: List of dictionaries with 'data' and 'filename' keys
    """
    
    if not sender_email or not sender_password:
        return False, "Email or Password was not provided."

    try:
        msg = MIMEMultipart('related')
        msg['From'] = f"{app.config['COMPANY_NAME']} <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        # Automatically attach the appropriate logo based on template type
        logo_data, logo_cid = get_logo_for_template(template_type)
        if logo_data and logo_cid:
            img = MIMEImage(logo_data)
            img.add_header('Content-ID', f"<{logo_cid}>")
            msg.attach(img)
            logging.info(f"Attached logo for template: {template_type}")

        # Attach multiple files if provided
        if attachments:
            for attachment in attachments:
                if 'data' in attachment and 'filename' in attachment:
                    try:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment['data'])
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {attachment["filename"]}'
                        )
                        msg.attach(part)
                        logging.info(f"Attached file: {attachment['filename']}")
                    except Exception as e:
                        logging.warning(f"Failed to attach file {attachment.get('filename', 'unknown')}: {e}")

        with smtplib.SMTP_SSL("smtp.zoho.in", 465, timeout=20) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            logging.info(f"Email sent successfully to {recipient_email}")
            return True, "Email sent successfully"
            
    except smtplib.SMTPAuthenticationError:
        logging.error(f"SMTP Authentication failed for {sender_email}")
        return False, "SMTP Authentication failed. Please check your email and app password."
    except smtplib.SMTPRecipientsRefused as e:
        logging.error(f"Recipient refused for {recipient_email}: {e}")
        return False, f"Recipient email address is invalid: {recipient_email}"
    except smtplib.SMTPServerDisconnected:
        logging.error("SMTP server disconnected")
        return False, "SMTP server disconnected. Please try again."
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error for {recipient_email}: {e}")
        return False, f"SMTP error: {str(e)}"
    except Exception as e:
        logging.error(f"Unexpected error sending email to {recipient_email}: {e}")
        return False, f"Unexpected error: {str(e)}"

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/preview/<template_name>')
def preview_email(template_name):
    if template_name not in [
        'interview',
        'congratulations',
        'partnership_enterprises',
        'partnership_hr',
        'trivantaedge',
        'trivantaedge_intro',
        'trivantaedge_followup',
        'trivantaedge_thanks',
        'trivantaedge_case_study',
        'hr_intro',
        'hr_followup',
        'hr_thanks',
        'hr_case_study',
        'enterprises_intro',
        'enterprises_followup',
        'enterprises_thanks',
        'enterprises_case_study'
    ]:
        abort(404)
    preview_data = {
        'name': "Alex Doe",
        'role': "Lead Product Designer",
        'slot': "October 25, 2025, at 11:00 AM",
        'company': "Sample Company Ltd",
        'current_date': format_date_for_email()
    }
    
    # Add sample sender information for partnership templates
    if template_name in [
        'partnership_enterprises',
        'partnership_hr',
        'trivantaedge',
        'trivantaedge_intro',
        'trivantaedge_followup',
        'trivantaedge_thanks',
        'trivantaedge_case_study',
        'hr_intro',
        'hr_followup',
        'hr_thanks',
        'hr_case_study',
        'enterprises_intro',
        'enterprises_followup',
        'enterprises_thanks',
        'enterprises_case_study'
    ]:
        preview_data.update({
            'sender_name': "John Smith",
            'sender_designation': "Senior Business Development Manager",
            'sender_email': "john.smith@dazzlo.co.in"
        })
    
    # Render the email template
    html_content = render_template(f"emails/{template_name}.html", **preview_data)
    
    # Replace Content-ID references with actual image URLs for preview
    if template_name in ['interview', 'congratulations', 'partnership_hr'] or template_name.startswith('hr_'):
        # Use HR.png for HR templates
        html_content = html_content.replace('src="cid:hr_logo"', 'src="/static/images/HR.png"')
    elif template_name == 'partnership_enterprises' or template_name.startswith('enterprises_'):
        # Use Primary.png for Dazzlo Enterprises template
        html_content = html_content.replace('src="cid:enterprises_logo"', 'src="/static/images/Primary.png"')
    elif template_name.startswith('trivantaedge'):
        # Use Trivanta Edge logo for preview
        html_content = html_content.replace('src="cid:trivanta_logo"', 'src="/static/images/trivanta.png"')
    
    return html_content

@app.route('/validate_credentials', methods=['POST'])
def validate_credentials():
    """Validates email credentials without sending any emails."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'})
        
        success, message = validate_email_credentials(email, password)
        return jsonify({'success': success, 'message': message})
        
    except Exception as e:
        logging.error(f"Error validating credentials: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during validation'})

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

    # --- CSV Data Handling & Validation ---
    csv_data = None
    csv_path = None
    
    # Check if CSV file was uploaded
    if 'csv_file' in request.files and request.files['csv_file'].filename != '':
        csv_file = request.files['csv_file']
        if not allowed_file(csv_file.filename, 'csv'):
            flash('Invalid file type. Please upload a .csv file.', 'danger')
            return redirect(url_for('index'))
        
        csv_filename = secure_filename(csv_file.filename)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        csv_file.save(csv_path)
    
    # Check if CSV data was entered in notepad
    elif 'csv_notepad' in request.form and request.form['csv_notepad'].strip():
        csv_data = request.form['csv_notepad'].strip()
        # Create a temporary file from notepad data
        csv_filename = f"notepad_data_{int(time.time())}.csv"
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as file:
                file.write(csv_data)
        except Exception as e:
            flash(f'Error creating CSV file from notepad data: {e}', 'danger')
            return redirect(url_for('index'))
    
    else:
        flash('Please either upload a CSV file or enter data in the notepad.', 'danger')
        return redirect(url_for('index'))

    # Logo handling is now automatic based on template type
    # No manual logo upload needed

    # Handle multiple attachment files
    attachments = []
    attachment_files = request.files.getlist('attachment_files')
    
    for attachment_file in attachment_files:
        if attachment_file and attachment_file.filename != '' and allowed_file(attachment_file.filename, 'attachment'):
            try:
                attachment_data = attachment_file.read()
                attachment_filename = secure_filename(attachment_file.filename)
                
                # Check file size (max 25MB per file)
                if len(attachment_data) > 25 * 1024 * 1024:
                    logging.warning(f"Attachment file {attachment_filename} is too large ({len(attachment_data)/1024/1024:.2f} MB)")
                    flash(f'File {attachment_filename} is too large. Maximum size is 25MB per file.', 'warning')
                    continue
                
                attachments.append({
                    'data': attachment_data,
                    'filename': attachment_filename
                })
                logging.info(f"Attachment file processed: {attachment_filename} ({len(attachment_data)/1024/1024:.2f} MB)")
            except Exception as e:
                logging.error(f"Error processing attachment file {attachment_file.filename}: {e}")
                flash(f'Error processing file {attachment_file.filename}', 'warning')
    
    # Check total attachment size (max 100MB total)
    total_size = sum(len(att['data']) for att in attachments)
    if total_size > 100 * 1024 * 1024:
        logging.warning(f"Total attachment size is too large ({total_size/1024/1024:.2f} MB)")
        flash(f'Total attachment size is too large ({total_size/1024/1024:.2f} MB). Maximum total size is 100MB.', 'danger')
        return redirect(url_for('index'))
    
    if attachments:
        logging.info(f"Total of {len(attachments)} attachment files processed, total size: {total_size/1024/1024:.2f} MB")

    # --- CSV Processing & Email Sending ---
    results = []
    sent_count, failed_count = 0, 0
    
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            required_columns = {
                'interview': ['email', 'name', 'role', 'slot'],
                'congratulations': ['email', 'name', 'role', 'company'],
                'partnership_enterprises': ['email', 'company'],
                'partnership_hr': ['email', 'company'],
                'trivantaedge': ['email', 'company'],
                'trivantaedge_intro': ['email', 'company'],
                'trivantaedge_followup': ['email', 'company'],
                'trivantaedge_thanks': ['email', 'company'],
                'trivantaedge_case_study': ['email', 'company'],
                'hr_intro': ['email', 'company'],
                'hr_followup': ['email', 'company'],
                'hr_thanks': ['email', 'company'],
                'hr_case_study': ['email', 'company'],
                'enterprises_intro': ['email', 'company'],
                'enterprises_followup': ['email', 'company'],
                'enterprises_thanks': ['email', 'company'],
                'enterprises_case_study': ['email', 'company']
            }.get(template_type)

            if not all(col in reader.fieldnames for col in required_columns):
                flash(f"CSV file is missing required columns. It needs: {', '.join(required_columns)}", 'danger')
                return redirect(url_for('index'))

            for row in reader:
                recipient_email = row.get('email', '').strip()
                if not recipient_email:
                    continue

                email_data = {key: row.get(key, '').strip() for key in required_columns}

                subject = (
                    f"🎉 Congratulations! You're Selected for the {email_data['role']} Role at {email_data['company']}" if template_type == 'congratulations' else
                    "Strategic Partnership Opportunity - Dazzlo Enterprises Pvt Ltd" if template_type == 'partnership_enterprises' else
                    "Strategic Partnership Opportunity - DazzloHR Solutions" if template_type == 'partnership_hr' else
                    "Strategic Partnership Opportunity - Trivanta Edge" if template_type == 'trivantaedge' else
                    "Introduction - Trivanta Edge" if template_type == 'trivantaedge_intro' else
                    "Following up: Strategic Partnership - Trivanta Edge" if template_type == 'trivantaedge_followup' else
                    "Thank you - Trivanta Edge" if template_type == 'trivantaedge_thanks' else
                    "Case Study Highlights - Trivanta Edge" if template_type == 'trivantaedge_case_study' else
                    "Introduction - DazzloHR Solutions" if template_type == 'hr_intro' else
                    "Following up: DazzloHR Solutions" if template_type == 'hr_followup' else
                    "Thank you - DazzloHR Solutions" if template_type == 'hr_thanks' else
                    "Case Study Highlights - DazzloHR Solutions" if template_type == 'hr_case_study' else
                    "Introduction - Dazzlo Enterprises Pvt Ltd" if template_type == 'enterprises_intro' else
                    "Following up: Dazzlo Enterprises Pvt Ltd" if template_type == 'enterprises_followup' else
                    "Thank you - Dazzlo Enterprises Pvt Ltd" if template_type == 'enterprises_thanks' else
                    "Case Study Highlights - Dazzlo Enterprises Pvt Ltd" if template_type == 'enterprises_case_study' else
                    f"Interview for {email_data['role']} at {app.config['COMPANY_NAME']}"
                )
                
                # Add sender information for partnership templates
                if template_type in [
                    'partnership_enterprises', 'partnership_hr',
                    'trivantaedge', 'trivantaedge_intro', 'trivantaedge_followup', 'trivantaedge_thanks', 'trivantaedge_case_study',
                    'hr_intro', 'hr_followup', 'hr_thanks', 'hr_case_study',
                    'enterprises_intro', 'enterprises_followup', 'enterprises_thanks', 'enterprises_case_study'
                ]:
                    email_data.update({
                        'sender_name': sender_name,
                        'sender_designation': sender_designation,
                        'sender_email': sender_email
                    })
                
                # Add current date to all templates
                email_data['current_date'] = format_date_for_email()
                
                html_body = render_template(f"emails/{template_type}.html", **email_data)

                # --- MODIFIED: Pass credentials and attachments to the sending function ---
                success, message = send_email_smtp(sender_email, sender_password, recipient_email, subject, html_body, template_type, attachments)
                
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
    # Allow specifying port via CLI arg or PORT env var. Default to 8000 to avoid Windows 5000 exclusion
    import sys
    port_str = os.environ.get('PORT') if 'PORT' in os.environ else (sys.argv[1] if len(sys.argv) > 1 else None)
    try:
        port = int(port_str) if port_str else 8000
    except (TypeError, ValueError):
        port = 8000
    app.run(debug=True, host='0.0.0.0', port=port)