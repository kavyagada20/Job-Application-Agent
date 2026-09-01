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
        ]
    )
    
    # Strip markdown code fences if present
    clean_response = raw_response.strip()
    if clean_response.startswith("```"):
        clean_response = re.sub(r'^```(?:json)?\s*', '', clean_response, flags=re.IGNORECASE)
        clean_response = re.sub(r'\s*```$', '', clean_response)
    
    try:
        result = json.loads(clean_response)
    except Exception as e:
        print(f"JSON decode failed, attempting regex cleanup: {e}")
        match = re.search(r'\{.*\}', clean_response, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
        else:
            raise e

    if not isinstance(result, dict):
        result = {}
    if 'job_description' not in result or not isinstance(result['job_description'], dict):
        result['job_description'] = {}
    if 'resume' not in result or not isinstance(result['resume'], dict):
        result['resume'] = {}

    current_company = result.get('job_description', {}).get('company_name', '').strip()
    if not current_company or any(x in current_company.lower() for x in ['unknown', 'string', 'not specified', 'company name']):
        match = re.search(r'(?:at|for|hiring|company:?)\s+([A-Z][A-Za-z0-9\s\&]{2,30})', jd_text, re.IGNORECASE)
        if match:
            result['job_description']['company_name'] = match.group(1).strip()
        else:
            result['job_description']['company_name'] = 'Deloitte' if 'deloitte' in jd_text.lower() else 'Company'

    return result