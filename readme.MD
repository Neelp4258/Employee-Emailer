# Dazzlo Bulk Emailer - Professional Email Automation

A modern, professional web application for sending bulk emails using Zoho SMTP with beautiful templates and enhanced user experience.

## ✨ Features

- **📧 Dual Email Templates**: Choose between Interview Notifications and Congratulations emails
- **🎨 Professional Design**: Modern blue + cream color theme with glass morphism effects
- **📱 Mobile Responsive**: Optimized for all devices and screen sizes
- **🖼️ Logo Integration**: Upload and embed company logos in emails
- **📊 Detailed Reporting**: Comprehensive email sending reports with success rates
- **🔐 Secure**: Zoho SMTP integration with app-specific password support
- **📁 Drag & Drop**: Easy file upload with drag and drop functionality
- **📥 Export Reports**: Download detailed email campaign reports

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Zoho email account with SMTP access

### Installation

1. **Clone or Download** the project files to your computer
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python app.py
   ```
4. **Access the Web Interface**:
   Open your browser and go to: `http://127.0.0.1:5000`

## 📧 Email Templates

### 1. Interview Notification Template
- **Purpose**: Send interview scheduling emails to shortlisted candidates
- **CSV Columns Required**: `email`, `name`, `role`, `slot`
- **Features**: Professional letterhead, interview instructions, company branding

### 2. Congratulations Template
- **Purpose**: Send selection congratulations with offer details
- **CSV Columns Required**: `email`, `name`, `role`
- **Features**: Celebration design, next steps, offer letter references

## 📋 CSV File Format

### For Interview Notifications:
```csv
email,name,role,slot
john@example.com,John Doe,Software Engineer,2025-01-15 10:00 AM
jane@example.com,Jane Smith,Product Manager,2025-01-16 2:00 PM
```

### For Congratulations:
```csv
email,name,role
john@example.com,John Doe,Software Engineer
jane@example.com,Jane Smith,Product Manager
```

## 🎨 UI/UX Features

- **Modern Design**: Blue + cream color scheme with gradient backgrounds
- **Glass Morphism**: Translucent effects with backdrop blur
- **Interactive Elements**: Hover effects, smooth transitions, and animations
- **Mobile-First**: Responsive design that works on all devices
- **Accessibility**: High contrast, readable fonts, and clear navigation
- **Visual Feedback**: Loading states, success/error indicators

## 🔧 Configuration

### Zoho Email Setup
1. **Enable SMTP** in your Zoho account settings
2. **Generate App Password** if you have 2FA enabled
3. **Use App Password** instead of regular password for security

### Logo Upload
- **Supported Formats**: PNG, JPEG
- **Recommended Size**: 200x200 pixels or larger
- **Placement**: Automatically embedded in email letterhead

## 📊 Reporting Features

- **Real-time Statistics**: Success/failure counts with visual indicators
- **Success Rate Calculation**: Percentage of successfully sent emails
- **Detailed Logs**: Individual email status with error messages
- **Export Functionality**: Download campaign reports as text files
- **Visual Progress Bars**: Campaign performance visualization

## 🛠️ Technical Details

### Backend
- **Framework**: Flask (Python)
- **Email**: Zoho SMTP with SSL/TLS
- **File Handling**: Secure file uploads with validation
- **Error Handling**: Comprehensive error catching and user feedback

### Frontend
- **Styling**: Tailwind CSS with custom gradients
- **Fonts**: Inter font family for modern typography
- **JavaScript**: Vanilla JS for interactions and animations
- **Responsive**: Mobile-first design approach

### Security
- **File Validation**: Secure filename handling
- **Input Sanitization**: Protection against malicious inputs
- **Temporary Files**: Automatic cleanup of uploaded files
- **HTTPS Ready**: Configured for secure deployments

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
The application includes `nixpacks.toml` for easy deployment to cloud platforms:
- **Port**: 8000
- **Server**: Gunicorn
- **Environment**: Production-ready configuration

## 📱 Mobile Experience

- **Touch-Friendly**: Large buttons and touch targets
- **Responsive Layout**: Adapts to different screen sizes
- **Fast Loading**: Optimized for mobile networks
- **Easy Navigation**: Intuitive mobile interface

## 🔄 Template Customization

Both email templates maintain consistent Dazzlo branding:
- **Company Information**: Hardcoded to Dazzlo Enterprises Pvt Ltd
- **Contact Details**: Phone, email, and location
- **Professional Styling**: Consistent with brand guidelines
- **Logo Integration**: Automatic logo embedding when provided

## 📈 Performance

- **Bulk Processing**: Efficient handling of large email lists
- **Memory Management**: Optimized file handling and cleanup
- **Error Recovery**: Graceful handling of SMTP failures
- **User Feedback**: Real-time progress and status updates

## 🤝 Support

For technical support or feature requests, please contact the development team.

---

**© 2025 Dazzlo Enterprises Pvt Ltd. All rights reserved.**