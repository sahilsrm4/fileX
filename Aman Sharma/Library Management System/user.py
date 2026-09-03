from exceptions import ValidationError

class User:
    MAX_BOOKS = 3
    def __init__(self, user_id, name):

        if not user_id.strip():
            raise ValidationError("User ID cannot be empty")

        if not name.strip():
            raise ValidationError("User name cannot be empty")
        self.user_id = user_id
        self.name = name
        self.borrowed_books = []
    def validate_user(self, user_id, name):
        if (self.user_id) or (self.name) is None:
            print("Enter valid user credentials")

