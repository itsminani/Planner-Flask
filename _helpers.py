from flask import redirect, render_template, session
from functools import wraps
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
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def send_simple_email(email="minanihertierluc@gmail.com", name="Minani"):
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
        data={"from": "Mailgun Sandbox <postmaster@sandbox241fab3c279641bb9a54d5d29592be9e.mailgun.org>",
              "to": "Name <"+email+">",
              "subject": "Confirmation",
              "text": "Thank you for confirming your email address with us!  You are truly awesome!"})

print(send_simple_email().content)