import os
import datetime
import exceptions

class Report_Gen:
    _instance = None
    _inialized = False
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance
    
    def __init__(self):
        if self._inialized:
            return
        
        os.makedirs("log_folder", exist_ok=True)
        
        self.file_name = self.file_name = datetime.datetime.now().strftime("log_%Y-%m-%d_%H-%M-%S.log")
        self.file = open(os.path.join("log_folder",self.file_name),"w")  
    
    def write_log(self,log:str):
        
        # Uncomment below code for debugging
        # if not isinstance(log,str):
        #     raise exceptions.NotString(f"write_log function require string but {type(log)} is given")
        
        self.file.write(log)
    
    def close(self):
        self.file.close()

    