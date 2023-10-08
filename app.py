from flask import Flask, render_template, request, url_for, redirect, session
from user import User, ValidationError
import os
import bcrypt
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = '92931b5234a849a5211112dfc55da37e005ce47d4ef2255f'
app.config["DEBUG"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/', methods=('GET', 'POST'))
def index():
    if "email" in session:
        logger.info("User redirected to dashboard")
        return redirect(url_for('dashboard'))
    logger.info("Rendering index.html")
    return render_template('index.html')


#Register User
@app.route('/register', methods=["POST"]) 
def register():
    if "email" in session:
        logger.info("User already logged in. Redirecting to dashboard.")
        return redirect(url_for('dashboard'))
    name = request.form.get('name')
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        email_found = User.objects.filter(email=email).first()
        if email_found != None:
            message = "User is Already Registered"
            return render_template("error.html", message=message, email=email, name=name)
        else:
            hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
            User(name=name, email=email, pwd=hashed)
            message = "Successfully Registered User"
            session["email"] = email
            session["name"] = name
            return redirect(url_for('dashboard'))
    except ValidationError:
        message = "Validation Error"
        return render_template("error.html", message=message)

#Login User
@app.route('/login', methods=["POST"])    
def login():
        email = request.form.get('email')
        pwd = request.form.get('password')
        try:
            email_found = User.objects.filter(email=email).first()
            message="Successfully Logged In"
            if email_found != None:
                user_pass = email_found.pwd
                # print("Existing Pass", user_pass.encode('utf-8'))
                # print("Login Pass", pwd)
                if bcrypt.checkpw(pwd.encode('utf-8'), user_pass.encode('utf-8')):
                    session["email"] = email
                    session["name"] = email_found.name
                    logger.info("User successfully logged in.")
                    return redirect(url_for('dashboard'))
                else:
                    logger.warning("Login credentials do not match.")
                    message="Credentials Doesn't match"
                    return render_template("error.html", message=message, email=email)
            else:
                message = "Cannot Find User"
                return render_template("error.html", message=message, email=email)
        except ValidationError:
            message = "Validation Error"
            return render_template("error.html", message=message)


#Logout User
@app.route('/logout', methods=["GET"])    
def logout():
        try:
           session.clear()
           logger.info("User logged out and session cleared.")
           return redirect(url_for('index'))
        except:
            logger.exception("Unable to clear session properly")
            print("Cannot clear session Properly")
            return redirect(url_for('error'))


#Error
@app.route('/error', methods=["GET"])    
def error():
        return render_template("error.html")


#Dashboard
@app.route('/dashboard', methods=["GET"])
def dashboard():
        if "email" in session:
            return render_template("dashboard/index.html", name=session["name"])
        else:
            return render_template("index.html")
