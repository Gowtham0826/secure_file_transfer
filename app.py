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
