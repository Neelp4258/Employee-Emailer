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
hr@designstudio.com,DesignStudio`,
        'trivantaedge': `email,company
md@builderco.com,BuilderCo
owner@realestategroup.com,RealEstate Group
director@skylinebuilders.com,Skyline Builders`,
        'trivantaedge_intro': `email,company
md@builderco.com,BuilderCo
owner@realestategroup.com,RealEstate Group
director@skylinebuilders.com,Skyline Builders`,
        'trivantaedge_followup': `email,company
md@builderco.com,BuilderCo
owner@realestategroup.com,RealEstate Group
director@skylinebuilders.com,Skyline Builders`,
        'trivantaedge_thanks': `email,company
md@builderco.com,BuilderCo
owner@realestategroup.com,RealEstate Group
director@skylinebuilders.com,Skyline Builders`,
        'trivantaedge_case_study': `email,company
md@builderco.com,BuilderCo
owner@realestategroup.com,RealEstate Group
director@skylinebuilders.com,Skyline Builders`,
        'hr_intro': `email,company
hr@techcorp.com,TechCorp Inc
hr@innovatelabs.com,InnovateLabs
hr@designstudio.com,DesignStudio`,
        'hr_followup': `email,company
hr@techcorp.com,TechCorp Inc
hr@innovatelabs.com,InnovateLabs
hr@designstudio.com,DesignStudio`,
        'hr_thanks': `email,company
hr@techcorp.com,TechCorp Inc
hr@innovatelabs.com,InnovateLabs
hr@designstudio.com,DesignStudio`,
        'hr_case_study': `email,company
hr@techcorp.com,TechCorp Inc
hr@innovatelabs.com,InnovateLabs
hr@designstudio.com,DesignStudio`,
        'enterprises_intro': `email,company
ceo@techcorp.com,TechCorp Inc
director@innovatelabs.com,InnovateLabs
manager@designstudio.com,DesignStudio`,
        'enterprises_followup': `email,company
ceo@techcorp.com,TechCorp Inc
director@innovatelabs.com,InnovateLabs
manager@designstudio.com,DesignStudio`,
        'enterprises_thanks': `email,company
ceo@techcorp.com,TechCorp Inc
director@innovatelabs.com,InnovateLabs
manager@designstudio.com,DesignStudio`,
        'enterprises_case_study': `email,company
ceo@techcorp.com,TechCorp Inc
director@innovatelabs.com,InnovateLabs
manager@designstudio.com,DesignStudio`,
        'ambivare_template': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'ambivare_blue': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'ambivare_dark': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'ambivare_green': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'Ambivare_AI_Intergration': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'Ambivare_Automation': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'Ambivare_Chatbot': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'Ambivare_app_dev': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`,
        'web_dev': `email,company
cto@techstartup.com,TechStartup
it@digitalagency.com,Digital Agency
ceo@innovativetech.com,Innovative Tech Solutions`
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
        'partnership_hr': 'email, company',
        'trivantaedge': 'email, company',
        'trivantaedge_intro': 'email, company',
        'trivantaedge_followup': 'email, company',
        'trivantaedge_thanks': 'email, company',
        'trivantaedge_case_study': 'email, company',
        'hr_intro': 'email, company',
        'hr_followup': 'email, company',
        'hr_thanks': 'email, company',
        'hr_case_study': 'email, company',
        'enterprises_intro': 'email, company',
        'enterprises_followup': 'email, company',
        'enterprises_thanks': 'email, company',
        'enterprises_case_study': 'email, company',
        'ambivare_template': 'email, company',
        'ambivare_blue': 'email, company',
        'ambivare_dark': 'email, company',
        'ambivare_green': 'email, company',
        'Ambivare_AI_Intergration': 'email, company',
        'Ambivare_Automation': 'email, company',
        'Ambivare_Chatbot': 'email, company',
        'Ambivare_app_dev': 'email, company',
        'web_dev': 'email, company'
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
        if (
            templateType === 'partnership_enterprises' ||
            templateType === 'partnership_hr' ||
            templateType === 'trivantaedge' ||
            templateType === 'trivantaedge_intro' ||
            templateType === 'trivantaedge_followup' ||
            templateType === 'trivantaedge_thanks' ||
            templateType === 'trivantaedge_case_study' ||
            templateType === 'hr_intro' ||
            templateType === 'hr_followup' ||
            templateType === 'hr_thanks' ||
            templateType === 'hr_case_study' ||
            templateType === 'enterprises_intro' ||
            templateType === 'enterprises_followup' ||
            templateType === 'enterprises_thanks' ||
            templateType === 'enterprises_case_study' ||
            templateType === 'ambivare_template' ||
            templateType === 'ambivare_blue' ||
            templateType === 'ambivare_dark' ||
            templateType === 'ambivare_green' ||
            templateType === 'Ambivare_AI_Intergration' ||
            templateType === 'Ambivare_Automation' ||
            templateType === 'Ambivare_Chatbot' ||
            templateType === 'Ambivare_app_dev' ||
            templateType === 'web_dev'
        ) {
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
    
    // Multiple attachment files upload
    const attachmentFiles = document.getElementById('attachment_files');
    const attachmentLabel = document.getElementById('attachment-label');
    const selectedFilesDiv = document.getElementById('selected-files');
    const filesListDiv = document.getElementById('files-list');
    const clearFilesBtn = document.getElementById('clear-files');
    
    if (attachmentFiles) {
        attachmentFiles.addEventListener('change', function() {
            displaySelectedFiles(this.files);
        });
    }
    
    if (clearFilesBtn) {
        clearFilesBtn.addEventListener('click', function() {
            attachmentFiles.value = '';
            selectedFilesDiv.style.display = 'none';
            attachmentLabel.textContent = 'Choose files or drag here';
        });
    }
    
    function displaySelectedFiles(files) {
        if (!files || files.length === 0) {
            selectedFilesDiv.style.display = 'none';
            attachmentLabel.textContent = 'Choose files or drag here';
            return;
        }
        
        // Update main label
        if (files.length === 1) {
            attachmentLabel.textContent = `📎 ${files[0].name}`;
        } else {
            attachmentLabel.textContent = `📎 ${files.length} files selected`;
        }
        
        // Clear and populate files list
        filesListDiv.innerHTML = '';
        let totalSize = 0;
        
        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const fileSize = (file.size / 1024 / 1024).toFixed(2); // Convert to MB
            totalSize += file.size;
            
            // Check file size (max 25MB per file)
            if (file.size > 25 * 1024 * 1024) {
                alert(`File "${file.name}" is too large. Maximum size is 25MB per file.`);
                attachmentFiles.value = '';
                selectedFilesDiv.style.display = 'none';
                attachmentLabel.textContent = 'Choose files or drag here';
                return;
            }
            
            const fileDiv = document.createElement('div');
            fileDiv.className = 'flex items-center justify-between text-xs text-gray-600 bg-gray-50 p-2 rounded';
            fileDiv.innerHTML = `
                <div class="flex items-center">
                    <span class="mr-2">${getFileIcon(file.name)}</span>
                    <span class="font-medium">${file.name}</span>
                    <span class="ml-2 text-gray-500">(${fileSize} MB)</span>
                </div>
            `;
            filesListDiv.appendChild(fileDiv);
        }
        
        // Check total size (max 100MB total)
        const totalSizeMB = (totalSize / 1024 / 1024).toFixed(2);
        if (totalSize > 100 * 1024 * 1024) {
            alert(`Total file size is too large (${totalSizeMB} MB). Maximum total size is 100MB.`);
            attachmentFiles.value = '';
            selectedFilesDiv.style.display = 'none';
            attachmentLabel.textContent = 'Choose files or drag here';
            return;
        }
        
        // Add total size info
        if (files.length > 1) {
            const totalDiv = document.createElement('div');
            totalDiv.className = 'text-xs text-gray-500 pt-2 border-t border-gray-200 mt-2';
            totalDiv.textContent = `Total size: ${totalSizeMB} MB`;
            filesListDiv.appendChild(totalDiv);
        }
        
        selectedFilesDiv.style.display = 'block';
    }
    
    function getFileIcon(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        const icons = {
            'pdf': '📄',
            'doc': '📝',
            'docx': '📝',
            'txt': '📝',
            'jpg': '🖼️',
            'jpeg': '🖼️',
            'png': '🖼️',
            'zip': '🗜️',
            'rar': '🗜️'
        };
        return icons[extension] || '📎';
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
    
    // Initialize brand selection to Enterprises and default template
    try {
        selectBrand('enterprises');
        // Prefer a default template within the selected brand
        const defaultEnterprises = document.getElementById('enterprises_intro');
        if (defaultEnterprises) {
            selectTemplate('enterprises_intro');
        }
    } catch (e) {
        // no-op if not yet defined
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

// Brand selector
function brandOfTemplate(templateType) {
    if (!templateType) return 'general';
    if (templateType === 'partnership_enterprises' || templateType.startsWith('enterprises_')) {
        return 'enterprises';
    }
    if (templateType === 'partnership_hr' || templateType.startsWith('hr_')) {
        return 'hr';
    }
    if (templateType === 'trivantaedge' || templateType.startsWith('trivantaedge_')) {
        return 'trivanta';
    }
    if (templateType.startsWith('ambivare') || templateType.startsWith('Ambivare') || templateType === 'web_dev') {
        return 'ambivare';
    }
    return 'general';
}

function selectBrand(brand) {
    // Toggle active class on brand buttons
    const brandButtons = [
        ['enterprises', document.getElementById('brand-enterprises-btn')],
        ['hr', document.getElementById('brand-hr-btn')],
        ['trivanta', document.getElementById('brand-trivanta-btn')],
        ['ambivare', document.getElementById('brand-ambivare-btn')],
        ['general', document.getElementById('brand-general-btn')]
    ];
    brandButtons.forEach(([key, btn]) => {
        if (!btn) return;
        if (key === brand) btn.classList.add('active');
        else btn.classList.remove('active');
    });

    // Show/hide brand sections
    const brandSections = [
        'brand-enterprises',
        'brand-hr', 
        'brand-trivanta',
        'brand-ambivare',
        'brand-general'
    ];
    
    let firstVisibleTemplate = null;
    brandSections.forEach(sectionId => {
        const section = document.getElementById(sectionId);
        if (!section) return;
        
        const shouldShow = sectionId === `brand-${brand}`;
        section.style.display = shouldShow ? '' : 'none';
        
        if (shouldShow && !firstVisibleTemplate) {
            // Find first template in this section
            const input = section.querySelector('input[name="template_type"]');
            if (input) firstVisibleTemplate = input.value;
        }
    });

    // If currently selected template is hidden, switch to the first visible in this brand
    const currentSelected = document.querySelector('input[name="template_type"]:checked');
    const currentType = currentSelected ? currentSelected.value : '';
    if (!currentType || brandOfTemplate(currentType) !== brand) {
        const fallback = firstVisibleTemplate || (brand === 'enterprises' ? 'enterprises_intro' : brand === 'hr' ? 'hr_intro' : brand === 'trivanta' ? 'trivantaedge' : brand === 'ambivare' ? 'ambivare_template' : 'interview');
        const radio = document.getElementById(fallback);
        if (radio) {
            selectTemplate(fallback);
        }
    }
}