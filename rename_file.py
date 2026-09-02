import os
from report_gen import Report_Gen

report = Report_Gen()

def rename_file(args):
   src = args[0]
   dest = args[1]
   report.write_log(f"Renaming {src} to {dest}")
   
   if not os.path.exists(src):
      print("Source path does not exist")
      report.write_log(f"{src} does not exist")
      return
   if not os.path.isfile(src):
      print("The src should be file")
      report.write_log("Soruce is not a file")
   try:
     os.rename(src,dest)
   except Exception as e:
      print(f"Error {e}")