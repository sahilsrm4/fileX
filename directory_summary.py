import os
import exceptions
from report_gen import Report_Gen
from helpers.collections.output import Output
report = Report_Gen()

class Dir_Summary:
   
   # Child number is used to keep track of the directory when recursion happens
   
   # Child number is used to keep track of the directory when recursion happens
   child_number = 0


   def dir_summary(self,args:list=[],options:list=[]) :
        """
        This funciton will Generate a visual summary of the directory provided if -r or --recursive option is provided it 
        will also generate summary of child directory
        
        """
        recursive = False
        
        # Prase arguments
        
        # Prase arguments

        if(len(args)==0):
            path = os.getcwd()
        else:
            path = args[0]


        try:
            # Parse option
            # Parse option
            if options:
                if options[0] == "-r" or options[0] == "--recursive":
                   recursive = True
                else:
                    raise exceptions.NotSupportedOption("Directory Summary",options[0])
            
            # Check Path 
            
            # Check Path 
            if not os.path.exists(path):
                 raise exceptions.PathNotExist(path)
            
            if not os.path.isdir(path):
                raise exceptions.NotADirectoryPath(path=path)
            
            # Print pattern for appealing visual summary
            # Using custom output object/data structure
            output_obj = Output()

            spaces_outer = " "*self.child_number*2

            reference_line_outer = spaces_outer+"|__"

            print(reference_line_outer + os.path.basename(path),file=output_obj)
            
            # Iterate through the directory
            for name in os.listdir(path):
                self.child_number += 1
                full_path = os.path.join(path,name)
                
                # Check File or Directory
                # Check File or Directory
                if os.path.isfile(full_path):

                    spaces_inner = " "*self.child_number*2

                    reference_line_inner = spaces_inner+"|__"
                    print(reference_line_inner + name,file=output_obj)

                else:
                    # If recursive is true then go inside the directory otherwise print the directory
                    # If recursive is true then go inside the directory otherwise print the directory
                    if recursive:
                       result = self.dir_summary([full_path],options) # we passed a list since the function accepts the list
                       output_obj.write(result.__str__())
                    else:
                       spaces_inner = " "*self.child_number*2
   
                       reference_line_inner = spaces_inner+"|__"
                       print(reference_line_inner + name,file=output_obj)

                self.child_number -=1
                # Back Tracking of child number
            return output_obj

        except Exception as e:
             print(e)
             report.write_log(e.__str__()+"\n")

if __name__ == "__main__":
    dir_s = Dir_Summary()
    dir_s.dir_summary()


 