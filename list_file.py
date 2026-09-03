import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()
 

def list_files(args):
    path = None
    try:
      
      if(len(args) == 0):
          path = os.getcwd()
      else:
          path = args[0]
      
      report.write_log(f"Listing files from the directory {path}")
      
      files = list()

      if not os.path.exists(path):
          raise exceptions.PathNotExist(path=path)
      
      if not os.path.isdir(path):
          raise exceptions.NotADirectoryPath(path=path)
      
      print(path)

      for name in os.listdir(path):
          full_path = os.path.join(path,name)
          # only append file since we have to list files only
          if os.path.isfile(full_path): 
              files.append(name)


      print(f"{len(files)} files present in {path}")

      for i in range(len(files)):
          print(i+1," ",files[i])

      return files
    
    except Exception as e:
        print(e)
        report.write_log(e.__str__()+"\n")

# list_files(os.path.join(os.getcwd(),"test"))

 
# print(type(files)) # type of files object is list
# print(os.path.)

def list_and_dir(path:str=os.getcwd()):
    files = list()
    dir = list()
    try:
      
      for name in os.listdir(path):
          full_path = os.path.join(path,name)
          if os.path.isfile(full_path):
              files.append(name)
          else:
              dir.append(name)

      return {"files":files,"dir":dir}
    
    except PermissionError:
        # print(f"Permission denied {path}")
        report.write_log(f"Permission denied {path}")
        return None
    
    except OSError as e:
        # print(f"Cannot Access{path}")
        report.write_log(f"Cannot Access{path}")
        return None

if __name__ == "__main__":
    list_files()