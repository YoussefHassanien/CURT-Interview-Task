from flask import Flask, render_template, request, redirect, session
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

def retrieve_user(email, password):
    cursor.execute("SELECT * FROM general_user WHERE email=%s AND password=%s", (email, password))
    database_user = cursor.fetchone()
    if database_user:
        return database_user
    return None

def retrieve_items(id):
    cursor.execute("SELECT admin_role FROM general_user WHERE id=%s", (id,))
    admin_role = cursor.fetchone()
    if admin_role.get('admin_role'):
        cursor.execute("SELECT * FROM item")
    else:
        cursor.execute("SELECT * FROM item WHERE user_id=%s", (id,))
    database_items = cursor.fetchall()
    if database_items:
        return database_items
    return None

@app.route('/', methods=['GET'])
def default():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = retrieve_user(email, password)
    if user:
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

@app.route('/home', methods=['POST'])
def home():
    return render_template("home.html", user=session.get('user'))

@app.route('/admin', methods=['POST'])
def admin():
    return render_template("admin.html", user=session.get('user'))


if __name__ == '__main__':
    app.run()
