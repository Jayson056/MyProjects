from flask import Flask, render_template, request, redirect, url_for
import os
from removebg import RemoveBg
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/save'

removebg = RemoveBg("AJqGuCnPuH3kB1kMCsF1eLri", "error.log")

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        output_filename = 'NoBackground.png'
        output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        # Ensure the output directory exists
        os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

        file.save(output_filepath)

        upload_filename = 'uploadIMG.png'
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

        # Ensure the upload directory exists
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], current_datetime)
        os.makedirs(upload_dir, exist_ok=True)

        removebg.remove_background_from_img_file(output_filepath)
        output_filepath_final = os.path.join(upload_dir, upload_filename)

        os.rename(output_filepath, output_filepath_final)

        return redirect(url_for('result', filename=output_filepath_final))

@app.route('/save/')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)