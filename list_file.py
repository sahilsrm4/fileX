import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()
 

def list_files(args:list=[],options:list=[]):
    """
    This function will list the files in the provided path
    This will only list files not the directory paths

    """
    path = None
    try:
      # Argumnents parsing

      if(len(args) == 0):
          path = os.getcwd() # if not path is provided  current directory path is used
      else:
          path = args[0]
      
      report.write_log(f"Listing files from the directory {path}")
      
      files = list()

      # Path validation

      if not os.path.exists(path):
          raise exceptions.PathNotExist(path=path)
      
      if not os.path.isdir(path):
          raise exceptions.NotADirectoryPath(path=path)
      
      print(path)
      
      # Iterator through the directory items
      for name in os.listdir(path):
          full_path = os.path.join(path,name)

          # only append file since we have to list files only
          if os.path.isfile(full_path): 
              files.append(name)

      # Print the listed files
      print(f"{len(files)} files present in {path}")

      for i in range(len(files)):
          print(i+1," ",files[i])

      return files
    
    except Exception as e:
        print(e)
        report.write_log(e.__str__()+"\n")

 
def list_and_dir(path:str=os.getcwd()):
    """
     This function will return a dictionary containing files and directory list 

    """
    files = list()
    dir = list()

    try:
      
      # Path validation
      if os.path.isdir(path):
          raise exceptions.NotADirectoryPath(path)
      
      # Iterate through the directory
      for name in os.listdir(path):
          
          full_path = os.path.join(path,name)

          # if file append to files
          if os.path.isfile(full_path):
              files.append(full_path)

          # if not file append to dir (directory)
          else:
              dir.append(full_path)

      return {"files":files,"dir":dir}
    
    except PermissionError:
        # print(f"Permission denied {path}")
        report.write_log(f"Permission denied {path}")
        return None
    
    except OSError as e:
        # print(f"Cannot Access{path}")
        report.write_log(f"Cannot Access{path}")
        return None
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    list_files()