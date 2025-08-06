<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('login.html')  # login page

# ---------------- LOGIN ROUTE ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']  # 'sender' or 'receiver'
        password = request.form['password']

        # Add your authentication logic here
        if role == 'sender':
            return redirect(url_for('upload_page'))
        else:
            return redirect(url_for('receiver_dashboard'))
    return render_template('login.html')

# ---------------- UPLOAD PAGE (SENDER) ----------------
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            return 'File uploaded successfully!'
    return render_template('upload.html')

# ---------------- RECEIVER DASHBOARD ----------------
@app.route('/receiver')
def receiver_dashboard():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('receiver_dashboard.html', files=files)

# ---------------- DOWNLOAD FILE ----------------
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# ---------------- RUN APP ----------------
if __name__ == '__main__':
    app.run(debug=True)
=======
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
>>>>>>> f5e8ac0294d88315cdd96ef3848a8f42bbf6a9ec
