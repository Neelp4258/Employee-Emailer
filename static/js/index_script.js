// CSV Input Toggle functionality
function toggleCsvInput(type) {
    const fileToggle = document.getElementById('csv-file-toggle');
    const notepadToggle = document.getElementById('csv-notepad-toggle');
    const fileSection = document.getElementById('csv-file-section');
    const notepadSection = document.getElementById('csv-notepad-section');
    const csvFile = document.getElementById('csv_file');
    const csvNotepad = document.getElementById('csv_notepad');
    
    if (type === 'file') {
        fileToggle.classList.add('active');
        notepadToggle.classList.remove('active');
        fileSection.style.display = 'block';
        notepadSection.style.display = 'none';
        csvFile.required = true;
        csvNotepad.required = false;
        csvNotepad.name = '';
        csvFile.name = 'csv_file';
    } else {
        notepadToggle.classList.add('active');
        fileToggle.classList.remove('active');
        notepadSection.style.display = 'block';
        fileSection.style.display = 'none';
        csvNotepad.required = true;
        csvFile.required = false;
        csvFile.name = '';
        csvNotepad.name = 'csv_notepad';
    }
    
    // Update requirements text for both sections
    updateCsvRequirements();
}

// Generate sample CSV data
function generateSampleCsv() {
    const templateType = document.querySelector('input[name="template_type"]:checked').value;
    const notepad = document.getElementById('csv_notepad');
    
    const samples = {
        'interview': `email,name,role,slot
john.doe@example.com,John Doe,Software Engineer,October 25, 2025 at 11:00 AM
jane.smith@example.com,Jane Smith,Product Manager,October 26, 2025 at 2:00 PM
mike.wilson@example.com,Mike Wilson,UI/UX Designer,October 27, 2025 at 10:00 AM`,
        'congratulations': `email,name,role,company
john.doe@example.com,John Doe,Software Engineer,TechCorp Inc
jane.smith@example.com,Jane Smith,Product Manager,InnovateLabs
mike.wilson@example.com,Mike Wilson,UI/UX Designer,DesignStudio`,
        'partnership_enterprises': `email,company
ceo@techcorp.com,TechCorp Inc
director@innovatelabs.com,InnovateLabs
manager@designstudio.com,DesignStudio`,
        'partnership_hr': `email,company
hr@techcorp.com,TechCorp Inc
hr@innovatelabs.com,InnovateLabs
hr@designstudio.com,DesignStudio`
    };
    
    notepad.value = samples[templateType] || samples['interview'];
}

// Update CSV requirements text
function updateCsvRequirements() {
    const templateType = document.querySelector('input[name="template_type"]:checked').value;
    const requirements = {
        'interview': 'email, name, role, slot',
        'congratulations': 'email, name, role, company',
        'partnership_enterprises': 'email, company',
        'partnership_hr': 'email, company'
    };
    
    const requirementsText = `Required columns: <b>${requirements[templateType]}</b>`;
    
    // Update both requirement elements
    const csvRequirements = document.getElementById('csv-requirements');
    const notepadRequirements = document.getElementById('notepad-requirements');
    
    if (csvRequirements) {
        csvRequirements.innerHTML = requirementsText;
    }
    if (notepadRequirements) {
        notepadRequirements.innerHTML = requirementsText;
    }
}

// Email validation functionality
async function validateEmailCredentials() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();
    const validateBtn = document.getElementById('validate-btn');
    const validationResult = document.getElementById('validation-result');
    
    if (!email || !password) {
        showValidationResult('Please enter both email and password', 'error');
        return;
    }
    
    // Show loading state
    validateBtn.disabled = true;
    validateBtn.innerHTML = '<span class="loading-spinner"></span> Validating...';
    showValidationResult('Validating credentials...', 'loading');
    
    try {
        const response = await fetch('/validate_credentials', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showValidationResult('✅ Credentials are valid!', 'success');
        } else {
            showValidationResult(`❌ ${data.message}`, 'error');
        }
    } catch (error) {
        showValidationResult('❌ Network error. Please try again.', 'error');
    } finally {
        // Reset button state
        validateBtn.disabled = false;
        validateBtn.textContent = 'Validate';
    }
}

function showValidationResult(message, type) {
    const validationResult = document.getElementById('validation-result');
    validationResult.textContent = message;
    validationResult.className = `mt-2 text-sm ${type}`;
    validationResult.classList.remove('hidden');
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            validationResult.classList.add('hidden');
        }, 5000);
    }
}

// Template selection and preview functionality
function selectTemplate(templateType) {
    // Remove selected class from all cards
    document.querySelectorAll('.template-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Add selected class to clicked card
    const selectedCard = document.querySelector(`[onclick="selectTemplate('${templateType}')"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Update radio button
    const radio = document.getElementById(templateType);
    if (radio) {
        radio.checked = true;
    }
    
    // Update preview iframe
    const previewFrame = document.getElementById('email-preview-frame');
    if (previewFrame) {
        previewFrame.src = `/preview/${templateType}`;
    }
    
    // Update CSV requirements text
    updateCsvRequirements();
    
    // Requirements text is clean and professional - no additional notes needed
    
    // Attachment section is always visible now - no need to show/hide
    
    // Show/hide sender info section
    const senderInfoSection = document.getElementById('sender-info-section');
    if (senderInfoSection) {
        if (templateType === 'partnership_enterprises' || templateType === 'partnership_hr') {
            senderInfoSection.style.display = 'block';
        } else {
            senderInfoSection.style.display = 'none';
        }
    }
}

// File upload handling
document.addEventListener('DOMContentLoaded', function() {
    // CSV file upload
    const csvFile = document.getElementById('csv_file');
    const csvLabel = document.getElementById('csv-label');
    
    if (csvFile) {
        csvFile.addEventListener('change', function() {
            if (this.files.length > 0) {
                csvLabel.textContent = `📊 ${this.files[0].name}`;
            } else {
                csvLabel.textContent = 'Choose CSV file or drag here';
            }
        });
    }
    
    // Logo file upload
    const logoFile = document.getElementById('logo_file');
    const logoLabel = document.getElementById('logo-label');
    
    if (logoFile) {
        logoFile.addEventListener('change', function() {
            if (this.files.length > 0) {
                logoLabel.textContent = `🖼️ ${this.files[0].name}`;
            } else {
                logoLabel.textContent = 'Choose logo file or drag here';
            }
        });
    }
    
    // CV file upload
    const cvFile = document.getElementById('cv_file');
    const cvLabel = document.getElementById('cv-label');
    
    if (cvFile) {
        cvFile.addEventListener('change', function() {
            if (this.files.length > 0) {
                const file = this.files[0];
                const fileSize = (file.size / 1024 / 1024).toFixed(2); // Convert to MB
                cvLabel.textContent = `📄 ${file.name} (${fileSize} MB)`;
                
                // Check file size (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB');
                    this.value = '';
                    cvLabel.textContent = 'Choose file or drag here';
                }
            } else {
                cvLabel.textContent = 'Choose file or drag here';
            }
        });
    }
    
    // Drag and drop functionality
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        area.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });
        
        area.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        });
        
        area.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const input = this.querySelector('input[type="file"]');
                if (input) {
                    input.files = files;
                    input.dispatchEvent(new Event('change'));
                }
            }
        });
    });
    
    // Add event listener for validate button
    const validateBtn = document.getElementById('validate-btn');
    if (validateBtn) {
        validateBtn.addEventListener('click', validateEmailCredentials);
    }
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const csvFile = document.getElementById('csv_file');
            const csvNotepad = document.getElementById('csv_notepad');
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            
            // Check if either CSV file is selected or notepad has content
            const isFileMode = csvFile.name === 'csv_file';
            const isNotepadMode = csvNotepad.name === 'csv_notepad';
            
            if (isFileMode && (!csvFile || !csvFile.files.length)) {
                e.preventDefault();
                alert('Please select a CSV file.');
                return;
            }
            
            if (isNotepadMode && (!csvNotepad || !csvNotepad.value.trim())) {
                e.preventDefault();
                alert('Please enter CSV data in the notepad.');
                return;
            }
            
            // Check if email is provided
            if (!email || !email.value.trim()) {
                e.preventDefault();
                alert('Please enter your Zoho email address.');
                return;
            }
            
            // Check if password is provided
            if (!password || !password.value.trim()) {
                e.preventDefault();
                alert('Please enter your Zoho app password.');
                return;
            }
            
            // Check sender information for partnership templates
            const templateType = document.querySelector('input[name="template_type"]:checked').value;
            if (templateType === 'partnership_enterprises' || templateType === 'partnership_hr') {
                const senderName = document.getElementById('sender_name');
                const senderDesignation = document.getElementById('sender_designation');
                
                if (!senderName || !senderName.value.trim()) {
                    e.preventDefault();
                    alert('Please enter your name for the partnership email.');
                    return;
                }
                
                if (!senderDesignation || !senderDesignation.value.trim()) {
                    e.preventDefault();
                    alert('Please enter your designation for the partnership email.');
                    return;
                }
            }
            
            // Show loading state
            const submitBtn = form.querySelector('.submit-btn');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="mr-3">⏳</span>Sending Emails...';
            }
        });
    }
}); 