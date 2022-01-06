from os import remove
from posixpath import join
from models.Book_model import Book
from models.Reader_model import Reader
from models.Shelf_model import Shelf


class Library(dict):

    def __init__(self, shelves: list[Shelf], readers: list[str]) -> None:
        self.shelves = shelves
        self.readers = readers
        super().__init__(vars(self))

    def is_there_place_for_new_book(self):
        return all(sh.is_shelf_full for sh in self.shelves)

    def add_new_book(self, book: Book):
        """
        receives a new Book object 
        and add it to the first Shelf with a free space
        """
        for sh in self.shelves:
            if not sh.is_shelf_full:
                return sh.add_book(book)
        print("ERROR: sorry there is not place for this book")

    def delete_book(self, book_title):
        for sh in self.shelves:
            for i, b in enumerate(sh.books):
                if b.title == book_title:
                    del sh.books[i]
                    return print(f"INFO: {book_title} was succesfully deleted!")
        print(f"ERROR: book {book_title} not found!")

    def change_locations(self, book_1_title, book_2_title):
        """
        receives 2 books titles, and replace between these 2 Books
        objects (their locations in the shelves).
        """
        book_1 = None
        book_2 = None
        errors = []
        for sh in self.shelves:
            for i, b in enumerate(sh.books):
                if book_1 == None and b['title'] == book_1_title:
                    book_1 = {'shelf': sh, 'location': i , 'book' : b}
                if book_2 == None and b['title'] == book_2_title:
                    book_2 = {'shelf': sh, 'location': i , 'book' : b}
        if book_1 ==None:
            errors.append(f"no book called '{book_1_title}' was found")
        if book_2 == None:
            errors.append(f"no book called '{book_2_title}' was found")
        if len(errors)>0:
            return print("ERROR: \n\t" + f"\n\t".join(errors))
        try:
            temp = book_1["book"]
            book_1["shelf"].books[book_1["location"]] = book_2["book"]
            book_2["shelf"].books[book_2["location"]] = temp
            print("INFO: books are now ordered in positions!")
        except Exception as e:
            print(f"ERROR: there is an error on 'Library.change_location':\n{e}")

    def change_locations_in_same_shelf(self , shelf_number , book_1_location , book_2_location):
        self.shelves[shelf_number-1].replace_books(book_1_location,book_2_location)

    def order_books(self):
        for sh in self.shelves:
            sh.order_books()
        print("INFO: all books are now ordered!")

    def register_reader(self,id:int,name:str):
        if name in self.readers:
            return print("ERROR: reader already exists.")
        r = Reader(id,name)
        self.readers.append(name)
        return print("INFO: reader has been register succesfully!")

    def remove_reader(self,name):
        try:
            self.readers.remove(name)
            print(f"INFO: user {name} deleted succesfully!")
        except ValueError:
            print("ERROR: user not found")

    # def reader_read_book(self , book_title , name):
    #     #TODO: get reader by name ?
    #     r = Reader(0,name) 
    #     r.read_book(book_title)

    def search_by_author(self , author):
        result = []
        for sh in self.shelves:
            for b in sh.books:
                if b.author == author:
                    result.append(f"book: '{b.title}' [{b.num_of_pages} pages]")
        print(f"INFO: {len(result)} books found for author {author}\n\t" + "\n\t".join(result))