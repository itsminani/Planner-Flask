import datetime
import email
from click import confirm
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, flash, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from models import *
from _helpers import login_required, raise_message, send_simple_email, confirm_email, confirmation_link

application = Flask(__name__)
app = application

# Ensure templates are auto-reloaded
# ! app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = "my crazy key"

# Configure database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialiaze SQLAlchemy
db = SQLAlchemy(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Handle pages that do not exist
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return raise_message(404, "Seems like you have wondered off", True)


@app.errorhandler(500)
def server_error(e):
    # note that we set the 404 status explicitly
    return raise_message(404, "Oops, a big Oopsie, Server error", True)

# Routing and navigation


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/base')
@login_required
def base():
    user = User.query.filter_by(id=session["user_id"]).first()

    # Test email sending
    # email_response = send_simple_email("minanihertierluc@gmail.com", user.name)
    email_response2 = confirm_email("minanihertierluc@gmail.com", user.name)
    response = confirmation_link(user.email,"minani")
    return raise_message(user.email, str(response)+str(email_response2))


@app.route('/events')
@login_required
def events():
    user = User.query.filter_by(id=session["user_id"]).first()
    if not user:
        return redirect("/")
    if not user.confirmed:
        flash("Please consider confirming your account to have more awesome features")
    return render_template("createEvent.html")


@app.route('/create_event', methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "GET":
        return render_template("createEvent.html")
    else:
        # When method comes in as create event
        title = request.form.get("title")
        invitee = request.form.get("invitee")
        platform = request.form.get("platform")
        location_link = request.form.get("location_link")
        details = request.form.get("details")
        event_time = request.form.get("datetime")
        duration = request.form.get("duration")
        print(duration)
        time_object = datetime.datetime.strptime(event_time,'%Y-%m-%dT%H:%M')

        if not (title and invitee  and platform):
            flash("Some fields were not correctly entered", "error")
            return raise_message("Ooops", "Forgot something important",True)

        # Add event to database
        new_event = Event(user_id = session["user_id"],creator_id = session["user_id"],title = title, platform =platform , location_link= location_link, invitees=invitee, details= details, event_time = time_object, duration= duration)
        db.session.add(new_event)
        db.session.commit()

        flash("Event successfully created"+str(time_object))
        return raise_message("title", invitee+"---"+platform+"---"+details+"---"+str(time_object)+duration)




@app.route("/my_events")
@login_required
def my_events():
    events = Event.query.filter_by(user_id=session["user_id"])
    for event in events:
        print(event.duration)
    return render_template("myEvents.html",events = events)


@app.route("/account")
@login_required
def account():
    user = User.query.filter_by(id=session["user_id"]).first()
    return render_template("account.html", name=user.name, email=user.email, confirmed=user.confirmed, date=user.created_at)


@app.route('/login', methods=["POST", "GET"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        # Check if the email was found
        if user:
            # Check if password is right
            if not check_password_hash(user.password_hash, password):
                return raise_message("Wrong!", "Wrong username or password")

            # Remember which user has logged in
            print(user.id)
            session["user_id"] = user.id
            flash("Successfully Logged in")
            return redirect("/account")
        else:
            return raise_message("Wrong!", "Wrong username or password")
    # Redirect to home if the request is GET
    return redirect("/", code=302)


@app.route('/logout')
def logout():
    """
    Logout the currently logged in used and delete cookies

    Deletes all user session data and notify the user
    """

    session.clear()
    flash("Successfully Logged Out")
    return raise_message("Success", "Logged out")


@app.route('/signup', methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        if not (password and email and name):
            flash("Some fields were not correctly entered", "error")
            return raise_message("Ooops", "Forgot something important",True)
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already exists", "error")
            return render_template("messageTemplate.html", title="Oops", text=email_exists.email + " is already taken")

        password_hash = generate_password_hash(password)

        # TODO Send authentication Email
        # Add new user to the database
        new_user = User(email=email, name=name, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash("Account Successfully Created")
        return redirect("/login")
    if request.path == "/signup":
        route = "signup"
    return render_template("index.html", route=route)


# TODO: Add a route for a currently existing user where other users can create events
# DONE: create a user database
# TODO: create an event database
# TODO: setup email verification for creating accounts
# TODO: setup emails for creating events
# TODO: check in database whether person has free periods at that time
