
import os
import json
import sys
import asyncio

sys.path.append(r"D:\WatchGuard\command-line-file-utility")

from google import genai
from openai import OpenAI

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from fileX_client import FileXClient


# =========================================================
# RESPONSE PROTOCOL
# =========================================================

protocol = """
Response Protocol:

You must respond using ONLY valid JSON.

There are two possible response types:

1. Tool Call

{
    "type": "tool_call",
    "tool_name": "<tool_name>",
    "arguments": [...]
}

2. Message

{
    "type": "message",
    "content": "<message_content>"
}


IMPORTANT RULES:

1. Return exactly ONE JSON object in each response.

2. Never return multiple JSON objects in the same response.

3. Never return a tool call and a message together.

4. When a tool is required, return ONLY the tool_call JSON object.

5. If no more tools are required, return ONLY a message JSON object.

6. The "arguments" field must ALWAYS be a JSON array.

7. Use the exact tool name provided in the available tools.

8. Do not put Markdown, explanations, code fences, or additional
   text outside the JSON object.

9. Execute only ONE tool at a time.

10. Wait for the tool result before making another tool call.


=========================================================
FILEX ARGUMENT RULE
=========================================================

FileX tools use positional arguments.

Example:

{
    "type": "tool_call",
    "tool_name": "search_file",
    "arguments": ["login"]
}


Another example:

{
    "type": "tool_call",
    "tool_name": "copy_file",
    "arguments": ["source.txt", "destination.txt"]
}


=========================================================
PLAYWRIGHT MCP ARGUMENT RULE
=========================================================

Playwright MCP tools require a JSON OBJECT for their arguments.

However, because the protocol requires "arguments" to always
be an array, the MCP argument object MUST be placed as the
ONLY element inside the array.

Example:

{
    "type": "tool_call",
    "tool_name": "browser_navigate",
    "arguments": [
        {
            "url": "https://example.com"
        }
    ]
}


Another example:

{
    "type": "tool_call",
    "tool_name": "browser_click",
    "arguments": [
        {
            "element": "Login button",
            "ref": "e12"
        }
    ]
}


IMPORTANT:

For MCP tools:

CORRECT:

"arguments": [
    {
        "url": "https://example.com"
    }
]


INCORRECT:

"arguments": [
    "https://example.com"
]


INCORRECT:

"arguments": {
    "url": "https://example.com"
}


The MCP argument object MUST be the first and only
element of the arguments array.

The keys inside that object MUST match the MCP tool's
Arguments Schema.
"""


# =========================================================
# LLM CLIENTS
# =========================================================

GEMINI_KEY = os.environ.get("gimini_api_key")
OPENAI_API_KEY = os.environ.get("openai_api_key")


gemini_ai_client = genai.Client(
    api_key=GEMINI_KEY
)


openai_ai_client = OpenAI(
    api_key=OPENAI_API_KEY
)


# =========================================================
# FILEX CLIENT
# =========================================================

file_client = FileXClient()


# =========================================================
# MCP TOOL DESCRIPTION
# =========================================================

def get_mcp_tool_description(mcp_tools):

    description = ""

    for tool in mcp_tools:

        description += f"""
Tool Name:
{tool.name}

Description:
{tool.description}

Arguments Schema:
{json.dumps(
    tool.input_schema,
    indent=2,
    default=str
)}

"""

    return description


# =========================================================
# FIND MCP TOOL
# =========================================================

def get_mcp_tool(
    mcp_tools,
    tool_name
):

    for tool in mcp_tools:

        if tool.name == tool_name:
            return tool

    return None


# =========================================================
# PARSE MCP ARGUMENTS
# =========================================================

def parse_mcp_arguments(
    tool,
    arguments
):
    """
    Convert the agent protocol:

        "arguments": [
            {
                "url": "https://example.com"
            }
        ]

    into the MCP format:

        {
            "url": "https://example.com"
        }

    The MCP tool's input_schema is used for validation.
    """

    # -----------------------------------------------------
    # arguments must be a list
    # -----------------------------------------------------

    if not isinstance(arguments, list):

        raise ValueError(
            f"MCP tool '{tool.name}' received invalid "
            f"arguments type: "
            f"{type(arguments).__name__}. "
            f"Expected a list."
        )


    # -----------------------------------------------------
    # MCP tool with no arguments
    # -----------------------------------------------------

    schema = tool.input_schema or {}

    properties = schema.get(
        "properties",
        {}
    )

    required = schema.get(
        "required",
        []
    )


    # -----------------------------------------------------
    # No arguments expected
    # -----------------------------------------------------

    if not properties:

        if len(arguments) == 0:

            return {}

        raise ValueError(
            f"MCP tool '{tool.name}' does not require "
            f"arguments, but received: {arguments}"
        )


    # -----------------------------------------------------
    # MCP arguments must contain exactly one object
    # -----------------------------------------------------

    if len(arguments) != 1:

        raise ValueError(
            f"MCP tool '{tool.name}' expects its "
            f"arguments as one JSON object inside the "
            f"arguments array.\n"
            f"Received: {arguments}"
        )


    # -----------------------------------------------------
    # Extract object
    # -----------------------------------------------------

    mcp_arguments = arguments[0]


    # -----------------------------------------------------
    # Object validation
    # -----------------------------------------------------

    if not isinstance(
        mcp_arguments,
        dict
    ):

        raise ValueError(
            f"MCP tool '{tool.name}' expects the first "
            f"argument to be a JSON object.\n"
            f"Received: {mcp_arguments}"
        )


    # -----------------------------------------------------
    # Validate required parameters
    # -----------------------------------------------------

    missing_parameters = []

    for parameter in required:

        if parameter not in mcp_arguments:

            missing_parameters.append(
                parameter
            )


    if missing_parameters:

        raise ValueError(
            f"MCP tool '{tool.name}' is missing required "
            f"arguments: {missing_parameters}\n"
            f"Received: {mcp_arguments}"
        )


    # -----------------------------------------------------
    # Validate parameter names
    # -----------------------------------------------------

    invalid_parameters = []

    for parameter in mcp_arguments:

        if parameter not in properties:

            invalid_parameters.append(
                parameter
            )


    if invalid_parameters:

        raise ValueError(
            f"MCP tool '{tool.name}' received unknown "
            f"arguments: {invalid_parameters}\n"
            f"Allowed arguments: "
            f"{list(properties.keys())}"
        )


    # -----------------------------------------------------
    # Everything is valid
    # -----------------------------------------------------

    return mcp_arguments


# =========================================================
# EXECUTE MCP TOOL
# =========================================================

async def execute_mcp_tool(
    session,
    mcp_tools,
    tool_name,
    arguments
):

    print(
        f"\n[MCP TOOL] {tool_name}"
    )

    print(
        f"[MCP RAW ARGUMENTS] {arguments}"
    )


    # -----------------------------------------------------
    # Find MCP tool
    # -----------------------------------------------------

    tool = get_mcp_tool(
        mcp_tools,
        tool_name
    )


    if tool is None:

        raise ValueError(
            f"MCP tool '{tool_name}' was not found."
        )


    # -----------------------------------------------------
    # Parse arguments
    # -----------------------------------------------------

    mcp_arguments = parse_mcp_arguments(
        tool,
        arguments
    )


    print(
        f"[MCP PARSED ARGUMENTS] "
        f"{mcp_arguments}"
    )


    # -----------------------------------------------------
    # Execute MCP tool
    # -----------------------------------------------------

    result = await session.call_tool(
        tool_name,
        arguments=mcp_arguments
    )


    return result


# =========================================================
# MAIN AGENT
# =========================================================

async def main():

    print(
        "Welcome to file application!"
    )

    print(
        "Enter stop to stop"
    )


    # =====================================================
    # CONNECT TO PLAYWRIGHT MCP
    # =====================================================

    async with streamable_http_client(
        "http://localhost:8931/mcp"
    ) as (
        read_stream,
        write_stream
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as mcp_session:


            # =================================================
            # INITIALIZE MCP
            # =================================================

            await mcp_session.initialize()


            # =================================================
            # DISCOVER MCP TOOLS
            # =================================================

            mcp_result = (
                await mcp_session.list_tools()
            )

            mcp_tools = mcp_result.tools


            print(
                "\nPlaywright MCP tools loaded:"
            )


            for tool in mcp_tools:

                print(
                    " -",
                    tool.name
                )


            # =================================================
            # FILEX TOOLS
            # =================================================

            filex_tool_description = (
                FileXClient.get_tool_desc()
            )


            # =================================================
            # MCP TOOLS
            # =================================================

            mcp_tool_description = (
                get_mcp_tool_description(
                    mcp_tools
                )
            )


            # =================================================
            # COMBINE TOOL DESCRIPTIONS
            # =================================================

            tool_description = f"""
================ FILEX TOOLS ================

{filex_tool_description}


================ PLAYWRIGHT MCP TOOLS ================

{mcp_tool_description}


=========================================================
IMPORTANT TOOL ARGUMENT FORMAT
=========================================================

ALL tool calls MUST use:

"arguments": [...]


FILEX:

FileX arguments are positional.

Example:

"arguments": ["login"]


PLAYWRIGHT MCP:

MCP arguments MUST be one JSON object inside the
arguments array.

Example:

"arguments": [
    {{
        "url": "https://example.com"
    }}
]


The object MUST match the MCP Arguments Schema.

Do NOT convert MCP arguments into positional values.

Do NOT return:

"arguments": ["https://example.com"]

Return:

"arguments": [
    {{
        "url": "https://example.com"
    }}
]
"""


            # =================================================
            # USER LOOP
            # =================================================

            while True:

                user_input = input(
                    "\nWrite your query: "
                )


                if user_input.strip().lower() == "stop":

                    break


                context = (
                    "User Input: "
                    + user_input
                )


                tool_call_count = 0


                # =================================================
                # AGENT LOOP
                # =================================================

                while True:

                    if tool_call_count > 10:

                        print(
                            "Maximum tool calls reached."
                        )

                        break


                    # =============================================
                    # BUILD PROMPT
                    # =============================================

                    final_prompt = f"""
{protocol}

{tool_description}

Conversation / Tool Context:

{context}
"""


                    # =============================================
                    # LLM CALL
                    # =============================================

                    response = (
                        gemini_ai_client
                        .models
                        .generate_content(
                            model="gemini-3.6-flash",
                            contents=final_prompt
                        )
                    )


                    response_text = (
                        response.text.strip()
                    )


                    print(
                        "\nMODEL:"
                    )

                    print(
                        response_text
                    )


                    # =============================================
                    # PARSE JSON
                    # =============================================

                    try:

                        response_json = json.loads(
                            response_text
                        )

                    except json.JSONDecodeError:

                        print(
                            "Invalid JSON returned "
                            "by model."
                        )

                        context += (
                            "\nSystem: Your previous "
                            "response was not valid JSON. "
                            "Return ONLY valid JSON."
                        )

                        continue


                    # =============================================
                    # FINAL MESSAGE
                    # =============================================

                    if response_json.get(
                        "type"
                    ) == "message":

                        content = (
                            response_json.get(
                                "content",
                                ""
                            )
                        )


                        print(
                            "\nASSISTANT:"
                        )

                        print(
                            content
                        )


                        context += (
                            "\nModel Message: "
                            + content
                        )


                        # -----------------------------------------
                        # Ask user for next request
                        # -----------------------------------------

                        user_input = input(
                            "\nYou: "
                        )


                        if user_input.strip().lower() == "exit":

                            break


                        context += (
                            "\nUser Input: "
                            + user_input
                        )


                        continue


                    # =============================================
                    # TOOL CALL
                    # =============================================

                    if response_json.get(
                        "type"
                    ) == "tool_call":

                        tool_call_count += 1


                        tool_name = (
                            response_json.get(
                                "tool_name"
                            )
                        )


                        arguments = (
                            response_json.get(
                                "arguments"
                            )
                        )


                        print(
                            "\nRequested tool:",
                            tool_name
                        )


                        print(
                            "Arguments:",
                            arguments
                        )


                        # =========================================
                        # MCP TOOL NAMES
                        # =========================================

                        mcp_tool_names = {
                            tool.name
                            for tool in mcp_tools
                        }


                        # =========================================
                        # PLAYWRIGHT MCP TOOL
                        # =========================================

                        if tool_name in mcp_tool_names:

                            try:

                                result = (
                                    await execute_mcp_tool(
                                        mcp_session,
                                        mcp_tools,
                                        tool_name,
                                        arguments
                                    )
                                )


                                print(
                                    "\nMCP RESULT:"
                                )


                                print(
                                    result
                                )


                                context += (
                                    f"\n{tool_name} "
                                    f"tool result: "
                                    f"{str(result)}"
                                )


                            except Exception as e:

                                print(
                                    "\nMCP tool execution "
                                    "failed:"
                                )


                                print(
                                    str(e)
                                )


                                context += (
                                    f"\n{tool_name} "
                                    f"tool result: "
                                    f"ERROR: {str(e)}"
                                )


                            continue


                        # =========================================
                        # FILEX TOOL
                        # =========================================

                        try:

                            tool_fn = getattr(
                                file_client,
                                tool_name
                            )


                        except AttributeError:

                            context += (
                                f"\nTool result: "
                                f"Unknown tool "
                                f"'{tool_name}'"
                            )

                            continue


                        try:

                            # -------------------------------------
                            # FileX receives positional arguments
                            # -------------------------------------

                            result = tool_fn(
                                arguments
                            )


                            print(
                                "\nFILEX RESULT:"
                            )


                            print(
                                result
                            )


                            context += (
                                f"\n{tool_name} "
                                f"tool result: "
                                f"{str(result)}"
                            )


                        except Exception as e:

                            print(
                                "\nFileX tool execution "
                                "failed:"
                            )


                            print(
                                str(e)
                            )


                            context += (
                                f"\n{tool_name} "
                                f"tool result: "
                                f"ERROR: {str(e)}"
                            )


                        continue


                    # =============================================
                    # UNKNOWN RESPONSE TYPE
                    # =============================================

                    print(
                        "\nUnknown response type."
                    )


                    context += (
                        "\nSystem: Invalid response type. "
                        "Return either 'tool_call' "
                        "or 'message'."
                    )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )
