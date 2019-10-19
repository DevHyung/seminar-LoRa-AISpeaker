class Book:
    """Information about a book"""

    def __init__(self, title="", authors=[], publisher="", isbn="0", price=10.0):
        """(Book, str, list of str, str, str, number) -> NoneType
        Create a new book entitled title, written by the people in authors,
        published by publisher, with ISBN isbn and costing price dollars.
        """
        self.title = title
        self.authors = authors[:]
        self.publisher = publisher
        self.ISBN = isbn
        self.price = price

    def __str__(self):
        """(Book) -> str
        Return a human-readable string representation of this book.
        """
        rep = " Title: {0}\n Authors: {1}\n Publisher: {2}\n ISBN: {3}\n Price: {4}".format(
            self.title, self.authors, self.publisher, self.ISBN, self.price)
        return rep

    def __eq__(self, other):
        """ (Book, Book) -> bool
        Return True iff this book and other have the same ISBN.
        """
        return self.ISBN == other.ISBN
        

    def num_authors(self):
        """(Book) -> int

        Return the number of authors of this book.
        """
        return len(self.authors)


