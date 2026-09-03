import search_file
import os
import exceptions
from datetime import datetime
from report_gen import Report_Gen

report = Report_Gen()

def file_info(args:list,options:list):
    """
    This function will print the information of file 
    Path of file, Size of file, Time of Creation , Time of modification, Time of last accessed
    
    """
    report.write_log(f"Finding the information of the file{args[0]}\n")
    file = None
    path = None

    try:
        # Parse The arguments
        if(len(args)==1):
            file=args[0]
            path=os.getcwd()
    
        elif(len(args)==2):
            file = args[0]
            path = args[1]
    
            if not os.path.exists(path):
                raise exceptions.PathNotExist(path)
        
        # use search_file function to find the exact path of the file
        result = search_file.search_file([file,path],['-r'])
        
        # if result len is 0 means no result found 
        if not len(result):
             raise exceptions.FileNotExist(file)
        
        file_path = None
        
        # Search into result list to find the exact match because search_file function also return related or partial matching result
        for f in result:
            filename = os.path.basename(f)
            if file == filename:
                file_path = f

        # if no exact file exist we raise error
        if not file_path:
            raise exceptions.ExactFileNotExist(file,result)
        
        info = os.stat(file_path)

        # print the Information of the file
        print("Path: ",file_path)
        print("Size: ",info.st_size," bytes")
        print("Created: ",datetime.fromtimestamp(info.st_ctime))
        print("Modified: ",datetime.fromtimestamp(info.st_mtime))
        print("Accessed: ",datetime.fromtimestamp(info.st_atime))

        # Write information into logs
        report.write_log(f"File information is:\nPath:{file_path}\nSize:{info.st_size} bytes\nCreated:{datetime.fromtimestamp(info.st_ctime)}\nModified:{datetime.fromtimestamp(info.st_mtime)}\nAccessed:{datetime.fromtimestamp(info.st_atime)}\n")

    except Exception as e:
        print(e)
        report.write_log(e.__str__()+"\n")

 


if __name__ == "__main__":
   file_info("test.txt")

