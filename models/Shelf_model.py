import json
from models.Book_model import Book


class Shelf(dict):
    count = 0
    def __init__(self) -> None:
        self.books:list[Book] = []
        self.is_shelf_full = False
        Shelf.count += 1
        self.number = Shelf.count
        super().__init__(vars(self))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def get_books(self):
        return [b["title"] for b in self["books"]]

    def print_books(self):
        print([f"{b.title} [{b.author}] #{b.num_of_pages} pages" for b in self.books])

    def _test_is_full(self):
        if len(self.books) == 5:
            self.is_shelf_full = True

    def add_book(self, book: Book):
        if self.is_shelf_full:
            return print("no more space in shelf")
        self.books.append(book)
        print(f"INFO: book '{book.title}' was added to shelf #{self.number} in location #{len(self.books)}")
        self._test_is_full()

    def replace_books(self, ind_1: int, ind_2: int):
        if not ind_1 in range(1, 6) or not ind_2 in range(1, 6):
            return print("invalid index [must be 1-5 only]")
        try:
            temp = self.books[ind_1 - 1]
            self.books[ind_1 - 1] = self.books[ind_2 - 1]
            self.books[ind_2 - 1] = temp
            print("INFO: books are now ordered in positions!")
        except Exception:
            return print("ERROR: there is no book in this index")

    def order_books(self):
        self.books = sorted(self.books, key=lambda b: b.num_of_pages )


# demo 1 add
# b1 = Book(author="tolkin", title="lord of rings", num_of_pages=540)
# b2 = Book(author="j.k rolling", title="harry poter", num_of_pages=620)
# sh = Shelf()
# sh.add_book(b1)
# sh.add_book(b2)
# print("init :", end="")
# sh.print_books()

# # demo 2 replace
# sh.replace_books(2, 1)
# print("after replace :", end="")
# sh.print_books()

# # demo 3 sort
# sh.order_books()
# print("after sord :", end="")
# sh.print_books()
