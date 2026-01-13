from flask import Flask, request, escape, jsonify
import subprocess
import bcrypt
import os
import re

app = Flask(__name__)

ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
if not ADMIN_PASSWORD_HASH:
    raise RuntimeError("ADMIN_PASSWORD_HASH must be set")

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def is_valid_hostname(host: str) -> bool:
    return re.match(r"^[a-zA-Z0-9.-]+$", host) is not None

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get("username", "")
    password = data.get("password", "")

    if username != "admin" or not check_password(password, ADMIN_PASSWORD_HASH):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Logged in successfully"})

@app.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "localhost")
    if not is_valid_hostname(host):
        return jsonify({"error": "Invalid host"}), 400

    result = subprocess.run(
        ["ping", "-c", "1", host],
        capture_output=True,
        text=True
    )
    return jsonify({"output": result.stdout})

@app.route("/hello", methods=["GET"])
def hello():
    name = escape(request.args.get("name", "user"))
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
