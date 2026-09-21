import list_file as list_file_module
import directory_summary as directory_summary_module
import info as info_module
import search_file as search_file_module
import copy_file as copy_file_module
import rename_file as rename_file_module
import create_directory as create_directory_module
from read_write_append import read_file as read_file_fn, write_file as write_file_fn, append_file as append_file_fn
import exceptions
import fileX
import os
import subprocess

from playwright.sync_api import Playwright,Page,sync_playwright


class FileXClient:
    __tool_list = [
        {
            "tool_name": "list_file",
            "tool_description": "It will give list of files in the directory",
            "arguments_desc": "Takes directory path if not provided it will use current directory path by default"
        },
        {
            "tool_name": "directory_summary",
            "tool_description": "It will give directory/folder structure",
            "arguments_desc": "takes directory absolute path ,if not provided uses current working directory path by default, if -r or --recursive given, it will go into child directory also and generate the full directory summary"
        },
        {
            "tool_name": "file_info",
            "tool_description": "It will give the infromation of a file like file created,modified,accessed date/time and , size in bytes",
            "arguments_desc": "takes file path"
        },
        {
            "tool_name": "search_file",
            "tool_description": "It will search file in the directory",
            "arguments_desc": "Takes file name or matching keyword, if -r or --recursive given search in parent directories also, it don't parse the * , it don't know that * means anything"
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
            "tool_name": "create_directory",
            "tool_description": "Create a directory",
            "arguments_desc": "Takes directory name as the first argument and an optional destination path as the second argument; uses the current directory if no path is provided"
        },
        {
            "tool_name": "read_file",
            "tool_description": "Read the contents of a file.",
            "arguments_desc": "takes the relative path of file as argument"
        },
        {
            "tool_name": "write_file",
            "tool_description": "write content to a file",
            "arguments_desc": "Take file relative or absolute path as first argument and content as second argument"
        },
        {
            "tool_name": "append_file",
            "tool_description": "It will append data to a file",
            "arguments_desc": "Take file relative or absolute path as first argument and content as second argument"
        },
        {
            "tool_name": "get_current_working_directory",
            "tool_description": "it will return the current working directory path",
            "arguments_desc": "takes no arguments"
        },
        # CommandRunner
        {
            "tool_name": "rerun_command",
            "tool_description": "Run a system command and return its output",
            "arguments_desc": "Takes the command and its arguments as a list of values"
        },

        # WebClient
        {
         "tool_name": "inspect_webpage",
         "tool_description": "Open a website in a browser and return information about the rendered webpage for analysis and test generation like dom of the page",
         "arguments_desc": "Takes the webpage URL as a string"
        }
       
    ]

    def list_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        return list_file_module.list_files(arguments, options)

    def directory_summary(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = directory_summary_module.Dir_Summary().dir_summary(arguments, options)
        return str(result)

    def file_info(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = info_module.file_info(arguments, options)
        return str(result)

    def search_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = search_file_module.search_file(arguments, options)
        return str(result)

    def copy_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = copy_file_module.copy_file(arguments, options)
        return str(result)

    def rename_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = rename_file_module.rename_file(arguments, options)
        return str(result)

    def create_directory(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = create_directory_module.create_directory(arguments, options)
        return str(result)

    def read_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = read_file_fn(arguments, options)
        return str(result)

    def write_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = write_file_fn(arguments, options)
        return str(result)

    def append_file(self, args):
        arguments, options = fileX.arg_and_opt(args)
        result = append_file_fn(arguments, options)
        return str(result)

    def get_current_working_directory(self, args):
        return os.getcwd()
    
    # codeRunner
    def rerun_command(self, args):
        """Execute a command in a visible Windows terminal window."""
        arguments, options = fileX.arg_and_opt(args)

        if not arguments:
            return "Error: rerun_command requires a command"

        try:
            creation_flags = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
            result = subprocess.run(
                arguments,
                creationflags=creation_flags,
                check=False
            )

            if result.returncode != 0:
                return f"Command exited with code {result.returncode}"

            return "Command completed successfully"

        except FileNotFoundError:
            return f"Error: command not found: {arguments[0]}"
        except OSError as error:
            return f"Error running command: {error}"
    
    # webCleint
    def inspect_webpage(self,args):
      url = args[0]
    
      # Open a sync playwright context manager
      with sync_playwright() as p:
          # Launch a headless browser instance
          browser = p.chromium.launch(headless=True)
          # Create a new page instance correctly
          page = browser.new_page()
          
          # Navigate to the URL
          page.goto(url)
  
          # Collect the results before the browser closes
          result = {
              "url": page.url,
              "title": page.title(),
              "dom": page.content(),
              # "elements": extract_elements(page) # Uncomment if you use this helper
          }
          
          # Clean up browser processes
          browser.close()
          
      return result
    
    @classmethod
    def get_tool_desc(cls):
        return cls.__tool_list
