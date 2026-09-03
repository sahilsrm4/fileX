class PathNotExist(Exception):
    def __init__(self,path,*args):
          self.path = path
          super().__init__(args)

    def __str__(self):
         return f"{self.path} Does not exist"
    
class SourcePathNotExist(Exception):
     def __init__(self,path, *args):
          super().__init__(*args)
          self.path = path
     def __str__(self):
          return f"Source path does not exist -> {self.path}"

class DestinationPathNotExist(Exception):
     def __init__(self,path, *args):
          super().__init__(*args)
          self.path = path
     def __str__(self):
          return f"Destination path does not exist -> {self.path}"

class NotAFilePath(Exception):
     def __init__(self,path,*args):
          super().__init__(*args)
          self.path = path
     def __str__(self):
          return f"This is not a file path {self.path}.\nPlease provide relative or absolute path of the file"

class NotADirectoryPath(Exception):
     def __init__(self,path, *args):
          super().__init__(*args)
          self.path = path
     def __str__(self):
          return f"This path is not a directory path {self.path}.\nPlase provide relative or absolute path of directory"

class InvalidCommand(Exception):
     def __init__(self,command,*args):
          super().__init__(*args)
          self.command = command
     def __str__(self):
          return f"{self.command} is an invalid command. Use help command to know valid commands"

class NoCommand(Exception):
     def __init__(self, *args):
          super().__init__(*args)
     def __str__(self):
          return "Please Provide command"

class ArgumentError(Exception):
     def __init__(self,command,required_arg:list,provided_arg, *args):
          super().__init__(*args)
          self.required_arg = required_arg
          self.provided_arg = provided_arg
          self.command = command
     def __str__(self):
          return f"{self.command} require {self.required_arg} but only {self.provided_arg} is provided"
     
class FileNotExist(Exception):
     def __init__(self,file,path,*args):
          super().__init__(*args)
          self.file = file
          self.path = path
     
     def __str__(self):
          return f"{self.file} doesn't exist in the folder {self.path}"
     
class ExactFileNotExist(Exception):
     def __init__(self,file,matching_result:list, *args):
          super().__init__(*args)
          self.file = file
          self.matching_result = matching_result

     def __str__(self):
          return f"Exact File does not exist -> {self.file}\nMatching results are {self.matching_result}"

class NotString(Exception):
     def __init__(self,message, *args):
          super().__init__(*args)
          self.message = message
     def __str__(self):
          return f"Not string{self.message}"

class NotSupportedOption(Exception):
     def __init__(self,function_name,option,*args):
          self.function_name = function_name
          self.option = option
          super().__init__(*args)
     def __str__(self):
          return f"{self.option} is not supported by {self.function_name}"

class PathLengthGreaterThan260(Exception):
     def __init__(self, *args):
          super().__init__(*args)
     
     def __str__(self):
          return "Path length is greater than 260 characters"