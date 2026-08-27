from flask import Flask, request, render_template, send_file, jsonify
import os
import tempfile
import traceback
from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.interview_prep import generate_interview_prep
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

        # Step 1: Parse
        context = parse_resume_and_jd(resume_path, jd_input)
        
        jd_info = context.get('job_description', {})
        company_name = jd_info.get('company_name', 'Company')
        job_title = jd_info.get('job_title', 'Role')
        location = jd_info.get('location', 'Not specified')
        experience_requirements = jd_info.get('experience_requirements', 'Not specified')
        salary_range = jd_info.get('salary_range', 'Not specified')

        # Step 2: Research
        context['company_brief'] = research_company(company_name, job_title)
        
        # Step 3: Tailor Resume
        context['tailored_resume'] = tailor_resume(context)
        
        # Step 4: Cover Letter
        context['cover_letter'] = write_cover_letter(context)
        
        # Step 5: Interview Prep
        context['interview_prep'] = generate_interview_prep(context)
        
        # Step 6: Package DOCX
        package_outputs(context)

        # Cleanup temp file
        try:
            os.remove(resume_path)
            os.rmdir(temp_dir)
        except Exception:
            pass

        return jsonify({
            'company_brief': context['company_brief'],
            'tailored_resume': context['tailored_resume'],
            'cover_letter': context['cover_letter'],
            'interview_prep': context['interview_prep'],
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
    file_path = os.path.join(OUTPUTS_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': f'File {filename} not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)