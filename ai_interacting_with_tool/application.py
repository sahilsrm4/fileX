import os
import json
import sys
sys.path.append("D:\WatchGuard\command-line-file-utility")
from google import genai
from openai import OpenAI

from fileX_client import FileXClient

protocol = "For normal response give message='message_content' . For tool call give tool_call={'tool_name':name_of_the_tool, 'arguments':[arg1,arg2,arg3...]}"

tool_discrption = FileXClient.get_tool_desc()

GEMINI_KEY = os.environ.get("gimini_api_key")
OPENAI_API_KEY = os.environ.get("openai_api_key")

gemini_ai_client = genai.Client(api_key=GEMINI_KEY)
openai_ai_client = OpenAI(api_key=OPENAI_API_KEY)
file_client = FileXClient()

print("Welcome to file application !\nEnter stop to stop")

while(True):
   user_prompt = input("Write your query:")
   if(user_prompt=="stop"):
      break
   

   while(True):
     final_prompt = f"{protocol}\n{tool_discrption}\n'User query':{user_prompt}"
     response = gemini_ai_client.models.generate_content(
        model= "gemini-3.7-flash",
        contents=  final_prompt
     )
     
   #   response = openai_ai_client.responses.create(
   #           model="gpt-5.6-luna",
   #           input = final_prompt
   #          )
     response_text = response.text
  
     if(response_text.startswith("message")):
        response_text = response_text.replace("message=","")
        print(response_text)
        break
     
     else:
        print("Tool call happend",response_text)
        response_text = response_text.replace("tool_call=","")
        res_json = json.load(response_text)
        tool_name = res_json["tool_name"]
        tool_fn = getattr(file_client,tool_name)
        result = tool_fn(res_json["arguments"])
        final_prompt = final_prompt + f"{tool_name} tool result:{str(result)}"



    
