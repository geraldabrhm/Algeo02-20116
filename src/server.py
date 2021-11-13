from flask import Flask, json, flash, request, jsonify, send_file, url_for, render_template, send_from_directory, redirect
from werkzeug.utils import secure_filename
# from flask_sqlalchemy import SQLAlchemy
import os
import svd

UPLOAD_FOLDER = os.path.join('static','Image') # ../static/Image
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = "secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

def download_image(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_image():
    variable = request.form['compression-rate']
    variableInt = int(variable)
    if (variableInt<1 or variableInt>100):
        flash('Masukkan angka 1-100')
        return redirect(request.url)

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        waktu, compressedFilename, pixel = svd.compress(filename, variableInt)
        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename, compressed = compressedFilename, waktu = waktu, pixel = pixel)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='Image/' + filename), code=301)

@app.route('/download/<filename>')
def download_file(filename):
    pathfile = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(pathfile, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)