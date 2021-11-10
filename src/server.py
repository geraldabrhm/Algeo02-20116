from flask import Flask, json, flash, request, jsonify, send_file, url_for
from flask.templating import render_template
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join('static','Image')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
defaultImage = os.path.join(app.config['UPLOAD_FOLDER'], 'no_image.jpg')
before_compressed = defaultImage
after_compressed = defaultImage

# @app.route("/")
# def hello_world():
#     return "<h1>Hello, World!</h1>"

@app.route('/', methods = ['GET'])
def getImage():
    after_compressed = 'messi.jpg'
    return render_template('index.html', before = before_compressed, after = after_compressed)

# @app.route('/get_image')
# def get_image():
#     if request.args.get('type') == '1':
#        filename = 'Image\\messi.jpg'
#     else:
#        filename = 'Image\\no_image.jpg'
#     return send_file(filename, mimetype='image/gif')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({ "status" : 500})
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return jsonify({ "status" : 500})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pathname = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return jsonify({ "status" : 200, "path" : pathname})
    return jsonify({ "status" : 200})


if __name__ == "__main__":
    app.run(debug=True)