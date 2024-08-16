from flask import Flask, render_template, request, session
import psycopg2.extras
from classes import User, ElectricalPart, MechanicalPart, RawMaterial
import hashlib

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


def verify_password(password, hashed_password):
    h = hashlib.sha256()
    h.update(password.encode())
    return h.hexdigest() == hashed_password


def new_id(table_name):
    cursor.execute(f"SELECT id FROM {table_name}")
    ids = cursor.fetchall()
    ids = [row['id'] for row in ids]
    ids.sort()
    new_id = 1
    for id in ids:
        if id == new_id:
            new_id += 1
        else:
            break
    return new_id    

def retrieve_user(email):
    cursor.execute("SELECT * FROM general_user WHERE email=%s", (email,))
    database_user = cursor.fetchone()
    if database_user:
        return database_user
    return None

def retrieve_all_users_ids():
    cursor.execute("SELECT * FROM general_user")
    database_users = cursor.fetchall()
    if database_users:
        users_ids =  [user.get('id') for user in database_users if not user.get('admin_role')]
        return users_ids
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
        if verify_password(password, user.get('password')):
            items = retrieve_items(user.get('id'))
            session['user'] = user
            if user.get('admin_role'):
                employees_ids = retrieve_all_users_ids()
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
    id = new_id('general_user')
    h = hashlib.sha256()
    h.update(password.encode())
    password = h.hexdigest()
    new_user = User(id, fname, lname, email, phone, address, birthdate, gender, ssn, password=password)                         
    account_flag = insert_user(new_user)
    if account_flag:
        return render_template("register.html", message_class="success-message", message="Account created successfully.")
    return render_template("register.html", message="Failed to create account. Please try again.", message_class="error-message")

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('addItemName')
    type = request.form.get('addItemType')
    description = request.form.get('addItemDescription')
    quantity = request.form.get('addItemQuantity')
    price = request.form.get('addItemPrice')
    employee_id = request.form.get('addItemEmployeeId')
    id = new_id('item')
    if type == "Electrical":
        new_item = ElectricalPart(id, name, description, quantity, price, employee_id)
    elif type == "Mechanical":
        new_item = MechanicalPart(id, name, description, quantity, price, employee_id)
    else:
        new_item = RawMaterial(id, name, description, quantity, price, employee_id)
    employees_ids = retrieve_all_users_ids()
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
    type = request.form.get('editItemType')
    description = request.form.get('editItemDescription')
    quantity = request.form.get('editItemQuantity')
    price = request.form.get('editItemPrice')
    employee_id = request.form.get('editItemEmployeeId')
    if type == "Electrical":
        edited_item = ElectricalPart(item_id, name, description, quantity, price, employee_id)
    elif type == "Mechanical":
        edited_item = MechanicalPart(item_id, name, description, quantity, price, employee_id)
    else:
        edited_item = RawMaterial(item_id, name, description, quantity, price, employee_id)
    item_flag = update_item(edited_item)
    employees_ids = retrieve_all_users_ids()
    if item_flag:
        return render_template("admin.html", edit_message="Item edited successfully.", message_class="success-message",
                               user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)
    return render_template("admin.html", edit_message="Failed to edit the item, Please try again", message_class="error-message",
                           user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    cursor.execute("SELECT COUNT(*) FROM item")
    total_items_before_delete = cursor.fetchone()[0]
    item_id = request.form.get('deletedItemId')
    cursor.execute("DELETE FROM item WHERE id=%s", (item_id,))
    database_session.commit()
    cursor.execute("SELECT COUNT(*) FROM item")
    total_items_after_delete = cursor.fetchone()[0]
    employees_ids = retrieve_all_users_ids()
    if total_items_before_delete <= total_items_after_delete:
        return render_template("admin.html", delete_message="Failed to delete item. Please try again.", message_class="error-message",
                               user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)
    return render_template("admin.html", delete_message="Item deleted successfully.", message_class="success-message",
                           user_list = session['user'], items = retrieve_items(session['user'][0]), employees_ids = employees_ids)

if __name__ == '__main__':
    app.run()
