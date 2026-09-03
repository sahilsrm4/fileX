import os
import exceptions
from report_gen import Report_Gen

report = Report_Gen()

class Dir_Summary:
   
   # Child number is used to keep track of the directory when recursion happens
   child_number = 0

   def dir_summary(self,args:list=[],options:list=[]) :
        """
        This funciton will Generate a visual summary of the directory provided if -r or --recursive option is provided it 
        will also generate summary of child directory
        """
        recursive = False
        
        # Prase arguments

        if(len(args)==0):
            path = os.getcwd()
        else:
            path = args[0]

        try:
            # Parse option
            if options:
                if options[0] == "-r" or options[0] == "--recursive":
                   recursive = True
                else:
                    raise exceptions.NotSupportedOption("Directory Summary",options[0])
            
            # Check Path 
            if not os.path.exists(path):
                 raise exceptions.PathNotExist(path)
            
            if not os.path.isdir(path):
                raise exceptions.NotADirectoryPath(path=path)
            
            # Print pattern for appealing visual summary
            for i in range(self.child_number*2):
                print(" ",end="")

            print("|__",end="")
            print(os.path.basename(path))
            
            # Iterate through the directory
            for name in os.listdir(path):
                self.child_number += 1
                full_path = os.path.join(path,name)
                
                # Check File or Directory
                if os.path.isfile(full_path):

                    for i in range(self.child_number*2):
                       print(" ",end="")

                    print("|__",end="")
                    print(name)

                else:
                    # If recursive is true then go inside the directory otherwise print the directory
                    if recursive:
                       self.dir_summary([full_path],options) # we passed a list since the function accepts the list

                    else:
                        for i in range(self.child_number*2):
                          print(" ",end="")

                        print("|__",end="")
                        print(name)

                self.child_number -=1
                # Back Tracking of child number

        except Exception as e:
             print(e)
             report.write_log(e.__str__()+"\n")

if __name__ == "__main__":
    dir_s = Dir_Summary()
    dir_s.dir_summary()


 