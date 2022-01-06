from os import path
import sys
import json
from models.Library_model import Library
from models.Reader_model import Reader
from models.Shelf_model import Shelf
from models.Book_model import Book


def input_item_in_list(msg, options:list[str]):
    user_select = ""
    times = 0
    while len(user_select)==0 or user_select not in options:
        if times > 0:
            print("INVALID_INPUT try again [input should be in list of options]")
        if times > 2:
            print("list of options is: \n",options)
        if times > 4:
            return print("INVALID_INPUT return to main manu")
        user_select = input(msg)
        times += 1
    return user_select

def input_non_empty_string(msg):
    user_select = ""
    times = 0
    while len(user_select)==0:
        if times > 0:
            print("INVALID_INPUT try again [input sould be non empty string]")
        if times > 4:
            return print("INVALID_INPUT return to main manu")
        user_select = input(msg)
        times += 1
    return user_select

def input_valid_number(msg):
    while True:
        try:
            return int(input(msg))
        except Exception:
            print("INVALID_INPUT try again [input sould a valid number]")

def input_pos_number(msg):
    while True:
        try:
            num =  int(input(msg))
            if num > 0:
                return num
            raise Exception
        except Exception:
            print("INVALID_INPUT try again [input sould a positive number]")



class Commands_manager:
    def __init__(self,library:Library, books:list[Book]) -> None:
        self.library =library
        self.books =books
        self.readers = []


    def add_new_book(self):
        print(f"COMMAND -> add_new_book: ")
        author = input_non_empty_string("please enter book author: ")
        title = input_non_empty_string("please enter book title: ")
        if title in [b.title for b in self.books]:
            return print(f"ERROR: sorry book {title} already exist!")
        num_of_pages = input_valid_number("please enter number of pages in book: ")
        b = Book(author=author,title=title,num_of_pages=num_of_pages)
        self.books.append(b)
        self.library.add_new_book(b)

    def delete_book(self):
        print(f"\nCOMMAND -> delete_book: ")
        title = input_item_in_list("please enter book title: ",[b.title for b in self.books])
        try:
            book_index =next(i for i,b in enumerate(self.books) if b.title == title)
            del self.books[book_index]
            self.library.delete_book(title)
        except Exception as e:
            print(f"ERROR: something went wrong:\n{e}")



    def change_book_location(self):
        print(f"\nCOMMAND -> change_book_location: ")
        book_1 = input_non_empty_string("please enter book 1 title: ")
        book_2 = input_non_empty_string("please enter book 2 title: ")
        self.library.change_locations(book_1,book_2)

    def register_reader(self):
        print(f"\nCOMMAND -> register_reader: ")
        reader_id = input_valid_number("please enter reader id: ")
        if reader_id in [r.id for r in self.readers]:
            return print("ERROR: reader id '{reader_id}' already exist!")
        reader_name = input_non_empty_string("please enter reader name: ")
        if reader_name in [r.name for r in self.readers]:
            return print(f"ERROR: reader name '{reader_name}' already exist!")
        self.library.register_reader(reader_id , reader_name)
        self.readers.append(Reader(reader_id,reader_name))

    def remove_reader(self):
        print(f"\nCOMMAND -> remove_reader: ")
        reader_name = input_item_in_list("please enter reader name to remove: ",[r.name for r in self.readers])
        try:
            reader_index =next(i for i,r in enumerate(self.readers) if r['name'] == reader_name)
            del self.books[reader_index]
            self.library.remove_reader(reader_name)
        except Exception as e:
            print(f"ERROR: something went wrong:\n{e}")


    def search_by_author(self):
        print(f"\nCOMMAND -> search_by_author: ")
        author_name = input_non_empty_string("please enter author name to search: ")
        self.library.search_by_author(author_name)

    def reader_read_book(self):
        print(f"\nCOMMAND -> reader_read_book: ")
        reader_id = input_item_in_list("please enter reader id: " , [str(r.id) for r in self.readers])
        book_title = input_item_in_list("please enter book title: " , [b.title for b in self.books])
        reader = next((r for r in self.readers if r.id == int(reader_id)),None)
        if reader==None:
            return print("ERROR: reader not found")
        reader.read_book(book_title)
    
    def order_all_books(self):
        print(f"\nCOMMAND -> order_all_books: ")
        self.library.order_books()
    
    def save_all_data(self):
        print(f"\nCOMMAND -> save_all_data: ")
        file_name = input_non_empty_string("please enter file name to output data: ")
        with open(path.join(sys.path[0],"output",f"{file_name}.json") , "w") as f:
            json.dump({
                "shelves":[sh for sh in self.library.shelves],
                "readers":[r for r in self.library.readers],
            },f)
            print(f"INFO: data saved succesfully to file {file_name}")
    
    def load_all_data(self):
        print(f"\nCOMMAND -> load_all_data: ")
        file_name = input_non_empty_string("please enter file name to load data from: ")
        try:
            with open(path.join(sys.path[0],"output",f"{file_name}.json") , "r") as f:
                data = json.load(f)
                self.library.shelves = []
                for shelf in data['shelves']:
                    sh = Shelf()
                    for b in shelf['books']:
                        book = Book(b['author'],b['title'],b['num_of_pages'])
                        sh.add_book(book)
                        self.books.append(book)
                for reader in data['readers']:
                    if not reader['id'] in [r.id for r in self.readers]:
                        self.readers.append(Reader(reader['id'],reader['name']))
                        self.library.register_reader(reader['id'] , reader['name'])
        except FileNotFoundError as e:
            print(f"ERROR: file {file_name} not found!")

    def _show_options(self):
            print(f"""
        “For adding a book - Press 1”.
        “For deleting a book - Press 2”.
        “For changing books locations - Press 3”.
        “For registering a new reader - Press 4”.
        “For removing a reader - Press 5”.
        “For searching books by author – Press 6.”
        “For reading a book by a reader – Press 7.”
        “For ordering all books – Press 8.”
        “For saving all data – Press 9”.
        “For loading data – Press 10”.
        “For exit – Press 11”.
        “To show all options – Press 'help'”.
            """)


    def run(self):
        print("WELCOME:")
        self._show_options()
        while True:
            user_select = 0
            while not user_select in [*(str(n) for n in range(1,12)) , 'help']:
                user_select = input_non_empty_string("\nplease enter your choice: [to see all options press 'help'] ")
            match user_select:
                case 'help':self._show_options()
                case '1':self.add_new_book()
                case '2':self.delete_book()
                case '3':self.change_book_location()
                case '4':self.register_reader()
                case '5':self.remove_reader()
                case '6':self.search_by_author()
                case '7':self.reader_read_book()
                case '8':self.order_all_books()
                case '9':self.save_all_data()
                case '10':self.load_all_data()
                case '11':return