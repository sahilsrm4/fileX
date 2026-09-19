import os
import json
import sys
sys.path.append("D:\WatchGuard\command-line-file-utility")
from google import genai
from openai import OpenAI

from fileX_client import FileXClient

protocol = """
Response Protocol:

You must respond using ONLY valid JSON.

There are two possible response types:

1. Tool Call
Use this when you need to execute a tool.

{
    "type": "tool_call",
    "tool_name": "<tool_name>",
    "arguments": [<arg1>, <arg2>, <arg3>]
}

2. Message
Use this when you want to communicate a result or response to the user.

{
    "type": "message",
    "content": "<message_content>"
}

IMPORTANT RULES:

1. Return exactly ONE JSON object in each response.
2. Never return multiple JSON objects in the same response.
3. Never return a tool call and a message together.
4. When a tool is required, return ONLY the tool_call JSON object.
5. After returning a tool_call, STOP and wait for the tool result.
6. Do not assume or invent the result of a tool call.
7. After the tool result is provided, decide what to do next.
8. If another tool is required, return ONLY the next tool_call JSON object.
9. If no more tools are required, return ONLY a message JSON object.
10. The arguments field must always be a JSON array, even when there is only one argument.
11. Use the exact tool name provided in the available tools.
12. Do not put Markdown, explanations, code fences, or additional text outside the JSON object.

Example:

User:
"Find the login implementation."

Assistant:
{
    "type": "tool_call",
    "tool_name": "search_file",
    "arguments": ["login"]
}

Tool result:
"Found login.py"

Assistant:
{
    "type": "message",
    "content": "I found the login implementation in login.py."
}

If multiple tools are needed, execute them ONE AT A TIME.

Example:

Assistant:
{
    "type": "tool_call",
    "tool_name": "search_file",
    "arguments": ["login"]
}

[Wait for tool result]

Assistant:
{
    "type": "tool_call",
    "tool_name": "info",
    "arguments": ["login.py"]
}

[Wait for tool result]

Assistant:
{
    "type": "message",
    "content": "I found the login implementation in login.py and inspected its details."
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
   user_prompt = "user_input:"+ input("Write your query:")
   if(user_prompt=="user_input:stop"):
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
        tool_name = response_json["tool_name"]
        tool_fn = getattr(file_client,tool_name)
        result = tool_fn(response_json["arguments"])
        print("Tool result:",result)
        context +=  f"{tool_name} tool result:{str(result)} "



    
