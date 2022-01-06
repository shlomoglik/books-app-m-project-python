from lib.mongo_manager import MongoManager
import seeders.load_books as load_books
from models.Shelf_model import Shelf

def load():
    load_books.run()

def unload():
    db = MongoManager.getDB()
    db.drop_collection("books")
    db.drop_collection("shelfs")