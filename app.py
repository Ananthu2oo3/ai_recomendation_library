from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from util import *


app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['library']
collection = db['login']


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')
    


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        
        mailid      = request.form['mailid']
        password    = request.form['password']

        result      = collection.find_one({"mailid": mailid})
        
        if result and result.get('password') == password:
            return redirect(url_for('dashboard'))
        
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    
    else:
        return render_template('login.html', error='Invalid username or password')



@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        mailid   = request.form['mailid']
        phn_no   = request.form['phn_no']
        password = request.form['password']
        
        data ={ 
            "username"  : username,
            "mailid"    : mailid,
            "phn_no"    : phn_no, 
            "password"  : password
            }

        collection.insert_one(data)
        return redirect(url_for('login'))
    
    else:
        return render_template('register.html')
    
    

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/add_book', methods=['GET','POST'])
def add_book():
    if request.method == 'POST':
        title       = request.form['title']
        author      = request.form['author']
        publication = request.form['publication']
        genre       = request.form['genre']

        util.enter_book(title, author, publication, genre)
        
    else:
        return render_template('add_book.html')


if __name__ == '__main__':
    app.run(debug=True, port = '8000')