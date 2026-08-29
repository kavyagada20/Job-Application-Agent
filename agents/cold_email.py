import os
from tools.groq_helper import call_groq_completion

def generate_cold_email(context):
    """Generate professional cold email / LinkedIn outreach messages."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'cold_email_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    resume_text = str(context.get('resume', ''))
    jd_text = str(context.get('job_description', ''))
    company_brief = str(context.get('company_brief', ''))

    prompt = prompt_template.format(
        resume=resume_text,
        job_description=jd_text,
        company_brief=company_brief
    )

    return call_groq_completion(
        messages=[{"role": "user", "content": prompt}]
    )
