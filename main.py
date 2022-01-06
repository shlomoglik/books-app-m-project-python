from lib.mongo_manager import MongoManager
from models.Library_model import Library
from models.Reader_model import Reader
from models.Shelf_model import Shelf
from models.Book_model import Book
from seeders.main import load, unload
from lib.utils import Commands_manager, input_non_empty_string
import requests


def main():

    # [-] sign in user and authintacte
    times = 5
    while times>0:
        print("lets login:")
        username = input_non_empty_string("please enter your username: ")
        email = input_non_empty_string("please enter your email: ")
        url = f"https://jsonplaceholder.typicode.com/users?email={email}&username={username}"
        res = requests.get(url)
        if res.status_code != 200:
            return print("someting wrong on our side try again later")
        res_data = res.json()[0]
        if res_data['username'] == username and res_data['email']  == email:
            print(f"welcome {username}")
            break
        times += 1
    else:
        return print("too many tries... by by..")

    # [1*] OPTIONAL: load DB using seeders module (make sure to not call it twice with the same data  or  call unload() at the end)
    # load() 

    # [2] load data from DB
    db = MongoManager.getDB()
    books_collection = db.get_collection("books").find()

    books = []
    shelfs = []

    for book in books_collection:
        b = Book(book['author'], book['title'], book['num_of_pages'])
        books.append(b)

    # [3] fill library
    NUM_OF_SHELFS = 3
    NUM_OF_BOOKS_IN_SHELF = 2
    i = 0
    for _ in range(NUM_OF_SHELFS):
        sh = Shelf()
        shelfs.append(sh)
        for _ in range(NUM_OF_BOOKS_IN_SHELF):
            sh.add_book(books[i])
            i += 1

    library = Library(shelfs, [])

    # [4] run program using commands_manager with curren library
    cmd = Commands_manager(library, books)
    cmd.run()

    # [5*] OPTIONAL: unload DB using seeders module
    # unload()


if __name__ == "__main__":
    main()