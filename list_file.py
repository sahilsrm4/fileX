import os
from report_gen import Report_Gen

report = Report_Gen()
 

def list_files(args):
    path = None
    if(len(args) == 0):
        path = os.getcwd()
    else:
        path = args[0]
    files = list()
    if not os.path.exists(path):
        print("No such path exist")
        report.write_log(f"No such path exist{path}")
    if not os.path.isdir(path):
        print("The path provided is not a directory")
        report.write_log(f"{path} not a directory")
    print(path)
    for name in os.listdir(path):
        full_path = os.path.join(path,name)
        if os.path.isfile(full_path):
            files.append(name)
    print(f"{len(files)} files present in {path}")
    for i in range(len(files)):
        print(i+1," ",files[i])
    return files

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