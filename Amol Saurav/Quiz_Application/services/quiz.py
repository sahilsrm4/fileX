import json,copy
from models.questions import Questions
from models.player import Player
import random 
from utils.validation import *

class Quiz:
    
    def __init__(self):
        self.questions = []
        self.result = []
    
    def load_questions_by_category(self,category:str):
        self.questions.clear()
        category_found = False
        try:
            with open("data\\questions.json",'r') as file:
                data = json.load(file)
                
                for cat in data['categories'] :
                    if cat['name'].lower()==category.lower():
                        category_found = True
                        for que in cat['questions']:
                           question_obj = Questions(
                               question=que['question'],
                               options=que['options'],
                               correct_answer=que['correct_answer'],
                               category=cat['name']
                           )
                           question_obj._id = que["id"]
                           self.questions.append(question_obj)
                        break
        except Exception as e:                
                print(e)
                return False
        return category_found
    
    def _generate_question_id(self,data):
        question_ids = []
        
        for category in data['categories']:
            for question in category["questions"]:
                question_ids.append(question["id"])
        
        if not question_ids:
            return 1
        return max(question_ids)+1
    
    def add_question(self,question:Questions,category):
        if validate_category(category) and validate_question(question.question) and validate_options(question.options) and validate_correct_answer(question.options,question.correct_answer):
            self.load_questions_by_category(category)
            normalized_question  = question.question.strip().lower()
            for que in self.questions:
                if que.question.strip().lower()==normalized_question:
                    print("This question already exists in this category")
                    return False
            try:
                with open("data\\questions.json",'r') as file:
                    que_data = json.load(file)
                    new_question_id = self._generate_question_id(que_data)
            except (FileNotFoundError,json.JSONDecodeError):
                print("Can't read file")
                return False
            question._id = new_question_id    
    
            category_found = False
            
            for cat in que_data["categories"]:
                if cat["name"].lower() == category.lower():
                    cat["questions"].append({
                        "id": new_question_id,
                        "question": question.question,
                        "options": question.options,
                        "correct_answer": question.correct_answer
                    })
                    category_found = True
                    break

            if not category_found:
                que_data["categories"].append({
                    "name": category,
                    "questions": [{
                        "id": new_question_id,
                        "question": question.question,
                        "options": question.options,
                        "correct_answer": question.correct_answer
                    }]
                })
            try:
                with open("data\\questions.json",'w') as file:
                    json.dump(que_data,file,indent=4)
                    
            except Exception as e:
                print(f"Could not save question : {e}")
                return False

            self.questions.append(question)
            return True
            
        else:
            return False
        
    
    def display_question(self,question:Questions,question_number:int):
        if question is None:
            return 
        
        print(f"Category : {question.category}")
        
        print(f"{question_number}. {question.question}")
        
        for i,option in enumerate(question.options,start=1):
            print(f"{i}. {option}")


    def start_quiz(self,player:Player,category):
        if not validate_login(player):
            print("Login Required")
            return False
        player.reset_answers()
        category_found = self.load_questions_by_category(category)
        
        if not category_found:
            print(f"Cateogy : {category} doesn't exist. Please choose a valid category")
            return False
        
        if not self.questions:
            print(f"Category : {category} has no questions yet.")
            return False
        
        current_questions = copy.deepcopy(self.questions)
        random.shuffle(current_questions)
        
        for question_number,question in enumerate(current_questions,start=1):
            self.display_question(question,question_number)
            
            while True:
                try:
                    user_choice = int(input("Enter option from 1 to 4 : ").strip())
                    if 1<=user_choice<=4:
                        break
                    else:
                        print("Please enter valid option")
                except ValueError:
                    print("Invalid Input! Please enter valid option.")
            
            is_correct = self.submit_answer(question,user_choice)
            
            result_entry = {
                "Question_number": question_number,
                "Question_id":question._id,
                "Selected_answer":question.options[user_choice-1],
                "Correct_answer":question.correct_answer,
                "is_correct":is_correct
            }
            
            player.answers.append(result_entry)
            
        self.calculate_score(player)
        self.result = {
            "Player": player.username,
            "Score": player.score,
            "Questions Attempted": len(player.answers),
            "Answers": player.answers
        }

        self.save_results(player.username)

        return self.get_result(player)
    
    
    def submit_answer(self,question:Questions,answer:int):
        return validate_answer(question.correct_answer,question.options[answer-1])
    
    def calculate_score(self,player:Player):
        player.reset_score()
        for item in player.answers:
            if item['is_correct']:
                player.score+=1
    
    def get_result(self,player:Player):
        results = self.load_results()

        for result in results:

            if result["Player"] == player.username:
                attempts = result["Attempts"] or []
                
                if not attempts:
                    print(f"No attempts found for {player.username}")
                    return None
                
                '''Dispaly result of the recent attempt'''
                                
                print("\n========== RESULT ==========")
                print(f"Player: {result['Player']}")
                print(
                    f"Score: {attempts[-1]['Score']}/"
                    f"{attempts[-1]['Questions Attempted']}"
                )

                print("\nAnswer Summary:")
                for answer in attempts[-1]["Answers"]:

                    status = (
                        "Correct"
                        if answer["is_correct"]
                        else "Incorrect"
                    )

                    print(
                        f"Question {answer['Question_number']}: "
                        f"Your answer = {answer['Selected_answer']}, "
                        f"Correct answer = {answer['Correct_answer']}, "
                        f"Status = {status}"
                    )

                return result

        print("No result found for this player.")
        return None

    def get_leaderboard(self):
        results = self.load_results()
        if not results:
            print("No Leaderboard Available")
            return []
        
        leaderboard = []
        
        for record in results:
            player_name = record["Player"]
            attempts = record["Attempts"]
            
            if not attempts:
                continue
            
            best_score = 0
            
            for a in attempts:
                if isinstance(a,dict) and "Score" in a:
                    score = int(a["Score"])
                    best_score = max(score,best_score)
            
            leaderboard.append({
                "Player":player_name,
                "Score":best_score
            })
        sorted_results = sorted(
            leaderboard,
            key = lambda r: (-int(r['Score']),r["Player"].lower())
        )
        
        print("Leaderboard:")
        rank=0
        previous_score = None
        
        for position,item in enumerate(sorted_results,start=1):
            if item["Score"] !=previous_score:
                rank = position
                previous_score = item["Score"]
            print(f"{rank}. {item['Player']} - {item['Score']}")
    
    def save_results(self,username):
        try:
            if not self.result:
                return
            attempt_data = {
                "attempt":1,
                "Score" : self.result["Score"],
                "Questions Attempted":self.result["Questions Attempted"],
                "Answers":self.result["Answers"]
            }
            data = self.load_results()
            
            user_record = None
            for record in data:
                if record["Player"]==username:
                    user_record = record
                    break
            
            if user_record is None:
                user_record = {
                    "Player":username,
                    "Attempts":[]
                }
                data.append(user_record)
            
            attempt_data["attempt"] = len(user_record["Attempts"])+1
            user_record["Attempts"].append(attempt_data)
            
            with open("data\\results.json",'w') as file:
                json.dump(data,file,indent=4)
    
        except Exception as e:
            print(e)
    
    def load_results(self):
        try:
            with open("data\\results.json","r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        return data