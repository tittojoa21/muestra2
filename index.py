from flask import Flask, request, send_from_directory, jsonify, redirect, url_for
import os

app = Flask(__name__, static_url_path='', static_folder='.')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'images' not in request.files:
        return jsonify({"error": "No file part"})
    
    files = request.files.getlist('images')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(url_for('uploaded_file', filename=filename))

    return jsonify({"filePaths": uploaded_files})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/images')
def list_images():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    images = [url_for('uploaded_file', filename=f) for f in files if allowed_file(f)]
    return jsonify({"images": images})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)