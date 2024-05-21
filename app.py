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
    

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']

        result = collection.find_one({"username": username})
        
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
        password = request.form['password']
        print(username, password)

        data ={ "username": username, "password": password}

        collection.insert_one(data)
        # return render_template('register.html')
        return redirect(url_for('login'))
    else:
        return render_template('register.html')
    
    
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')



if __name__ == '__main__':
    app.run(debug=True, port = '8000')