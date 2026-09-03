import sys
import list_file
import directory_summary
import info
import search_file
import copy_file
import rename_file
import report_gen
import exceptions

ls_file = list_file.list_files
dir_summary = directory_summary.Dir_Summary().dir_summary
file_info = info.file_info
search_f = search_file.search_print_file
copy_f = copy_file.copy_file
rename_f = rename_file.rename_file

def help(args:list = [],options:list=[]):
    print("\nCommand-Line File Automation Utility")
    print("=" * 45)

    print("\nAvailable commands:\n")

    print("lsfile")
    print("  List files in a directory.")
    print("  Usage: python mytool.py lsfile [directory]")
    print("  Arguments: 0 or 1")

    print("\ndirs")
    print("  Generate a summary of a directory.")
    print("  Usage: python mytool.py dirs [directory] [ -r | --recursive]")
    print("-r or --recursive will also summarize child directories")
    print("  Arguments: 0 or 1")

    print("\ninfo")
    print("  Display information about a file.")
    print("  Usage: python mytool.py info <file> [option]")
    print("  Arguments: 1 or 2")

    print("\nsearch")
    print("  Search for files by name or extension.")
    print("  Usage: python mytool.py search [pattern] <directory>")
    print("  Arguments: 1 or 2")

    print("\ncopyf")
    print("  Copy a file to another directory.")
    print("  Usage: python mytool.py copyf <source> <destination>")
    print("  Arguments: 2")

    print("\nrenamef")
    print("  Rename a file.")
    print("  Usage: python mytool.py renamef <old_name> <new_name>")
    print("  Arguments: 2")

    print("\nhelp")
    print("  Display this help message.")
    print("  Usage: python mytool.py help")
    print("  Arguments: 0")

def arg_and_opt(args:list|None):
   arguments = list()
   options = list()
   if not args:
      return arguments,options
   for arg in args:
      if arg.startswith("-") or arg.startswith("--"):
         options.append(arg)
      else:
         arguments.append(arg)
      
   return arguments,options

command_to_fun = dict()
# the list will contain at 0th index the function mapped to command ,at 1st index number of arg , 2nd index number of argument also possible 
command_to_fun["lsfile"] = [ls_file,0,1]
command_to_fun["dirs"] = [dir_summary,0,1]
command_to_fun["info"] = [file_info,1,2]
command_to_fun["search"] = [search_f,1,2]
command_to_fun["copyf"] = [copy_f,2,2]
command_to_fun["renamef"] = [rename_f,2,2]
command_to_fun["help"] = [help,0,0]



if __name__ == "__main__":
   report = report_gen.Report_Gen()
   try:
       if(len(sys.argv)==1):
          raise exceptions.NoCommand
          
       try:
         report.write_log(f"Provided Arguments: {sys.argv}\n")
         ls = command_to_fun[sys.argv[1]]

       except KeyError:
          raise exceptions.InvalidCommand(sys.argv[1])
       
       except Exception as e:
          print(f"Error {e}")
          report.close()
          sys.exit()
    
       fn = ls[0]
       arguments,options = arg_and_opt(sys.argv[2:])
       number_of_arg = len(arguments)
       
       if(ls[1] == number_of_arg or ls[2] == number_of_arg):
            report.write_log(f"Calling the functionality {fn.__name__}\n")
            report.write_log(f"Arguments = {arguments}\nOptions ={options}\n")
            result = fn(arguments,options)
            report.write_log(f"Data returned by the fucntionality {fn.__name__} is {result}")
            
       else:
          if(ls[1] == ls[2]):
             print(f"{sys.argv[1]} functionality require {ls[1]} args")
             report.write_log(f"{sys.argv[1]} functionality require {ls[2]} args but {len(sys.argv[2:])} is provided")
    
          else:
            print(f"{sys.argv[1]} functionality require either {ls[1]} or {ls[2]} args")
            report.write_log(f"{sys.argv[1]} functionality require either {ls[1]} or {ls[2]} args but {len(sys.argv[2:])} is provided")

   except exceptions.NoCommand as e:
      print(e)
      help()
      report.write_log(e.__str__()+"\n")

   except exceptions.InvalidCommand as e:
      print(e)
      report.write_log(e.__str__()+"\n")
   
   except Exception as e:
      print(f"Error {e}")
      report.write_log(f"Error {e}")
   
   
   report.file.close()