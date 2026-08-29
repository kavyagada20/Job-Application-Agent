import os
import re
from tools.groq_helper import call_groq_completion

def analyze_job_fit(context):
    """Analyze candidate resume against JD and produce Match Score & gap breakdown."""
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'fit_analyzer_prompt.txt')
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

    analysis_text = call_groq_completion(
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract score percentage if present
    match = re.search(r'Match Score:\s*(\d+)%', analysis_text, re.IGNORECASE)
    score = int(match.group(1)) if match else 85

    return {
        'score': score,
        'report': analysis_text
    }
