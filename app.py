from flask import Flask, render_template, request, session
import psycopg2.extras
from classes import User, Admin, Item, ElectricalPart, MechanicalPart, RawMaterial

app = Flask(__name__)
app.secret_key = "Youssef.8.3"

database_session = psycopg2.connect(
     database="postgres",
     port=5432,
     host="localhost",
     user="postgres",
     password="Youssef.8.3"
)
database_session.autocommit = True
cursor = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)

def retrieve_user(email):
    cursor.execute("SELECT * FROM general_user WHERE email=%s", (email,))
    database_user = cursor.fetchone()
    print(f" Retrieve user function database user : {database_user}")
    if database_user:
        return database_user
    return None

def retrieve_items(id):
    cursor.execute("SELECT admin_role FROM general_user WHERE id=%s", (id,))
    admin_role = cursor.fetchone()
    if admin_role and admin_role.get('admin_role'):
        cursor.execute("SELECT * FROM item")
    else:
        cursor.execute("SELECT * FROM item WHERE user_id=%s", (id,))
    database_items = cursor.fetchall()
    if database_items:
        return database_items
    return None

def insert_user(user):
    database_user = retrieve_user(user.email)
    print(f" Insert user function database user : {database_user}")
    if database_user:
        return False
    cursor.execute("SELECT ssn FROM general_user WHERE ssn=%s", (user.ssn,))
    ssn = cursor.fetchone()
    print(f" Insert user function database ssn : {ssn}")
    if ssn:
        return False
    cursor.execute("INSERT INTO general_user (id, fname, lname, email, password, birthdate, phone, gender, address, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user.id, user.first_name, user.last_name, user.email, user.password, user.birthdate, user.phone, user.gender, user.address, user.ssn))
    database_session.commit()
    return True


@app.route('/', methods=['GET'])
def default():
    return render_template("login.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')
    user = retrieve_user(email)
    if user:
        if user.get('password') == password:
            items = retrieve_items(user.get('id'))
            session['user'] = user
            if user.get('admin_role'):
                return render_template('admin.html', user = user, items = items)
            return render_template('/home.html', user = user, items = items)
    session.pop('user', None)
    error_message = "Invalid email or password. Please try again."
    return render_template("login.html", error=error_message)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return render_template("login.html")

@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_user():
    email = request.form.get('email')
    if email.find('@') <= 0 or email.find('.') <= 0:
        return render_template("register.html", message="Invalid email. Please try again.", message_class="error-message")
    password = request.form.get('password')
    fname = request.form.get('f-name')
    lname = request.form.get('l-name')
    birthdate = request.form.get('birthdate')
    phone = request.form.get('phone')
    address = request.form.get('address')
    ssn = request.form.get('ssn')
    if len(ssn) != 14:
        return render_template("register.html", message="Invalid SSN. Please try again.", message_class="error-message")
    gender = request.form.get('gender')
    cursor.execute("SELECT id FROM general_user")
    ids = cursor.fetchall()
    new_user = User(len(ids) + 1, fname, lname, email, phone, address, birthdate, gender, ssn, password=password)                         
    account_flag = insert_user(new_user)
    if account_flag:
        return render_template("register.html", message_class="success-message", message="Account created successfully.")
    return render_template("register.html", message="Failed to create account. Please try again.", message_class="error-message")


if __name__ == '__main__':
    app.run()
