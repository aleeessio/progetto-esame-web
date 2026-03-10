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
        return redirect(url_for('register'))

        ############################ End DB update ############################
    
    return render_template("register.html")
        

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/contanct')
def contact():
    return render_template("contact.html")

# -------------------------------


if __name__ == '__main__':
    database_init()
    app.run(debug=True, port=1234)