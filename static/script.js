// Configure Marked.js options for safe & clean rendering
if (window.marked) {
    marked.setOptions({
        gfm: true,
        breaks: true,
        headerIds: false
    });
}

// Global Tab Switching
function switchTab(tabId, btnElement) {
    // Hide all tab panes
    const panes = document.querySelectorAll('.tab-pane');
    panes.forEach(pane => pane.classList.remove('active'));

    // Deactivate all tab buttons
    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show target tab pane
    const targetPane = document.getElementById(tabId);
    if (targetPane) {
        targetPane.classList.add('active');
    }

    // Activate button
    if (btnElement) {
        btnElement.classList.add('active');
    }
}

// Copy Content to Clipboard
function copyContent(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Use textContent or innerText to copy raw formatted text
    const textToCopy = element.innerText || element.textContent;
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert("Copied to clipboard!");
    }).catch(err => {
        alert("Failed to copy text: " + err);
    });
}

// Form Submission & Workflow Management
document.getElementById('applicationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const mainUI = document.getElementById('main-interface');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const statusText = document.getElementById('status-text');
    const progressFill = document.getElementById('progressFill');

    // UI State Transition
    mainUI.style.display = 'none';
    loading.style.display = 'block';

    const steps = [
        "Parsing your resume document...",
        "Researching company culture & tech stack...",
        "Tailoring experience bullet points...",
        "Drafting customized cover letter...",
        "Generating STAR behavioral & technical interview prep..."
    ];
    let stepIdx = 0;
    progressFill.style.width = '15%';

    const interval = setInterval(() => {
        if (stepIdx < steps.length) {
            statusText.innerText = steps[stepIdx];
            const pct = Math.min(20 + (stepIdx + 1) * 16, 95);
            progressFill.style.width = pct + '%';
            stepIdx++;
        }
    }, 4000);

    async function processApplication() {
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Server Error (${response.status})`);
            }

            return data;

        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error("Network connection interrupted. Please verify the Flask server is running and try again.");
            }
            throw error;
        }
    }

    try {
        const data = await processApplication();
        clearInterval(interval);
        progressFill.style.width = '100%';

        // Render Parsed Markdown into formatted HTML
        const renderMarkdown = (text) => {
            if (!text) return '<p class="text-muted">No content generated.</p>';
            return window.marked ? marked.parse(text) : text.replace(/\n/g, '<br>');
        };

        document.getElementById('companyBrief').innerHTML = renderMarkdown(data.company_brief);
        document.getElementById('tailoredResume').innerHTML = renderMarkdown(data.tailored_resume);
        document.getElementById('coverLetter').innerHTML = renderMarkdown(data.cover_letter);
        document.getElementById('interviewPrep').innerHTML = renderMarkdown(data.interview_prep);

        // Update Title Header & Metadata Badges
        const safeCompanyName = data.company_name ? data.company_name.replace(/\s+/g, '_') : 'Company';
        const displayCompanyName = data.company_name || 'Target Company';
        
        const titleEl = document.getElementById('targetCompanyTitle');
        if (titleEl) {
            titleEl.innerHTML = `<i class="fa-solid fa-building"></i> Application Package for ${displayCompanyName}`;
        }

        const badgesEl = document.getElementById('jobMetadataBadges');
        if (badgesEl) {
            let badgesHtml = '';
            if (data.job_title) badgesHtml += `<span class="meta-tag"><i class="fa-solid fa-briefcase"></i> ${data.job_title}</span>`;
            if (data.location) badgesHtml += `<span class="meta-tag"><i class="fa-solid fa-location-dot"></i> ${data.location}</span>`;
            if (data.experience_requirements) badgesHtml += `<span class="meta-tag"><i class="fa-solid fa-user-graduate"></i> ${data.experience_requirements}</span>`;
            if (data.salary_range && data.salary_range.toLowerCase() !== 'not specified') {
                badgesHtml += `<span class="meta-tag"><i class="fa-solid fa-money-bill-wave"></i> ${data.salary_range}</span>`;
            }
            badgesEl.innerHTML = badgesHtml;
        }

        // Set Download Links
        document.getElementById('dl-resume').href = `/download/tailored_resume_${safeCompanyName}.docx`;
        document.getElementById('dl-cover').href = `/download/cover_letter_${safeCompanyName}.docx`;
        
        const dlPrepEl = document.getElementById('dl-prep');
        if (dlPrepEl) {
            dlPrepEl.href = `/download/interview_prep_${safeCompanyName}.docx`;
        }

        // Display Results
        loading.style.display = 'none';
        results.style.display = 'block';

    } catch (error) {
        clearInterval(interval);
        alert("Application Processing Error: " + error.message);
        mainUI.style.display = 'block';
        loading.style.display = 'none';
    }
});

// File Upload Drag & Drop Feedback
const resumeInput = document.getElementById('resume');
const dropZone = document.getElementById('file-drop-zone');

if (resumeInput && dropZone) {
    resumeInput.addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name;
        if (fileName) {
            dropZone.innerHTML = `
                <div class="upload-icon" style="color: #10b981;"><i class="fa-solid fa-file-circle-check"></i></div>
                <span class="upload-title"><strong>File Selected:</strong> ${fileName}</span>
                <span class="upload-hint">Click or drag another file to change</span>
            `;
            dropZone.style.borderColor = '#10b981';
            dropZone.style.background = 'rgba(16, 185, 129, 0.08)';
        }
    });
}