# /Happy Birthday/app.py
from flask import Flask, render_template, request
from datetime import datetime
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form.get('student_name')
    birthday_info = request.form.get('birthday_info')
    birth_Date = request.form.get('birth_Date')
    current_date = datetime.now().strftime("%B-%d")

    create_upload_folder()

    if 'image_upload' in request.files:
        image_file = request.files['image_upload']
        if image_file and allowed_file(image_file.filename):
            filename = 'background.png'
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
    return render_template('result.html', student_name=student_name, birthday_info=birthday_info, background_image=image_path, current_date=current_date)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000, debug=True)
