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
    const requirementsElement = document.getElementById('csv-requirements');
    if (requirementsElement) {
        const requirements = {
            'interview': 'email, name, role, slot',
            'congratulations': 'email, name, role, company',
            'partnership': 'email, company'
        };
        requirementsElement.innerHTML = `Required columns: <b>${requirements[templateType]}</b>`;
        
        // Add note for partnership template
        if (templateType === 'partnership') {
            requirementsElement.innerHTML += '<br><span class="text-orange-600 text-xs">Note: You\'ll also need to provide your name and designation below</span>';
        }
    }
    
    // Show/hide CV upload section
    const cvSection = document.getElementById('cv-upload-section');
    if (cvSection) {
        if (templateType === 'partnership') {
            cvSection.style.display = 'block';
        } else {
            cvSection.style.display = 'none';
        }
    }
    
    // Show/hide sender info section
    const senderInfoSection = document.getElementById('sender-info-section');
    if (senderInfoSection) {
        if (templateType === 'partnership') {
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
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const csvFile = document.getElementById('csv_file');
            const email = document.getElementById('email');
            const password = document.getElementById('password');
            
            // Check if CSV file is selected
            if (!csvFile || !csvFile.files.length) {
                e.preventDefault();
                alert('Please select a CSV file.');
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
            
            // Check sender information for partnership template
            const templateType = document.querySelector('input[name="template_type"]:checked').value;
            if (templateType === 'partnership') {
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