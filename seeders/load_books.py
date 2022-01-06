from models.Book_model import Book
from lib.mongo_manager import MongoManager


def run():
    db = MongoManager.getDB()
    books = []
    try:
        books.append(Book(author="Stephen King",title="The Institute",num_of_pages=560))    
        books.append(Book(author="Stephen King",title="Doctor Sleep",num_of_pages=672))

        books.append(Book(author="J. K. Rowling",title="Harry Potter and the Prisoner of Azkaban",num_of_pages=250))
        books.append(Book(author="J. K. Rowling",title="Harry Potter and the Goblet of Fire",num_of_pages=230))
        
        books.append(Book(author="John Grisham",title="The Guardians",num_of_pages=320))
        books.append(Book(author="John Grisham",title="Sooley",num_of_pages=290))
        
        db.get_collection("books").insert_many([vars(b) for b in books])
    except Exception as e:
        print(f"some error occured! cannot load books: \n{e}")
    return books