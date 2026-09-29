from google import genai
import json
import os
import sys

sys.path.append("d:\WatchGuard\command-line-file-utility")

import list_file

gemini_api_key = os.environ.get("gemini_api_key")

def read_file(args):
      path = args[0]
      print(path)
      content = str()
      with open(path,"r") as f:
           content = f.read()
      return content

tools = {"list_file":list_file.list_files,
          "read_file":read_file}
    
# tool_description = ['I have tool to list file if no argumnent is provided it uses the current directory and if argument is provided it uses that directory to list the path of the directory should be absolute if you want to use that tool just provide me the list_file in methods inside tool_call in json format like tool_call={"tool" : "list_file"} the response should start with tool_call so i can interpret it, if you dont want to use tool just give the normal resposne']
tool_description = {
      "list_file": "This will list the files in the current directory if no directory provided, if path provided then in that path",
      "read_file": "This will read the content of a file , it takes one argument which is file absolute path or file_name if you want current working directry path"
}

tool_calling_protocol = 'To call a tool use the format tool_call={"tool":"tool_name","arguments":[arg1,arg2,....]}'

final_response = str()


client = genai.Client(api_key=gemini_api_key)

response = client.models.generate_content(
    model= "gemini-3.7-flash",
    # contents = f"{tool_description} can you list files in my directory"
    contents= f"{tool_description}, {tool_calling_protocol}, can you read the file fileX.py"
)

response = response.text
print(response)


if response.startswith("tool_call"):
     response = response.replace("tool_call=","")

     tool_json = json.loads(response)
     tool_fn = tools[tool_json["tool"]]
     
     if(tool_fn == list_file.list_files): 
        output = tool_fn()
        final_response = client.models.generate_content(
             model = "gemini-3.7-flash",
             contents = f"Format this correctly with file number {output}"
        )
     elif(tool_fn == read_file):
        print(tool_json["arguments"])
        output = tool_fn(tool_json["arguments"])
        
        final_response = client.models.generate_content(
             model = "gemini-3.7-flash",
             contents = f"Can you Tell me any bug in this code {output}"
        )
else:
     sys.exit()


print(final_response.text)