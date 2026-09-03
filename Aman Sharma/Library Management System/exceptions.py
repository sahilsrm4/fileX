class LibraryError(Exception):
    pass

class BookNotFoundError(LibraryError):
    pass

class DuplicateBookError(LibraryError):
    pass

class BookAlreadyBorrowedError(LibraryError):
    pass

class BookAlreadyAvailableError(LibraryError):
    pass

class DuplicateUserError(LibraryError):
    pass

class UserNotFoundError(LibraryError):
    pass

class BorrowLimitExceededError(LibraryError):
    pass

class UserHasBorrowedBooksError(LibraryError):
    pass

class ValidationError(LibraryError):
    pass