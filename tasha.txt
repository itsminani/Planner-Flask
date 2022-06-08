from flask import Flask,flash, render_template,request,redirect

application = Flask(__name__)
app=application

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
    return render_template('messageTemplate.html',error=True, title = 404, text="Seems like you have wondered off")

@app.errorhandler(500)
def server_error(e):
    # note that we set the 404 status explicitly
    return render_template('messageTemplate.html',error=True, title = 500, text="oops we fucked up")

# Routing and navigation
@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/base')
# def base():
#     user= User(name="Mbokolo",email="Email Yanjye",password_hash="password",confirmed=True)
#     db.session.add(user)
#     db.session.commit()
#     return render_template("base.html")

# @app.route('/login',methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password= request.form.get("password")
#         user = User.query.filter_by(email= email).first()
#         # Check if the email was found
#         if user:
#             if not check_password_hash(user.password_hash,password):
#                 return render_template("messageTemplate.html", error = False, title= "Wrong!", text = "Wrong username or password")
#             print("User Logged in")
#             print("LOGIN function")
#             return redirect("/signup")
#         return render_template('messageTemplate.html',  error = True,title = 500, text=user)
#     return redirect("/",code=302)

# @app.route('/signup',methods=["GET","POST"])
# def signUp():

#     if request.method == "POST":
#         # TODO setup FLASH
#         email = request.form.get("email")
#         name = request.form.get("name")
#         password = request.form.get("password")

#         if not (password and email and name):
#             return render_template("messageTemplate.html", title= "Oops", text= "Forgot something important")
#         email_exists = User.query.filter_by(email= email).first()
#         if email_exists:
#             return render_template("messageTemplate.html", title= "Oops", text= email_exists.email + " is already taken")

#         password_hash = generate_password_hash(password)

        
#         # TODO Send authentication Email 
#         # Add new user to the database
#         new_user = User(email= email, name= name, password_hash= password_hash)
#         db.session.add(new_user)
#         db.session.commit()

#         print("User successfully created")
#         return redirect("/login")
#     if request.path=="/signup":
#         route = "signup"
#     return render_template("index.html",route=route)






# TODO: Add a route for a currently existing user where other users can create events
# DONE: create a user database
# TODO: create an event database
# TODO: setup email verification for creating accounts
# TODO: setup emails for creating events
# TODO: check in database whether person has free periods at that time
