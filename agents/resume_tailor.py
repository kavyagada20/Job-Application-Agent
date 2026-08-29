import json
import os
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

def tailor_resume(context):
    """Tailor the resume with improved summarization accuracy."""
    resume_json = json.dumps(context.get('resume', {}), indent=2)
    keywords = ', '.join(context.get('job_description', {}).get('keywords', []))
    required_skills = ', '.join(context.get('job_description', {}).get('required_skills', []))
    responsibilities = '; '.join(context.get('job_description', {}).get('responsibilities', []))

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

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert career coach and professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return completion.choices[0].message.content