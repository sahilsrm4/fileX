import os
import list_file
import exceptions
from report_gen import Report_Gen

report = Report_Gen()

def search_file(args:list=[],options:list=[]):
     """
     This function will search file in the same direcotry and in child directory if -r or --recursive option is provided
     Also return partial matching result
     """
     file = None
     path = None
     recursive = False
     search_result = list()

     try:
        # Parse the arguments
        if(len(args)==1):
            file=args[0]
            path=os.getcwd()
        elif(len(args)==2):
            file = args[0]
            path = args[1]
        
        # Prase the options
        if options:
          if(options[0]=='-r' or options[0] == "--recursive"):
              recursive = True
        
        # validate Path
        if len(path) > 260:
            raise exceptions.PathLengthGreaterThan260
        
        if not os.path.exists(path):
            raise exceptions.PathNotExist(path)
        
        if not os.path.isdir(path):
            raise exceptions.NotADirectoryPath(path)
        
        # The below code with combine the path and search_pattern if it exist it will be returned directly without going down
        temp_full_path = os.path.join(path,file)
        if os.path.exists(temp_full_path):
             search_result.append(temp_full_path) 
             return search_result
        
        # This function will give file and directory seprated from the provided path
        file_dir= list_file.list_and_dir(path)
   
        files = None
        dir = None
        
        # if file_dir is not empty we will seperate files and directory from it
        if file_dir:

            files = file_dir["files"]
            dir = file_dir["dir"]

            # Iterate throgh the files and match the file
            for f in files:
                if file in f:
                     search_result.append(f)
            
            # Iterate throught the directory
            for d in dir:
               
               # if recursive is true then go into the child directories
               if recursive:
                   if file in d:
                       search_result.append(d)

                   result = search_file([file, d ],options)
                   search_result.extend(result)

               # if recursive is not true the match pattern to directory path 
               else:
                   if file in d:
                       search_result.append(d)

     except exceptions.PathNotExist as e:
         print(e)
         report.write_log(e)

     except exceptions.PathLengthGreaterThan260 as e:
         # i have to handle this error so that i can search for bigger paths also for now i am returning an emptyh list
         return search_result
     except Exception as e:
         print(e)
         
     return search_result

def search_print_file(args:list=[],options:list=[]):
    """
    This function will be used to first search the result using search_file function and then print
    the results
    """
    try:
      result = search_file(args,options)
      
      # If result length is zero it means no such file exist
      if(len(result)==0):
        raise exceptions.FileNotExist(args[0])
      
      # Print the search result
      else:
        print("Search result :")
        for r in result:
            print(r)
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
