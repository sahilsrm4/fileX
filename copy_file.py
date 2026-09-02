import shutil
import os
from report_gen import Report_Gen

report = Report_Gen()

def copy_file(args:list):
    src = args[0]
    dest = args[1]
    report.write_log(f"Copying {src} to {dest}\n")
    if not os.path.exists(src):
       print("Source path does not exist")
       report.write_log("Source path does not exist\n")
       return
    if not os.path.exists(dest):
       print("Destination path does not exist")
       report.write_log("Destination Path does not Exist\n")
       return 
    if not os.path.isfile(src):
       print("Source should be a file")
       report.write_log("Source is not a file")
       return 
    if not os.path.isdir(dest):
       print("Destination should be a directory")
       report.write_log("Destination is not a directory")
       return 
    try:
      shutil.copy(src,dest)
    except FileNotFoundError:
       print("Please provide either the right relative path or the exact path of the file")
       report.write_log("Relative or abolute path is not correct\n")
       return
    except Exception as e:
       print(f"Error {e}")
       return
    report.write_log("Copied Successfully\n")
    print("Copied")



if __name__ == "__main__":
    # copy_file("test\\test.txt","new_directory")
    pass