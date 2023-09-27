import os
import tempfile
from rembg import remove
from PIL import Image
from flask import Flask,request,send_file
from flask_cors import CORS

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

app = Flask(__name__)
CORS(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def remove_background(input_path,output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


@app.route('/')
def home():
    return "<p>REMBG service</p>"

@app.route('/remback',methods=['POST'])
def remback():
    temp_dir = tempfile.mkdtemp()
    output_file = os.path.join(temp_dir, 'processed.png')
    file = request.files['file']
    if file and allowed_file(file.filename):
        file.save(os.path.join(temp_dir, file.filename))
        remove_background(os.path.join(temp_dir, file.filename), output_file)
        return send_file(output_file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

