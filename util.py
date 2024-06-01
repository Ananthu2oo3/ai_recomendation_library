from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['library']
book_db = db['books']
login_db = db['login']

# username = 'abc'

# user = login_db.find_one({"username": username})

# if user:
#     interests = user.get('interests', [])
#     for interest in interests:
#         print(interest)
# else:
#     print("User not found.")

# interests = ["Poetry","History"]

# for interest in interests:
#     books_by_genre[interest] = list(book_db.find({"Category": interest}))
