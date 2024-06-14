from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId


app = Flask(__name__)

client          = MongoClient('mongodb://localhost:27017')
db              = client['library']
app.secret_key  = 'supersecretkey' 
login_db        = db['login']
book_db         = db['books']
history_db      = db['history']




@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    return redirect(url_for('login'))
    



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
        return render_template('login.html')




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
    



@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

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




@app.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('query')

    if query:
        
        search_results = book_db.find({"Title": {"$regex": query, "$options": "i"}})
        search_results = list(search_results)
        
        query_data={
            'username'  : session['username'],
            'query'     : query,
            'result'    : search_results
        }
        history_db.insert_one(query_data)

    else:
        search_results = []

    return render_template('search_results.html', query=query, search_results=search_results)





@app.route('/book/<string:_id>', methods=['GET'])
def book_details(_id):
    
    book = book_db.find_one({"_id": ObjectId(_id)})
    
    if book:
        return render_template('book.html', book=book)
    else:
        return "Book not found", 404



if __name__ == '__main__':
    app.run(debug=True, port = '8000')