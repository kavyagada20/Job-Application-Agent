import json
import os
from tools.groq_helper import call_groq_completion

def tailor_resume(context):
    """Tailor the resume with improved summarization accuracy."""
    resume_json = json.dumps(context.get('resume', {}), indent=2)
    
    kw_raw = context.get('job_description', {}).get('keywords', [])
    keywords = ', '.join(kw_raw) if isinstance(kw_raw, list) else str(kw_raw or '')

    req_raw = context.get('job_description', {}).get('required_skills', [])
    required_skills = ', '.join(req_raw) if isinstance(req_raw, list) else str(req_raw or '')

    resp_raw = context.get('job_description', {}).get('responsibilities', [])
    responsibilities = '; '.join(resp_raw) if isinstance(resp_raw, list) else str(resp_raw or '')

    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'tailor_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    instruction_overlay = (
        "\nCRITICAL: The 'Summary' section must be a professional narrative (3-4 sentences) "
        "highlighting specific years of experience and top technical achievements found in the resume."
    )

    prompt = prompt_template.format(
        job_title=context.get('job_description', {}).get('job_title', 'Role'),
        company_name=context.get('job_description', {}).get('company_name', 'Company'),
        resume_text=resume_json,
        keywords=keywords,
        required_skills=required_skills,
        responsibilities=responsibilities
    ) + instruction_overlay

    return call_groq_completion(
        messages=[
            {"role": "system", "content": "You are an expert career coach and professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )