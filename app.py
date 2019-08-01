import json
from os import urandom

from flask import Flask, request, render_template, redirect, flash, session
from util import Database

ALLOWED_EXTENSIONS = {'csv'}

config = json.load(open("config/mongo.json"))

app = Flask(__name__)

app.config["MONGO_DBNAME"] = config['databaseName']
app.config["MONGO_URI"] = config['mongoURI']
app.config["SECRET_KEY"] = urandom(32)

dbtools = Database.DBTools(app)

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods = ["GET", "POST"])
def log():
    if request.method == "GET":
        if 'username' in session:
            if session['userType'] == 'admin':
                return redirect('/admin')
        return render_template('login.html')
    if 'username' in session:
        flash('Already logged in!')
        return render_template('login.html')
    inputPass = request.form['pass']
    inputUsername = request.form['username']
    if request.form['schoolid'] == '': #Admin login
        if dbtools.authAdmin(inputUsername, inputPass):
            session['username'] = inputUsername
            session['userType'] = 'admin'
            return redirect('/admin')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route("/register", methods = ['GET', 'POST'])
def reg():
    if request.method == 'GET':
        return render_template("register.html")
    inputPass = request.form['pass']
    passConfirm = request.form['passConfirm']
    inputUsername = request.form['username']
    if passConfirm != inputPass:
        flash('Passwords do not match!')
    else:
        flash(dbtools.registerAdmin(inputUsername, inputPass))
    return render_template('register.html')

@app.route("/uploadStudentCSV", methods = ['POST'])
def uploadStudentCSV():
    if 'username' not in session:
        return redirect('/login')
    if session['userType'] != 'admin':
        flash('You are not a administrator!')
    if 'inputCSV' not in request.files:
        flash('No file part')
        return redirect(request.referrer)
    inputFile = request.files['inputCSV']
    if inputFile.filename == '':
        flash('No file uploaded')
        return redirect(request.referrer)
    if inputFile.filename.rsplit('.',1)[1].lower() != 'csv':
        flash('Invalid file type')
        return redirect(request.referrer)
    csv = inputFile.read().decode('utf-8')
    flash(dbtools.addStudentsFromCSV(session['username'], request.form['schoolID'], csv))
    return redirect(request.referrer)

@app.route("/admin")
def admin():
    if 'username' not in session:
        return redirect('/login')
    return render_template("admin_home.html", username = session['username'], managed = dbtools.getBasicSchoolInfo(session['username']))

@app.route("/createSchool", methods = ["POST"])
def createClass():
    if 'username' not in session:
        return redirect('/login')
    if session['userType'] != 'admin':
        flash('You are not a administrator!')
        return redirect('/admin')
    if request.form['schoolName'] == '':
        flash('No school name given')
        return redirect('/admin')
    dbtools.registerSchool(session['username'], request.form['schoolName'])
    flash('Registration successful')
    return redirect('/admin')

@app.route("/school/<schoolID>")
def schoolPage(schoolID):
    if 'username' not in session:
        return redirect('/login')
    if not(dbtools.checkAdmin(schoolID, session['username'])):
        flash('You are not a administrator of this school!')
        return redirect('/admin')
    return render_template("schools.html", schoolData=dbtools.getSchoolInfo(schoolID))

@app.route('/addClass', methods = ['POST'])
def addClass():
    if 'username' not in session:
        return redirect('/login')
    if session['userType'] != 'admin':
        flash('You are not a administrator!')
        redirect('/admin')
    flash(dbtools.addClass(session['username'], request.form['schoolID'], request.form['className']))
    return redirect(request.referrer)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        session.pop('userType')
    return redirect('/')

if __name__ == "__main__":
    app.debug = True
    app.run()
