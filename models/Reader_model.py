from datetime import datetime
import json


class Reader(dict):

    def __init__(self, id: int, name: str) -> None:
        self.name = name
        self.id = id
        self.books = []
        super().__init__(vars(self))

    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self) -> str:
        return f"Reader {self.id} -> read {len(self.books)} books"

    def show_readings(self, title: None | str = None):
        for b in self.books:
            if title == None or title == b.title:
                print(f"INFO: book : {b.title} has been read on:")
                for t in b["dates"]:
                    print(t.strftime("%d/%m/%y %H:%M"))

    def read_book(self, title):
        now = datetime.now()
        find_books = [b for b in self.books if b["title"] == title]
        if len(find_books) == 0:
            self.books.append({"title": title, "dates": [now]})
        else:
            find_books[0]["dates"].append(now)
        print(f"INFO: book {title} has been mark as read at : {now}")
        # self.show_readings(title) # THINK: which one to use


# # demo 1
# r = Reader(1)
# print(r)

# # demo2 append book
# r.read_book("lord of the rings")
# r.read_book("lord of the rings")
# r.read_book("lord of the rings")
# r.read_book("period numbers")
# print(r)

# print(r.show_readings())