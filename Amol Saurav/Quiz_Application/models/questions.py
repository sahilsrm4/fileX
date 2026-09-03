class Questions:
    
    def __init__(self,question : str, options : list, correct_answer : str, category : str):
        self._id =None
        self._question = question
        self._options = options
        self._correct_answer = correct_answer
        self._category = category
    
    @property
    def question(self):
        return self._question
    
    @property
    def options(self):
        return self._options
    
    @property
    def category(self):
        return self._category
    
    @property
    def correct_answer(self):
        return self._correct_answer    
        