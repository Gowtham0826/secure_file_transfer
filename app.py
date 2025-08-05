from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
from cryptography.fernet import Fernet

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Generate and store a key (you can store this in an env variable or file)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def index():
    return '''
        <h2>Secure File Transfer</h2>
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <input type="submit" value="Upload & Encrypt">
        </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    uploaded_file.save(filepath)

    # Encrypt the file
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted_data = cipher_suite.encrypt(data)

    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], f'encrypted_{filename}')
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)

    return f'''
        <p>File uploaded and encrypted successfully!</p>
        <a href="/download/{'encrypted_' + filename}">Download Encrypted File</a>
    '''

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(path, as_attachment=True)

# ✅ REQUIRED for Render to detect the correct port and bind publicly
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
