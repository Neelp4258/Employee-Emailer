# config.py
# Central configuration file for the Dazzlo Bulk Emailer application.

import os

# --- Flask App Configuration ---
SECRET_KEY = os.urandom(24)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'png', 'jpg', 'jpeg', 'pdf', 'doc', 'docx'}

# --- Company Configuration ---
# All company details are managed here for easy updates.
COMPANY_NAME = "Dazzlo Enterprises Pvt Ltd"
COMPANY_TAGLINE = "Redefining lifestyle with Innovations and Dreams"
COMPANY_EMAIL = "info@dazzlo.co.in"
COMPANY_PHONE = "+91 9373015503"
COMPANY_LOCATION = "Kalyan, Maharashtra 421301"
COMPANY_WEBSITE = "www.dazzlo.co.in"

# --- Email Configuration ---
# The Content-ID for the embedded logo in emails.
LOGO_CID = "company_logo"