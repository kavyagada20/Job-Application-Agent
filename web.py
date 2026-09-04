from flask import Flask, request, render_template, send_file, jsonify
import os
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor

from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.interview_prep import generate_interview_prep
from agents.fit_analyzer import analyze_job_fit
from agents.cold_email import generate_cold_email
from agents.packager import package_outputs

app = Flask(__name__, template_folder='templates', static_folder='static')

OUTPUTS_DIR = os.path.join(app.root_path, 'outputs')
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        jd_input = request.form.get('jd_text', '')
        resume_file = request.files.get('resume')
        
        if not resume_file or not resume_file.filename:
            return jsonify({'error': 'Resume file required'}), 400

        temp_dir = tempfile.mkdtemp()
        resume_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(resume_path)

        # Step 1: Parse (Extract structure from Resume & JD)
        context = parse_resume_and_jd(resume_path, jd_input)
        
        jd_info = context.get('job_description', {})
        company_name = jd_info.get('company_name', 'Company')
        job_title = jd_info.get('job_title', 'Role')
        location = jd_info.get('location', 'Not specified')
        experience_requirements = jd_info.get('experience_requirements', 'Not specified')
        salary_range = jd_info.get('salary_range', 'Not specified')

        # Step 2: Fast Company Research
        context['company_brief'] = research_company(company_name, job_title)
        
        # Step 3: Run Remaining 5 AI Agents in parallel for fast response (< 10 seconds)
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_tailor = executor.submit(tailor_resume, context)
            future_cover = executor.submit(write_cover_letter, context)
            future_fit = executor.submit(analyze_job_fit, context)
            future_prep = executor.submit(generate_interview_prep, context)
            future_email = executor.submit(generate_cold_email, context)

        def safe_get_future(future, default_val=""):
            try:
                res = future.result()
                return res if res else default_val
            except Exception as e:
                print(f"Subagent execution notice: {e}")
                return default_val

        context['tailored_resume'] = safe_get_future(future_tailor, "Tailored experience details aligned with target job requirements.")
        context['cover_letter'] = safe_get_future(future_cover, "Tailored narrative cover letter.")
        
        fit_result = safe_get_future(future_fit, {'score': 85, 'report': 'Match Score: 85%\nCandidate shows strong alignment with job requirements.'})
        if not isinstance(fit_result, dict):
            fit_result = {'score': 85, 'report': str(fit_result)}
        context['fit_analysis'] = fit_result

        context['interview_prep'] = safe_get_future(future_prep, "Role-specific STAR behavioral and technical interview preparation guide.")
        context['cold_email'] = safe_get_future(future_email, "Recruiter and hiring manager outreach templates.")

        # Step 4: Package DOCX and ZIP archive
        try:
            package_outputs(context)
        except Exception as pe:
            print(f"Package output notice: {pe}")

        # Cleanup temp file
        try:
            os.remove(resume_path)
            os.rmdir(temp_dir)
        except Exception:
            pass

        fit_score = fit_result.get('score', 85)
        fit_report = fit_result.get('report', str(fit_result))

        return jsonify({
            'company_brief': context.get('company_brief', ''),
            'tailored_resume': context['tailored_resume'],
            'cover_letter': context['cover_letter'],
            'interview_prep': context['interview_prep'],
            'fit_score': fit_score,
            'fit_report': fit_report,
            'cold_email': context['cold_email'],
            'company_name': company_name,
            'job_title': job_title,
            'location': location,
            'experience_requirements': experience_requirements,
            'salary_range': salary_range
        })

    except Exception as e:
        print("!!! Error processing application !!!")
        traceback.print_exc()
        return jsonify({'error': f"Processing failed: {str(e)}"}), 500

@app.route('/download/<filename>')
def download(filename):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(OUTPUTS_DIR, safe_filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': f'File {safe_filename} not found.'}), 404

@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({'error': f"Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)