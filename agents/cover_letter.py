import os
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

def write_cover_letter(context):
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'cover_letter_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        candidate_name=context.get('resume', {}).get('name', 'Candidate'),
        job_title=context.get('job_description', {}).get('job_title', 'Role'),
        company_name=context.get('job_description', {}).get('company_name', 'Company'),
        company_brief=context.get('company_brief', ''),
        tailored_resume=context.get('tailored_resume', ''),
        responsibilities='; '.join(context.get('job_description', {}).get('responsibilities', []))
    )

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content