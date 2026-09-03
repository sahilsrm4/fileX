import os
from library import Library
from book import Book
from user import User
from exceptions import LibraryError

def display_menu():
    print("\n" + "=" * 40)
    print("       LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)

    print("1. Add Book")
    print("2. Remove Book")
    print("3. Search Book")
    print("4. Add User")
    print("5. Remove User")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. View Available Books")
    print("9. View Borrowed Books")
    print("10. View Borrowing History")
    print("11. Save Library")
    print("12. Load Library")
    print("0. Exit")

    print("=" * 40)



def main():
    library = Library()

    # Loads the library data automatically
    if os.path.exists("library.json"):
        print("Loading Library Data...")
        try:
            library.load_library("library.json")
            
            print("Library Loaded Successfully!")
        except(OSError, LibraryError) as e:
            print(f"Could not load library: {e}")
    
    while True:
        display_menu()

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Exiting Library Management System...")
            break

        elif choice == "1":
            print("\n--- Add Book ---")

            book_id = input("Enter Book ID: ")
            title = input("Enter Book Title: ")
            author = input("Enter Book Author: ")

            try:
                book = Book(book_id, title, author)
                library.add_book(book)
                print("Book added successfully!")

            except LibraryError as e:
                print(f"{e}")

        elif choice == "2":
            print("\n--- Remove Book ---")

            book_id = input("Enter Book ID: ")
            try:
                library.remove_book(book_id)
                print("Book Removed  Successfully!")
            except LibraryError as e:
                print(f"{e}")


        elif choice == "3":
            print("\n--- Search Book ---")

            query = input("Enter search query: ")

            try:
                results = library.search_book(query)

                if not results:
                    print("No books found.")

                else:
                    print("\nBooks Found:")
                    for book in results:
                        print(
                            f"{book.book_id} | "
                            f"{book.title} | "
                            f"{book.author} | "
                            f"{book.status}"
                        )

            except LibraryError as e:
                print(f"{e}")


        elif choice == "4":
            print("\n--- Add User ---")

            user_id = input("Enter User ID: ")
            name = input("Enter User Name: ")

            try:
                user = User(user_id, name)
                library.add_user(user)
                print("User added successfully!")

            except LibraryError as e:
                print(f"{e}")

        elif choice == "5":
            print("\n--- Remove User ---")

            user_id = input("Enter User ID: ")

            try:
                library.remove_user(user_id)
                print("User removed successfully!")

            except LibraryError as e:
                print(f"{e}")

        elif choice == "6":
            print("\n--- Borrow Book ---")

            book_id = input("Enter Book ID: ")
            user_id = input("Enter User ID: ")

            try:
                library.borrow_book(book_id, user_id)
                print("Book borrowed successfully!")

            except LibraryError as e:
                print(f"{e}")

        elif choice == "7":
            print("\n--- Return Book ---")

            book_id = input("Enter Book ID: ")

            try:
                library.return_book(book_id)
                print("Book returned successfully!")

            except LibraryError as e:
                print(f"{e}")

        elif choice == "8":
            print("\n--- Available Books ---")

            books = library.get_available_books()

            if not books:
                print("No available books.")

            else:
                for book in books:
                    print(
                        f"{book.book_id} | "
                        f"{book.title} | "
                        f"{book.author}"
                    )

        elif choice == "9":
            print("\n--- Borrowed Books ---")

            books = library.get_borrowed_books()

            if not books:
                print("No borrowed books.")

            else:
                for book in books:
                    print(
                        f"{book.book_id} | "
                        f"{book.title} | "
                        f"{book.author} | "
                        f"Borrowed By: {book.borrowed_by}"
                    )

        elif choice == "10":
            print("\n--- Borrowing History ---")

            history = library.get_borrowing_history()

            if not history:
                print("No borrowing history found.")

            else:
                for record in history:
                    print(
                        f"{record['borrower']} | "
                        f"{record['book_id']} | "
                        f"{record['action']}"
                    )

        elif choice == "11":
            print("\n--- Save Library ---")

            filename = input("Enter filename: ")

            try:
                library.save_library(filename)
                print("Library saved successfully!")

            except (OSError, LibraryError) as e:
                print(f"{e}")

        elif choice == "12":
            print("\n--- Load Library ---")

            filename = input("Enter filename: ")

            try:
                library.load_library(filename)
                print("Library loaded successfully!")

            except (OSError, LibraryError) as e:
                print(f"{e}")

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()