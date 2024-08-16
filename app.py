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
    if database_user:
        return database_user
    return None

def retrieve_all_users():
    cursor.execute("SELECT * FROM general_user")
    database_users = cursor.fetchall()
    if database_users:
        return database_users
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
    if database_user:
        return False
    cursor.execute("SELECT ssn FROM general_user WHERE ssn=%s", (user.ssn,))
    ssn = cursor.fetchone()
    if ssn:
        return False
    cursor.execute("INSERT INTO general_user (id, fname, lname, email, password, birthdate, phone, gender, address, ssn) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user.id, user.first_name, user.last_name, user.email, user.password, user.birthdate, user.phone, user.gender, user.address, user.ssn))
    database_session.commit()
    return True

def insert_item(item):
    cursor.execute("SELECT id FROM item WHERE id=%s", (item.id,))
    database_item = cursor.fetchone()
    if database_item:
        return False
    cursor.execute("INSERT INTO item (id, name, type, description, quantity, price, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (item.id, item.name, item.type, item.description, item.quantity, item.price, item.user_id))
    database_session.commit()
    return True

def update_item(item):
    cursor.execute("SELECT id FROM item WHERE id=%s", (item.id,))
    database_item = cursor.fetchone()
    if not database_item:
        return False
    cursor.execute("UPDATE item SET name=%s, type=%s, description=%s, quantity=%s, price=%s, user_id=%s WHERE id=%s",
                   (item.name, item.type, item.description, item.quantity, item.price, item.user_id, item.id))
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
                all_users = retrieve_all_users()
                employees_ids = [user.get('id') for user in all_users if not user.get('admin_role')]
                return render_template('admin.html', user_dict = user, items = items, employees_ids = employees_ids)
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

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('addItemName')
    itype = request.form.get('addItemType')
    description = request.form.get('addItemDescription')
    quantity = request.form.get('addItemQuantity')
    price = request.form.get('addItemPrice')
    employee_id = request.form.get('addItemEmployeeId')
    cursor.execute("SELECT id FROM item")
    ids = cursor.fetchall()
    if itype == "Electrical":
        new_item = ElectricalPart(len(ids) + 1, name, description, quantity, price, employee_id)
    elif itype == "Mechanical":
        new_item = MechanicalPart(len(ids) + 1, name, description, quantity, price, employee_id)
    else:
        new_item = RawMaterial(len(ids) + 1, name, description, quantity, price, employee_id)
    all_users = retrieve_all_users()
    employees_ids = [user.get('id') for user in all_users if not user.get('admin_role')]
    item_flag = insert_item(new_item)
    if item_flag:
        return render_template("admin.html", add_message="Item added successfully.", message_class="success-message",
                                user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)
    return render_template("admin.html", add_message="Failed to add item. Please try again.", message_class="error-message", 
                           user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)    

@app.route('/edit_item', methods=['POST'])
def edit_item():
    item_id = request.form.get('editItemId')
    name = request.form.get('editItemName')
    itype = request.form.get('editItemType')
    description = request.form.get('editItemDescription')
    quantity = request.form.get('editItemQuantity')
    price = request.form.get('editItemPrice')
    employee_id = request.form.get('editItemEmployeeId')
    if itype == "Electrical":
        edited_item = ElectricalPart(item_id, name, description, quantity, price, employee_id)
    elif itype == "Mechanical":
        edited_item = MechanicalPart(item_id, name, description, quantity, price, employee_id)
    else:
        edited_item = RawMaterial(item_id, name, description, quantity, price, employee_id)
    item_flag = update_item(edited_item)
    all_users = retrieve_all_users()
    if item_flag:
        employees_ids = [user.get('id') for user in all_users if not user.get('admin_role')]
        return render_template("admin.html", edit_message="Item edited successfully.", message_class="success-message",
                               user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)
    employees_ids = [user.get('id') for user in all_users if not user.get('admin_role')]
    return render_template("admin.html", edit_message="Failed to edit the item, Please try again", message_class="error-message",
                           user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)

if __name__ == '__main__':
    app.run()
