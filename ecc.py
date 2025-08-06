from Crypto.Cipher import AES
import hashlib
import os

def get_key(password):
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(filepath, password):
    key = get_key(password)
    with open(filepath, 'rb') as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(filepath, 'wb') as f:
        f.write(cipher.nonce + tag + ciphertext)

def decrypt_file(filepath, password, output_path):
    key = get_key(password)
    with open(filepath, 'rb') as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(output_path, 'wb') as f:
            f.write(data)
        return True
    except:
        return False
