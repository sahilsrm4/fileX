def validate_question(text: str):
    if text is None:
        return False

    cleaned_text = text.strip()

    if cleaned_text == "":
        print("Question can't be empty")
        return False

    words = cleaned_text.split()
    if len(words) < 5:
        print("Question is too short")
        return False

    if len(words) > 100:
        print("Question is too long")
        return False

    if "  " in cleaned_text:
        print("Question contains extra spaces")
        return False

    return True


def validate_options(options: list):
    if not isinstance(options, list):
        print("Options must be a list")
        return False

    if len(options) != 4:
        print("Question must have exactly 4 options")
        return False

    for option in options:
        if not isinstance(option, str):
            print("Each option must be a string")
            return False
        if option.strip() == "":
            print("Options cannot be empty")
            return False

    normalized = [opt.strip().lower() for opt in options]
    if len(set(normalized)) != len(normalized):
        print("Options cannot be duplicate")
        return False

    return True


def validate_correct_answer(options: list, correct_answer: str):
    if correct_answer is None:
        print("Correct answer cannot be None")
        return False

    if not isinstance(correct_answer, str):
        print("Correct answer must be a string")
        return False

    if correct_answer.strip() == "":
        print("Correct answer cannot be empty")
        return False

    if correct_answer.strip() not in [opt.strip() for opt in options]:
        print("Correct answer must be one of the options")
        return False

    return True


def validate_answer(correct_answer, answer):
    if answer is None:
        return False

    if not isinstance(answer, str):
        return False

    return correct_answer.strip().lower() == answer.strip().lower()

def validate_category(category:str):
    if category is None:
        return False
    
    if not isinstance(category,str):
        print("Category must be an string")
        return False
    
    cleaned_category = category.strip()
    
    if cleaned_category=="":
        print("Category can't be empty")
        return False
    
    return True

def validate_login(player):
    if player is None:
        return False
    if not hasattr(player,"is_logged_in"):
        return False
    return player.is_logged_in

def validate_username(username):
    if username is None:
        print("Username can't be Empty")
        return False
    
    if not isinstance(username,str):
        print("Username must be a string")
        return False
    
    if username.strip()=="":
        print("Username can't be empty")
        return False
    return True

def validate_password(password):
    if password is None:
        print("Password can't be Empty")
        return False
    
    if password.strip() == "":
        print("Password can't be Empty")
        return False
    
    if not isinstance(password,str):
        print("Password must be an string")
        return False
    
    return True
 
    