import os
import list_file
import exceptions
from report_gen import Report_Gen

report = Report_Gen()

def search_file(args:list=[],options:list=[]):
     file = None
     path = None
     try:
        if(len(args)==1):
            file=args[0]
            path=os.getcwd()
        elif(len(args)==2):
            file = args[0]
            path = args[1]
   
        search_result = list()
   
        if len(path) > 260:
            raise exceptions.PathLengthGreaterThan260
        
        if not os.path.exists(path):
            raise exceptions.PathNotExist(path)
        
        file_dir= list_file.list_and_dir(path)
   
        files = None
        dir = None
   
        if file_dir:
            files = file_dir["files"]
            dir = file_dir["dir"]
   
            for f in files:
                if file in f:
                     search_result.append(f)
   
            for d in dir:
               result = search_file([file, d ],options)
               search_result.extend(result)

     except exceptions.PathNotExist as e:
         print(e)
         report.write_log(e)

     except exceptions.PathLengthGreaterThan260 as e:
         # i have to handle this error so that i can search for bigger paths also for now i am returning an emptyh list
         return []
         
         
     return search_result

def search_print_file(args:list=[],options:list=[]):
    try:
      result = search_file(args)
      
      if(len(result)==0):
        raise exceptions.FileNotExist(args[0])
      
      else:
        print("Search result :")
        print(result)
        return result
    
    except Exception as e:
        print(e)
        report.write_log(e.__str__()+"\n")
        return []

if __name__ == "__main__":
   result = search_file(["rocket.obj"])
   if(len(result)==0):
       print("No such file exist")
   else:
       print("Search Result")
       print(result)
