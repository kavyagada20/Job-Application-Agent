import os
from tools.groq_helper import call_groq_completion
from tools.web_search import search_web

def research_company(company_name, job_title):
    """Research company and return a brief efficiently."""
    query = f"{company_name} company mission culture tech stack"
    all_snippets = []

    try:
        results = search_web(query, max_results=3)
        for result in results:
            if isinstance(result, dict) and 'content' in result:
                all_snippets.append(result['content'])
    except Exception as e:
        print(f"Company research search notice: {e}")

    research_snippets = "\n\n".join(all_snippets) if all_snippets else f"{company_name} is a leader in its industry hiring for {job_title}."

    prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'prompts', 'research_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(company_name=company_name, job_title=job_title, research_snippets=research_snippets)

    return call_groq_completion(
        messages=[{"role": "user", "content": prompt}]
    )