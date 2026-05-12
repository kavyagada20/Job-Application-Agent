<<<<<<< HEAD
from flask import Flask, request, render_template, send_file, jsonify
import os
import tempfile
from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.packager import package_outputs

app = Flask(__name__, template_folder='templates', static_folder='static')

# Ensure the outputs directory exists when the app starts
OUTPUTS_DIR = os.path.join(app.root_path, 'outputs')
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get JD
        jd_input = request.form.get('jd_text', '')

        # Get resume file
        resume_file = request.files.get('resume')
        if not resume_file:
            return jsonify({'error': 'Resume file required'})

        # Save temp file
        temp_dir = tempfile.mkdtemp()
        resume_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(resume_path)

        # Process through agents
        context = parse_resume_and_jd(resume_path, jd_input)
        
        # Extract company name early for UI/download consistency
        company_name = context.get('job_description', {}).get('company_name', 'Company')
        
        context['company_brief'] = research_company(company_name, context['job_description']['job_title'])
        context['tailored_resume'] = tailor_resume(context)
        context['cover_letter'] = write_cover_letter(context)
        
        # This function generates the .docx files in the 'outputs' folder
        package_outputs(context)

        # Clean up temp
        os.remove(resume_path)
        os.rmdir(temp_dir)

        # Return results including the company_name for the frontend to build download links
        return jsonify({
            'company_brief': context['company_brief'],
            'tailored_resume': context['tailored_resume'],
            'cover_letter': context['cover_letter'],
            'company_name': company_name
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    # Construct an absolute path to avoid directory issues
    file_path = os.path.join(OUTPUTS_DIR, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        # Return a 404 if the AI failed to generate the specific file
        return jsonify({'error': f'File {filename} not found.'}), 404

if __name__ == '__main__':
=======
from flask import Flask, request, render_template, send_file, jsonify
import os
import tempfile
from agents.parser import parse_resume_and_jd
from agents.researcher import research_company
from agents.resume_tailor import tailor_resume
from agents.cover_letter import write_cover_letter
from agents.packager import package_outputs

app = Flask(__name__, template_folder='templates', static_folder='static')

# Ensure the outputs directory exists when the app starts
OUTPUTS_DIR = os.path.join(app.root_path, 'outputs')
if not os.path.exists(OUTPUTS_DIR):
    os.makedirs(OUTPUTS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        # Get JD
        jd_input = request.form.get('jd_text', '')

        # Get resume file
        resume_file = request.files.get('resume')
        if not resume_file:
            return jsonify({'error': 'Resume file required'})

        # Save temp file
        temp_dir = tempfile.mkdtemp()
        resume_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(resume_path)

        # Process through agents
        context = parse_resume_and_jd(resume_path, jd_input)
        
        # Extract company name early for UI/download consistency
        company_name = context.get('job_description', {}).get('company_name', 'Company')
        
        context['company_brief'] = research_company(company_name, context['job_description']['job_title'])
        context['tailored_resume'] = tailor_resume(context)
        context['cover_letter'] = write_cover_letter(context)
        
        # This function generates the .docx files in the 'outputs' folder
        package_outputs(context)

        # Clean up temp
        os.remove(resume_path)
        os.rmdir(temp_dir)

        # Return results including the company_name for the frontend to build download links
        return jsonify({
            'company_brief': context['company_brief'],
            'tailored_resume': context['tailored_resume'],
            'cover_letter': context['cover_letter'],
            'company_name': company_name
        })

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    # Construct an absolute path to avoid directory issues
    file_path = os.path.join(OUTPUTS_DIR, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        # Return a 404 if the AI failed to generate the specific file
        return jsonify({'error': f'File {filename} not found.'}), 404

if __name__ == '__main__':
>>>>>>> 06116eaa0f9be49c8fcaabd5f2720b3ecc5dc093
    app.run(debug=True)