import datetime
from flask import redirect, render_template, session
from functools import wraps
import random
import os
import requests

def raise_message(title, msg="message goes here", error= False):
    """
    Function to easily print sites with messages in case of errors
    
    error attribute is boolean
    """
    return render_template('messageTemplate.html',error=error, title = title, text=msg)


def login_required(f):
    """
    Decorate routes to require login    .

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def send_simple_email(email="minanihertierluc@gmail.com", name="user name", subject = "Email from planner", html = "<p>Welcome to our amazing app!</p>"):
    """
    Email sending function 

    email: user email you want to send it to
    name: name to display while sending the email
    
    """
    # The Api_key am using has been received mailgun API
    if not os.environ.get("EMAIL_KEY"):
        return "Mail key not set"
    return requests.post(
        "https://api.mailgun.net/v3/sandbox241fab3c279641bb9a54d5d29592be9e.mailgun.org/messages",
        auth=("api", os.environ.get("EMAIL_KEY")),
        data={"from": "The Planner team <minanitest@gmail.com>",
              "to": name+ " <"+email+">",
              "subject": subject,
              "html" : "<div style='text-align:center; color: grey'>"+html+"</div>"})


def confirm_email(email, name):
    """
    Function to send a confirmation 6 code digit to the users

    email: email of receiver
    name: name of person
    """

    user_code = random.randint(100000,999999)
    # TODO commit the code to the database
    # Tell the user that the code will expire in 3 days
    expiry = datetime.date.today() + datetime.timedelta(days=3)
    html_content = f"<h3>Please find below your activation code</h3><br> <h1>{user_code}</h1><p style='font-size:10px;'>your code will expire on {expiry} click <a href='rickroll.com'>Here</a> to get a new code </p>"
    return send_simple_email(email, name, subject="Confirmation Code",html=html_content)

def confirmation_link(email, name):
    """
    Function to send a confirmation link to the user's email address

    email: email of receiver
    name: name of person

    returns link
    """
    hash = 0
    # Very simple hash function that works by adding the ascii values in order to confirm the user's account
    for x in email+name:
        hash += ord(x)
    # Just a way to complicate the hash
    hash = hash*hash
    hash = hash% 10000000
    return hash

def create_event_email(email,name, invitee, event_time):
    """
    An email that will be automatically sent to users when an event is created

    email: Destination email
    name: The destination's name
    invitee: email of the inviteed person to the meeting
    event_time: string of the datetime object
    """

    # Email to the event creator
    html_for_confirmation = f"""<h2>Event Confirmation</h2><br> <p style='font-size:18px;'>Your event on {event_time} has been successfully created. click <a href='http://127.0.0.1:5000/my_events'>Here</a> to edit this event </p>"""
    print(send_simple_email(email = email, name=name,subject="Confirmation For new Event",html=html_for_confirmation))
    
    # Email to the invitees
    html_for_invitee = f"""<h2>Invitation</h2><br> <p style='font-size:18px;'>{name} has invited you to an event on {event_time} click <a href='http://127.0.0.1:5000/my_events'>Here</a> to attend this event </p>"""
    print(send_simple_email(email = invitee, name=invitee,subject="Invitation to event",html=html_for_invitee))

