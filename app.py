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

def car_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   color TEXT NOT NULL,
                   transmission TEXT NOT NULL,
                   fuel TEXT NOT NULL,
                   power INTEGER NOT NULL,
                   traction TEXT NOT NULL,
                   number_of_seats TEXT NOT NULL
            )
        ''')

def supercar_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS supercars (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   color TEXT NOT NULL,
                   transmission TEXT NOT NULL,
                   fuel TEXT NOT NULL,
                   power INTEGER NOT NULL,
                   traction TEXT NOT NULL,
                   number_of_seats TEXT NOT NULL,
                   inside_color TEXT NOT NULL,
                   inside_material TEXT NOT NULL
            )
        ''')

def bike_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS bikes (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   type TEXT NOT NULL,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   frame_size TEXT NOT NULL,
                   traction TEXT NOT NULL,
                   suspensions TEXT NOT NULL,
                   terrain TEXT NOT NULL
            )
        ''')

def scooter_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS scooters (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   color TEXT NOT NULL,
                   engine TEXT NOT NULL,
                   fuel TEXT NOT NULL,
                   power INTEGER NOT NULL,
                   required_license TEXT NOT NULL,
                   number_of_seats TEXT NOT NULL,
                   storage_capacity INTEGER NOT NULL,
                   windshield BOOLEAN NOT NULL
            )
        ''')

def motorcycle_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS motorcycles (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   style TEXT NOT NULL,
                   color TEXT NOT NULL,
                   engine TEXT NOT NULL,
                   fuel TEXT NOT NULL,
                   power INTEGER NOT NULL,
                   required_license TEXT NOT NULL,
                   number_of_seats TEXT NOT NULL,
                   storage_capacity INTEGER NOT NULL
            )
        ''')

def camper_db_init():
    with db_connect() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS campers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   rent_length INTEGER NOT NULL,
                   price REAL NOT NULL,
                   color TEXT NOT NULL,
                   fuel TEXT NOT NULL, 
                   type TEXT NOT NULL,
                   sleeping_beds TEXT NOT NULL,
                   approved_seats INTEGER NOT NULL,
                   type_bathroom TEXT NOT NULL,
                   climate_control BOOLEAN NOT NULL,
                   pets_allowed BOOLEAN NOT NULL
            )
        ''')

def db_init():
    user_db_init()
    car_db_init()
    supercar_db_init()
    bike_db_init()
    scooter_db_init()
    motorcycle_db_init()
    camper_db_init()    
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
    session.clear()
    flash("Logged out!", 'success')
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

        #CAR
        if vehicle_type == "car":
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            color = request.form.get('color')
            transmission = request.form.get('transmission')
            fuel = request.form.get('fuel')
            power = request.form.get('power')
            traction = request.form.get('traction')
            number_of_seats = request.form.get('number_of_seats')

            with db_connect() as db:
                db.execute(
                    'INSERT INTO cars (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats)
                )
                db.commit()
            
            flash("Car added!", 'success')
            return redirect(url_for('add_vehicle'))
        
        #SUPERCAR
        if vehicle_type == "supercar":
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            color = request.form.get('color')
            transmission = request.form.get('transmission')
            fuel = request.form.get('fuel')
            power = request.form.get('power')
            traction = request.form.get('traction')
            number_of_seats = request.form.get('number_of_seats')
            inside_color = request.form.get("inside_color")
            inside_material = request.form.get("inside_material")

            with db_connect() as db:
                db.execute(
                    'INSERT INTO supercars (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats, inside_color, inside_material) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats, inside_color, inside_material)
                )
                db.commit()
            
            flash("SuperCar added!", 'success')
            return redirect(url_for('add_vehicle'))

        #BIKE
        if vehicle_type == "bike":
            bike_type = request.form.get('type')
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            frame_size = request.form.get('frame_size')
            traction = request.form.get('traction')
            suspensions = request.form.get('suspensions')
            terrain = request.form.get('terrain')

            with db_connect() as db:
                db.execute(
                    'INSERT INTO bikes (type, brand, rent_length, price, frame_size, traction, suspensions, terrain) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (bike_type, brand, rent_length, price, frame_size, traction, suspensions, terrain)
                )
                db.commit()
            
            flash("Bike added!", 'success')
            return redirect(url_for('add_vehicle'))
        
        #SCOOTER
        if vehicle_type == "scooter":
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            color = request.form.get('color')
            engine = request.form.get('engine')
            fuel = request.form.get('fuel')
            power = request.form.get('power')
            required_license = request.form.get('required_license')
            number_of_seats = request.form.get('number_of_seats')
            storage_capacity = request.form.get('storage_capacity')
            windshield = request.form.get('windshield') == "on"

            with db_connect() as db:
                db.execute(
                    'INSERT INTO scooters (brand, rent_length, price, color, engine, fuel, power, required_license, number_of_seats, storage_capacity, windshield) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, engine, fuel, power, required_license, number_of_seats, storage_capacity, windshield)
                )
                db.commit()
            
            flash("Scooter added!", 'success')
            return redirect(url_for('add_vehicle'))
        
        #MOTORCYCLE
        if vehicle_type == "motorcycle":
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            style = request.form.get('style')
            color = request.form.get('color')
            engine = request.form.get('engine')
            fuel = request.form.get('fuel')
            power = request.form.get('power')
            required_license = request.form.get('required_license')
            number_of_seats = request.form.get('number_of_seats')
            storage_capacity = request.form.get('storage_capacity')

            with db_connect() as db:
                db.execute(
                    'INSERT INTO motorcycles (brand, rent_length, price, style, color, engine, fuel, power, required_license, number_of_seats, storage_capacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, style, color, engine, fuel, power, required_license, number_of_seats, storage_capacity)
                )
                db.commit()
            
            flash("Motorcycle added!", 'success')
            return redirect(url_for('add_vehicle'))
        
        #CAMPER
        if vehicle_type == "camper":
            brand = request.form.get('brand')
            rent_length = request.form.get('rent_length')
            price = request.form.get('price')
            color = request.form.get('color')
            fuel = request.form.get('fuel') 
            camper_type = request.form.get('type')
            sleeping_beds = request.form.get('sleeping_beds')
            approved_seats = request.form.get('approved_seats')
            type_bathroom = request.form.get('type_bathroom')
            climate_control = request.form.get('climate_control') == "on"
            pets_allowed = request.form.get('pets_allowed') == "on"

            with db_connect() as db:
                db.execute(
                    'INSERT INTO campers (brand, rent_length, price, color, fuel, type, sleeping_beds, approved_seats, type_bathroom, climate_control, pets_allowed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, fuel, camper_type, sleeping_beds, approved_seats, type_bathroom, climate_control, pets_allowed)
                )
                db.commit()
            
            flash("Camper added!", 'success')
            return redirect(url_for('add_vehicle'))
    
    return render_template("add_vehicle.html")
    
@app.route('/vehicle_list')
def vehicle_list():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    with db_connect() as db:
        cars = db.execute('SELECT id, brand, rent_length, price FROM cars').fetchall()
        supercars = db.execute('SELECT id, brand, rent_length, price FROM supercars').fetchall()
        bikes = db.execute('SELECT id, brand, rent_length, price FROM bikes').fetchall()
        scooters = db.execute('SELECT id, brand, rent_length, price FROM scooters').fetchall()
        motorcycles = db.execute('SELECT id, brand, rent_length, price FROM motorcycles').fetchall()
        campers = db.execute('SELECT id, brand, rent_length, price FROM campers').fetchall()
    
    return render_template("vehicle_list.html", 
                           cars=cars, supercars=supercars, bikes=bikes, 
                           scooters=scooters, motorcycles=motorcycles, campers=campers)

@app.route('/remove_vehicle', methods=['POST'])
def remove_vehicle():
    if not session.get('is_admin'):
        return redirect(url_for('index'))
    
    vehicle_id = request.form.get('vehicle_id')
    vehicle_type = request.form.get('vehicle_type')

    allowed_tables = ['cars', 'supercars', 'bikes', 'scooters', 'motorcycles', 'campers']
    
    if vehicle_type not in allowed_tables:
        flash("Tipo di veicolo non valido!", 'error')
        return redirect(url_for('vehicle_list'))

    with db_connect() as db:
        db.execute(
            f'DELETE FROM {vehicle_type} WHERE id = ?', (vehicle_id,)
        )
        db.commit()

    flash("Vehicle removed!", 'info')
    return redirect(url_for('vehicle_list'))

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
