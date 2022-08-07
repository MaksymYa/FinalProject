from ast import operator
from re import S
from flask_session import Session
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_create, db_insert, db_select, db_delete, db_update
from start_table import start_table
from helpers import login_required, usd
from datetime import datetime


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

start_table()

@app.route('/')
@login_required
def index():
    
    return render_template("index.html")

@app.route('/home')
def index2():
    return "Hello, Worsld2!"

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    error = 0

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        
        # Ensure username was submitted
        if not username:
            error = 1
            data = 'empty login or password'
            return render_template("login.html", error=error, text=data)


        # Ensure password was submitted
        elif not password:
                error = 1
                data = 'empty login or password'
                return render_template("login.html", error=error, text=data)

        # Query database for username
       
        value = "SELECT * FROM users WHERE login = %s"
        param = [username]
        result = db_select(value, param)
        rows = result.fetchone()

        # Query database for salart
       
        value_user = "SELECT * FROM users INNER JOIN salary ON users.id=salary.id_user WHERE users.id = %s"
        param_user = [rows[0]]
        print(param_user)
        operator = db_select(value_user, param_user)
        salary = operator.fetchone()

        # Ensure username exists and password is correct
        if result == None or not check_password_hash(rows[4], password):
            error = 1
            text = "incorrect login or password"
            return render_template("login.html", error=error, text=text)

        # Remember which user has logged in
        session["user_id"] = rows[0]
        session["role_id"] = rows[5]
        session["first_name"] = rows[1]
        try:
            session["salary"] = salary[8]
        except: session["salary"] = 0
        #print(session.get("user_id"))

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        error = 0
        return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")

@app.route("/users")
@login_required
def users():
    if session["role_id"] != 1:
        return redirect('/')
    """Show users table"""
    value = "SELECT * FROM users INNER JOIN role ON users.id_role=role.id"
    param = []
    users = db_select(value, param)
    return render_template("users.html", users=users)

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    page = request.form.get("page")
    if id:
        value = "DELETE FROM " + page + " WHERE id = %s"
        print(value)
        param = [id]
        db_delete(value, param)
    return redirect('/'+ page)

@app.route("/register", methods=["GET", "POST"])
def register():
    if session["role_id"] != 1:
        return redirect('/')
    """Register user"""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        login = request.form.get("login")
        value_role = "SELECT id FROM role WHERE role = %s" 
        param_role = [request.form.get("role")]
        rows = db_select(value_role, param_role)
        role = rows.fetchone()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        value = "SELECT * FROM users WHERE login = %s"
        param = [login]
        result = db_select(value, param)
        rows = result.fetchone()

        if login == '' or result.rowcount > 0:
            error = 1
            data = 'empty or busy login'
            return render_template("register.html", error=error, text=data)
        elif password == '' or confirmation == '' or password != confirmation:
             error = 1
             data = 'check password!'
             return render_template("register.html", error=error, text=data)
        else:
            hash = generate_password_hash(password)
            value = "INSERT INTO users (first_name, last_name, login, password, id_role) VALUES (%s, %s, %s, %s, %s)" 
            param = [first_name, last_name, login, hash, role]
            db_insert(value, param)

            id_user = db_select("SELECT id FROM users WHERE login = %s", login).fetchone()
            value_salary = "INSERT INTO salary (id_user, salary) VALUES (%s, %s)" 
            param_salary = [id_user, 0]
            db_insert(value_salary, param_salary)
            return redirect("/users")

    value = "SELECT role FROM role" 
    param = []
    roles = db_select(value, param)
    return render_template("register.html", roles=roles)

@app.route("/customers")
@login_required
def customer():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Show customer table"""
    value = "SELECT * FROM customers"
    param = []
    customers = db_select(value, param)
    return render_template("customers.html", customers=customers)

@app.route("/cp_add", methods=["GET", "POST"])
@login_required
def cu_add():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Add customer"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")

        if name == '' or email == '' or country == '':
            error = 1
            data = 'check fields'
            return render_template("cu_add.html", error=error, text=data)
        else:
            value = "INSERT INTO customer (name, email, country) VALUES (%s, %s, %s)" 
            param = [name, email, country]
            db_insert(value, param)
            return redirect("/customer")

    return render_template("cu_add.html")

@app.route("/parts")
@login_required
def parts():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Show parts table"""
    value = "SELECT * FROM parts INNER JOIN customers ON parts.id_customer=customers.id"
    param = []
    parts = db_select(value, param)
    return render_template("parts.html", parts=parts)

@app.route("/part_add", methods=["GET", "POST"])
@login_required
def part_add():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Add part"""
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        cust_id = request.form.get("cust_id")
        value_customer = "SELECT id FROM customers WHERE name = %s" 
        param_customer = [cust_id]
        rows = db_select(value_customer, param_customer)
        customer = rows.fetchone()
        price_fw = request.form.get("price_fw")

        value = "SELECT * FROM parts WHERE name = %s"
        param = [name]
        result = db_select(value, param)
        rows = result.fetchone()

        if name == '' or result.rowcount > 0:
            error = 1
            data = 'empty or busy name'
            return render_template("part_add.html", error=error, text=data)

        if  price == '' or customer == '' or price_fw == '':
            error = 1
            data = 'check fields'
            return render_template("part_add.html", error=error, text=data)
        else:
            value = "INSERT INTO parts (name, price, id_customer, worcker_price) VALUES (%s, %s, %s, %s)" 
            param = [name, price, customer, price_fw]
            db_insert(value, param)
            return redirect("/parts")

    value = "SELECT name FROM customers" 
    param = []
    customers = db_select(value, param)
    return render_template("part_add.html", customers=customers)

@app.route("/orders")
@login_required
def orders():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Show orders table"""
    value = "SELECT * FROM orders INNER JOIN parts ON orders.id_part=parts.id"
    param = []
    orders = db_select(value, param)
    return render_template("orders.html", orders=orders)

@app.route("/order_add", methods=["GET", "POST"])
@login_required
def order_add():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Add order"""
    if request.method == "POST":
        part = request.form.get("part")
        amount = request.form.get("amount")
        reg_data = request.form.get("reg_data")
        ship_data = request.form.get("ship_data")
        value_part = "SELECT id FROM parts WHERE name = %s" 
        param_part = [part]
        rows = db_select(value_part, param_part)
        id_part = rows.fetchone()
        status = request.form.get("status")

        if  part == '' or reg_data == '' or ship_data == '' or status == '' or amount == '':
            error = 1
            data = 'check fields'
            return render_template("order_add.html", error=error, text=data)
        else:
            value_insert = "INSERT INTO orders (id_part, amount, reg_data, shipping_data, status) VALUES (%s, %s, %s, %s, %s)" 
            param = [id_part, amount, reg_data, ship_data, status ]
            db_insert(value_insert, param)

            stage = "workpiece"
            value_amount = 'SELECT stock.amount, stock.id FROM stock INNER JOIN stages ON id_stage=stages.id WHERE stage = ' + '"'+ stage+'"' + ' AND id_part = %s' 
            param = [id_part]
            rows = db_select(value_amount, param)
            amount_in_stock = rows.fetchone()

            value_amount = "SELECT id FROM stages WHERE stage = %s" 
            param = [stage]
            rows = db_select(value_amount, param)
            id_stage =  rows.fetchone()
            if amount_in_stock is None:
                value_am = "INSERT INTO stock (id_part, amount, id_stage) VALUES (%s, %s, %s)" 
                param = [id_part, amount, id_stage]
                db_insert(value_am, param)
            else:
                value = "UPDATE stock SET amount = %s WHERE id = %s" 
                new_amount = amount_in_stock[0] + int(amount)
                param = [new_amount, amount_in_stock[1]]
                db_update(value, param)

            return redirect("/orders")

    value_parts = "SELECT name FROM parts" 
    param = []
    parts = db_select(value_parts, param)
    value_status = "SELECT status FROM statuses" 
    param = []
    statuses = db_select(value_status, param)
    return render_template("order_add.html", parts=parts, statuses=statuses)

@app.route("/statuses")
@login_required
def statuses():
    if session["role_id"] != 1:
        return redirect('/')
    """Show statuses table"""
    value = "SELECT * FROM statuses"
    param = []
    statuses = db_select(value, param)
    return render_template("statuses.html", statuses=statuses)

@app.route("/status_add", methods=["GET", "POST"])
@login_required
def status_add():
    if session["role_id"] != 1:
        return redirect('/')
    """Add status"""
    if request.method == "POST":
        status = request.form.get("status")

        if  status == '':
            error = 1
            data = 'check fields'
            return render_template("status_add.html", error=error, text=data)
        else:
            value = "INSERT INTO statuses (status) VALUES (%s)" 
            param = [status]
            db_insert(value, param)
            return redirect("/statuses")

    return render_template("status_add.html")

@app.route("/shift_tasks")
@login_required
def shift_tasks():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Show shift_tasks table"""
    value = "SELECT * FROM shift_tasks INNER JOIN users ON operator_id=users.id INNER JOIN parts ON shift_tasks.id_part=parts.id"
    param = []
    shift_tasks = db_select(value, param)
    return render_template("shift_tasks.html", shift_tasks=shift_tasks)

@app.route("/shift_task_add", methods=["GET", "POST"])
@login_required
def shift_task_add():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Add shift_task"""
    if request.method == "POST":
        date = request.form.get("date")
        operator_id = request.form.get("operator")
        id_part = request.form.get("part")
        amount_plan = request.form.get("amount_plan")
        
        stage = "workpiece"
        amount_part_in_stock = "SELECT stock.amount FROM stock INNER JOIN stages ON stock.id_stage = stages.id INNER JOIN parts ON stock.id_part = parts.id WHERE stage = %s AND id_part =%s" 
        param_part_in_stock = [stage, id_part]
        rows = db_select(amount_part_in_stock, param_part_in_stock)
        amount = rows.fetchone()
 
        if  date == '' or operator_id == '' or id_part == '' or amount_plan == '' or amount is None:
            error = 1
            data = 'check fields'
            return render_template("shift_task_add.html", error=error, text=data)
        elif int(amount_plan) > amount[0]:
            error = 1
            data = 'Not enough workpieces in stock'
            return render_template("shift_task_add.html", error=error, text=data)
        else:
            value = "INSERT INTO shift_tasks (date, operator_id, id_part, amount_plan) VALUES (%s, %s, %s, %s)" 
            param = [date, operator_id, id_part, amount_plan]
            db_insert(value, param)
            return redirect("/shift_tasks")
    
    value_operator = "SELECT * FROM users WHERE id_role = %s" 
    param = [3]
    operators = db_select(value_operator, param)
    value_part = "SELECT * FROM parts" 
    param = []
    parts = db_select(value_part, param)        
    return render_template("shift_task_add.html", operators=operators, parts=parts)

@app.route("/stock")
@login_required
def stock():
    if session["role_id"] != 1 and session["role_id"] != 2:
        return redirect('/')
    """Show stock table"""
    value = "SELECT * FROM stock INNER JOIN parts ON stock.id_part=parts.id INNER JOIN stages ON stock.id_stage=stages.id"
    param = []
    stock = db_select(value, param)
    return render_template("stock.html", stock=stock)

@app.route("/worcker")
@login_required
def worcker():
    if session["role_id"] != 3:
        return redirect('/')
    """Show worcker window"""
    current_date = datetime.today().strftime("%Y/%m/%d")
    value_task = "SELECT * FROM shift_tasks INNER JOIN parts ON shift_tasks.id_part=parts.id WHERE operator_id = %s AND date = %s AND id_status != %s"
    param_task = [session["user_id"], current_date, 5]
    shift_tasks = db_select(value_task, param_task)

    value_user = "SELECT * FROM users INNER JOIN salary ON users.id=salary.id_user WHERE users.id = %s"
    param_user = [session["user_id"]]
    operator = db_select(value_user, param_user)
    salary = operator.fetchone()
    try:
            session["salary"] = salary[8]
    except: session["salary"] = 0
    return render_template("worcker.html", shift_tasks=shift_tasks, operator=salary)

@app.route("/shift_task_submit", methods=["GET", "POST"])
@login_required
def shift_task_submit():
    """Submit shift_task"""
    current_date = datetime.today().strftime("%Y/%m/%d")
    shift_task_id = request.form.get("id")
    amount_fact = request.form.get("amount_fact")
    row = db_select("SELECT * FROM shift_tasks INNER JOIN parts ON shift_tasks.id_part=parts.id WHERE operator_id = %s AND date = %s AND id_status != %s", [session["user_id"], current_date, 5]).fetchone()
    amount_plan = row[4]
    print(row)
    price_for_worcker = row[9]
    worcker_salary = db_select("SELECT salary FROM salary WHERE id_user = %s", [session["user_id"]]).fetchone()[0]
    id_part = row[3]
    amount_worckpiece_part_in_stock = db_select("SELECT amount FROM stock WHERE id_part = %s AND id_stage = %s", [id_part, 1]).fetchone()
    amount_finish_part_in_stock = db_select("SELECT amount FROM stock WHERE id_part = %s AND id_stage = %s", [id_part, 2]).fetchone()
    
    if  amount_fact == '' or int(amount_fact) > amount_plan:
        print(int(amount_fact))
        print(amount_plan)
        error = 1
        data = 'invalid value'
        return render_template("worcker.html", error=error, text=data)
    else:
        worck_pay = price_for_worcker * float(amount_fact) + worcker_salary
        value = "UPDATE salary SET salary = %s WHERE id_user = %s" 
        param = [worck_pay, session["user_id"]]
        db_update(value, param)

        if amount_finish_part_in_stock is None:
            db_insert("INSERT INTO stock (id_part, amount, id_stage) VALUES (%s, %s, %s)", [id_part, amount_fact, 2])
        else: 
            amount_finish_part_in_stock = amount_finish_part_in_stock[0] + int(amount_fact)
            db_update("UPDATE stock SET amount = %s WHERE id_part = %s AND id_stage = %s", [amount_finish_part_in_stock, id_part, 2])

        amount_w = amount_worckpiece_part_in_stock[0] - int(amount_fact)
        db_update("UPDATE stock SET amount = %s WHERE id_part = %s AND id_stage = %s", [amount_w, id_part, 1])
        db_update("UPDATE shift_tasks SET amount_fact = %s, id_status = %s WHERE id = %s", [amount_fact, 5, shift_task_id])
        row = db_select("SELECT id FROM stock WHERE amount = %s AND id_stage = %s", ['0', '1'])
        zero_stock = row.fetchone()
        print(zero_stock)
        if zero_stock is not None:
            value_del = "DELETE FROM stock WHERE id = %s"
            param_del = [zero_stock[0]]
            db_delete(value_del, param_del)
        
        return redirect("/shift_tasks")     
    
    