
import os
import sys
import json
import asyncio
import threading

from google import genai
from openai import OpenAI

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

sys.path.append(r"D:\WatchGuard\command-line-file-utility")

from fileX_client import FileXClient

# ============================================================
# CONFIGURATION
# ============================================================

MCP_URL = "http://localhost:8931/mcp"

GEMINI_KEY = os.environ.get("gimini_api_key")
OPENAI_API_KEY = os.environ.get("openai_api_key")


# ============================================================
# LLM CLIENTS
# ============================================================

gemini_ai_client = genai.Client(api_key=GEMINI_KEY)
openai_ai_client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================
# FILEX CLIENT
# ============================================================

file_client = FileXClient()


# ============================================================
# RESPONSE PROTOCOL
# ============================================================
with open("pypilot_rules_and_protocols/response_protocol.txt","r") as f:

   RESPONSE_PROTOCOL =  f.read()

 


# ============================================================
# PERSISTENT MCP CLIENT
# ============================================================

class PersistentMCPClient:
    """
    Synchronous wrapper around the asynchronous MCP client.

    The MCP event loop and session live inside a dedicated
    background thread for the entire lifetime of this object.
    """

    def __init__(self, url):
        self.url = url

        self.loop = None
        self.thread = None

        self.session = None
        self.mcp_tools = []

        self.ready = threading.Event()
        self.startup_error = None

        self._start_worker()

    # --------------------------------------------------------
    # START WORKER
    # --------------------------------------------------------

    def _start_worker(self):

        self.thread = threading.Thread(
            target=self._run_worker,
            daemon=True
        )

        self.thread.start()

        # Wait until MCP session has been initialized
        self.ready.wait()

        if self.startup_error:
            raise RuntimeError(
                f"Failed to start MCP client: {self.startup_error}"
            )

    # --------------------------------------------------------
    # WORKER THREAD
    # --------------------------------------------------------

    def _run_worker(self):

        self.loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self.loop)

        try:
            self.loop.run_until_complete(
                self._mcp_worker()
            )

        except Exception as e:

            self.startup_error = e

            self.ready.set()

        finally:

            self.loop.close()

    # --------------------------------------------------------
    # MCP WORKER
    # --------------------------------------------------------

    async def _mcp_worker(self):

        try:

            async with streamable_http_client(
                self.url
            ) as (read_stream, write_stream):

                async with ClientSession(
                    read_stream,
                    write_stream
                ) as session:

                    self.session = session

                    # ----------------------------------------
                    # INITIALIZE MCP SESSION
                    # ----------------------------------------

                    await session.initialize()

                    print("\n[MCP] Session initialized")

                    # ----------------------------------------
                    # LOAD MCP TOOLS
                    # ----------------------------------------

                    result = await session.list_tools()

                    self.mcp_tools = result.tools

                    print(
                        f"[MCP] Loaded {len(self.mcp_tools)} tools"
                    )

                    self.ready.set()

                    # ----------------------------------------
                    # KEEP SESSION ALIVE
                    # ----------------------------------------
                    #
                    # This is extremely important.
                    #
                    # We do NOT return from this function.
                    #
                    # The async context remains open.
                    #

                    await asyncio.Event().wait()

        except Exception as e:

            self.startup_error = e

            self.ready.set()

            print(
                f"\n[MCP] Worker terminated: {e}"
            )

    # --------------------------------------------------------
    # GET TOOLS
    # --------------------------------------------------------

    def get_tools(self):

        return self.mcp_tools

    # --------------------------------------------------------
    # CALL MCP TOOL
    # --------------------------------------------------------

    def call_tool(
        self,
        tool_name,
        arguments
    ):
        """
        Synchronous method.

        Internally schedules the async MCP call
        on the persistent MCP event loop.
        """

        if self.loop is None:
            raise RuntimeError(
                "MCP event loop is not running"
            )

        if self.session is None:
            raise RuntimeError(
                "MCP session is not initialized"
            )

        future = asyncio.run_coroutine_threadsafe(
            self._call_tool_async(
                tool_name,
                arguments
            ),
            self.loop
        )

        return future.result()

    # --------------------------------------------------------
    # ASYNC TOOL CALL
    # --------------------------------------------------------

    async def _call_tool_async(
        self,
        tool_name,
        arguments
    ):

        print(
            f"\n[MCP TOOL] {tool_name}"
        )

        print(
            f"[MCP ARGUMENTS] {arguments}"
        )

        result = await self.session.call_tool(
            tool_name,
            arguments=arguments
        )

        return result

    # --------------------------------------------------------
    # CLOSE
    # --------------------------------------------------------

    def close(self):

        print("\n[MCP] Closing client")

        if self.loop and self.loop.is_running():

            self.loop.call_soon_threadsafe(
                self.loop.stop
            )

        if self.thread:

            self.thread.join(
                timeout=5
            )


# ============================================================
# MCP TOOL HELPERS
# ============================================================

def get_mcp_tool(
    mcp_tools,
    tool_name
):

    for tool in mcp_tools:

        if tool.name == tool_name:
            return tool

    return None


def parse_mcp_arguments(
    tool,
    arguments
):

    if not isinstance(arguments, list):

        raise ValueError(
            "MCP arguments must be a list"
        )

    schema = tool.input_schema or {}

    properties = schema.get(
        "properties",
        {}
    )

    required = schema.get(
        "required",
        []
    )

    # --------------------------------------------------------
    # NO ARGUMENT MCP TOOL
    # --------------------------------------------------------

    if not properties:

        if len(arguments) == 0:
            return {}

        raise ValueError(
            f"MCP tool '{tool.name}' does not "
            f"accept arguments"
        )

    # --------------------------------------------------------
    # PARAMETERIZED MCP TOOL
    # --------------------------------------------------------

    if len(arguments) != 1:

        raise ValueError(
            f"MCP tool '{tool.name}' requires "
            f"exactly one argument object"
        )

    mcp_arguments = arguments[0]

    if not isinstance(
        mcp_arguments,
        dict
    ):

        raise ValueError(
            f"MCP tool '{tool.name}' arguments "
            f"must contain a dictionary"
        )

    # --------------------------------------------------------
    # REQUIRED PARAMETERS
    # --------------------------------------------------------

    missing_parameters = [
        parameter
        for parameter in required
        if parameter not in mcp_arguments
    ]

    if missing_parameters:

        raise ValueError(
            f"Missing required MCP parameters: "
            f"{missing_parameters}"
        )

    # --------------------------------------------------------
    # UNKNOWN PARAMETERS
    # --------------------------------------------------------

    invalid_parameters = [
        parameter
        for parameter in mcp_arguments
        if parameter not in properties
    ]

    if invalid_parameters:

        raise ValueError(
            f"Unknown MCP parameters: "
            f"{invalid_parameters}"
        )

    return mcp_arguments


# ============================================================
# MCP TOOL DESCRIPTION
# ============================================================

def get_mcp_tool_description(
    mcp_tools
):

    descriptions = []

    for tool in mcp_tools:

        descriptions.append(
            {
                "tool_name": tool.name,
                "tool_description": tool.description,
                "input_schema": tool.input_schema
            }
        )

    return descriptions


# ============================================================
# EXECUTE MCP TOOL
# ============================================================

def execute_mcp_tool(
    mcp_client,
    tool_name,
    arguments
):

    print(
        f"\n[MCP REQUEST]"
    )

    print(
        f"Tool: {tool_name}"
    )

    print(
        f"Arguments: {arguments}"
    )

    tool = get_mcp_tool(
        mcp_client.get_tools(),
        tool_name
    )

    if tool is None:

        raise ValueError(
            f"MCP tool '{tool_name}' not found"
        )

    mcp_arguments = parse_mcp_arguments(
        tool,
        arguments
    )

    print(
        f"[MCP PARSED ARGUMENTS] "
        f"{mcp_arguments}"
    )

    # IMPORTANT:
    # This call does NOT create another MCP session.
    #
    # It reuses the same persistent session.

    result = mcp_client.call_tool(
        tool_name,
        mcp_arguments
    )

    return result


# ============================================================
# CONVERT MCP RESULT
# ============================================================

def convert_result_to_text(result):

    try:

        if hasattr(result, "content"):

            output = []

            for item in result.content:

                if hasattr(item, "text"):

                    output.append(
                        item.text
                    )

                else:

                    output.append(
                        str(item)
                    )

            return "\n".join(output)

        return str(result)

    except Exception:

        return str(result)


# ============================================================
# MAIN APPLICATION
# ============================================================

def main():

    print(
        "\nStarting persistent Playwright MCP client..."
    )

    # --------------------------------------------------------
    # START MCP CLIENT ONCE
    # --------------------------------------------------------

    mcp_client = PersistentMCPClient(
        MCP_URL
    )

    print(
        "\nPlaywright MCP connected."
    )

    # --------------------------------------------------------
    # MCP TOOLS
    # --------------------------------------------------------

    mcp_tools = mcp_client.get_tools()

    mcp_tool_names = {
        tool.name
        for tool in mcp_tools
    }

    print(
        f"MCP tools available: "
        f"{len(mcp_tools)}"
    )

    # --------------------------------------------------------
    # TOOL DESCRIPTIONS
    # --------------------------------------------------------

    filex_tools = file_client.get_tool_desc()

    mcp_descriptions = (
        get_mcp_tool_description(
            mcp_tools
        )
    )

    all_tools = {
        "filex_tools": filex_tools,
        "mcp_tools": mcp_descriptions
    }

    tools_text = json.dumps(
        all_tools,
        indent=2,
        default=str
    )

    print(
        "\nAgent ready."
    )

    # --------------------------------------------------------
    # USER LOOP
    # --------------------------------------------------------

    try:

        while True:

            user_input = input(
                "\nUser: "
            )

            if user_input.lower() in [
                "exit",
                "quit"
            ]:

                break

            context = f"""
User request:
{user_input}

Available tools:
{tools_text}
"""

            # ------------------------------------------------
            # AGENT LOOP
            # ------------------------------------------------

            while True:

                prompt = f"""
{RESPONSE_PROTOCOL}

{context}

Return exactly one JSON object.
"""

                response = gemini_ai_client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                raw_response = response.text.strip()

                print(
                    f"\n[MODEL RAW RESPONSE]\n"
                    f"{raw_response}"
                )

                # --------------------------------------------
                # PARSE MODEL RESPONSE
                # --------------------------------------------

                try:

                    agent_response = json.loads(
                        raw_response
                    )

                except json.JSONDecodeError as e:

                    print(
                        f"\nInvalid JSON from model: {e}"
                    )

                    break

                response_type = agent_response.get(
                    "type"
                )

                # --------------------------------------------
                # MESSAGE
                # --------------------------------------------

                if response_type == "message":

                    message = agent_response.get(
                        "content",
                        ""
                    )

                    print(
                        f"\nAgent: {message}"
                    )

                    break

                # --------------------------------------------
                # TOOL CALL
                # --------------------------------------------

                if response_type != "tool_call":

                    print(
                        "\nInvalid response type"
                    )

                    break

                tool_name = agent_response.get(
                    "tool_name"
                )

                arguments = agent_response.get(
                    "arguments",
                    []
                )

                print(
                    f"\nRequested tool: "
                    f"{tool_name}"
                )

                print(
                    f"Arguments: "
                    f"{arguments}"
                )

                # --------------------------------------------
                # MCP TOOL
                # --------------------------------------------

                if tool_name in mcp_tool_names:

                    try:

                        result = execute_mcp_tool(
                            mcp_client,
                            tool_name,
                            arguments
                        )

                        result_text = (
                            convert_result_to_text(
                                result
                            )
                        )

                    except Exception as e:

                        result_text = (
                            f"ERROR: {e}"
                        )

                        print(
                            "\nMCP tool execution failed:"
                        )

                        print(e)

                        # ------------------------------------
                        # DO NOT BLINDLY RETRY A DEAD SESSION
                        # ------------------------------------

                        if "Session terminated" in str(e):

                            print(
                                "\nMCP session terminated."
                            )

                            print(
                                "Stopping current agent task."
                            )

                            break

                # --------------------------------------------
                # FILEX TOOL
                # --------------------------------------------

                else:

                    try:

                        tool_fn = getattr(
                            file_client,
                            tool_name
                        )

                    except AttributeError:

                        result_text = (
                            f"ERROR: "
                            f"Unknown tool '{tool_name}'"
                        )

                    else:

                        try:
                            if tool_name in file_client.get_critical_fn():
                                user_confirmation = input(f"Agent want to run tool {tool_name} type (y/n)")
                            
                                if user_confirmation == 'n' or user_confirmation == "N":
                                    result_text = f"User didn't give the permission to run tool {tool_name}"
                                elif user_confirmation=="y" or user_confirmation=="Y":
                                   result = tool_fn(
                                       arguments
                                   )
       
                                   result_text = str(
                                       result
                                   )
                                else:
                                    result_text = f"User didn't gave the permission to execute tool {tool_name}"
                            else:
                                result = tool_fn(
                                       arguments
                                   )
       
                                result_text = str(
                                       result
                                   )


                        except Exception as e:

                            result_text = (
                                f"ERROR: {e}"
                            )

                # --------------------------------------------
                # ADD TOOL RESULT TO CONTEXT
                # --------------------------------------------

                context += f"""

Tool called:
{tool_name}

Tool arguments:
{json.dumps(arguments, default=str)}

Tool result:
{result_text}
"""

                print(
                    f"\n[TOOL RESULT]\n"
                    f"{result_text}"
                )

    finally:

        # ----------------------------------------------------
        # CLOSE MCP ONLY WHEN APPLICATION EXITS
        # ----------------------------------------------------

        mcp_client.close()

        print(
            "\nApplication closed."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
 