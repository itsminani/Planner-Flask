from flask import redirect, render_template, session
from functools import wraps


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