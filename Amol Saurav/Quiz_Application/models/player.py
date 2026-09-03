class Player:
    
    def __init__(self,username,password):
        self.id = None
        self.username = username
        self.password = password
        self.score = 0
        self.answers = []
        self.is_logged_in = False
    
    def reset_score(self):
        self.score = 0
    
    def reset_answers(self):
        self.answers = []
    