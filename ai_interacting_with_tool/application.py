import os
import json
import sys
sys.path.append("D:\WatchGuard\command-line-file-utility")
from google import genai
from openai import OpenAI

from fileX_client import FileXClient

protocol = """
You have to give response in json format like mentioned below .
Give one tool call at once not many tool call together , first one tool call made and that tool reponse is returned to you and then you have to make next tool call also at one time either do tool call or give message not give both together
Response Protocol:"
"{
    "type": "tool_call",
    "tool_name": "search_file",
    "arguments":  [arg1,arg2,arg3...]
}

{
    "type": "message",
    "content": "I found the login implementation."
}
"""

tool_discrption = FileXClient.get_tool_desc()

GEMINI_KEY = os.environ.get("gimini_api_key")
OPENAI_API_KEY = os.environ.get("openai_api_key")

gemini_ai_client = genai.Client(api_key=GEMINI_KEY)
openai_ai_client = OpenAI(api_key=OPENAI_API_KEY)
file_client = FileXClient()

print("Welcome to file application !\nEnter stop to stop")

while(True):
   user_prompt = "user_input"+ input("Write your query:")
   if(user_prompt=="stop"):
      break
   
   context = ""
   context += user_prompt
   tool_call = 0
   while(True):
   
     final_prompt = f"{protocol}\n{tool_discrption}\n {context}"
     if tool_call > 10:
      break
   #   response = gemini_ai_client.models.generate_content(
   #      model= "gemini-3.7-flash",
   #      contents=  final_prompt
   #   )
     
     response = openai_ai_client.responses.create(
             model="gpt-5.6-luna",
             input = final_prompt
            )
     response_text = response.output_text
     print(response_text)
     response_json = json.loads(response_text)
    
     if response_json["type"] == "message":
        print(response_json["content"])
        context += "Model Message:" + f" {response_json['content']}"
        user_prompt = input()
        if user_prompt == "exit":
         break
        context += "User Input:" + f" {user_prompt}"
        
     
     else:
        tool_call += 1
        print("Tool call happend",response_text)
        tool_name = response_json["tool_name"]
        tool_fn = getattr(file_client,tool_name)
        result = tool_fn(response_json["arguments"])
        print("Tool response:", result)
        context = final_prompt + context + f"{tool_name} tool result:{str(result)} "



    
