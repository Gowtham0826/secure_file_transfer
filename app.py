from flask import Flask, render_template, request, send_file, redirect, url_for
import os
import time
from ecc_utils import encrypt_file, decrypt_file, derive_key
from blockchain import Blockchain
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
blockchain = Blockchain()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    password = request.form['password']
    if file and password:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        key = derive_key(password)
        encrypted_path = filepath + ".enc"
        encrypt_file(filepath, encrypted_path, key)
        os.remove(filepath)

        os.utime(encrypted_path, (time.time(), time.time()))
        blockchain.add_transaction(f"File {filename} uploaded.")

        return render_template("message.html", message="File uploaded and encrypted successfully.", filename=filename+".enc")
    return render_template("message.html", message="Upload failed.")

@app.route('/download')
def download_page():
    return render_template("download.html")

@app.route('/download', methods=['POST'])
def download():
    filename = request.form['filename']
    password = request.form['password']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(filepath):
        # Check expiration (1 hour)
        if time.time() - os.path.getmtime(filepath) > 3600:
            os.remove(filepath)
            return render_template("message.html", message="File expired.")

        key = derive_key(password)
        decrypted_path = filepath + ".dec"
        try:
            decrypt_file(filepath, decrypted_path, key)
            blockchain.add_transaction(f"File {filename} downloaded.")
            return send_file(decrypted_path, as_attachment=True)
        except Exception as e:
            return render_template("message.html", message="Decryption failed. Wrong password?")
    return render_template("message.html", message="File not found.")

if __name__ == '__main__':
    app.run(debug=True)