# Secure File Transfer System

## 🔐 Features
- ECC Encryption/Decryption (AES simulated)
- File password protection
- File auto-expiry (1 hour)
- Blockchain log for uploads
- Role-based access (Sender/Receiver)
- Web-based via Flask & Render

## 🚀 Setup Instructions
```bash
pip install -r requirements.txt
python app.py
```

## 👥 User Roles
Defined in `users.json`:
- alice / 1234 (Sender)
- bob / 5678 (Receiver)

## 📤 Sender Flow
1. Login as sender
2. Upload a file with password
3. Share file ID

## 📥 Receiver Flow
1. Login as receiver
2. Enter file ID + password
3. Download decrypted file

## 🌐 Deployment (Render)
1. Push to GitHub
2. Connect Render
3. Auto-deploy using `render.yaml`
