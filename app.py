from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
import shutil

app = Flask(__name__)
app.secret_key = 'temprorary-secret-key'

DB_USERS_PATH = 'data.db'
IMG_PATH = os.path.join('static', 'imgs')
IMG_ALLOWED = {'jpg', 'png', 'webp', 'jpeg'}

ADMIN_EMAIL = "2.2@22"
ADMIN_PWD = "12" 

TYPE_TO_TABLE = {
    'car':        'cars',
    'supercar':   'supercars',
    'bike':       'bikes',
    'scooter':    'scooters',
    'motorcycle': 'motorcycles',
    'camper':     'campers',
}

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
                   number_of_seats TEXT NOT NULL,
                   img TEXT
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
                   inside_material TEXT NOT NULL,
                   img TEXT
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
                   terrain TEXT NOT NULL,
                   img TEXT
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
                   windshield BOOLEAN NOT NULL,
                   img TEXT
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
                   storage_capacity INTEGER NOT NULL,
                   img TEXT
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
                   pets_allowed BOOLEAN NOT NULL,
                   img TEXT
            )
        ''')

def rental_db_init():
    with db_connect() as db:
        # db.execute('''DROP TABLE IF EXISTS rental_requests ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS rental_requests (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   user_name TEXT NOT NULL,
                   user_email TEXT NOT NULL,
                   user_phone TEXT NOT NULL,
                   vehicle_type TEXT NOT NULL,
                   vehicle_id INTEGER NOT NULL,
                   vehicle_brand TEXT NOT NULL,
                   start_date TEXT NOT NULL,
                   end_date TEXT NOT NULL,
                   message TEXT,
                   status TEXT NOT NULL
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
    rental_db_init()   
# -------------------------------

# -------------------------------
# Extra functions
# -------------------------------

def is_img_allowed(fname):
    if '.' not in fname:
        return False
    return fname.rsplit('.', 1)[-1].lower() in IMG_ALLOWED

def img_handler(db_conn, vehicle_type, vehicle_id):
    fname = None
    input_file = request.files.get('img')
    if input_file and input_file.filename and is_img_allowed(input_file.filename):
                    fname = secure_filename(input_file.filename)
                    new_folder = os.path.join(IMG_PATH, vehicle_type, str(vehicle_id))
                    os.makedirs(new_folder, exist_ok=True)
                    input_file.save(os.path.join(new_folder, fname))
    
    db_conn.execute(f'UPDATE {vehicle_type} SET img = ? WHERE id = ?', (fname, vehicle_id))
    db_conn.commit()

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
            return redirect(url_for('login'))
        
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
            return redirect(url_for('profile'))
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
                data = db.execute(
                    'INSERT INTO cars (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats)
                )

                curr_id = data.lastrowid
                img_handler(db, 'cars', curr_id)
            
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
                data = db.execute(
                    'INSERT INTO supercars (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats, inside_color, inside_material) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, transmission, fuel, power, traction, number_of_seats, inside_color, inside_material)
                )

                curr_id = data.lastrowid
                img_handler(db, 'supercars', curr_id)
            
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
                data = db.execute(
                    'INSERT INTO bikes (type, brand, rent_length, price, frame_size, traction, suspensions, terrain) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (bike_type, brand, rent_length, price, frame_size, traction, suspensions, terrain)
                )

                curr_id = data.lastrowid
                img_handler(db, 'bikes', curr_id)
            
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
                data = db.execute(
                    'INSERT INTO scooters (brand, rent_length, price, color, engine, fuel, power, required_license, number_of_seats, storage_capacity, windshield) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, engine, fuel, power, required_license, number_of_seats, storage_capacity, windshield)
                )

                curr_id = data.lastrowid
                img_handler(db, 'scooters', curr_id)
            
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
                data = db.execute(
                    'INSERT INTO motorcycles (brand, rent_length, price, style, color, engine, fuel, power, required_license, number_of_seats, storage_capacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, style, color, engine, fuel, power, required_license, number_of_seats, storage_capacity)
                )

                curr_id = data.lastrowid
                img_handler(db, 'motorcycles', curr_id)
            
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
                data = db.execute(
                    'INSERT INTO campers (brand, rent_length, price, color, fuel, type, sleeping_beds, approved_seats, type_bathroom, climate_control, pets_allowed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (brand, rent_length, price, color, fuel, camper_type, sleeping_beds, approved_seats, type_bathroom, climate_control, pets_allowed)
                )

                curr_id = data.lastrowid
                img_handler(db, 'campers', curr_id)
            
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

    curr_veichle_imgs = os.path.join(IMG_PATH, str(vehicle_type), str(vehicle_id))
    if os.path.isdir(curr_veichle_imgs):
        shutil.rmtree(curr_veichle_imgs)

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

@app.route('/request_list')
def request_list():
    if not session.get('is_admin'):
        flash("Access denied!", 'error')
        return redirect(url_for('index'))
    
    with db_connect() as db:
        reqs = db.execute(
            'SELECT * FROM rental_requests ORDER BY id DESC'
        ).fetchall()

    return render_template("request_list.html", requests=reqs)

@app.route('/remove_request', methods=['POST'])
def remove_request():
    index = request.form.get('req_id')

    if session.get('is_admin'):
        with db_connect() as db:
            db.execute(
                'DELETE FROM rental_requests WHERE id = ?', (index,)
            )
            db.commit()

        flash("Request removed!", 'info')
        return redirect(url_for('request_list'))
    
    elif session.get('user_id'):
        with db_connect() as db:
            db.execute(
                'DELETE FROM rental_requests WHERE id = ?', (index,)
            )
            db.commit()

        flash("Request removed!", 'info')
        return redirect(url_for('profile'))

@app.route('/update_req_status/<int:req_id>', methods=['POST'])
def update_req_status(req_id):
    if not session.get('is_admin'):
        flash("Access denied!", 'error')
        return redirect(url_for('index'))
    
    new_status = request.form.get('status')
    if new_status not in ('pending', 'rejected', 'approved'):
        flash("Invalid status!", 'error')
        return redirect(url_for('request_list'))
    
    with db_connect() as db:
        db.execute(
            'UPDATE rental_requests SET status = ? WHERE id = ?', (new_status, req_id,)
        )
        db.commit()
    
    flash("Request updated!", 'success')
    return redirect(url_for('request_list'))

@app.route('/search')
def search():
    vehicle_type = request.args.get('type', '')
    table        = TYPE_TO_TABLE.get(vehicle_type)
    results      = []

    if table:
        conditions = []
        params     = []

        # Filtri comuni a tutti i veicoli
        price_min = request.args.get('price_min')
        price_max = request.args.get('price_max')
        if price_min:
            conditions.append('price >= ?')
            params.append(price_min)
        if price_max:
            conditions.append('price <= ?')
            params.append(price_max)

        # Filtri per durata in giorni
        day_min = request.args.get('day_min')
        day_max = request.args.get('day_max')
        if day_min:
            conditions.append('rent_length >= ?')
            params.append(day_min)
        if day_max:
            conditions.append('rent_length <= ?')
            params.append(day_max)

        # Filtri per durata in mesi
        month_min = request.args.get('month_min')
        month_max = request.args.get('month_max')
        if month_min:
            conditions.append('rent_length >= ?')
            params.append(month_min)
        if month_max:
            conditions.append('rent_length <= ?')
            params.append(month_max)

        # Filtri per potenza (se applicabile)
        if vehicle_type in ('car', 'supercar', 'scooter', 'motorcycle'): 
            power_min = request.args.get('power_min')
            power_max = request.args.get('power_max')
            if power_min:
                conditions.append('power >= ?')
                params.append(power_min)
            if power_max:
                conditions.append('power <= ?')
                params.append(power_max)

        # Filtri specifici per tipo
        if vehicle_type == 'car':
            for field in ('brand', 'fuel', 'transmission', 'traction', 'color', 'number_of_seats'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)

        elif vehicle_type == 'supercar':
            for field in ('brand', 'fuel', 'transmission', 'traction', 'color', 'number_of_seats', 'inside_color', 'inside_material'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)

        elif vehicle_type == 'bike':
            for field in ('brand', 'frame_size', 'traction', 'suspensions', 'terrain'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)
            specific_type = request.args.get('specific_type')
            if specific_type:
                conditions.append('type = ?')
                params.append(specific_type)

        elif vehicle_type == 'scooter':
            for field in ('brand', 'engine', 'fuel', 'color', 'required_license', 'number_of_seats'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)

        elif vehicle_type == 'motorcycle':
            for field in ('brand', 'style', 'engine', 'fuel', 'color', 'required_license', 'number_of_seats'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)

        elif vehicle_type == 'camper':
            for field in ('brand', 'fuel', 'sleeping_beds', 'approved_seats', 'type_bathroom'):
                val = request.args.get(field)
                if val:
                    conditions.append(f'{field} = ?')
                    params.append(val)
            specific_type = request.args.get('specific_type')
            if specific_type:
                conditions.append('type = ?')
                params.append(specific_type)

        where = 'WHERE ' + ' AND '.join(conditions) if conditions else ''

        with db_connect() as db:
            results = db.execute(
                f'SELECT * FROM {table} {where}', params
            ).fetchall()

        # Converti in lista di dict e aggiungi img_url
        results_list = []
        for r in results:
            v = dict(r)
            if v.get('img'):
                v['img_url'] = f"imgs/{table}/{v['id']}/{v['img']}"
            else:
                v['img_url'] = None
            results_list.append(v)
        results = results_list

    return render_template('search.html',
                           results=results,
                           vehicle_type=vehicle_type,
                           args=request.args)

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        flash("You have to login first!", 'error')
        return redirect(url_for('login'))
    
    with db_connect() as db:
        requests = db.execute(
            'SELECT * FROM rental_requests WHERE user_id = ? ORDER BY id DESC', (session['user_id'],)
        ).fetchall()

    with db_connect() as db:
        user_data = db.execute(
            'SELECT id, name, email FROM users WHERE id = ? ', (session['user_id'],)
        ).fetchone()

        user_email = dict(user_data)['email'] if user_data else "Email not found"

    return render_template("profile.html", requests=requests, user_email = user_email)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/privacy_policy')
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/terms_conditions')
def terms_conditions():
    return render_template("terms_conditions.html")

@app.route('/social_redirect')
def social_redirect():
    flash("Work in progress! Our social media channels will be available soon.", "info")
    return redirect(request.referrer or url_for('index'))

@app.route('/vehicle/<vehicle_type>/<int:vehicle_id>')
def vehicle_detail(vehicle_type, vehicle_id):
    table = TYPE_TO_TABLE.get(vehicle_type)

    if not table:
        flash("Tipo di veicolo non trovato.", "error")
        return redirect(url_for('search'))

    with db_connect() as db:
        vehicle = db.execute(
            f'SELECT * FROM {table} WHERE id = ?', (vehicle_id,)
        ).fetchone()

    if not vehicle:
        flash("Veicolo non trovato.", "error")
        return redirect(url_for('search'))

    # Converti in dizionario per poter aggiungere l'URL dell'immagine se serve
    v_dict = dict(vehicle)
    if v_dict.get('img'):
        v_dict['img_url'] = f"imgs/{table}/{v_dict['id']}/{v_dict['img']}"
    else:
        v_dict['img_url'] = None

    return render_template('vehicle.html', vehicle=v_dict, vehicle_type=vehicle_type)


@app.route('/rent/<vehicle_type>/<int:vehicle_id>', methods=['GET', 'POST'])
def rent(vehicle_type, vehicle_id):
    if session.get('is_admin'):
        flash("You are the Admin!!", 'error')
        return redirect(url_for('request_list'))

    if not session.get('user_id'):
        flash("You have to login first!", 'error')
        return redirect(url_for('login'))
    
    table = TYPE_TO_TABLE.get(vehicle_type)
    if not table:
        flash("Invalid vehicle type!", 'error')
        return redirect(url_for('index'))
    
    with db_connect() as db:
        vehicle = db.execute(
            f'SELECT * FROM {table} WHERE id = ?', (vehicle_id,)
            ).fetchone()
    
    if not vehicle:
        flash("Vehicle not found!", 'error')
        return redirect(url_for('index'))
    
    with db_connect() as db:
        already_exists = db.execute(
            'SELECT * FROM rental_requests WHERE user_id = ? AND vehicle_type = ? AND vehicle_id = ? AND (status = "pending" OR status = "approved")', (session['user_id'], vehicle_type, vehicle_id,)
        ).fetchone()

    if already_exists:
        flash("Request already sent!", 'error')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()
        message = request.form.get('message', '').strip()
        
        if not phone or not start_date or not end_date:
            flash("Please, instert all data!", 'error')
            return redirect(url_for('rent', vehicle_type=vehicle_type, vehicle_id=vehicle_id))
        
        if start_date > end_date:
            flash("Please, date not allowed", 'error')
            return redirect(url_for('rent', vehicle_type=vehicle_type, vehicle_id=vehicle_id))
        
        with db_connect() as db:
            db.execute(
                'INSERT INTO rental_requests (user_id, user_name, user_email, user_phone, vehicle_type, vehicle_id, vehicle_brand, start_date, end_date, message, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (
                    session['user_id'],
                    session['user_name'],
                    email,
                    phone,
                    vehicle_type,
                    vehicle_id,
                    vehicle['brand'],
                    start_date,
                    end_date,
                    message,
                    'pending'
                )
            )
            db.commit()
        
        flash("Rental request sent!", 'success')
        return redirect(url_for('profile'))
    
    return render_template('rent.html', vehicle=dict(vehicle), vehicle_type=vehicle_type)

# -------------------------------


if __name__ == '__main__':
    db_init()
    app.run(debug=True, port=1234)
