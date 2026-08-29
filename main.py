import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.fit_analyzer import analyze_job_fit
from agents.interview_prep import generate_interview_prep
from agents.cold_email import generate_cold_email
from agents.packager import package_outputs

def main(resume_path, jd_input):
    """Main orchestrator."""
    # Phase 1: Parse
    context = parse_resume_and_jd(resume_path, jd_input)
    print("Phase 1: Parsing complete")

    # Phase 2: Research
    context['company_brief'] = research_company(context['job_description'].get('company_name', 'Company'), context['job_description'].get('job_title', 'Role'))
    print("Phase 2: Research complete")

    # Phase 3: Fit Analysis & Match Score
    fit_result = analyze_job_fit(context)
    context['fit_analysis'] = fit_result
    print(f"Phase 3: Candidate-Job Fit Analysis complete (Score: {fit_result['score']}%)")

    # Phase 4: Tailor Resume
    context['tailored_resume'] = tailor_resume(context)
    print("Phase 4: Resume tailoring complete")

    # Phase 5: Cover Letter
    context['cover_letter'] = write_cover_letter(context)
    print("Phase 5: Cover letter complete")

    # Phase 6: Interview Prep
    context['interview_prep'] = generate_interview_prep(context)
    print("Phase 6: Interview prep complete")

    # Phase 7: Recruiter Cold Email
    context['cold_email'] = generate_cold_email(context)
    print("Phase 7: Cold email generation complete")

    # Phase 8: Package DOCX & ZIP Bundle
    package_outputs(context)
    print("Phase 8: Packaging complete")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <resume_path> <jd_input_or_url>")
        sys.exit(1)
    resume_path = sys.argv[1]
    jd_input = sys.argv[2]
    main(resume_path, jd_input)