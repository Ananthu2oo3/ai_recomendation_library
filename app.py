from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)

client          = MongoClient('mongodb://localhost:27017')
db              = client['library']
app.secret_key  = 'supersecretkey' 
login_db        = db['login']
book_db         = db['books']

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

        result      = login_db.find_one({"mailid": mailid})
        
        if result and result.get('password') == password:
            session['username'] = result['username']
            return redirect(url_for('dashboard'))
        
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)
    
    else:
        return render_template('login.html', error='Invalid username or password')



@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        username    = request.form['username']
        mailid      = request.form['mailid']
        phn_no      = request.form['phn_no']
        password    = request.form['password']
        interests   = request.form.getlist('interests')

        
        data ={ 
            "username"  : username,
            "mailid"    : mailid,
            "phn_no"    : phn_no, 
            "password"  : password,
            "interests" : interests
        }

        login_db.insert_one(data)
        return redirect(url_for('login'))
    
    else:
        return render_template('register.html')
    


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user = login_db.find_one({"username": username})
        
        if not user:
            return render_template('dashboard.html', error='User not found')

        interests = user.get('interests', [])
        
        books_by_genre = {}
        for interest in interests:
            books_by_genre[interest] = list(book_db.find({"Category": interest}))

        remaining_books = list(book_db.find({"Category": {"$nin": interests}}))
        books_by_genre["Others"] = remaining_books

        return render_template('dashboard.html', username=username, books_by_genre=books_by_genre)
    
    return render_template('dashboard.html', error='Session ID not found')

@app.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query')

    if query:
        # Search for books matching the query in the title or category
        search_results = book_db.find({"Title": {"$regex": query, "$options": "i"}})
        search_results = list(search_results)
        
    else:
        search_results = []

    return render_template('search_results.html', query=query, search_results=search_results)


if __name__ == '__main__':
    app.run(debug=True, port = '8000')