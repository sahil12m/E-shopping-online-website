from flask import (
    Flask,
    render_template,
    flash,
    redirect,
    url_for,
    session,
    request,
    logging,
)
from flask_mysqldb import MySQL
from wtforms import (
    Form,
    StringField,
    TextAreaField,
    PasswordField,
    validators,
    SelectField,
)
from functools import wraps
from flask_uploads import UploadSet, configure_uploads, IMAGES
import timeit
import datetime
from flask_mail import Mail, Message
import os
from wtforms.fields.html5 import EmailField

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOADED_PHOTOS_DEST"] = "static/image/product"
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

# Config MySQL
mysql = MySQL()
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "mysql"
app.config["MYSQL_DB"] = "proton_hub_database"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Initialize the app for use with this MySQL class
mysql.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for("login"))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return redirect(url_for("index"))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "admin_logged_in" in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for("admin_login"))

    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "admin_logged_in" in session:
            return redirect(url_for("admin"))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


@app.route("/")
def index():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = "laptop"
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,)
    )
    laptop = cur.fetchall()
    values = "mobile"
    cur.execute(
        "SELECT * FROM products WHERE category=%s ORDER BY RAND() LIMIT 4", (values,)
    )
    mobile = cur.fetchall()
    cur.close()
    return render_template("home.html", laptop=laptop, mobile=mobile, form=form)


class LoginForm(Form):  # Create Login Form
    username = StringField(
        "",
        [validators.length(min=1)],
        render_kw={"autofocus": True, "placeholder": "Username"},
    )
    password = PasswordField(
        "", [validators.length(min=3)], render_kw={"placeholder": "Password"}
    )


# User Login
@app.route("/login", methods=["GET", "POST"])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM login WHERE username=%s", [username])
        # result  = cur.execute("select login_check(%s,%s)",(username,password_candidate))
        print(result)

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            dat_id = cur.execute(
                "SELECT id FROM user_details WHERE username=%s", [username]
            )
            dat_id = cur.fetchone()
            password = data["password"]
            uid = dat_id["id"]
            data_name = cur.execute("SELECT name FROM user_name WHERE id=%s", [uid])
            data_name = cur.fetchone()
            name = data_name["name"]

            # Compare password
            # if result == 1:
            if password == password_candidate:
                # passed
                session["logged_in"] = True
                session["uid"] = uid
                session["s_name"] = name

                # x = '1'
                # cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))

                return redirect(url_for("index"))

            else:
                flash("Incorrect password", "danger")
                return render_template("login.html", form=form)

        else:
            flash("Username not found", "danger")
            # Close connection
            cur.close()
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@app.route("/out")
def logout():
    if "uid" in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session["uid"]
        # x = '0'
        # cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash("You are logged out", "success")
        return redirect(url_for("index"))
    return redirect(url_for("login"))


class RegisterForm(Form):
    name = StringField(
        "",
        [validators.length(min=3, max=50)],
        render_kw={"autofocus": True, "placeholder": "Full Name"},
    )
    username = StringField(
        "", [validators.length(min=3, max=25)], render_kw={"placeholder": "Username"}
    )
    email = EmailField(
        "",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.length(min=4, max=25),
        ],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "", [validators.length(min=3)], render_kw={"placeholder": "Password"}
    )
    mobile = StringField(
        "",
        [validators.length(min=10, max=13)],
        render_kw={"placeholder": "Mobile Number"},
    )
    zip_code = StringField(
        "", [validators.length(min=6, max=6)], render_kw={"placeholder": "Zip Code"}
    )
    city = StringField(
        "", [validators.length(min=3, max=50)], render_kw={"placeholder": "City"}
    )


@app.route("/register", methods=["GET", "POST"])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = str(form.password.data)
        mobile = form.mobile.data
        user_zip = form.zip_code.data
        user_city = form.city.data

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_name(name) VALUES(%s)", [name])
        cur.execute("INSERT INTO zip VALUES(%s, %s)", (user_zip, user_city))
        cur.execute("INSERT INTO login VALUES(%s, %s)", (username, password))
        cur.execute(
            "INSERT INTO user_details(email, username, mobile, user_zip) VALUES(%s, %s, %s, %s)",
            (email, username, mobile, user_zip),
        )

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()
        flash("You are now registered and can login", "success")

        return redirect(url_for("index"))
    return render_template("register.html", form=form)


class MessageForm(Form):  # Create Message Form
    body = StringField("", [validators.length(min=1)], render_kw={"autofocus": True})


class OrderForm(Form):  # Create Order Form
    name = StringField(
        "",
        [validators.length(min=1), validators.DataRequired()],
        render_kw={"autofocus": True, "placeholder": "Full Name"},
    )
    mobile_num = StringField(
        "",
        [validators.length(min=1), validators.DataRequired()],
        render_kw={"autofocus": True, "placeholder": "Mobile Number"},
    )
    quantity = SelectField(
        "",
        [validators.DataRequired()],
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
    )
    order_place = StringField(
        "",
        [validators.length(min=1), validators.DataRequired()],
        render_kw={"placeholder": "Order Place"},
    )


@app.route("/laptop", methods=["GET", "POST"])
def laptop():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = "laptop"
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == "POST" and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args["order"]
        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if "uid" in session:
            uid = session["uid"]
            curs.execute(
                "INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (uid, pid, name, mobile, order_place, quantity, now_time),
            )
        else:
            curs.execute(
                "INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                "VALUES(%s, %s, %s, %s, %s, %s)",
                (pid, name, mobile, order_place, quantity, now_time),
            )
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash("Order successful", "success")
        return render_template("laptop.html", laptop=products, form=form)
    if "view" in request.args:
        product_id = request.args["view"]
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        if "uid" in session:
            uid = session["uid"]
            # Create cursor
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM product_view WHERE user_id=%s AND product_id=%s",
                (uid, product_id),
            )
            result = cur.fetchall()
            if result:
                now = datetime.datetime.now()
                now_time = now.strftime("%y-%m-%d %H:%M:%S")
                cur.execute(
                    "UPDATE product_view SET date=%s WHERE user_id=%s AND product_id=%s",
                    (now_time, uid, product_id),
                )
            else:
                cur.execute(
                    "INSERT INTO product_view(user_id, product_id) VALUES(%s, %s)",
                    (uid, product_id),
                )
                mysql.connection.commit()
        return render_template("view_product.html", laptops=product)
    elif "order" in request.args:
        product_id = request.args["order"]
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        return render_template("order_product.html", laptops=product, form=form)
    return render_template("laptop.html", laptop=products, form=form)


@app.route("/mobile", methods=["GET", "POST"])
def mobile():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = "mobile"
    cur.execute("SELECT * FROM products WHERE category=%s ORDER BY id ASC", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()

    if request.method == "POST" and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        pid = request.args["order"]

        now = datetime.datetime.now()
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if "uid" in session:
            uid = session["uid"]
            curs.execute(
                "INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                (uid, pid, name, mobile, order_place, quantity, now_time),
            )
        else:
            curs.execute(
                "INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                "VALUES(%s, %s, %s, %s, %s, %s)",
                (pid, name, mobile, order_place, quantity, now_time),
            )
        # Commit cursor
        mysql.connection.commit()
        # Close Connection
        cur.close()

        flash("Order successful", "success")
        return render_template("mobile.html", mobile=products, form=form)
    if "view" in request.args:
        q = request.args["view"]
        product_id = q
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        products = curso.fetchall()
        return render_template("view_product.html", laptops=products)
    elif "order" in request.args:
        product_id = request.args["order"]
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        return render_template("order_product.html", laptops=product, form=form)
    return render_template("mobile.html", mobile=products, form=form)


@app.route("/admin_login", methods=["GET", "POST"])
@not_admin_logged_in
def admin_login():
    if request.method == "POST":
        # GEt user form
        username = request.form["email"]
        password_candidate = request.form["password"]

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data["password"]
            uid = data["id"]
            name = data["firstName"]

            # Compare password
            if password_candidate == password:
                # passed
                session["admin_logged_in"] = True
                session["admin_uid"] = uid
                session["admin_name"] = name

                return redirect(url_for("admin"))

            else:
                flash("Incorrect password", "danger")
                return render_template("pages/login.html")

        else:
            flash("Username not found", "danger")
            # Close connection
            cur.close()
            return render_template("pages/login.html")
    return render_template("pages/login.html")


@app.route("/admin_out")
def admin_logout():
    if "admin_logged_in" in session:
        session.clear()
        return redirect(url_for("admin_login"))
    return redirect(url_for("admin"))


@app.route("/admin")
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    result = curso.fetchall()
    order_rows = curso.execute("select get_no_order() as ord;")
    order_rows = curso.fetchone()
    order_rows = str(order_rows["ord"])
    users_rows = curso.execute("SELECT * FROM user_details")
    return render_template(
        "pages/index.html",
        result=result,
        row=num_rows,
        order_rows=order_rows,
        users_rows=users_rows,
    )


@app.route("/orders")
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("select get_no_order() as ord;")
    order_rows = curso.fetchone()
    order_rows = str(order_rows["ord"])
    
    curso.execute("SELECT * FROM orders")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM user_details")
    return render_template(
        "pages/all_orders.html",
        result=result,
        row=num_rows,
        order_rows=order_rows,
        users_rows=users_rows,
    )


@app.route("/users")
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("select get_no_order() as ord;")
    order_rows = curso.fetchone()
    order_rows = str(order_rows["ord"])
    
    curso.execute("SELECT * FROM orders")
    users_rows = curso.execute(
        "select * from user_details inner join user_name on user_name.id = user_details.id"
    )
    result = curso.fetchall()
    return render_template(
        "pages/all_users.html",
        result=result,
        row=num_rows,
        order_rows=order_rows,
        users_rows=users_rows,
    )


@app.route("/admin_add_product", methods=["POST", "GET"])
@is_admin_logged_in
def admin_add_product():
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form["price"]
        description = request.form["description"]
        quantity = request.form["qty"]
        category = request.form["category"]
        code = request.form["code"]
        file = request.files["picture"]
        if name and price and description and quantity and category and code and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith((".png", ".jpg", ".jpeg")):
                save_photo = photos.save(file, folder=category)
                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    curs.execute(
                        "INSERT INTO products(pName,price,description,quantity,category,pCode,picture)"
                        "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (name, price, description, quantity, category, code, picture),
                    )
                    mysql.connection.commit()
                    flash("Product added successful", "success")
                    return redirect(url_for("admin_add_product"))
                else:
                    flash("Picture not save", "danger")
                    return redirect(url_for("admin_add_product"))
            else:
                flash("File not supported", "danger")
                return redirect(url_for("admin_add_product"))
        else:
            flash("Please fill up all form", "danger")
            return redirect(url_for("admin_add_product"))
    else:
        return render_template("pages/add_product.html")


@app.route("/edit_product", methods=["POST", "GET"])
@is_admin_logged_in
def edit_product():
    if "id" in request.args:
        product_id = request.args["id"]
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM products WHERE id=%s", (product_id,))
        product = curso.fetchall()
        if res:
            if request.method == "POST":
                name = request.form.get("name")
                price = request.form["price"]
                description = request.form["description"]
                quantity = request.form["qty"]
                category = request.form["category"]
                code = request.form["code"]
                file = request.files["picture"]
                # Create Cursor
                if (
                    name
                    and price
                    and description
                    and quantity
                    and category
                    and code
                    and file
                ):
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith((".png", ".jpg", ".jpeg")):
                        file.filename = picture
                        save_photo = photos.save(file, folder=category)
                        if save_photo:
                            # Create Cursor
                            # cur = mysql.connection.cursor()
                            exe = curso.execute(
                                "UPDATE products SET pName=%s, price=%s, description=%s, quantity=%s, category=%s, pCode=%s, picture=%s WHERE id=%s",
                                (
                                    name,
                                    price,
                                    description,
                                    quantity,
                                    category,
                                    code,
                                    picture,
                                    product_id,
                                ),
                            )

                            print(exe)
                            if exe:
                                mysql.connection.commit()
                                curso.close()
                                flash("Data updated", "success")
                                return redirect(url_for("edit_product"))
                            else:
                                flash("Error", "danger")
                                return redirect(url_for("pages/edit_product.html"))
                        else:
                            flash("Pic not upload", "danger")
                            return render_template(
                                "pages/edit_product.html", product=product
                            )
                    else:
                        flash("File not support", "danger")
                        return render_template(
                            "pages/edit_product.html", product=product
                        )
                else:
                    flash("Fill all field", "danger")
                    return render_template("pages/edit_product.html", product=product)
            else:
                return render_template("pages/edit_product.html", product=product)
        else:
            return redirect(url_for("admin_login"))
    else:
        return redirect(url_for("admin_login"))


@app.route("/search", methods=["POST", "GET"])
def search():
    form = OrderForm(request.form)
    if "q" in request.args:
        q = request.args["q"]
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM products WHERE pName LIKE %s ORDER BY id ASC"
        exe = cur.execute(query_string, ("%" + q + "%",))
        products = cur.fetchall()
        # Close Connection
        cur.close()
        if exe:
            flash("Showing result for: " + q, "success")
            return render_template("search.html", products=products, form=form)
        else:
            flash("Product not found.. please search again", "danger")
            return render_template("search.html")

    else:
        flash("Search again", "danger")
        return render_template("search.html")


@app.route("/profile")
@is_logged_in
def profile():
    if "user" in request.args:
        q = request.args["user"]
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM user_details WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result["id"] == session["uid"]:
                
                curso.execute("select orders.*,products.pName from orders inner join products on orders.pid = products.id where uid=%s order by odate desc",(session["uid"],),
                )
                res = curso.fetchall()
                return render_template("profile.html", result=res)
            else:
                flash("Unauthorised", "danger")
                return redirect(url_for("login"))
        else:
            flash("Unauthorised! Please login", "danger")
            return redirect(url_for("login"))
    else:
        flash("Unauthorised", "danger")
        return redirect(url_for("login"))


class UpdateRegisterForm(Form):
    name = StringField(
        "Full Name",
        [validators.length(min=3, max=50)],
        render_kw={"autofocus": True, "placeholder": "Full Name"},
    )
    email = EmailField(
        "Email",
        [
            validators.DataRequired(),
            validators.Email(),
            validators.length(min=4, max=25),
        ],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        "Password", [validators.length(min=3)], render_kw={"placeholder": "Password"}
    )
    mobile = StringField(
        "Mobile",
        [validators.length(min=10, max=13)],
        render_kw={"placeholder": "Mobile"},
    )


@app.route("/settings", methods=["POST", "GET"])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if "user" in request.args:
        q = request.args["user"]
        curso = mysql.connection.cursor()
        curso.execute(
            "select * from user_details inner join user_name on user_name.id = user_details.id where user_Details.id =%s",
            (q,),
        )
        result = curso.fetchone()
        if result:
            if result["id"] == session["uid"]:
                if request.method == "POST" and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = str(form.password.data)
                    mobile = form.mobile.data

                    # Create Cursor
                    cur = mysql.connection.cursor()

                    data_uname = cur.execute(
                        "select username from user_details where id = %s", [q]
                    )
                    data_uname = cur.fetchone()

                    exe = cur.execute(
                        "UPDATE login SET password  =%s WHERE username=%s",
                        (password, data_uname["username"]),
                    )

                    # print(exe)

                    exe = cur.execute(
                        "UPDATE user_details SET  email=%s, mobile=%s WHERE id=%s",
                        (email, mobile, q),
                    )
                    # print(exe)

                    exe = cur.execute(
                        "UPDATE user_name SET name=%s WHERE id=%s", (name, q)
                    )
                    # print(exe)

                    print("id", q)

                    mysql.connection.commit()
                    if exe:
                        flash("Profile updated", "success")
                        session["s_name"] = name
                        return render_template(
                            "user_settings.html", result=result, form=form
                        )
                    else:
                        flash("Profile not updated", "danger")
                return render_template("user_settings.html", result=result, form=form)
            else:
                flash("Unauthorised", "danger")
                return redirect(url_for("login"))
        else:
            flash("Unauthorised! Please login", "danger")
            return redirect(url_for("login"))
    else:
        flash("Unauthorised", "danger")
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
