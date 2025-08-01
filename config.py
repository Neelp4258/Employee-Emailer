# config.py
# Central configuration file for the Dazzlo Bulk Emailer application.

import os

# --- Flask App Configuration ---
SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

# --- Company Configuration ---
# All company details are managed here for easy updates.

# Dazzlo Enterprises Configuration (for business proposals)
ENTERPRISES_NAME = "Dazzlo Enterprises Pvt Ltd"
ENTERPRISES_TAGLINE = "Redefining lifestyle with Innovations and Dreams"
ENTERPRISES_EMAIL = "info@dazzlo.co.in"
ENTERPRISES_PHONE = "+91 9373015503"
ENTERPRISES_LOCATION = "Kalyan, Maharashtra 421301"
ENTERPRISES_WEBSITE = "www.dazzlo.co.in"
ENTERPRISES_LOGO = "static/images/Primary.png"

# DazzloHR Configuration (for interview notifications and congratulations)
HR_NAME = "DazzloHR"
HR_TAGLINE = "Redefining lifestyle with Innovations and Dreams"
HR_EMAIL = "info@dazzlohr.in"
HR_PHONE = "+91 9373015503"
HR_LOCATION = "Kalyan, Maharashtra 421301"
HR_WEBSITE = "www.dazzlo.co.in"
HR_LOGO = "static/images/HR.png"

# Legacy configuration (keeping for backward compatibility)
COMPANY_NAME = ENTERPRISES_NAME
COMPANY_TAGLINE = ENTERPRISES_TAGLINE
COMPANY_EMAIL = ENTERPRISES_EMAIL
COMPANY_PHONE = ENTERPRISES_PHONE
COMPANY_LOCATION = ENTERPRISES_LOCATION
COMPANY_WEBSITE = ENTERPRISES_WEBSITE

# --- Email Configuration ---
# The Content-ID for the embedded logo in emails.
LOGO_CID = "company_logo"