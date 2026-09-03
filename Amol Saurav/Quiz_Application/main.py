from services.authentication import Authentication
from services.quiz import Quiz
from models.player import Player
from models.questions import Questions
import json
import getpass 

def display_main_menu():
    print("\n")
    print("1. Register Player")
    print("2. Player Login")
    print("3. Admin Login")
    print("4. Exit")

def take_user_input():
    while True:
        try:
            user_choice = int(input("Enter your choice : ").strip())
            if 1<=user_choice<=4:
                return user_choice
            else:
                print("Please enter valid option")
        except ValueError:
            print("Invalid Input! Please enter valid option.")
            
def display_player_menu():
    print("\n")
    print("1. Start Quiz")
    print("2. View My Result")
    print("3. View Leaderboard")
    print("4. Logout")

def display_question_category():
    try:
        with open("data\\questions.json") as file:
            data = json.load(file)
            for cat in data['categories']:
                print(cat['name'])
    except (FileNotFoundError,json.JSONDecodeError,KeyError):
        print("Somethig went Wrong can't load questions")
        return False
        

print("========== QUIZ APPLICATION ==========")
authenticate = Authentication()
quiz = Quiz()

while True:
    display_main_menu()
    user_input = take_user_input()
    if user_input==1:
        try:
            username = input("Enter your Username : ")
            password = getpass.getpass("Enter Password : ")
            player = Player(username,password)
            authenticate.register_player(player)
        except Exception as e:
            print(f"Something went wrong during registration: {e}")

    elif user_input==2:
        try:
            username = input("Enter Username : ")
            password = getpass.getpass("Enter Password : ")
            current_player = authenticate.login_player(username,password)
            
            while current_player:
                display_player_menu()
                player_input = take_user_input()
                if player_input ==1 :
                    display_question_category()
                    category = input("Select Question Category for Quiz : ").strip()
                    quiz.start_quiz(current_player,category)
                
                elif player_input ==2:
                    quiz.get_result(current_player)
                
                elif player_input ==3:
                    quiz.get_leaderboard()
                
                elif player_input ==4 : 
                    current_player = None
                    break
        except Exception as e:
            print(f"Something went wrong during the player session: {e}")
            
    elif user_input==3:
        try:
            password = getpass.getpass("Enter your Password : ")
            is_admin = authenticate.login_admin(password)
            while is_admin:
                print("1. Add Question")
                print("2. Logout")
                while True:
                    try:
                        admin_input = int(input("Enter your choice : ").strip())
                        if 1<=admin_input<=2:
                            break
                    except ValueError:
                        print("Please Select Valid Option")
                if admin_input==1:
                    category = input("Enter the question Category : ").strip()
                    question = input("Enter question in ....? format : \n")
                    print("Enter options for this question : \n")
                    options = []
                    for i in range(0,4):
                        option = input(f"option {i+1} : ")
                        options.append(option)
                    correct_answer = input("Enter the correct answer for this question : ")
                    question_obj = Questions(question,options,correct_answer,category)
                    quiz.add_question(question_obj,category)
                
                if admin_input==2:
                    print("Logged Out")
                    is_admin = False
                    break

            else:
                print("You are not authorize for this Action")
        except Exception as e:
            print(f"Something went wrong during the admin session: {e}")

    elif user_input==4:
        print("THANKYOU VISIT AGAIN ")
        break
