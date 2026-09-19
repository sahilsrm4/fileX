import list_file as list_file_module
import directory_summary as directory_summary_module
import info as info_module
import search_file as search_file_module
import copy_file as copy_file_module
import rename_file as rename_file_module
import report_gen  as report_gen_module
import exceptions
import fileX 
import os

class FileXClient():
      __tool_list = [
         {
            "tool_name": "list_file",
            "tool_description": "It will give list of files in the directory",
            "arguments_desc": "Takes directory path if not provided it will use current directory path by default"
         },
         {
            "tool_name": "directory_summary",
             "tool_description": "It will give directory/folder structure",
             "arguments_desc": "takes directory path if not provided uses current working directory path by default, if -r or --recursive given, it will go into child directory also and generate the full directory summary"
         },
         {
            "tool_name": "file_info",
            "tool_description":"It will give the infromation of a file like file created,modified,accessed date/time and , size in bytes",
            "arguments_desc": "takes file path"
         },
         {
            "tool_name": "search_file",
             "tool_description": "It will search file in the directory",
             "arguments_desc": "takes file name or matching keyword, if -r or --recursive given search in parent directories also, it don't parse the * , it don't know that * means anything"
         },
         {
            "tool_name": "copy_file",
            "tool_description": "it will copy file to a destination folder",
            "arguments_desc": "takes source path as first argument and destination path a second argument"
         },
         {
            "tool_name": "rename_file",
            "tool_description": "It will rename a file ",
            "arguments_desc": "takes source path as first argument and destination path as second argument"
         },
         {
              "tool_name": "get_current_working_directory",
              "tool_description": "it will return the current working directory path",
              "arguments_desc" : "takes no arguments"
         }
      ]

      def list_file(self,args):
         arguments,options = fileX.arg_and_opt(args)
         files = list_file_module.list_files(arguments,options)
         return files
     
      def directory_summary(self,args):
           arguments,options = fileX.arg_and_opt(args)
           # we have to find a way to store the pattern into a data structure which can be printed directly and can be shared 
           result = directory_summary_module.Dir_Summary().dir_summary(arguments,options)
           return str(result)
      
      def file_info(self,args):
           arguments,options = fileX.arg_and_opt(args)
           result =  info_module.file_info(arguments,options)
           return str(result)
     
      def search_file(self,args):
           print(args)
           arguments,options = fileX.arg_and_opt(args)
           result = search_file_module.search_file(arguments,options)
           return str(result)
      
      def copy_file(self,args):
           arguments,options = fileX.arg_and_opt(args)
           result = copy_file_module.copy_file(arguments,options)
           return str(result)
      
      def rename_file(self,args):
           arguments,options = fileX.arg_and_opt(args)
           result = rename_file_module.rename_file(arguments,options)
           return str(result)
      
      def get_current_working_directory(self,args):
           return os.getcwd()
      
      @classmethod
      def get_tool_desc(cls):
           return cls.__tool_list
      
      