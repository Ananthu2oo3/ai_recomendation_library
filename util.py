from pymongo import MongoClient

client  = MongoClient('mongodb://localhost:27017')
db      = client['library']
book_db = db['books']
login_db= db['login']


def get_next_sequence_value(sequence_name):
    counter = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        return_document=True
    )
    return counter["sequence_value"]



def enter_book(title, author, publication, genre):
        
        book_id = get_next_sequence_value("book_id")
        data ={ 
            "book_id"       : book_id,
            "title"         : title,
            "author"        : author, 
            "publication"   : publication,
            "genre"         : genre
            }

        book_db.insert_one(data)

