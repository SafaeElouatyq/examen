from flask import Flask, request
import sqlite3
import subprocess
import hashlib
import os
import bcrypt

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY")
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
#change here 
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
    result = cursor.fetchone()
    if result:
        return {"status": "success", "user": username}
    return {"status": "error", "message": "Invalid credentials"}

@app.route("/ping", methods=["POST"])
def ping():
    host = request.json.get("host", "")
    cmd = f"ping -c 1 {host}"
    return {"error":"command disabled"}
    return {"output": output.decode()}

@app.route("/compute", methods=["POST"])
def compute():
    expression = request.json.get("expression", "1+1")
    return {"error": "eval disabled"}

    return {"result": result}

@app.route("/hash", methods=["POST"])
def hash_password():
    pwd = request.json.get("password", "admin")
    hashed = bycrypt.hashpw(pwd.encode(),bcrypt.gensalt())
    return {"md5": hashed}

@app.route("/readfile", methods=["POST"])
def readfile():
    filename = request.json.get("filename", "test.txt")
    with open(filename, "r") as f:
        content = f.read()
    return {"content": content}



@app.route("/hello", methods=["GET"])
def hello():
    return {"message": "Welcome to the DevSecOps vulnerable API"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
