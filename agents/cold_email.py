import os
from tools.groq_helper import call_groq_completion

def generate_cold_email(context):
    """Generate professional cold email / LinkedIn outreach messages."""
    raw_resume = context.get('raw_resume', '')
    resume_json = str(context.get('resume', ''))
    resume_text = raw_resume if raw_resume and len(raw_resume) > 50 else resume_json

    raw_jd = context.get('raw_jd', '')
    jd_text = raw_jd if raw_jd and len(raw_jd) > 50 else str(context.get('job_description', ''))
    company_brief = str(context.get('company_brief', ''))

    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'cold_email_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        resume=resume_text,
        job_description=jd_text,
        company_brief=company_brief
    )

    return call_groq_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
