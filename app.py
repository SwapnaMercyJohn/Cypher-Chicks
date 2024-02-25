from flask import Flask, render_template, request, jsonify
from cryptography.fernet import Fernet
import json

app = Flask(__name__)

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt and decrypt functions
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data).decode()

# File to store encrypted passwords
PASSWORD_FILE = "passwords.json"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_password():
    try:
        data = request.json
        website = data.get('website')
        username = data.get('username')
        password = encrypt_data(data.get('password'))

        with open(PASSWORD_FILE, 'a+') as file:
            file.seek(0)
            passwords = json.load(file)
            passwords.append({"website": website, "username": username, "password": password})
            file.seek(0)
            json.dump(passwords, file)

        return jsonify({"message": "Password saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get')
def get_passwords():
    try:
        with open(PASSWORD_FILE, 'r') as file:
            passwords = json.load(file)
            decrypted_passwords = [{"website": password["website"], "username": password["username"]} for password in passwords]
            return jsonify(decrypted_passwords), 200
    except FileNotFoundError:
        return jsonify([]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
