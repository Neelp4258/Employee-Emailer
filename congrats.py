import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Company Configuration
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Dazzlo Enterprises Pvt Ltd')
COMPANY_TAGLINE = os.getenv('COMPANY_TAGLINE', 'Redefining lifestyle with Innovations and Dreams')
COMPANY_EMAIL = os.getenv('COMPANY_EMAIL', 'info@dazzlo.co.in')
COMPANY_PHONE = os.getenv('COMPANY_PHONE', '+91 9373015503')
COMPANY_LOCATION = os.getenv('COMPANY_LOCATION', 'Kalyan, Maharashtra 421301')
COMPANY_WEBSITE = os.getenv('COMPANY_WEBSITE', 'www.dazzlo.co.in')

# Zoho SMTP Configuration
SMTP_SERVER = os.getenv('ZOHO_SMTP_SERVER', "smtp.zoho.in")
SMTP_PORT = int(os.getenv('ZOHO_SMTP_PORT', 465))
SMTP_USER = os.getenv('ZOHO_EMAIL', 'operations@dazzlo.co.in')
SMTP_PASSWORD = os.getenv('ZOHO_PASSWORD', 'U4dZLAg5ZmX0')

class DazzloSelectionEmailSender:
    """Send congratulatory selection emails with Dazzlo branding"""

    def __init__(self):
        if not SMTP_USER or not SMTP_PASSWORD:
            logging.error("Zoho email credentials not found in environment variables.")
            raise ValueError("Email credentials are required")

    def create_selection_email_content(self, candidate_name, role):
        """
        Create congratulatory email content for selected candidates
        
        Args:
            candidate_name: Name of the selected candidate
            role: Role they were selected for
            
        Returns:
            Tuple of (subject, html_body, text_body)
        """
        subject = f"🎉 Congratulations! You're Selected at Dazzlo - {role} Position"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Times New Roman', serif; line-height: 1.6; color: #333; margin: 0; padding: 0; background-color: #fafafa; }}
                .container {{ max-width: 650px; margin: 20px auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
                
                /* Celebration Ribbon */
                .celebration-ribbon {{ 
                    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 50%, #d4af37 100%);
                    padding: 18px 0;
                    text-align: center;
                    position: relative;
                    overflow: hidden;
                }}
                .celebration-ribbon::before {{
                    content: "🎉 CONGRATULATIONS! YOU'RE SELECTED! 🎉";
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
                    letter-spacing: 1px;
                }}
                
                /* Letterhead */
                .letterhead {{ padding: 40px 40px 20px 40px; border-bottom: 3px solid #d4af37; position: relative; background: linear-gradient(135deg, #ffffff 0%, #fffef9 100%); }}
                .logo-area {{ display: inline-block; width: 55px; height: 55px; margin-right: 18px; vertical-align: top; margin-top: 5px; }}
                .logo-img {{ width: 55px; height: 55px; object-fit: contain; border-radius: 8px; }}
                .company-info {{ display: inline-block; vertical-align: top; }}
                .company-name {{ font-family: 'Times New Roman', serif; font-size: 20px; font-weight: bold; color: #2c2c2c; margin: 0; }}
                .tagline {{ font-family: 'Times New Roman', serif; font-size: 11px; font-style: italic; color: #666; margin: 8px 0 0 0; }}
                .contact-info {{ position: absolute; top: 50px; right: 40px; text-align: right; font-size: 10px; font-weight: bold; color: #333; }}
                .contact-info div {{ margin: 3px 0; }}
                
                /* Selection Notice */
                .selection-notice {{ 
                    background: linear-gradient(135deg, #fff8e1 0%, #fffef7 100%);
                    margin: 30px 40px;
                    padding: 25px;
                    border-radius: 12px;
                    border-left: 5px solid #d4af37;
                    border-right: 5px solid #d4af37;
                    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.15);
                }}
                .selection-title {{ 
                    font-size: 22px; 
                    font-weight: bold; 
                    color: #b8860b; 
                    margin: 0 0 15px 0; 
                    text-align: center;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
                }}
                .role-highlight {{ 
                    background: linear-gradient(135deg, #d4af37 0%, #f4d03f 100%);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    font-weight: bold;
                    display: inline-block;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                    font-size: 16px;
                }}
                
                /* Content */
                .content {{ padding: 0 40px 40px 40px; }}
                .content p {{ margin: 15px 0; font-size: 14px; line-height: 1.7; color: #333; }}
                .highlight-box {{ 
                    background: linear-gradient(135deg, #fff8e1 0%, #fffcf0 100%);
                    padding: 22px; 
                    border-radius: 10px; 
                    border-left: 4px solid #d4af37; 
                    border-right: 4px solid #d4af37;
                    margin: 20px 0;
                    box-shadow: 0 3px 10px rgba(212, 175, 55, 0.1);
                }}
                .next-steps {{ 
                    background: linear-gradient(135deg, #fafbfc 0%, #ffffff 100%);
                    padding: 22px; 
                    border-radius: 10px; 
                    margin: 25px 0;
                    border: 2px solid #e8e8e8;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                }}
                .next-steps h3 {{ color: #666; margin-top: 0; font-size: 16px; }}
                .next-steps ul {{ margin: 10px 0; padding-left: 20px; }}
                .next-steps li {{ margin: 10px 0; color: #555; }}
                
                .offer-letter-notice {{
                    background: linear-gradient(135deg, #fff3e0 0%, #fffef7 100%);
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #d4af37;
                    margin: 25px 0;
                    text-align: center;
                    box-shadow: 0 3px 12px rgba(212, 175, 55, 0.2);
                }}
                .offer-letter-notice h3 {{ 
                    color: #b8860b; 
                    margin: 0 0 10px 0; 
                    font-size: 16px; 
                }}
                .offer-letter-notice p {{ 
                    margin: 0; 
                    color: #666; 
                    font-weight: 500; 
                }}
                
                /* Footer */
                .footer {{ 
                    background: linear-gradient(135deg, #2c2c2c 0%, #404040 100%);
                    color: #ccc; 
                    padding: 25px 40px; 
                    text-align: center; 
                    font-size: 10px; 
                }}
                .footer-content {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; }}
                .footer-left, .footer-right {{ flex: 1; }}
                .footer-right {{ text-align: right; }}
                
                /* Decorative elements */
                .golden-line {{ height: 3px; background: linear-gradient(to right, #d4af37, #f4d03f, #d4af37); margin: 25px 0 10px 0; border-radius: 2px; }}
                .golden-line-thin {{ height: 1px; background: linear-gradient(to right, #d4af37, #f4d03f, #d4af37); margin: 0 0 20px 0; border-radius: 1px; }}
                
                .signature {{ 
                    margin-top: 30px; 
                    padding: 20px; 
                    background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%); 
                    border-radius: 10px; 
                    border: 1px solid #e8e8e8;
                }}
                .auto-generated {{ font-style: italic; color: #888; font-size: 11px; margin-top: 20px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <!-- Celebration Ribbon -->
                <div class="celebration-ribbon"></div>
                
                <!-- Letterhead -->
                <div class="letterhead">
                    <div class="logo-area">
                        <img src="cid:logo" class="logo-img" alt="Dazzlo Logo">
                    </div>
                    <div class="company-info">
                        <div class="company-name">{COMPANY_NAME}</div>
                        <div class="tagline">{COMPANY_TAGLINE}</div>
                    </div>
                    <div class="contact-info">
                        <div>📞 {COMPANY_PHONE}</div>
                        <div>✉️ {COMPANY_EMAIL}</div>
                        <div>📍 {COMPANY_LOCATION}</div>
                    </div>
                    <div class="golden-line"></div>
                    <div class="golden-line-thin"></div>
                </div>
                
                <!-- Selection Notice -->
                <div class="selection-notice">
                    <div class="selection-title">🎊 YOU'RE SELECTED! 🎊</div>
                    <p style="text-align: center; margin: 0; font-size: 16px; color: #666;">
                        We are thrilled to offer you the position of<br>
                        <span class="role-highlight">{role}</span>
                    </p>
                </div>
                
                <!-- Content -->
                <div class="content">
                    <p><strong>Dear {candidate_name},</strong></p>
                    
                    <p>Congratulations! 🎉 We are delighted to inform you that you have been <strong>selected</strong> for the 
                    <strong>{role}</strong> position at <strong>{COMPANY_NAME}</strong>.</p>
                    
                    <div class="highlight-box">
                        <p><strong>🌟 Why We Selected You:</strong></p>
                        <p>After careful evaluation of your skills, experience, and potential, our team believes you are the perfect fit 
                        for this role. Your qualifications and enthusiasm impressed us greatly during the selection process.</p>
                    </div>
                    
                    <div class="offer-letter-notice">
                        <h3>📄 Offer Letter Attached</h3>
                        <p>Please find your official offer letter attached to this email with detailed terms and conditions.</p>
                    </div>
                    
                    <div class="next-steps">
                        <h3>📋 Next Steps:</h3>
                        <ul>
                            <li><strong>Review Documents:</strong> Please carefully review all attached documents</li>
                            <li><strong>HR Discussion:</strong> Our HR team will contact you within 2-3 business days</li>
                            <li><strong>Acceptance:</strong> Please confirm your acceptance as per the timeline mentioned in offer letter</li>
                            <li><strong>Documentation:</strong> Keep your documents ready for verification process</li>
                        </ul>
                    </div>
                    
                    <p>We are excited to welcome you to the <strong>{COMPANY_NAME}</strong> family and look forward to your valuable 
                    contributions to our team's success.</p>
                    
                    <div class="signature">
                        <p><strong>Warm Regards,</strong><br>
                        <strong>The {COMPANY_NAME} Team</strong><br>
                        <em>Human Resources Department</em></p>
                        
                        <div class="auto-generated">
                            <em>(This is an automated selection notification)</em>
                        </div>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <div class="footer-content">
                        <div class="footer-left">© {datetime.now().year} {COMPANY_NAME}. All rights reserved.</div>
                        <div class="footer-right">🌐 {COMPANY_WEBSITE}</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        🎉 CONGRATULATIONS! YOU'RE SELECTED! 🎉
        
        Dear {candidate_name},

        Congratulations! We are delighted to inform you that you have been SELECTED for the {role} position at {COMPANY_NAME}.

        WHY WE SELECTED YOU:
        After careful evaluation of your skills, experience, and potential, our team believes you are the perfect fit for this role. Your qualifications and enthusiasm impressed us greatly during the selection process.

        DOCUMENTS ATTACHED:
        Please find the following documents attached to this email:
        • Official Offer Letter with terms and conditions
        • Company policies and guidelines  
        • Additional documentation as required

        NEXT STEPS:
        • Review Documents: Please carefully review all attached documents
        • HR Discussion: Our HR team will contact you within 2-3 business days
        • Acceptance: Please confirm your acceptance as per the timeline mentioned in offer letter
        • Documentation: Keep your documents ready for verification process

        We are excited to welcome you to the {COMPANY_NAME} family and look forward to your valuable contributions to our team's success.

        Warm Regards,
        The {COMPANY_NAME} Team
        Human Resources Department

        Contact: {COMPANY_PHONE}
        Email: {COMPANY_EMAIL}
        Website: {COMPANY_WEBSITE}

        (This is an automated selection notification)
        """
        
        return subject, html_body, text_body

    def send_selection_email(self, candidate_name, candidate_email, role, pdf_paths=None):
        """
        Send selection congratulatory email to the candidate with multiple PDF attachments
        
        Args:
            candidate_name: Name of the selected candidate
            candidate_email: Email address of the candidate
            role: Role they were selected for
            pdf_paths: List of paths to PDF files to attach (up to 3)
            
        Returns:
            Boolean indicating success/failure
        """
        if not candidate_email:
            logging.error("No email address provided")
            return False

        try:
            subject, html_body, text_body = self.create_selection_email_content(candidate_name, role)
            
            msg = MIMEMultipart('alternative')
            msg['From'] = SMTP_USER
            msg['To'] = candidate_email
            msg['Subject'] = subject
            
            # Attach text and HTML versions
            msg.attach(MIMEText(text_body, 'plain'))
            msg.attach(MIMEText(html_body, 'html'))

            # Attach logo if available
            logo_path = "logo.png"
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as logo_file:
                    logo_part = MIMEImage(logo_file.read())
                    logo_part.add_header('Content-ID', '<logo>')
                    logo_part.add_header('Content-Disposition', 'inline', filename='logo.png')
                    msg.attach(logo_part)
            else:
                logging.warning(f"Logo file not found at {logo_path}. Email will be sent without logo.")

            # Attach PDFs if provided
            if pdf_paths:
                attachment_names = [
                    f"Offer_Letter_{candidate_name.replace(' ', '_')}.pdf",
                    f"Company_Policies_{candidate_name.replace(' ', '_')}.pdf", 
                    f"Additional_Documents_{candidate_name.replace(' ', '_')}.pdf"
                ]
                
                for i, pdf_path in enumerate(pdf_paths):
                    if pdf_path and os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        
                        # Use predefined names or fallback to original filename
                        if i < len(attachment_names):
                            filename = attachment_names[i]
                        else:
                            filename = os.path.basename(pdf_path)
                        
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename}",
                        )
                        msg.attach(part)
                        logging.info(f"PDF {i+1} attached: {pdf_path}")
                    else:
                        if pdf_path:
                            logging.warning(f"PDF file not found at {pdf_path}")

            # Send email
            if SMTP_PORT == 465:
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
            else:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
            
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Selection email sent successfully to {candidate_email} for {candidate_name} ({role})")
            return True
            
        except Exception as e:
            logging.error(f"Error sending selection email to {candidate_email}: {str(e)}")
            return False

def main():
    """Main function to send selection emails"""
    print("🎉 DAZZLO ENTERPRISES - SELECTION EMAIL SENDER")
    print("=" * 50)
    
    try:
        sender = DazzloSelectionEmailSender()
        
        while True:
            print("\n📧 Send Selection Congratulations Email")
            print("-" * 40)
            
            candidate_name = input("Enter candidate name: ").strip()
            if not candidate_name:
                print("❌ Candidate name is required!")
                continue
                
            role = input("Enter role/position: ").strip()
            if not role:
                print("❌ Role is required!")
                continue
                
            candidate_email = input("Enter candidate email: ").strip()
            if not candidate_email:
                print("❌ Email address is required!")
                continue
            
            # Ask for PDF attachments
            pdf_paths = []
            pdf_descriptions = [
                "Offer Letter PDF",
                "Company Policies PDF", 
                "Additional Documents PDF"
            ]
            
            print("\n📎 PDF Attachments (up to 3 files):")
            for i, description in enumerate(pdf_descriptions, 1):
                pdf_path = input(f"Enter {description} path (optional, press Enter to skip): ").strip()
                if pdf_path:
                    if os.path.exists(pdf_path):
                        pdf_paths.append(pdf_path)
                        print(f"   ✅ {description}: {pdf_path}")
                    else:
                        print(f"   ❌ File not found: {pdf_path}")
                        confirm_proceed = input(f"   Continue without {description}? (y/n): ").strip().lower()
                        if confirm_proceed != 'y':
                            continue
                        pdf_paths.append(None)
                else:
                    pdf_paths.append(None)
            
            # Filter out None values
            valid_pdf_paths = [path for path in pdf_paths if path is not None]
            
            print(f"\n📋 Sending selection email to:")
            print(f"   👤 Name: {candidate_name}")
            print(f"   💼 Role: {role}")
            print(f"   📧 Email: {candidate_email}")
            print(f"   📄 PDF Attachments: {len(valid_pdf_paths)} files")
            for i, path in enumerate(valid_pdf_paths, 1):
                print(f"      {i}. {os.path.basename(path)}")
            
            confirm = input("\nSend email? (y/n): ").strip().lower()
            if confirm == 'y':
                print("\n📤 Sending email...")
                if sender.send_selection_email(candidate_name, candidate_email, role, valid_pdf_paths):
                    print("✅ Selection email sent successfully! 🎉")
                else:
                    print("❌ Failed to send email. Please check the logs.")
            else:
                print("📧 Email cancelled.")
            
            another = input("\nSend another email? (y/n): ").strip().lower()
            if another != 'y':
                break
        
        print("\n👋 Thank you for using Dazzlo Selection Email Sender!")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Exiting...")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main()