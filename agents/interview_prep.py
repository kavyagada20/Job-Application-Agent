import os
import re
from tools.groq_helper import call_groq_completion

def generate_interview_prep(context):
    """Generate STAR behavioral questions, technical Q&A, and culture prep."""
    raw_resume = context.get('raw_resume', '')
    resume_json = str(context.get('resume', ''))
    resume_text = raw_resume if raw_resume and len(raw_resume) > 50 else resume_json

    raw_jd = context.get('raw_jd', '')
    jd_text = raw_jd if raw_jd and len(raw_jd) > 50 else str(context.get('job_description', ''))
    company_brief = str(context.get('company_brief', ''))

    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'interview_prep_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        resume=resume_text,
        job_description=jd_text,
        company_brief=company_brief
    ) + "\nCRITICAL: Ensure all question titles and talking points use clean Markdown lists without unclosed asterisks."

    output = call_groq_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2500
    )

    # Clean any orphan asterisks in table rows or headers
    if output:
        output = re.sub(r'\|\s*\*([^\*]+)\s*\|', r'| \1 |', output)
        output = re.sub(r'^\s*\*([A-Za-z0-9])', r'• \1', output, flags=re.MULTILINE)

    return output
