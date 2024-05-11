from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['library']
collection = db['login']

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')
    
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    result = collection.find_one({"username": username})
    
    if result and result.get('password') == password:
        return redirect(url_for('dashboard'))
    
    else:
        return render_template('login.html', error='Invalid username or password')
    
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



if __name__ == '__main__':
    app.run(debug=True)