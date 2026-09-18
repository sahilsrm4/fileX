import sys
import list_file
import directory_summary
import info
import search_file
import copy_file
import rename_file
import report_gen
import exceptions
import fileX

class FileXClient():
      tool_list = [
         {
            "tool_name": "list_file",
            "tool_description": ""
         },
         {
            "tool_name": "directory_summary",
             "tool_description": ""
         },
         {
            "tool_name": "file_info",
            "tool_description":""
         },
         {
            "tool_name": "search_file",
             "tool_description": ""
         },
         {
            "tool_name": "copy_file",
            "tool_description": ""
         },
         {
            "tool_name": "rename_file",
            "tool_description": " "
         },
      ]

      def list_file(*args):
         arguments,options = fileX.arg_and_opt(args)
         files = list_file.list_files(arguments,options)
         return files
     
      def directory_summary(*args):
           arguments,options = fileX.arg_and_opt(args)
           # we have to find a way to store the pattern into a data structure which can be printed directly and can be shared 
      
      def file_info(*args):
           arguments,options = fileX.arg_and_opt(args)
           # we have to 
