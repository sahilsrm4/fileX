import shutil
import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()

def copy_file(args:list,options:list):
    src = args[0]
    dest = args[1]
    report.write_log(f"Copying {src} to {dest}\n")

    try:
      if not os.path.exists(src):
         raise exceptions.SourcePathNotExist(src)
      
      if not os.path.exists(dest):
          raise exceptions.DestinationPathNotExist(dest)
      
      if not os.path.isfile(src):
          raise exceptions.NotAFilePath(src)
      
      if not os.path.isdir(dest):
         raise exceptions.NotADirectoryPath(dest)
      
      shutil.copy(src=src,dst=dest)

    except Exception as e:
        print(e)
        report.write_log(e.__str__()+"\n")
    else:
      report.write_log("Copied Successfully\n")
      print("Copied")



if __name__ == "__main__":
    # copy_file("test\\test.txt","new_directory")
    pass