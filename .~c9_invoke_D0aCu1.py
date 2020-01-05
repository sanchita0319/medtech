import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

id = 0
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hospitals.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/name", methods=["GET", "POST"])
@login_required
def name():
    if request.method == "GET":
        return render_template("name.html")
    else:
        name = request.form.get("name")
        if (len(db.execute("SELECT name from HOSPITALS WHERE name=?", name)) != 0):
            return apology("A hospital with this name already exists. Profile could not be updated")
        else:
            db.execute("UPDATE hospitals SET name=? WHERE id=?", name, session["user_id"])
            return redirect("/me")


@app.route("/street", methods=["GET", "POST"])
@login_required
def street():
    if request.method == "GET":
        return render_template("street.html")
    else:
        street = request.form.get("street")
        db.execute("UPDATE hospitals SET street=? WHERE id=?", street, session["user_id"])
        return redirect("/me")


@app.route("/city", methods=["GET", "POST"])
@login_required
def city():
    if request.method == "GET":
        return render_template("city.html")
    else:
        city = request.form.get("city")
        db.execute("UPDATE hospitals SET city=? WHERE id=?", city, session["user_id"])
        return redirect("/me")


@app.route("/website", methods=["GET", "POST"])
@login_required
def website():
    if request.method == "GET":
        return render_template("website.html")
    else:
        street = request.form.get("street")
        db.execute("UPDATE hospitals SET website=? WHERE id=?", website, session["user_id"])
        return redirect("/me")


@app.route("/areas_of_specialization", methods=["GET", "POST"])
@login_required
def areas():
    if request.method == "GET":
        return render_template("areas_of_specialization.html")
    else:
        areas = request.form.get("areas")
        db.execute("UPDATE hospitals SET areas=? WHERE id=?", areas, session["user_id"])
        return redirect("/me")


@app.route("/type_of_control", methods=["GET", "POST"])
@login_required
def control():
    if request.method == "GET":
        return render_template("type_of_control")
    else:
        control = request.form.get("control")
        db.execute("UPDATE hospitals SET control=? WHERE id=?", control, session["user_id"])
        return redirect("/me")


@app.route("/revenue", methods=["GET", "POST"])
@login_required
def revenue():
    if request.method == "GET":
        return render_template("revenue.html")
    else:
        revenue = request.form.get("revenue")
        db.execute("UPDATE hospitals SET revenue=? WHERE id=?", revenue, session["user_id"])
        return redirect("/me")


@app.route("/hospital", methods=["GET", "POST"])
@login_required
def hospital():
    if request.method == "GET":
        return render_template("hospital.html")
    else:
        type = request.form.get("type")
        db.execute("UPDATE hospitals SET type=? WHERE id=?", type, session["user_id"])
        return redirect("/me")


@app.route("/hospital", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        contact = request.form.get("contact")
        db.execute("UPDATE hospitals SET contact=? WHERE id=?", contact, session["user_id"])
        return redirect("/me")


@app.route("/bio", methods=["GET", "POST"])
@login_required
def bio():
    if request.method == "GET":
        return render_template("bio.html")
    else:
        bio = request.form.get("bio")
        db.execute("UPDATE hospitals SET bio=? WHERE id=?", bio, session["user_id"])
        return redirect("/me")


@app.route("/Inventory_History")
@login_required
def inventory_history():
    history = db.execute(
        "SELECT supplies.name, supplies.department, supplies.brand, supplies.year, inventory.user_id, inventory.date, inventory.quantity FROM supplies INNER JOIN inventory ON supplies.id=inventory.supply_id WHERE inventory.user_id=?", session["user_id"])
    return render_template("Inventory_History.html", history=history)


@app.route("/inventory")
@login_required
def inventory():
    '''Show portfolio of stocks'''
    inventory = db.execute(
        "SELECT * FROM supplies WHERE user_id=?", session["user_id"])
    return render_template("inventory.html", inventory=inventory)


@app.route("/about")
@login_required
def about():
    '''Show description of company'''
    return render_template("about.html", about=about)


@app.route("/me")
@login_required
def me():
    '''An individuals profile'''
    me = db.execute("SELECT * FROM hospitals WHERE id=?", session["user_id"])
    return render_template("me.html", me=me)


@app.route("/profiles")
@login_required
def profiles():
    list = db.execute("SELECT * FROM hospitals")
    return render_template("profiles.html", list=list)


@app.route("/create_profile", methods=["GET", "POST"])
def create_profile():
    if request.method == "GET":
        return render_template("create_profile.html")
    else:
        print("here")
        name = request.form.get("name")
        state = request.form.get("state")
        street = request.form.get("street")
        city = request.form.get("city")
        areas = request.form.get("areas")
        type_hospital = request.form.get("type")
        control = request.form.get("control")
        revenue = request.form.get("revenue")
        contact = request.form.get("contact")
        website = request.form.get("website")
        number = request.form.get("number")
        bio = request.form.get("bio")
        if (len(db.execute("SELECT name from HOSPITALS WHERE name=?", name)) != 0):
            db.execute("DELETE FROM hospitals WHERE id=?", session["user_id"])
            return apology("An account already exists for this user")
        else:
            db.execute("UPDATE hospitals SET phone_number=?, control=?, street=?, city=?, state=?, areas=?, revenue=?, type=?, name=?, contact=?, bio=? WHERE id=?",
                       number, control, street, city, state, areas, revenue, type_hospital, name, contact, bio, session["user_id"])
            return redirect("/login")


@app.route("/inventory_add", methods=["GET", "POST"])
@login_required
def inventory_add():
    if request.method == "GET":
        return render_template("inventory_add.html")
    else:
        name = request.form.get("name")
        department = request.form.get("department")
        brand = request.form.get("brand")
        year = request.form.get("year")
        quantity = request.form.get("quantity")
        if int(quantity) < 0 or int(quantity) == 0:
            return apology("Invalid quantity")
        else:
            date_transacted = datetime.datetime.now()
            if (len(db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?", name, session['user_id'], brand, year, department))) == 0:
                db.execute("INSERT INTO supplies(name, user_id, brand, year, department, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                           name, session["user_id"], brand, year, department, quantity)
                list = db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                                  name, session['user_id'], brand, year, department)
                id = list[0]['id']
                db.execute("INSERT INTO inventory (user_id, supply_id, date, quantity) VALUES (?, ?, ?, ?)",
                           session['user_id'], id, date_transacted, quantity)
            else:
                list = db.execute("SELECT quantity FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                                  name, session['user_id'], brand, year, department)
                quantity_current = list[0]['quantity']
                quantity_updated = quantity_current + int(quantity)
                db.execute("UPDATE supplies SET quantity=? WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                           quantity_updated, name, session['user_id'], brand, year, department)
            list = db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                              name, session['user_id'], brand, year, department)
            id = list[0]['id']
            db.execute("INSERT INTO inventory (user_id, supply_id, date, quantity) VALUES (?, ?, ?, ?)",
                       session['user_id'], id, date_transacted, quantity)
            return redirect("/inventory")


@app.route("/inventory_remove", methods=["GET", "POST"])
@login_required
def inventory_remove():
    if request.method == "GET":
        return render_template("inventory_remove.html")
    else:
        name = request.form.get("name")
        department = request.form.get("department")
        brand = request.form.get("brand")
        year = request.form.get("year")
        quantity = request.form.get("quantity")
        if int(quantity) < 0 or int(quantity) == 0:
            return apology("Invalid quantity")
        else:
            if (len(db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                               name, session['user_id'], brand, year, department))) == 0:
                return apology("You do not have any of these supplies")
            else:
                list = db.execute("SELECT quantity, id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                                  name, session['user_id'], brand, year, department)
                quantity_current = list[0]['quantity']
                if (quantity_current < int(quantity)):
                    return apology("You do not own enough of this supply")
                else:
                    date_transacted = datetime.datetime.now()
                    quantity = -int(quantity)
                    id = list[0]['id']
                    quantity_updated = quantity_current + int(quantity)
                    db.execute("UPDATE supplies SET quantity=? WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                               quantity_updated, name, session['user_id'], brand, year, department)
                    db.execute("INSERT INTO inventory (user_id, supply_id, date, quantity) VALUES (?, ?, ?, ?)",
                               session['user_id'], id, date_transacted, quantity)
                    return redirect("/inventory")


@app.route("/history")
@login_required
def history():
    transaction = db.execute(
        "SELECT requests.brand, requests.amount, requests.version, requests.supply_name, requests.department FROM requests AND INNER JOIN histories ON requests.requester_id=histories.request_id WHERE histories.request_id=?", session["user_id"])
    return render_template("history.html", transaction=transaction)


@app.route("/login", methods=["GET", "POST"])
@app.route("/")
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM hospitals WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/profiles")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/request", methods=["GET", "POST"])
@login_required
def make_request():
    if request.method == "GET":
        return render_template("request.html")
    else:
        name = request.form.get("name")
        supply_name = request.form.get("supply_name")
        brand = request.form.get("brand")
        quantity = request.form.get("quantity")
        version = request.form.get("version")
        if (len(db.execute("SELECT * FROM requests WHERE hospital_name=? AND supply_name=? AND brand=? AND amount=? AND version=?", name, supply_name, brand, quantity, version))) == 0:
            db.execute("INSERT INTO requests(hospital_name, supply_name, brand, amount, version) VALUES (?, ?, ?, ?, ?)",
                       name, supply_name, brand, quantity, version)
            return redirect("/request_display")
        else:
            return apology("This request already exists")


@app.route("/respond", methods=["GET", "POST"])
@login_required
def respond():
    if request.method == "GET":
        return render_template("respond.html")
    else:
        name_respond = request.form.get("name_respond")
        name_request = request.form.get("name_request")
        supply_name = request.form.get("supply_name")
        brand = request.form.get("brand")
        quantity_request = request.form.get("quantity_request")
        quantity_respond = request.form.get("quantity_respond")
        department = request.form.get("department")
        version = request.form.get("version")
        date_transacted = datetime.datetime.now()
        responder = db.execute("SELECT id FROM hospitals WHERE name=?", name_respond)
        responder_id = responder[0]["id"]
        check = db.execute("SELECT quantity FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                           supply_name, responder_id, brand, version, department)
        if ((len(db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?", supply_name, responder_id, brand, version, department))) == 0) or (check[0]["quantity"] < int(quantity_respond)):
            return apology("This exchange cannot be made")
        elif int(quantity_request) == int(quantity_respond):
            db.execute("DELETE FROM requests WHERE hospital_name=? AND supply_name=? AND brand=? AND version=?",
                       name_request, supply_name, brand, version)
        else:
            quantity = int(quantity_request) - int(quantity_respond)
            db.execute("UPDATE requests SET amount=? WHERE hospital_name=? AND supply_name=? AND brand=? AND version=? AND department=?",
                       quantity, name_request, supply_name, brand, version, department)
        requester = db.execute("SELECT id FROM hospitals WHERE name=?", name_request)
        requester_id = requester[0]["id"]
        responder_supply = db.execute("SELECT id FROM supplies WHERE name=? AND user_id=?",
                                      supply_name, responder_id)
        supply_respond_id = responder_supply[0]["id"]
        if (len(db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? AND brand=? AND year=? AND department=?",
                           supply_name, requester_id, brand, version, department))) == 0:
            db.execute("INSERT INTO supplies(name, user_id, brand, year, department, quantity) VALUES (?, ?, ?, ?, ?, ?)",
                       supply_name, requester_id, brand, version, department, quantity_respond)
            db.execute("INSERT INTO inventory (user_id, supply_id, date, quantity) VALUES (?, ?, ?, ?)",
                       requester_id, id, date_transacted, quantity_respond)
        else:
            requester_supply = db.execute("SELECT id FROM supplies WHERE name=? AND user_id=? ",
                                          supply_name, requester_id)
            supply_request_id = requester_supply[0]["id"]
            requester_info = db.execute("SELECT quantity FROM supplies WHERE user_id=? AND id =?",
                                        requester_id, supply_request_id)
            responder_info = db.execute("SELECT quantity FROM supplies WHERE user_id=? AND id =?",
            responder_id, supply_respond_id)
            quantity_request = (requester_info[0]["quantity"]+int(quantity_respond))
            db.execute("UPDATE supplies SET quantity=? WHERE user_id=? AND name=? AND brand=? AND year=? AND department=?",
                       quantity_request, requester_id, supply_name, brand, version, department)
            db.execute("INSERT INTO inventory (user_id, supply_id, date, quantity) VALUES (?, ?, ?, ?)",
                       requester_id, id, date_transacted, quantity_request)
        quantity_responder = (responder_info[0]["quantity"]) - int(quantity_respond)
        db.execute("UPDATE supplies SET quantity=? WHERE user_id=? AND name=? AND brand=? AND year=? AND department=?",
                   quantity_responder, responder_id, supply_name, brand, version, department)
        db.execute("INSERT INTO inventory(user_id, supply_id, date, quantity) VALUES(?, ?, ?, ?)",
                   responder_id, id, date_transacted, quantity_responder)
        return redirect("/inventory")


@app.route("/request_display")
@login_required
def request_display():
    '''Show portfolio of stocks'''
    hospital = db.execute(
        "SELECT * FROM requests")
    return render_template("request_display.html", hospital=hospital)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        length = db.execute("SELECT * FROM hospitals WHERE username = :username", username=username)
        print(length)
        print(username)
        password = request.form.get("password")
        print(password)
        password_confirmation = request.form.get("password_confirmation")
        if username == "":
            return apology("Username required")
        elif (len(length) >= 1):
            return apology("Username already exists")
        elif password == "":
            return apology("Password required")
        elif password_confirmation == "":
            return apology("Password confirmation required")
        elif password != password_confirmation:
            return apology("Passwords do not match")
        else:
            print("got here")
            hash = generate_password_hash(password)
            print(hash)
            db.execute("INSERT INTO hospitals (username, hash) VALUES(:username, :hash)", username=username, hash=hash)
            rows = db.execute("SELECT * FROM hospitals WHERE username = :username",
                              username=request.form.get("username"))
            session["user_id"] = rows[0]["id"]
        return redirect("/create_profile")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
