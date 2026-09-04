import json
import os
import re
from tools.groq_helper import call_groq_completion

def write_cover_letter(context):
    """Write a highly personalized, compelling narrative cover letter."""
    raw_resume = context.get('raw_resume', '')
    resume_json = json.dumps(context.get('resume', {}), indent=2)
    resume_text = raw_resume if raw_resume and len(raw_resume) > 50 else resume_json

    raw_jd = context.get('raw_jd', '')
    
    resp_raw = context.get('job_description', {}).get('responsibilities', [])
    responsibilities = '; '.join(resp_raw) if isinstance(resp_raw, list) else str(resp_raw or '')

    candidate_name = context.get('resume', {}).get('name') or 'Candidate'
    if candidate_name in ['Candidate', 'string', 'First Last']:
        # Extract candidate name if available in resume text
        name_match = re.search(r'^([A-Z][a-z]+\s+[A-Z][a-z]+)', resume_text)
        if name_match:
            candidate_name = name_match.group(1)

    job_title = context.get('job_description', {}).get('job_title', 'Role')
    company_name = context.get('job_description', {}).get('company_name', 'Company')
    company_brief = context.get('company_brief', '')

    prompt = (
        f"You are a professional executive career strategist.\n"
        f"Write a personalized, highly persuasive narrative Cover Letter in Markdown for candidate {candidate_name} applying for the {job_title} role at {company_name}.\n\n"
        f"Target Company Intelligence:\n{company_brief}\n\n"
        f"Job Responsibilities & Requirements:\n{responsibilities}\n\n"
        f"Candidate Resume Details:\n{resume_text}\n\n"
        f"INSTRUCTIONS:\n"
        f"1. Structure as a formal cover letter with Date, Recruiter/Hiring Manager Salutation, 3-4 persuasive body paragraphs, and Professional Sign-off.\n"
        f"2. Paragraph 1: High-energy hook expressing genuine enthusiasm for {company_name}'s mission.\n"
        f"3. Paragraph 2-3: Highlight candidate's top technical accomplishments, frameworks, and relevant project experience directly matching the role's expectations.\n"
        f"4. Paragraph 4: Enthusiastic closing statement with call to action for an interview.\n"
        f"5. Output clean, ready-to-send Markdown without placeholders or fallback notes."
    )

    return call_groq_completion(
        messages=[
            {"role": "system", "content": "You are a professional cover letter specialist writing compelling application letters."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )