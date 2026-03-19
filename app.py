from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'temprorary-secret-key'

DB_USERS_PATH = 'data.db'

# -------------------------------
# Database config
# -------------------------------

def db_connect():
    conn = sqlite3.connect(DB_USERS_PATH)
    conn.row_factory = sqlite3.Row
    return conn 

def database_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL
            )
        ''')
        db.commit()

# -------------------------------



# -------------------------------
# Routes
# -------------------------------

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        repeat_password = request.form.get("repeat_password", "").strip()

        ############################ Start errors check ############################
        
        check_nullness = [len(name), len(email), len(password), len(repeat_password)]

        if 0 in check_nullness:
            flash("Riempi ogni campo!", "error")
            return redirect(url_for('register'))
        
        if password != repeat_password:
            flash("Passwords don't match!", "error")
            return redirect(url_for('register'))
        
        if len(password) < 6:
            flash("At least 6 characters!", "error")
            return redirect(url_for('register'))
        
        with db_connect() as db:
            double_check = db.execute(
                'SELECT id FROM users where email = ?', (email,)
            ).fetchone() 
        
        if double_check:
            flash("Email already exists, login!", "error")
            return redirect(url_for('register'))
        
        ############################ End errors check ############################
        
        ############################ Start DB update ############################
        
        passwd_hash = generate_password_hash(password)
        with db_connect() as db:
            db.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, passwd_hash)
            )
            db.commit()

        flash("Registration succeded, login!", 'success')
        return redirect(url_for('login'))

        ############################ End DB update ############################
    
    return render_template("register.html")
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email", "").strip()
        pwd = request.form.get("password", "").strip()

        with db_connect() as db:
            user = db.execute(
                'SELECT id, name, password FROM users where email = ?', (email,)
            ).fetchone()

        if user is None:
            flash("Register first!", 'error')
            return redirect(url_for('register'))

        auth = check_password_hash(user['password'], pwd)

        if auth:
            session['user_id'] = user['id']
            session['user_name'] = user['name']

            flash("Logged in!", 'success')
            return redirect(url_for('index'))
        else:
            flash("Password incorrect!", 'error')
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/privacy_policy')
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/terms_conditions')
def terms_conditions():
    return render_template("terms_conditions.html")

# -------------------------------


if __name__ == '__main__':
    database_init()
    app.run(debug=True, port=1234)
