import json
import os
import re
from tools.groq_helper import call_groq_completion
from tools.pdf_reader import extract_text_from_file
from tools.url_scraper import is_valid_url, scrape_job_url

def parse_resume_and_jd(resume_path, jd_input):
    """Parse resume and job description (text or URL) into structured JSON."""
    resume_text = extract_text_from_file(resume_path)
    resume_text = re.sub(r'\s+', ' ', resume_text).strip()

    if is_valid_url(jd_input):
        print(f"Scraping Job URL: {jd_input}")
        jd_text = scrape_job_url(jd_input)
    else:
        jd_text = jd_input
    
    jd_text = re.sub(r'\s+', ' ', jd_text).strip()

    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'parse_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(resume_text=resume_text, jd_text=jd_text)

    raw_response = call_groq_completion(
        messages=[
            {"role": "system", "content": "You are a precise data extraction expert. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(raw_response)

    current_company = result.get('job_description', {}).get('company_name', '').lower()
    if not current_company or any(x in current_company for x in ['unknown', 'string', 'company name']):
        focused_text = jd_text[:1000]
        verify_prompt = f"Identify the hiring company name from this text. Return ONLY the name: {focused_text}"
        
        found_name = call_groq_completion(
            messages=[{"role": "user", "content": verify_prompt}]
        ).strip()
        result['job_description']['company_name'] = found_name

    return result