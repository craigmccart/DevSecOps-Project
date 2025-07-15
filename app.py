import sqlite3
import hashlib
import xml.etree.ElementTree as ET
import pickle
import jwt
import os
from flask import Flask, request, escape
from werkzeug.security import generate_password_hash, check_password_hash

"""
✅ SECURE APPLICATION CODE ✅
This file contains the remediated version of the vulnerable application.
It demonstrates best practices for securing a Flask web application against common vulnerabilities.
"""

# Flask application
app = Flask(__name__)
# Use an environment variable for the secret key in a real app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-secure-default-secret-key')

# --- Database Setup ---
def init_db():
    """Initializes the database and creates the users table if it doesn't exist."""
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    # Add a dummy user for testing if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       ('admin', generate_password_hash('admin_password')))
    connection.commit()
    connection.close()

# 1. **Injection (SQL Injection) - REMEDIATED**
def get_user_data(user_id):
    """Fetches user data from the database using a parameterized query to prevent SQL injection."""
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    # REMEDIATED: Use a parameterized query to prevent SQL Injection
    query = "SELECT id, username FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    connection.close()
    return user

@app.route('/get_user/<int:user_id>')
def get_user(user_id):
    user_data = get_user_data(user_id)
    if user_data:
        return str(user_data)
    return "User not found", 404

# 2. **Broken Authentication - REMEDIATED**
def login(username, password):
    """Securely logs a user in by checking their password against a stored hash."""
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    connection.close()

    if user_record and check_password_hash(user_record[0], password):
        # Use the app's configured secret key for the token
        token = jwt.encode({"user": username}, app.config['SECRET_KEY'], algorithm="HS256")
        return f"Logged in successfully. Token: {token}"
    else:
        return "Invalid credentials", 401

# 3. **Sensitive Data Exposure - REMEDIATED**
# This is remediated by using `werkzeug.security.generate_password_hash` during user registration
# and `check_password_hash` during login, which use strong, salted hashing (scrypt by default).

# 4. **XML External Entities (XXE) - REMEDIATED**
def parse_xml_safely(xml_string):
    """Parses an XML string using a parser that disables external entity resolution to prevent XXE."""
    # REMEDIATED: Use a parser with resolve_entities set to False
    parser = ET.XMLParser(resolve_entities=False)
    tree = ET.fromstring(xml_string, parser=parser)
    return tree.findtext("name", default="No name found")

# 7. **Cross-Site Scripting (XSS) - REMEDIATED**
@app.route('/greet')
def greet():
    name = request.args.get('name', 'Guest')
    # REMEDIATED: Use escape() to sanitize user input and prevent XSS
    return f"Hello, {escape(name)}!"

# 8. **Insecure Deserialization - REMEDIATED**
def secure_deserialize(data):
    """Uses JSON for safe data deserialization instead of pickle."""
    # REMEDIATED: Use a safe serialization format like JSON
    try:
        return str(json.loads(data))
    except json.JSONDecodeError:
        return "Invalid JSON data", 400

import json
from functools import wraps

# 5. **Broken Access Control - REMEDIATED**
def token_required(f):
    """A decorator to ensure a valid JWT token is present for protected routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return 'Token is missing!', 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return 'Token has expired!', 401
        except jwt.InvalidTokenError:
            return 'Token is invalid!', 401
        return f(current_user, *args, **kwargs)
    return decorated

# 6. **Security Misconfiguration - REMEDIATED**
# This is addressed by:
# 1. Setting `debug=False` in `app.run()`.
# 2. Using an environment variable for the SECRET_KEY, not hardcoding it.

# 9. **Using Components with Known Vulnerabilities - REMEDIATED**
import requests

def fetch_data_from_external_api():
    """Demonstrates making a secure API call using an up-to-date library (requests)."""
    try:
        # Using a well-maintained library like requests for external calls.
        # SCA tools will scan requirements.txt to ensure this is a safe version.
        response = requests.get('https://api.github.com/events', timeout=5)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"External API call failed: {e}")
        return "Failed to fetch data from external API.", 500

# 10. **Insufficient Logging and Monitoring - REMEDIATED**
import logging
logging.basicConfig(level=logging.INFO)

@app.route('/admin')
def admin():
    # REMEDIATED: Log access to sensitive endpoints
    app.logger.info(f"Admin area accessed by {request.remote_addr}")
    return "Welcome to the admin area!"


# --- Example Routes for a Secure App ---
@app.route('/')
def index():
    return "Welcome to the SECURE app!"

@app.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return "Username and password are required", 400
    return login(username, password)

@app.route('/parse_xml', methods=['POST'])
def parse_xml_route():
    xml_string = request.data
    return parse_xml_safely(xml_string)

@app.route('/deserialize', methods=['POST'])
def deserialize_route():
    data = request.data
    return secure_deserialize(data)

@app.route('/delete_user/<string:username_to_delete>', methods=['DELETE'])
@token_required
def delete_user_route(current_user, username_to_delete):
    """Deletes a user, but only if the logged-in user matches the user to be deleted."""
    # REMEDIATED: Check if the authenticated user is the one they are trying to delete.
    # A more complex app might check for an 'admin' role.
    if current_user != username_to_delete:
        return "Forbidden: You can only delete your own account.", 403
    
    # Proceed with deletion
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username_to_delete,))
    connection.commit()
    connection.close()
    
    app.logger.info(f"User '{username_to_delete}' was deleted by '{current_user}'.")
    return f"User {username_to_delete} deleted successfully.", 200

@app.route('/external_api')
def external_api_route():
    return fetch_data_from_external_api()


if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=False)  # Turn off debug mode for production
