import json
import os
from tools.groq_helper import call_groq_completion

def tailor_resume(context):
    """Tailor the candidate's resume to match target job requirements with rich formatting."""
    raw_resume = context.get('raw_resume', '')
    resume_json = json.dumps(context.get('resume', {}), indent=2)
    resume_text = raw_resume if raw_resume and len(raw_resume) > 50 else resume_json
    
    kw_raw = context.get('job_description', {}).get('keywords', [])
    keywords = ', '.join(kw_raw) if isinstance(kw_raw, list) else str(kw_raw or '')

    req_raw = context.get('job_description', {}).get('required_skills', [])
    required_skills = ', '.join(req_raw) if isinstance(req_raw, list) else str(req_raw or '')

    resp_raw = context.get('job_description', {}).get('responsibilities', [])
    responsibilities = '; '.join(resp_raw) if isinstance(resp_raw, list) else str(resp_raw or '')

    job_title = context.get('job_description', {}).get('job_title', 'Role')
    company_name = context.get('job_description', {}).get('company_name', 'Company')

    prompt = (
        f"You are an expert career coach and professional resume writer.\n"
        f"Target Role: {job_title} at {company_name}\n"
        f"Job Keywords: {keywords}\n"
        f"Required Skills: {required_skills}\n"
        f"Responsibilities: {responsibilities}\n\n"
        f"Candidate Resume Content:\n{resume_text}\n\n"
        f"INSTRUCTIONS:\n"
        f"1. Generate a complete, beautifully formatted Tailored Resume in Markdown.\n"
        f"2. Include sections: Professional Summary (3-4 impactful sentences), Enhanced Experience (rewrite bullets with action verbs & metric impact), Key Technical Skills (grouped by category), Projects, Education, and Certifications/Awards.\n"
        f"3. Elevate bullet points to align directly with key requirements of the target role while preserving candidate factual details.\n"
        f"4. Do NOT output fallback text or placeholders."
    )

    return call_groq_completion(
        messages=[
            {"role": "system", "content": "You are a top-tier executive resume writer. Output complete, polished markdown resumes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )