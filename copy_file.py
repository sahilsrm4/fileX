import shutil
import os
import exceptions
from report_gen import Report_Gen
from helpers.collections.output import Output

report = Report_Gen()

def copy_file(args:list,options:list):
    """
    This funciton will copy file from source path to destination path
    
    """
    """
    This funciton will copy file from source path to destination path
    
    """
    src = args[0]
    dest = args[1]
    output_obj = Output()

    report.write_log(f"Copying {src} to {dest}\n")

    try:
      # Source and destination path validation
      # Source and destination path validation
      if not os.path.exists(src):
         raise exceptions.SourcePathNotExist(src)
      
      if not os.path.exists(dest):
          raise exceptions.DestinationPathNotExist(dest)
      
      if not os.path.isfile(src):
          raise exceptions.NotAFilePath(src)
      
      if not os.path.isdir(dest):
         raise exceptions.NotADirectoryPath(dest)
      
      shutil.copy(src=src,dst=dest)
    
    # Handling Exception
    
    # Handling Exception
    except Exception as e:
        print(e,file=output_obj)
        report.write_log(e.__str__()+"\n")
    else:
      print("Copied Successfully",file=output_obj)
      report.write_log(output_obj.__str__())
    
    return output_obj



if __name__ == "__main__":
    # copy_file("test\\test.txt","new_directory")
    pass