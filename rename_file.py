import os
import exceptions
from report_gen import Report_Gen
from helpers.collections.output import Output

report = Report_Gen()

def rename_file(args:list=[],options:list=[]):
   """
   This function will rename source file into provided destiantion name
   """
   src = args[0]
   dest = args[1]
   output_obj = Output()
   try:
      report.write_log(f"Renaming {src} to {dest}\n")
      
      # Path validation
      if not os.path.exists(src):
          raise exceptions.SourcePathNotExist(src)
      
      if not os.path.isfile(src):
         raise exceptions.NotAFilePath(src)
      
      os.rename(src,dest)
      
      report.write_log("Renaming Successful\n")
      print(f"Scuccessfully renamed the src {src} to destination {dest}",file=output_obj)
      
      return output_obj
   

   except Exception as e:
      print(e)
      report.write_log(e.__str__()+"\n")