from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'secure_file_transfer_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Sample users
users = {
    "sender1": {"password": "pass1", "role": "sender"},
    "receiver1": {"password": "pass1", "role": "receiver"}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        user = users.get(username)

        if user and user["password"] == password and user["role"] == role:
            session['username'] = username
            session['role'] = role
            return redirect(url_for('upload' if role == 'sender' else 'download'))
        return "Invalid credentials"

    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session or session['role'] != 'sender':
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return "File uploaded successfully!"

    return render_template('upload.html')

@app.route('/download')
def download():
    if 'username' not in session or session['role'] != 'receiver':
        return redirect(url_for('login'))

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('download.html', files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
