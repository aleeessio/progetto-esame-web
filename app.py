from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import json
import os

app = Flask(__name__)
app.secret_key = 'temprorary-secret-key'

DB_USERS_PATH = 'data.db'
ADMIN_EMAIL = "2.2@22"
ADMIN_PWD = "12" 

# -------------------------------
# Database config
# -------------------------------

def db_connect():
    conn = sqlite3.connect(DB_USERS_PATH)
    conn.row_factory = sqlite3.Row
    return conn 

def user_db_init():
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

def bike_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS bikes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   type TEXT NOT NULL,
                   transmission TEXT NOT NULL,
                   suspensions TEXT NOT NULL,
                   accessories  TEXT CHECK(json_valid(accessories)),
                   terrain TEXT NOT NULL
            )
        ''')

def db_init():
    user_db_init()
    bike_db_init()

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

        if email == ADMIN_EMAIL:
            if pwd == ADMIN_PWD:
                session['is_admin'] = True
                flash("Welcome admin!", 'success')
                return redirect(url_for('admin'))
            
            else:
                flash("Password incorrect!", 'error')
                return redirect(url_for('login'))

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
    flash("Are you sure?", 'logout')
    return redirect(request.referrer)

@app.route('/confirm_logout')
def confirm_logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        flash("Access denied!", 'error')
        return redirect(url_for('index'))
    
    return render_template("admin.html")

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        vehicle_type = request.form.get('vehicle_type')

        if vehicle_type == "bike":
            bike_type = request.form.get('type')
            transmission = request.form.get('transmission')
            suspensions = request.form.get('suspensions')
            accessories = json.dumps(request.form.getlist('accessories'))
            terrain = request.form.get('terrain')

            with db_connect() as db:
                db.execute(
                    'INSERT INTO bikes (type, transmission, suspensions, accessories, terrain) VALUES (?, ?, ?, ?, ?)', (bike_type, transmission, suspensions, accessories, terrain)
                )
                db.commit()
            
            flash("Vehicle added!", 'success')
            return redirect(url_for('add_vehicle'))
    
    return render_template("add_vehicle.html")
    
@app.route('/list_vehicles')
def list_vehicles():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    return redirect(url_for('admin'))

@app.route('/user_list')
def user_list():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    with db_connect() as db:
        users = db.execute(
            'SELECT id, name, email FROM users'
        ).fetchall()
    
    return render_template("user_list.html", users=users)

@app.route('/remove_user', methods=['POST'])
def remove_user():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    index = request.form.get('user_id')

    with db_connect() as db:
        db.execute(
            'DELETE FROM users WHERE id = ?', (index,)
        )
        db.commit()

    flash("User removed!", 'info')
    return redirect(url_for('user_list'))

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
    db_init()
    app.run(debug=True, port=1234)
