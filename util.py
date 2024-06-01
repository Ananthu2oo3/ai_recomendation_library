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

new_field = 'url'
new_value = 'https://drive.google.com/file/d/1xFW-8MURyRc3R9cvBZswjlSMWLuM0RjR/view?usp=sharing'

# Run the update_many method
result = book_db.update_many(
    {},  # Empty filter to match all documents
    { '$set': { new_field: new_value } }
)
