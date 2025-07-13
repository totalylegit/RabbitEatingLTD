from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib
import os
import re
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'
app.secret_key = os.urandom(24).hex()

bcrypt = Bcrypt(app)

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL UNIQUE,
                 email TEXT NOT NULL UNIQUE,
                 password TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

# Hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

# Route for account info (sign-up and login)
@app.route('/accountinfo', methods=['GET', 'POST'])
def accountinfo():
    if request.method == 'POST':
        if 'signup' in request.form:
            # Handle sign-up
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            try:
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                         (username, email, hash_password(password)))
                conn.commit()
                conn.close()
                flash('Sign-up successful! Please log in.', 'success')
                return redirect(url_for('accountinfo'))
            except sqlite3.IntegrityError:
                flash('Username or email already exists.', 'error')
                conn.close()
        
        elif 'login' in request.form:
            # Handle login
            email = request.form['login-email']
            password = request.form['login-password']
            
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash('Invalid email format.', 'error')
                return redirect(url_for('accountinfo')) 

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ? AND password = ?",
                     (email, hash_password(password)))
            user = c.fetchone()
            conn.close()
            
            if user and bcrypt.check_password_hash(user[3], password):
                session['user_id'] = user[0]
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password.', 'error')
                return redirect(url_for('accountinfo')) 

    return render_template('accountinfo.html')

if __name__ == '__main__':
    init_db()  # Create database and table on startup
    app.run(debug=True)