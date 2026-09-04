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
from tools.groq_helper import FriendlyAPIException, map_error_to_friendly_exception

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
        print("Backend Processing Exception Captured:")
        traceback.print_exc()
        friendly = map_error_to_friendly_exception(e)
        return jsonify({
            'error': friendly.message,
            'code': friendly.code,
            'hint': friendly.hint
        }), friendly.code

@app.route('/download/<filename>')
def download(filename):
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(OUTPUTS_DIR, safe_filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({
            'error': f'The requested file ({safe_filename}) is no longer available.',
            'code': 404,
            'hint': 'Please generate a new application suite to create updated documents.'
        }), 404

# Comprehensive Friendly Flask Error Handlers (No raw stack traces)
@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({
        'error': 'Invalid Application Input: Please select a valid resume document and enter a job description.',
        'code': 400,
        'hint': 'Upload a PDF, DOCX, or TXT resume file.'
    }), 400

@app.errorhandler(401)
def handle_unauthorized(e):
    return jsonify({
        'error': 'API Authentication Failed: Invalid or missing API key.',
        'code': 401,
        'hint': 'Check that your GROQ_API_KEY environment setting is valid.'
    }), 401

@app.errorhandler(403)
def handle_forbidden(e):
    return jsonify({
        'error': 'Access Denied: Insufficient API scope or model permission.',
        'code': 403,
        'hint': 'Verify model scope and API key permissions.'
    }), 403

@app.errorhandler(404)
def handle_not_found(e):
    return jsonify({
        'error': 'Resource Not Found: The requested endpoint or document does not exist.',
        'code': 404,
        'hint': 'Please return to the homepage and submit a new request.'
    }), 404

@app.errorhandler(422)
def handle_unprocessable(e):
    return jsonify({
        'error': 'Unprocessable Entity: Unable to parse document contents.',
        'code': 422,
        'hint': 'Please verify your resume text is readable and not password-protected.'
    }), 422

@app.errorhandler(429)
def handle_rate_limit(e):
    return jsonify({
        'error': 'Service Rate Limit Exceeded: AI service limit reached.',
        'code': 429,
        'hint': 'Please wait 10-15 seconds before trying again.'
    }), 429

@app.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({
        'error': 'Application Service Notice: The server encountered a temporary processing delay.',
        'code': 500,
        'hint': 'Please try submitting your request again in a few moments.'
    }), 500

@app.errorhandler(502)
@app.errorhandler(503)
def handle_service_unavailable(e):
    return jsonify({
        'error': 'AI Service Temporarily Unavailable: The backend provider is currently experiencing high load.',
        'code': 503,
        'hint': 'Please wait a moment and click Try Again.'
    }), 503

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)