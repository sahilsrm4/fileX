from exceptions import BookAlreadyAvailableError, BookAlreadyBorrowedError, ValidationError

class Book:
    def __init__(self, book_id, title, author):

        if not book_id.strip():
            raise ValidationError("Book ID cannot be empty")

        if not title.strip():
            raise ValidationError("Enter a valid Book Title")

        if not author.strip():
            raise ValidationError("Enter a valid Author")
        self.book_id = book_id.strip()
        self.title = title.strip()
        self.author = author.strip()
        self.status = "AVAILABLE"
        self.borrowed_by = None

    def borrow(self, borrower):
        if self.status == "AVAILABLE":
            self.borrowed_by = borrower
            self.status = "BORROWED"
        else:
            raise BookAlreadyBorrowedError("Book is already borrowed..!")

    def return_book(self):
        if self.status == "BORROWED":
            self.borrowed_by = None
            self.status = "AVAILABLE"
        else:
            raise BookAlreadyAvailableError("The Book is already Available in the library..!")
