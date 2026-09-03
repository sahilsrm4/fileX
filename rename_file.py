import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()

def rename_file(args:list=[],options:list=[]):
   """
   This function will rename source file into provided destiantion name
   """
   src = args[0]
   dest = args[1]

   try:
      report.write_log(f"Renaming {src} to {dest}")
      
      # Path validation
      if not os.path.exists(src):
          raise exceptions.SourcePathNotExist(src)
      
      if not os.path.isfile(src):
         raise exceptions.NotAFilePath(src)
      
      os.rename(src,dest)
      
      report.write_log("Renaming Successful")

   except Exception as e:
      print(e)
      report.write_log(e.__str__()+"\n")