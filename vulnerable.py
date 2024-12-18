import sqlite3
import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Database setup
db = sqlite3.connect(':memory:', check_same_thread=False)
cursor = db.cursor()
cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
db.commit()

@app.route("/")
def home():
    return "Welcome to the Vulnerable Application!"

# 1. SQL Injection
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    # Vulnerable SQL query allowing SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"Executing query: {query}")
    result = cursor.execute(query).fetchall()
    
    if result:
        return "Login successful!"
    else:
        return "Invalid credentials!"

# 2. XSS (Cross-Site Scripting)
@app.route("/xss", methods=["GET", "POST"])
def xss():
    if request.method == "POST":
        user_input = request.form.get("input")
        
        # Render user input directly, leading to XSS
        html = f"<h1>Your input: {user_input}</h1>"
        return render_template_string(html)
    return '''
        <form method="POST">
            <input type="text" name="input">
            <button type="submit">Submit</button>
        </form>
    '''

# 3. SSRF (Server-Side Request Forgery)
@app.route("/ssrf", methods=["POST"])
def ssrf():
    url = request.form.get("url")
    
    # Directly use user input for a request, leading to SSRF
    response = requests.get(url)
    return f"Response from {url}: {response.text}"

# 4. File Inclusion
@app.route("/file", methods=["GET"])
def file_inclusion():
    filename = request.args.get("file")
    
    # Dangerous file inclusion vulnerability
    if filename:
        with open(filename, 'r') as file:
            content = file.read()
        return f"<pre>{content}</pre>"
    return '''
        <form>
            <input type="text" name="file" placeholder="Enter file path">
            <button type="submit">View File</button>
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
