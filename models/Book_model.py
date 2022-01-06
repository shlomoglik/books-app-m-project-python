class Book(dict):

    def __init__(self,author:str="" , title:str="" , num_of_pages:int=0) -> None:
        self.author = author
        self.title = title
        self.num_of_pages = num_of_pages
        super().__init__(vars(self))