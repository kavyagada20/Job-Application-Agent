import os
import re
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

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

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    
    analysis_text = completion.choices[0].message.content

    # Extract score percentage if present
    match = re.search(r'Match Score:\s*(\d+)%', analysis_text, re.IGNORECASE)
    score = int(match.group(1)) if match else 85

    return {
        'score': score,
        'report': analysis_text
    }
