# from flask import Flask, render_template, request, redirect, url_for, session

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def index():
#     return render_template('login.html')

# @app.route('/register', methods=['GET','POST'])
# def register():
    
#     if request.method == 'POST':

#         username = request.form['username']
#         password = request.form['password']

#         return redirect(url_for('login'))

#     else:    
#         return render_template('register.html')

# if __name__ == '__main__':
#     app.run(debug=True)

from pymongo import MongoClient 

client = MongoClient('mongodb://localhost:27017')
db = client['library']
collection = db['login']

data = {"username": "padma", "password": "456"}
collection.insert_one(data)