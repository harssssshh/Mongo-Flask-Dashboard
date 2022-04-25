from flask import Flask, render_template, request, url_for, redirect, session
from user import User, ValidationError
import os
import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '92931b5234a849a5211112dfc55da37e005ce47d4ef2255f'
app.config["DEBUG"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0




# dbName = os.environ["DB_NAME"]
# dbUsername = os.environ["DB_USERNAME"]
# dbPassword = os.environ["DB_PASS"]
# cluster = os.environ["CLUSTER_NAME"]
# host = f"mongodb+srv://{dbUsername}:{dbPassword}@{cluster}/{dbName}?retryWrites=true&w=majority"
# print(host)
# api = os.environ["API_URI"]
# api = "http://localhost:5000"


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', methods=('GET', 'POST'))
def index():
    if "email" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


#Register User
@app.route('/register', methods=["POST"]) 
def register():
    if "email" in session:
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
                    return redirect(url_for('dashboard'))
                else:
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
           return redirect(url_for('index'))
        except:
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