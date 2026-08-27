import os
from tools.docx_writer import (
    create_resume_docx, 
    create_cover_letter_docx, 
    create_company_brief_docx,
    create_interview_prep_docx
)

def package_outputs(context):
    """Package the outputs into .docx files."""
    company_name = context['job_description']['company_name'].replace(' ', '_')
    candidate_name = context['resume']['name'].replace(' ', '_')

    outputs_dir = 'outputs'
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    # Tailored resume
    resume_filename = f"{outputs_dir}/tailored_resume_{company_name}.docx"
    create_resume_docx(context['tailored_resume'], resume_filename)

    # Cover letter
    cover_filename = f"{outputs_dir}/cover_letter_{company_name}.docx"
    create_cover_letter_docx(context['cover_letter'], cover_filename, context['resume']['name'], company_name)

    # Company brief
    brief_filename = f"{outputs_dir}/company_brief_{company_name}.docx"
    create_company_brief_docx(context['company_brief'], brief_filename)

    # Interview prep
    prep_filename = f"{outputs_dir}/interview_prep_{company_name}.docx"
    if 'interview_prep' in context and context['interview_prep']:
        create_interview_prep_docx(context['interview_prep'], prep_filename)

    # Log summary
    print(f"Generated files:")
    print(f"- {resume_filename}")
    print(f"- {cover_filename}")
    print(f"- {brief_filename}")
    print(f"- {prep_filename}")

    # Calculate keyword match score
    jd_keywords = set(context['job_description'].get('keywords', []))
    resume_text = context['tailored_resume'].lower()
    matched = sum(1 for kw in jd_keywords if kw.lower() in resume_text)
    score = (matched / len(jd_keywords)) * 100 if jd_keywords else 0
    print(f"Keyword match score: {score:.1f}%")