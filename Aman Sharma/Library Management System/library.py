from book import Book
from user import User
from exceptions import (
    LibraryError,
    BookNotFoundError,
    DuplicateBookError,
    BookAlreadyBorrowedError,
    DuplicateUserError,
    UserNotFoundError,
    BorrowLimitExceededError,
    UserHasBorrowedBooksError
)
import json

class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.borrowing_history = []

    # Book Management
    def add_book(self, book):
        if isinstance(book, Book ):
            if book.book_id in self.books:
                raise DuplicateBookError("Book already exists")
            
            self.books[book.book_id] = book
            self.auto_save()
                
        else:
            raise TypeError("Invalid Object type")

    def remove_book(self, book_id):
        if book_id in self.books:
            book = self.books[book_id]
            if book.status == "AVAILABLE":
                del self.books[book_id]
                self.auto_save()
            else:
                raise BookAlreadyBorrowedError("Cannot remove a borrowed book")
        else:
            raise BookNotFoundError("Book does not exist..! ")

    def search_book(self, query):
        if query.strip() == "":
            return []
        normalized_query = query.strip().lower()
        result = []
        for book in self.books.values():
            if (normalized_query in book.book_id.lower()) or (normalized_query in book.title.lower()) or (normalized_query in book.author.lower()):
                result.append(book)

        return result


    # User Management
    def add_user(self, user):
        if isinstance(user, User):
            if user.user_id in self.users:
                raise DuplicateUserError("User Already Exists")
                    
            self.users[user.user_id] = user
            self.auto_save()
        else:
            raise TypeError("Invalid Object Type")
                
    def find_user(self, user_id):
        if user_id in self.users:
            return self.users[user_id]
        else:
            raise UserNotFoundError("User does not exist..!")

    def remove_user(self, user_id):
        if user_id not in self.users:
            raise UserNotFoundError("User does not exist..!")

        user = self.users[user_id]

        if user.borrowed_books:
            raise UserHasBorrowedBooksError(
                "Cannot remove a user with borrowed books"
            )
        del self.users[user_id]
        self.auto_save()
        
    # Borrowing
    def borrow_book(self, book_id, user_id):
        if book_id not in self.books:
            raise BookNotFoundError("Book does not exist..!")
        user = self.find_user(user_id)
        book = self.books[book_id]

        if len(user.borrowed_books) >= User.MAX_BOOKS:
            raise BorrowLimitExceededError(
                "User has reached the maximum borrowing limit"
            )

        book.borrow(user_id)

        user.borrowed_books.append(book_id)

        borrowing_dict = {
            "book_id" : book_id,
            "borrower" : user_id,
            "action": "BORROW"
        }

        self.borrowing_history.append(borrowing_dict)
        self.auto_save()
            

    def return_book(self, book_id):
        if book_id not in self.books:
            raise BookNotFoundError("Book does not exist..!")
        book = self.books[book_id]
        user_id = book.borrowed_by
        book.return_book()

        if user_id in self.users:
            user = self.users[user_id]

            if book_id in user.borrowed_books:
                user.borrowed_books.remove(book_id)

        borrowing_dict = {
            "book_id" : book_id,
            "borrower" : user_id,
            "action" : "RETURN"
        }
        self.borrowing_history.append(borrowing_dict)
        self.auto_save()

    def get_available_books(self):
        result = []
        for book in self.books.values():
            if book.status == "AVAILABLE":
                result.append(book)
        return result

    def get_borrowed_books(self):
        result = []
        for book in self.books.values():
            if book.status == "BORROWED":
                result.append(book)
        return result

    def get_borrowing_history(self):
        return self.borrowing_history

    def save_library(self, filename):
        library_data = {
            "books": [],
            "users": [],
            "borrowing_history": self.borrowing_history
        }

        for book in self.books.values():
            book_data = {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "status": book.status,
                "borrowed_by": book.borrowed_by
            }

            library_data["books"].append(book_data)

        for user in self.users.values():
            user_data = {
                "user_id": user.user_id,
                "name": user.name,
                "borrowed_books": user.borrowed_books
            }

            library_data["users"].append(user_data)

        with open(filename, "w") as file:
            json.dump(library_data, file, indent=4)

    def auto_save(self):
        self.save_library("library.json")

    def load_library(self, filename):
        try:
            with open(filename, "r") as file:
                library_data = json.load(file)
        except json.JSONDecodeError:
            raise LibraryError("Invalid library file")

        self.books = {}
        self.users = {}

        for book_data in library_data["books"]:
            book = Book(
                book_id=book_data["book_id"],
                title=book_data["title"],
                author=book_data["author"]
            )
            book.status = book_data["status"]
            book.borrowed_by = book_data["borrowed_by"]
            self.books[book.book_id] = book

        for user_data in library_data["users"]:
            user = User(
                user_id=user_data["user_id"],
                name=user_data["name"]
            )
            user.borrowed_books = user_data["borrowed_books"]
            self.users[user.user_id] = user
        self.borrowing_history = library_data["borrowing_history"]