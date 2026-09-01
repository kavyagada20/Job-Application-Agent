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
    const panes = document.querySelectorAll('.tab-pane');
    panes.forEach(pane => pane.classList.remove('active'));

    const buttons = document.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));

    const targetPane = document.getElementById(tabId);
    if (targetPane) {
        targetPane.classList.add('active');
    }

    if (btnElement) {
        btnElement.classList.add('active');
    }
}

// Copy Content to Clipboard
function copyContent(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

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

    mainUI.style.display = 'none';
    loading.style.display = 'block';

    const steps = [
        "Parsing resume document & job requirements...",
        "Analyzing candidate-job compatibility & fit score...",
        "Researching target company intelligence & web data...",
        "Tailoring experience bullets & skills alignment...",
        "Drafting customized narrative cover letter...",
        "Generating STAR behavioral & technical interview prep...",
        "Writing recruiter & hiring manager cold email...",
        "Packaging Word (.docx) files & ZIP archive..."
    ];
    let stepIdx = 0;
    let elapsedSeconds = 0;
    progressFill.style.width = '10%';

    const loadingSubtext = document.querySelector('.loading-subtext');

    const interval = setInterval(() => {
        elapsedSeconds += 2;
        if (stepIdx < steps.length) {
            statusText.innerText = steps[stepIdx];
            const pct = Math.min(10 + (stepIdx + 1) * 11, 95);
            progressFill.style.width = pct + '%';
            stepIdx++;
        } else {
            statusText.innerText = "Finalizing AI suite & building download packages...";
            progressFill.style.width = '98%';
        }

        if (loadingSubtext) {
            loadingSubtext.innerText = `Executing Multi-Agent Workflow (${elapsedSeconds}s elapsed)`;
        }
    }, 2000);

    async function processApplication() {
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            const contentType = response.headers.get("content-type");
            if (!contentType || !contentType.includes("application/json")) {
                throw new Error(`Server returned non-JSON response (${response.status}). The request may have timed out. Please try again.`);
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `Server Error (${response.status})`);
            }

            return data;

        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error("Network connection interrupted. Please verify the server is active and try again.");
            }
            throw error;
        }
    }

    try {
        const data = await processApplication();
        clearInterval(interval);
        progressFill.style.width = '100%';

        const renderMarkdown = (text) => {
            if (!text) return '<p class="text-muted">No content generated.</p>';
            return window.marked ? marked.parse(text) : text.replace(/\n/g, '<br>');
        };

        // Render contents into tabs
        document.getElementById('fitReport').innerHTML = renderMarkdown(data.fit_report);
        document.getElementById('companyBrief').innerHTML = renderMarkdown(data.company_brief);
        document.getElementById('tailoredResume').innerHTML = renderMarkdown(data.tailored_resume);
        document.getElementById('coverLetter').innerHTML = renderMarkdown(data.cover_letter);
        document.getElementById('interviewPrep').innerHTML = renderMarkdown(data.interview_prep);
        document.getElementById('coldEmail').innerHTML = renderMarkdown(data.cold_email);

        // Update Match Score Badge
        const scoreBadge = document.getElementById('fitScoreBadge');
        if (scoreBadge && data.fit_score !== undefined) {
            scoreBadge.innerText = `Match Score: ${data.fit_score}%`;
            if (data.fit_score >= 80) {
                scoreBadge.style.background = 'rgba(16, 185, 129, 0.2)';
                scoreBadge.style.borderColor = '#10b981';
                scoreBadge.style.color = '#34d399';
            } else if (data.fit_score >= 65) {
                scoreBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                scoreBadge.style.borderColor = '#f59e0b';
                scoreBadge.style.color = '#fbbf24';
            } else {
                scoreBadge.style.background = 'rgba(239, 68, 68, 0.2)';
                scoreBadge.style.borderColor = '#ef4444';
                scoreBadge.style.color = '#f87171';
            }
        }

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
        document.getElementById('dl-zip').href = `/download/Job_Application_Package_${safeCompanyName}.zip`;
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