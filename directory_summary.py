import os
from report_gen import Report_Gen

report = Report_Gen()

class Dir_Summary:
   child_number = 0
   def dir_summary(self,args:list):
        if(len(args)==0):
            path = os.getcwd()
        else:
            path = args[0]
            
        if not os.path.exists(path):
            print(f"Path {path} does not exist")
            report.write_log(f"Path {path} does not exist\n")
            return
        if not os.path.isdir(path):
            print(f"Plase give directory Path not file path")
            report.write_log("Provided path is not of a directory")
            return
        for i in range(self.child_number*2):
            print(" ",end="")
        print("|__",end="")
        print(os.path.basename(path))
        for name in os.listdir(path):
            self.child_number += 1
            full_path = os.path.join(path,name)
            if os.path.isfile(full_path):
                for i in range(self.child_number*2):
                   print(" ",end="")
                print("|__",end="")
                print(name)
            else:
                self.dir_summary([full_path]) # we passed a list since the function accepts the list
            self.child_number -=1

if __name__ == "__main__":
    dir_s = Dir_Summary()
    dir_s.dir_summary()


 