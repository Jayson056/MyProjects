from flask import Flask, render_template, request
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    file_count = int(request.form['file_count'])
    file_type = request.form['fileType']

    uploaded_files = request.files.getlist('resume')
    upload_dir = os.path.join(app.root_path, 'static', 'uploads', name, file_type)
    os.makedirs(upload_dir, exist_ok=True)
    file_names = save_uploaded_files(uploaded_files[:file_count], upload_dir)

    save_student_info(name, email, subject, file_names, file_type)

    return render_template('thank-you.html', name=name, email=email, subject=subject)

def save_uploaded_files(uploaded_files, upload_dir):
    file_names = []
    for i, file in enumerate(uploaded_files):
        original_filename = secure_filename(file.filename)
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f'{current_datetime}{"-"}{original_filename}'
        upload_path = os.path.join(upload_dir, file_name)
        file.save(upload_path)
        file_names.append(file_name)
    return file_names

def save_student_info(name, email, subject, file_names, file_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info = f"Name: {name}\nEmail: {email}\nSubject: {subject}\nFile Type: {file_type}\nFiles: {', '.join(file_names)}\nTimestamp: {timestamp}\n\n"

    log_file_path = os.path.join(app.root_path, 'static', 'uploads', 'student_log.txt')
    with open(log_file_path, 'a') as log_file:
        log_file.write(info)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
