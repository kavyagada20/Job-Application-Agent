import os
import zipfile
from tools.docx_writer import (
    create_resume_docx, 
    create_cover_letter_docx, 
    create_company_brief_docx,
    create_interview_prep_docx,
    create_fit_analysis_docx,
    create_cold_email_docx
)

def package_outputs(context):
    """Package the outputs into .docx files and a single .zip archive."""
    company_name = context['job_description'].get('company_name', 'Company').replace(' ', '_')
    
    outputs_dir = 'outputs'
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    created_files = []

    # 1. Tailored resume
    resume_filename = f"{outputs_dir}/tailored_resume_{company_name}.docx"
    create_resume_docx(context['tailored_resume'], resume_filename)
    created_files.append(resume_filename)

    # 2. Cover letter
    cover_filename = f"{outputs_dir}/cover_letter_{company_name}.docx"
    create_cover_letter_docx(context['cover_letter'], cover_filename, context.get('resume', {}).get('name', 'Candidate'), company_name)
    created_files.append(cover_filename)

    # 3. Company brief
    brief_filename = f"{outputs_dir}/company_brief_{company_name}.docx"
    create_company_brief_docx(context['company_brief'], brief_filename)
    created_files.append(brief_filename)

    # 4. Interview prep
    if 'interview_prep' in context and context['interview_prep']:
        prep_filename = f"{outputs_dir}/interview_prep_{company_name}.docx"
        create_interview_prep_docx(context['interview_prep'], prep_filename)
        created_files.append(prep_filename)

    # 5. Fit analysis
    if 'fit_analysis' in context and context['fit_analysis']:
        fit_report = context['fit_analysis'].get('report', '') if isinstance(context['fit_analysis'], dict) else str(context['fit_analysis'])
        fit_filename = f"{outputs_dir}/fit_analysis_{company_name}.docx"
        create_fit_analysis_docx(fit_report, fit_filename)
        created_files.append(fit_filename)

    # 6. Cold email
    if 'cold_email' in context and context['cold_email']:
        cold_filename = f"{outputs_dir}/cold_email_{company_name}.docx"
        create_cold_email_docx(context['cold_email'], cold_filename)
        created_files.append(cold_filename)

    # 7. Create combined ZIP package
    zip_filename = f"{outputs_dir}/Job_Application_Package_{company_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filepath in created_files:
            zipf.write(filepath, arcname=os.path.basename(filepath))

    print(f"Generated {len(created_files)} DOCX files and ZIP package: {zip_filename}")