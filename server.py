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

@app.route('/reg')
def registration():
    print 'sign_up'
    return render_template('sign_up.html')