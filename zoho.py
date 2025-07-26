import smtplib
import csv
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
import os
from typing import List, Dict

class ZohoBulkMailer:
    def __init__(self, email: str, password: str, smtp_server: str = None, smtp_port: int = None):
        """
        Initialize the Zoho bulk mailer
        
        Args:
            email: Your Zoho email address
            password: Your Zoho email password (or app-specific password)
            smtp_server: SMTP server (auto-detected based on email domain)
            smtp_port: SMTP port
        """
        self.email = email
        self.password = password
        
        # Auto-detect SMTP settings based on email domain
        if smtp_server is None:
            domain = email.split('@')[1].lower()
            if 'zoho' in domain:
                self.smtp_server = "smtp.zoho.com"
                self.smtp_port = 587
            elif domain.endswith('.zoho.com') or domain.endswith('.zoho.in'):
                self.smtp_server = f"smtp.{domain}"
                self.smtp_port = 587
            else:
                # Default Zoho settings
                self.smtp_server = "smtp.zoho.com"
                self.smtp_port = 587
        else:
            self.smtp_server = smtp_server
            self.smtp_port = smtp_port if smtp_port else 587
        
    def read_emails_from_csv(self, csv_file: str) -> List[Dict]:
        """
        Read email addresses and company names from CSV file
        Expected CSV format: email,company (company name for personalization)
        
        Args:
            csv_file: Path to CSV file containing email addresses and company names
            
        Returns:
            List of dictionaries with email and company
        """
        recipients = []
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                # First, try to detect if there are headers
                sample = file.read(1024)
                file.seek(0)
                
                # Check if first line looks like headers
                first_line = file.readline().strip().lower()
                file.seek(0)
                
                has_headers = 'email' in first_line or 'mail' in first_line
                
                if has_headers:
                    reader = csv.DictReader(file)
                    for row_num, row in enumerate(reader, start=2):  # Start from 2 since headers are line 1
                        try:
                            # Try different possible column names for email
                            email = None
                            company = None
                            
                            # Look for email column
                            for key in row.keys():
                                if key and key.lower() in ['email', 'e-mail', 'mail', 'email_address']:
                                    email = row[key]
                                    break
                            
                            # Look for company/name column
                            for key in row.keys():
                                if key and key.lower() in ['company', 'name', 'company_name', 'organization']:
                                    company = row[key]
                                    break
                            
                            # Clean and validate email
                            if email:
                                email = str(email).strip() if email else ''
                                company = str(company).strip() if company else ''
                                
                                if email and '@' in email:  # Basic email validation
                                    recipients.append({
                                        'email': email,
                                        'company': company
                                    })
                                else:
                                    print(f"Warning: Invalid email in row {row_num}: '{email}'")
                            else:
                                print(f"Warning: No email found in row {row_num}")
                                
                        except Exception as e:
                            print(f"Error processing row {row_num}: {e}")
                            continue
                else:
                    # No headers, assume first column is email, second is company
                    reader = csv.reader(file)
                    for row_num, row in enumerate(reader, start=1):
                        try:
                            if len(row) >= 1:
                                email = str(row[0]).strip() if row[0] else ''
                                company = str(row[1]).strip() if len(row) > 1 and row[1] else ''
                                
                                if email and '@' in email:  # Basic email validation
                                    recipients.append({
                                        'email': email,
                                        'company': company
                                    })
                                else:
                                    print(f"Warning: Invalid email in row {row_num}: '{email}'")
                        except Exception as e:
                            print(f"Error processing row {row_num}: {e}")
                            continue
                            
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_file}' not found!")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
        
        print(f"Successfully loaded {len(recipients)} valid recipients from CSV")
        return recipients
    
    def create_message(self, to_email: str, company_name: str, subject: str, 
                      body: str, pdf_path: str = None, logo_path: str = None) -> MIMEMultipart:
        """
        Create email message with company name personalization, embedded logo, and optional PDF attachment
        
        Args:
            to_email: Recipient email address
            company_name: Company name for personalization
            subject: Email subject
            body: Email body (use {company} for company name personalization)
            pdf_path: Path to PDF attachment (optional)
            logo_path: Path to logo image for embedding (optional)
            
        Returns:
            MIMEMultipart email message
        """
        # Use 'related' to embed images in the HTML body
        msg = MIMEMultipart('related')
        
        # Email headers
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Personalize body with company name
        personalized_body = body
        if company_name and '{company}' in body:
            personalized_body = body.replace('{company}', company_name)
        
        # Also support {Company} (capitalized) for proper formatting
        if company_name and '{Company}' in personalized_body:
            personalized_body = personalized_body.replace('{Company}', company_name)
        
        # Attach body as HTML. It must be the first part.
        msg.attach(MIMEText(personalized_body, 'html', 'utf-8'))
        
        # Attach logo image if provided and embed it using Content-ID
        if logo_path and os.path.exists(logo_path):
            try:
                with open(logo_path, 'rb') as fp:
                    img = MIMEImage(fp.read())
                # This ID is referenced in the HTML body <img src="cid:logoimage">
                img.add_header('Content-ID', '<logoimage>')
                msg.attach(img)
            except Exception as e:
                print(f"Error attaching logo image {logo_path}: {e}")

        # Attach PDF if provided
        if pdf_path and os.path.exists(pdf_path):
            try:
                with open(pdf_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(pdf_path)}'
                )
                msg.attach(part)
            except Exception as e:
                print(f"Error attaching PDF {pdf_path}: {e}")
        
        return msg
    
    def send_bulk_emails(self, recipients: List[Dict], subject: str, 
                        body: str, pdf_path: str = None, logo_path: str = None, delay: int = 1):
        """
        Send bulk emails to multiple recipients with company personalization
        
        Args:
            recipients: List of dictionaries with 'email' and 'company' keys
            subject: Email subject
            body: Email body (use {company} for company name personalization)
            pdf_path: Path to PDF attachment (optional)
            logo_path: Path to the logo image (optional)
            delay: Delay between emails in seconds (to avoid being flagged as spam)
        """
        successful_sends = 0
        failed_sends = 0
        
        # Try different SMTP configurations
        smtp_configs = [
            ("smtp.zoho.com", 587),
            ("smtp.zoho.in", 587),
            ("smtppro.zoho.com", 587),
            ("smtp.zoho.com", 465),
            ("smtp.zoho.in", 465),
            ("mail.dazzlo.co.in", 587),
            ("smtp.dazzlo.co.in", 587)
        ]
        
        server = None
        connected = False
        
        for smtp_server, smtp_port in smtp_configs:
            try:
                print(f"Trying {smtp_server}:{smtp_port}...")
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.set_debuglevel(0)
                
                if smtp_port == 465:
                    # For SSL connections
                    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                else:
                    # For TLS connections
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                
                print(f"Attempting login with: {self.email}")
                server.login(self.email, self.password)
                print(f"✓ Successfully connected to {smtp_server}:{smtp_port}")
                connected = True
                break
                
            except Exception as e:
                print(f"✗ Failed with {smtp_server}:{smtp_port} - {e}")
                if server:
                    try:
                        server.quit()
                    except:
                        pass
                continue
        
        if not connected:
            print("\n❌ Could not connect with any SMTP configuration!")
            print("Please check:")
            print(f"1. Your email: {self.email}")
            print("2. Your password is correct (App-Specific Password)")
            print("3. 2FA is enabled and you're using App Password")
            print("4. Account is not locked/suspended")
            return
        
        try:
            for i, recipient in enumerate(recipients, 1):
                try:
                    email_addr = recipient['email']
                    company_name = recipient.get('company', '')
                    
                    print(f"Sending email {i}/{len(recipients)} to {email_addr} ({company_name})...")
                    
                    # Create message with company personalization
                    message = self.create_message(
                        email_addr, company_name, subject, body, pdf_path, logo_path
                    )
                    
                    # Send email
                    text = message.as_string()
                    server.sendmail(self.email, email_addr, text)
                    
                    successful_sends += 1
                    print(f"✓ Email sent successfully to {email_addr} ({company_name})")
                    
                    # Add delay to avoid spam detection
                    if delay > 0 and i < len(recipients):
                        time.sleep(delay)
                        
                except Exception as e:
                    failed_sends += 1
                    print(f"✗ Failed to send email to {recipient['email']}: {e}")
            
            if server:
                server.quit()
            
        except Exception as e:
            print(f"Error during email sending: {e}")
            return
        
        # Summary
        print(f"\n--- Email Campaign Summary ---")
        print(f"Total emails: {len(recipients)}")
        print(f"Successful: {successful_sends}")
        print(f"Failed: {failed_sends}")

def create_sample_csv(csv_file: str):
    """Create a sample CSV file with proper format"""
    sample_data = [
        ["email", "company"],
        ["recipient1@example.com", "Tech Corp"],
        ["recipient2@example.com", "Business Solutions"],
        ["recipient3@example.com", "Innovation Ltd"]
    ]
    
    try:
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(sample_data)
        
        print(f"✓ Created sample CSV file: {csv_file}")
        print("Please update it with your recipient list before running the script.")
        print("Format: email,company")
        print("Example: john@company.com,ABC Corporation")
        return True
    except Exception as e:
        print(f"Error creating sample CSV: {e}")
        return False

def main():
    """
    Complete working email sender with embedded logo
    """
    # Configuration - Your Zoho Mail Details
    ZOHO_EMAIL = "siddhant@dazzlo.co.in"
    ZOHO_PASSWORD = "LGNaX0gk213b"  # App-Specific Password
    
    print("=== ZOHO MAIL BULK SENDER ===")
    print(f"Email: {ZOHO_EMAIL}")
    print("Using App-Specific Password for authentication")
    print()
    
    # Professional Email Template - LOGO FIXED VERSION
    SUBJECT = "Strategic Partnership Opportunity - DazzloHR Solutions"
    BODY = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DazzloHR Solutions - Partnership Opportunity</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Times New Roman', 'Georgia', serif; line-height: 1.6; color: #2c2c2c; background-color: #f8f8f8; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
        <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
            <div style="background-color: #ffffff; padding: 25px 30px 20px 30px; border-bottom: 3px solid #d4af37; position: relative;">
                <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                    <tr>
                        <td style="width: 90px; vertical-align: middle; padding: 0;">
                            <img src="cid:logoimage" width="80" alt="DazzloHR Logo" style="border-radius: 8px; border: 1px solid #eee;">
                        </td>
                        <td style="vertical-align: bottom; padding: 0 0 0 20px;">
                            <div style="font-size: 24px; font-weight: bold; color: #2c2c2c; margin-bottom: 5px; letter-spacing: 0.5px;">DazzloHR Solutions</div>
                            <div style="font-size: 12px; font-style: italic; color: #666666; font-weight: normal;">Your Growth • Our People • Your Success</div>
                        </td>
                        <td style="vertical-align: bottom; text-align: right; padding: 0; font-size: 11px; font-weight: bold; line-height: 1.4; color: #444444;">
                            Tel: +91 9373015503<br>
                            Email: operations@dazzlohr.in<br>
                            Location: Kalyan, Maharashtra 421301<br>
                            Web: www.dazzlohr.in
                        </td>
                    </tr>
                </table>
            </div>
            
            <div style="padding: 40px 30px; background-color: #ffffff;">
                <div style="text-align: right; font-size: 13px; color: #666666; margin-bottom: 30px; font-style: italic;">Date: [23rd July 2025]</div>
                
                <div style="font-size: 16px; color: #2c2c2c; margin-bottom: 25px; font-weight: 500;">Dear {company} Leadership Team,</div>
                
                <div style="font-size: 14px; color: #444444; line-height: 1.7; margin-bottom: 20px; text-align: justify;">
                    I hope this letter finds you in excellent health and prosperity. I am writing to introduce <span style="font-weight: 600; color: #d4af37;">DazzloHR Solutions</span>, a premier recruitment consultancy dedicated to connecting exceptional talent with forward-thinking organizations like <span style="font-weight: 600; color: #d4af37;">{company}</span>.
                </div>
                
                <div style="font-size: 14px; color: #444444; line-height: 1.7; margin-bottom: 20px; text-align: justify;">
                    In today's competitive business landscape, acquiring the right talent at the right time is crucial for sustainable growth. At DazzloHR Solutions, we understand that your success depends not just on finding qualified candidates, but on identifying individuals who align with your company culture and long-term vision.
                </div>
                
                <div style="margin: 30px 0; background-color: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px; padding: 25px;">
                    <div style="font-size: 18px; font-weight: bold; color: #2c2c2c; text-align: center; margin-bottom: 20px; position: relative;">
                        Our Comprehensive Recruitment Services
                        <div style="position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%); width: 60px; height: 3px; background: #d4af37; border-radius: 2px;"></div>
                    </div>
                    
                    <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Executive Search & Leadership Hiring</div>
                            </td>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Mid-Level Professional Recruitment</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Bulk Hiring Solutions (Pan-India)</div>
                            </td>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Technical & IT Specialization</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Contractual & Temporary Staffing</div>
                            </td>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Campus & Fresh Talent Acquisition</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Remote & Hybrid Work Solutions</div>
                            </td>
                            <td style="padding: 8px;">
                                <div style="background: #2c2c2c; color: #ffffff; padding: 15px 18px; text-align: center; font-size: 13px; font-weight: 500; border-radius: 6px; border-left: 4px solid #d4af37;">Specialized Industry Consultants</div>
                            </td>
                        </tr>
                    </table>
                </div>
                
                <div style="font-size: 14px; color: #444444; line-height: 1.7; margin-bottom: 20px; text-align: justify;">
                    Our methodology combines traditional recruitment wisdom with modern technology-driven approaches. We maintain a robust database of pre-screened professionals and utilize advanced assessment techniques to ensure cultural fit alongside technical competency.
                </div>
                
                <div style="background: #2c2c2c; color: #ffffff; padding: 30px; margin: 30px 0; border-radius: 10px; text-align: center; position: relative; overflow: hidden; border-top: 4px solid #d4af37;">
                    <div style="font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #d4af37;">Partnership Opportunity</div>
                    <div style="font-size: 14px; line-height: 1.6; color: #e0e0e0;">
                        We would welcome the opportunity to discuss how DazzloHR Solutions can support <span style="font-weight: 600; color: #d4af37;">{company}</span>'s talent acquisition strategy. Whether you have immediate hiring needs or are planning for future growth, we are committed to delivering exceptional results that align with your organizational objectives.
                    </div>
                </div>
                
                <div style="font-size: 14px; color: #444444; line-height: 1.7; margin: 25px 0; text-align: justify;">
                    I would be honored to schedule a brief consultation at your convenience to explore how our services can add value to your recruitment process. Please feel free to reach out to discuss your specific requirements.
                </div>
                
                <div style="font-size: 14px; color: #444444; line-height: 1.7; margin: 25px 0; text-align: justify;">
                    Thank you for considering DazzloHR Solutions as your strategic recruitment partner. We look forward to contributing to <span style="font-weight: 600; color: #d4af37;">{company}</span>'s continued success.
                </div>
            </div>
            
            <div style="background: #f8f8f8; padding: 30px; border-top: 2px solid #d4af37; border-radius: 0 0 8px 8px;">
                <div style="font-size: 16px; font-weight: bold; color: #2c2c2c; margin-bottom: 5px;">Siddhant Suryavanshi</div>
                <div style="font-size: 13px; color: #666666; margin-bottom: 5px; font-style: italic;">Founder & Managing Director</div>
                <div style="font-size: 15px; font-weight: bold; color: #d4af37; margin-bottom: 15px;">DazzloHR Solutions</div>
                
                <div style="font-size: 12px; color: #666666; line-height: 1.5;">
                    Mobile: +91-9373015503<br>
                    Email: siddhant@dazzlo.co.in<br>
                    Operations: operations@dazzlohr.in<br>
                    Website: www.dazzlohr.in
                </div>
            </div>
            
            <div style="background: #2c2c2c; color: #cccccc; text-align: center; padding: 20px; font-size: 11px; border-radius: 0 0 8px 8px;">
                <table style="width: 100%; border-spacing: 0; border-collapse: collapse;">
                    <tr>
                        <td style="text-align: left; padding: 0;">
                            © 2025 DazzloHR Solutions. All rights reserved.
                        </td>
                        <td style="text-align: right; padding: 0;">
                            Confidential Communication | Professional Excellence
                        </td>
                    </tr>
                </table>
            </div>
        </div>
    </body>
    </html>
    """
    
    # File paths
    CSV_FILE = "email_list.csv"  # CSV with email addresses
    PDF_FILE = "DazzloHR_Company_Profile.pdf"    # PDF attachment
    LOGO_FILE = "logo1.png"      # Logo image file

    # Check if CSV file exists, if not create a sample
    if not os.path.exists(CSV_FILE):
        if create_sample_csv(CSV_FILE):
            return  # Exit to let user update the CSV
        else:
            print("Failed to create sample CSV file.")
            return
    
    # Initialize mailer
    mailer = ZohoBulkMailer(ZOHO_EMAIL, ZOHO_PASSWORD)
    
    # Read recipients from CSV
    print("Reading CSV file...")
    recipients = mailer.read_emails_from_csv(CSV_FILE)
    
    if not recipients:
        print("\n❌ No valid recipients found in CSV file!")
        print("Please check that your CSV file contains:")
        print("1. A column named 'email' with valid email addresses")
        print("2. Optionally, a column named 'company' for personalization")
        print("\nExample CSV format:")
        print("email,company")
        print("john@example.com,ABC Corp")
        print("jane@company.com,XYZ Ltd")
        return
    
    print(f"\n✓ Found {len(recipients)} valid recipients")
    
    # Show first few recipients for verification
    print("\nFirst few recipients:")
    for i, recipient in enumerate(recipients[:3]):
        print(f"  {i+1}. {recipient['email']} - {recipient['company']}")
    if len(recipients) > 3:
        print(f"  ... and {len(recipients) - 3} more")
    
    # Check if Logo file exists
    if os.path.exists(LOGO_FILE):
        print(f"\n✓ Logo image found: {LOGO_FILE}")
    else:
        print(f"\n⚠️  Logo image not found: {LOGO_FILE}. Emails will be sent without the logo.")

    # Check if PDF file exists
    if os.path.exists(PDF_FILE):
        print(f"✓ PDF attachment found: {PDF_FILE}")
    else:
        print(f"⚠️  PDF attachment not found: {PDF_FILE}. Emails will be sent without an attachment.")
    
    # Confirm before sending
    print(f"\n📧 Email Subject: {SUBJECT}")
    confirm = input(f"\nSend emails to {len(recipients)} recipients? (y/n): ")
    if confirm.lower() != 'y':
        print("Email sending cancelled.")
        return
    
    # Send bulk emails
    print("\nStarting email campaign...")
    mailer.send_bulk_emails(
        recipients=recipients,
        subject=SUBJECT,
        body=BODY,
        pdf_path=PDF_FILE if os.path.exists(PDF_FILE) else None,
        logo_path=LOGO_FILE if os.path.exists(LOGO_FILE) else None,
        delay=2  # 2 seconds delay between emails
    )

if __name__ == "__main__":
    main()