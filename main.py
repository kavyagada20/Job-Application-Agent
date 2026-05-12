import sys
import os
sys.path.append(os.path.dirname(__file__))

from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.packager import package_outputs

def main(resume_path, jd_input):
    """Main orchestrator."""
    # Phase 1: Parse
    context = parse_resume_and_jd(resume_path, jd_input)
    print("Phase 1: Parsing complete")

    # Phase 2: Research
    context['company_brief'] = research_company(context['job_description']['company_name'], context['job_description']['job_title'])
    print("Phase 2: Research complete")

    # Phase 3: Tailor Resume
    context['tailored_resume'] = tailor_resume(context)
    print("Phase 3: Resume tailoring complete")

    # Phase 4: Cover Letter
    context['cover_letter'] = write_cover_letter(context)
    print("Phase 4: Cover letter complete")

    # Phase 5: Package
    package_outputs(context)
    print("Phase 5: Packaging complete")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <resume_path> <jd_input>")
        sys.exit(1)
    resume_path = sys.argv[1]
    jd_input = sys.argv[2]
    main(resume_path, jd_input)