from flask import Flask, request, redirect, render_template, session, flash
from connect import MySQLConnector
import re, md5
REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = "notthekey"
mysql = MySQLConnector(app,'thewall')

@app.route('/')
def index():
    print 'index'
    return render_template('index.html') 

@app.route('/login', methods=["POST"])
def login_check():
    print 'login_check'
    e = request.form['email']
    p = md5.new(request.form['password']).hexdigest()
    print e, p
    # que = "SELECT * FROM Users WHERE (user.email = :email and user.password = :password)"
    # inputs ={"password": p,"email": e}
    # guest = mysql.query_db(que,inputs)
    # if len(guest) > 0:
    #     print "logged in"
    #     session['firsts'] = guest[0]['first_name']
    #     return redirect('/wall')
    # else:
    #     print "incorrect"
    return redirect('/wall')

@app.route('/wall')
def the_downfall():
    print 'wall'
    print session['id']
    return render_template("wall.html")

@app.route('/reg')
def registration():
    print 'sign_up'
    return render_template('sign_up.html')

@app.route('/check', methods=['POST'])
def sign_up_check():
    Fname = request.form["Fname"].encode('utf8')
    Lname = request.form["Lname"].encode('utf8')
    email = request.form["email"]
    pass1 = request.form["password_1"]
    pass2 = request.form["password_2"]
    print Fname, Lname, email, pass1, pass2
    if len(Fname) < 3 or len(Lname) < 3:
        flash("Name is to short.")
        return redirect('/reg')
    elif str.isalpha(Fname) != True or str.isalpha(Lname) != True:
        flash("No numbers in the name.")
        return redirect('/reg')
    elif len(email) <1:
        flash("EMAIL CCANNOT BE EMPTY!")
        return redirect('/reg')
    elif not REGEX.match(email):
        flash('INVALID EMAIL ADDRESS!')
        return redirect('/reg')
    elif len(pass1) < 8:
        flash('Password must be atleast 8 characters long.')
        return redirect('/reg')
    elif pass1 != pass2:
        flash("Passwords didn't match up.")
        return redirect('/reg')
    else:
        flash("SUCCESS!")
        pass1 = md5.new(request.form["password_1"]).hexdigest()
        pass2 = md5.new(request.form["password_2"]).hexdigest()
        
        query = "INSERT INTO Users (first_name, last_name, email, password, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW())"
        data ={
                'first_name': Fname,
                'last_name': Lname,
                'email': email,
                'password': pass1
            }
        mysql.query_db(query, data)
        session['id'] = mysql.query_db(query, data)
    return redirect('/wall')

app.run(debug=True)