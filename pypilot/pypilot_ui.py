import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

import threading
import queue
import json

from pypilot import (
    gemini_ai_client,
    file_client,
    PersistentMCPClient,
    execute_mcp_tool,
    convert_result_to_text,
    get_mcp_tool_description,
    RESPONSE_PROTOCOL,
    MCP_URL,
)


# ============================================================
# UI COLORS / CONFIG
# ============================================================

WINDOW_TITLE = "PyPilot - AI QA Automation Agent"

FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

BG_COLOR = "#f5f6f8"
CHAT_BG = "#ffffff"
USER_BG = "#e8f0fe"
AGENT_BG = "#eef7ee"
TOOL_BG = "#fff8e5"
ERROR_BG = "#fdecec"


# ============================================================
# PYPILOT APPLICATION
# ============================================================

class PyPilotUI:

    def __init__(self, root):

        self.root = root

        self.root.title(WINDOW_TITLE)

        self.root.geometry("1100x750")

        self.root.minsize(850, 600)

        self.root.configure(
            bg=BG_COLOR
        )

        # ----------------------------------------------------
        # THREAD COMMUNICATION
        # ----------------------------------------------------

        self.ui_queue = queue.Queue()

        self.agent_running = False

        # ----------------------------------------------------
        # MCP CLIENT
        # ----------------------------------------------------

        self.mcp_client = None

        self.mcp_tools = []

        self.mcp_tool_names = set()

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.create_header()

        self.create_chat_area()

        self.create_input_area()

        self.create_status_bar()

        # ----------------------------------------------------
        # START BACKEND
        # ----------------------------------------------------

        self.root.after(
            100,
            self.start_backend
        )

        # ----------------------------------------------------
        # CHECK UI QUEUE
        # ----------------------------------------------------

        self.root.after(
            100,
            self.process_ui_queue
        )

        # ----------------------------------------------------
        # WINDOW CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f2937",
            height=60
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="PyPilot",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 17, "bold")
        )

        title.pack(
            side="left",
            padx=20
        )

        subtitle = tk.Label(
            header,
            text="AI QA Automation Agent",
            bg="#1f2937",
            fg="#cbd5e1",
            font=("Segoe UI", 9)
        )

        subtitle.pack(
            side="left"
        )

        self.connection_label = tk.Label(
            header,
            text="● Connecting...",
            bg="#1f2937",
            fg="#fbbf24",
            font=FONT_BOLD
        )

        self.connection_label.pack(
            side="right",
            padx=20
        )

    # ========================================================
    # CHAT AREA
    # ========================================================

    def create_chat_area(self):

        container = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(15, 5)
        )

        self.chat = ScrolledText(
            container,
            wrap="word",
            font=FONT,
            bg=CHAT_BG,
            fg="#111827",
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=15,
            state="disabled"
        )

        self.chat.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # TAGS
        # ----------------------------------------------------

        self.chat.tag_config(
            "user_name",
            foreground="#2563eb",
            font=FONT_BOLD
        )

        self.chat.tag_config(
            "agent_name",
            foreground="#15803d",
            font=FONT_BOLD
        )

        self.chat.tag_config(
            "tool_name",
            foreground="#b45309",
            font=FONT_BOLD
        )

        self.chat.tag_config(
            "error_name",
            foreground="#dc2626",
            font=FONT_BOLD
        )

        self.chat.tag_config(
            "normal",
            foreground="#111827"
        )

    # ========================================================
    # INPUT AREA
    # ========================================================

    def create_input_area(self):

        outer = tk.Frame(
            self.root,
            bg=BG_COLOR
        )

        outer.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.input_box = tk.Text(
            outer,
            height=4,
            wrap="word",
            font=FONT,
            relief="solid",
            borderwidth=1
        )

        self.input_box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.input_box.bind(
            "<Control-Return>",
            self.send_message
        )

        self.send_button = ttk.Button(
            outer,
            text="Send",
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            ipadx=15,
            ipady=15
        )

    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):

        status = tk.Frame(
            self.root,
            bg="#e5e7eb",
            height=30
        )

        status.pack(
            fill="x"
        )

        status.pack_propagate(False)

        self.status_label = tk.Label(
            status,
            text="Starting PyPilot...",
            bg="#e5e7eb",
            fg="#374151",
            font=("Segoe UI", 9)
        )

        self.status_label.pack(
            side="left",
            padx=15
        )

    # ========================================================
    # BACKEND START
    # ========================================================

    def start_backend(self):

        self.connection_label.config(
            text="● Connecting...",
            fg="#fbbf24"
        )

        thread = threading.Thread(
            target=self.initialize_backend,
            daemon=True
        )

        thread.start()

    # ========================================================
    # BACKEND INITIALIZATION
    # ========================================================

    def initialize_backend(self):

        try:

            self.mcp_client = PersistentMCPClient(
                MCP_URL
            )

            self.mcp_tools = (
                self.mcp_client.get_tools()
            )

            self.mcp_tool_names = {
                tool.name
                for tool in self.mcp_tools
            }

            self.ui_queue.put(
                (
                    "backend_ready",
                    None
                )
            )

        except Exception as e:

            self.ui_queue.put(
                (
                    "backend_error",
                    str(e)
                )
            )

    # ========================================================
    # ADD CHAT MESSAGE
    # ========================================================

    def add_message(
        self,
        sender,
        message,
        message_type="normal"
    ):

        self.chat.config(
            state="normal"
        )

        if sender == "You":

            self.chat.insert(
                "end",
                "\nYou\n",
                "user_name"
            )

        elif sender == "PyPilot":

            self.chat.insert(
                "end",
                "\nPyPilot\n",
                "agent_name"
            )

        elif sender == "Tool":

            self.chat.insert(
                "end",
                "\nTool\n",
                "tool_name"
            )

        elif sender == "Error":

            self.chat.insert(
                "end",
                "\nError\n",
                "error_name"
            )

        self.chat.insert(
            "end",
            message + "\n",
            "normal"
        )

        self.chat.see(
            "end"
        )

        self.chat.config(
            state="disabled"
        )

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(
        self,
        event=None
    ):

        if self.agent_running:

            return "break"

        user_input = self.input_box.get(
            "1.0",
            "end"
        ).strip()

        if not user_input:

            return "break"

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.add_message(
            "You",
            user_input
        )

        self.agent_running = True

        self.send_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Agent is working..."
        )

        thread = threading.Thread(
            target=self.run_agent,
            args=(user_input,),
            daemon=True
        )

        thread.start()

        return "break"

    # ========================================================
    # AGENT LOOP
    # ========================================================

    def run_agent(
        self,
        user_input
    ):

        try:

            filex_tools = (
                file_client.get_tool_desc()
            )

            mcp_descriptions = (
                get_mcp_tool_description(
                    self.mcp_tools
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

                raw_response = (
                    response.text.strip()
                )

                self.ui_queue.put(
                    (
                        "model_raw",
                        raw_response
                    )
                )

                # --------------------------------------------
                # PARSE JSON
                # --------------------------------------------

                try:

                    agent_response = json.loads(
                        raw_response
                    )

                except json.JSONDecodeError as e:

                    self.ui_queue.put(
                        (
                            "error",
                            f"Invalid JSON from model:\n{e}"
                        )
                    )

                    break

                response_type = (
                    agent_response.get("type")
                )

                # --------------------------------------------
                # MESSAGE
                # --------------------------------------------

                if response_type == "message":

                    message = (
                        agent_response.get(
                            "content",
                            ""
                        )
                    )

                    self.ui_queue.put(
                        (
                            "agent_message",
                            message
                        )
                    )

                    break

                # --------------------------------------------
                # INVALID RESPONSE
                # --------------------------------------------

                if response_type != "tool_call":

                    self.ui_queue.put(
                        (
                            "error",
                            "Invalid response type."
                        )
                    )

                    break

                # --------------------------------------------
                # TOOL CALL
                # --------------------------------------------

                tool_name = (
                    agent_response.get(
                        "tool_name"
                    )
                )

                arguments = (
                    agent_response.get(
                        "arguments",
                        []
                    )
                )

                self.ui_queue.put(
                    (
                        "tool_requested",
                        (
                            tool_name,
                            arguments
                        )
                    )
                )

                # --------------------------------------------
                # MCP TOOL
                # --------------------------------------------

                if tool_name in self.mcp_tool_names:

                    try:

                        result = execute_mcp_tool(
                            self.mcp_client,
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
                            f"ERROR: Unknown tool "
                            f"'{tool_name}'"
                        )

                    else:

                        # ------------------------------------
                        # CRITICAL TOOL
                        # ------------------------------------

                        if tool_name in (
                            file_client.get_critical_fn()
                        ):

                            approved = (
                                self.request_confirmation(
                                    tool_name,
                                    arguments
                                )
                            )

                            if not approved:

                                result_text = (
                                    f"User denied execution "
                                    f"of tool '{tool_name}'."
                                )

                            else:

                                try:

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

                        # ------------------------------------
                        # NORMAL TOOL
                        # ------------------------------------

                        else:

                            try:

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
                # DISPLAY TOOL RESULT
                # --------------------------------------------

                self.ui_queue.put(
                    (
                        "tool_result",
                        (
                            tool_name,
                            result_text
                        )
                    )
                )

                # --------------------------------------------
                # ADD TO AGENT CONTEXT
                # --------------------------------------------

                context += f"""

Tool called:
{tool_name}

Tool arguments:
{json.dumps(arguments, default=str)}

Tool result:
{result_text}
"""

        except Exception as e:

            self.ui_queue.put(
                (
                    "error",
                    str(e)
                )
            )

        finally:

            self.ui_queue.put(
                (
                    "agent_finished",
                    None
                )
            )

    # ========================================================
    # CONFIRMATION
    # ========================================================

    def request_confirmation(
        self,
        tool_name,
        arguments
    ):

        result = {
            "approved": False
        }

        event = threading.Event()

        self.ui_queue.put(
            (
                "confirmation",
                (
                    tool_name,
                    arguments,
                    result,
                    event
                )
            )
        )

        event.wait()

        return result["approved"]

    # ========================================================
    # UI QUEUE PROCESSOR
    # ========================================================

    def process_ui_queue(self):

        try:

            while True:

                message_type, data = (
                    self.ui_queue.get_nowait()
                )

                # --------------------------------------------
                # BACKEND READY
                # --------------------------------------------

                if message_type == "backend_ready":

                    self.connection_label.config(
                        text="● Connected",
                        fg="#22c55e"
                    )

                    self.status_label.config(
                        text="Ready"
                    )

                    self.add_message(
                        "PyPilot",
                        "PyPilot is ready. "
                        "You can ask me to inspect files, "
                        "run tests, or interact with "
                        "Playwright."
                    )

                # --------------------------------------------
                # BACKEND ERROR
                # --------------------------------------------

                elif message_type == "backend_error":

                    self.connection_label.config(
                        text="● Disconnected",
                        fg="#ef4444"
                    )

                    self.status_label.config(
                        text="Backend connection failed"
                    )

                    self.add_message(
                        "Error",
                        data
                    )

                # --------------------------------------------
                # MODEL RAW
                # --------------------------------------------

                elif message_type == "model_raw":

                    # Keep raw model output out of normal chat.
                    # Print it in terminal for debugging.

                    print(
                        "\n[MODEL RAW RESPONSE]"
                    )

                    print(data)

                # --------------------------------------------
                # AGENT MESSAGE
                # --------------------------------------------

                elif message_type == "agent_message":

                    self.add_message(
                        "PyPilot",
                        data
                    )

                # --------------------------------------------
                # TOOL REQUESTED
                # --------------------------------------------

                elif message_type == "tool_requested":

                    tool_name, arguments = data

                    self.add_message(
                        "Tool",
                        f"{tool_name}\n"
                        f"Arguments: "
                        f"{json.dumps(arguments, indent=2)}"
                    )

                # --------------------------------------------
                # TOOL RESULT
                # --------------------------------------------

                elif message_type == "tool_result":

                    tool_name, result = data

                    self.add_message(
                        "Tool",
                        f"{tool_name} result:\n{result}"
                    )

                # --------------------------------------------
                # CONFIRMATION
                # --------------------------------------------

                elif message_type == "confirmation":

                    (
                        tool_name,
                        arguments,
                        result,
                        event
                    ) = data

                    approved = messagebox.askyesno(
                        "Tool Execution Confirmation",
                        (
                            f"PyPilot wants to execute:\n\n"
                            f"Tool: {tool_name}\n\n"
                            f"Arguments:\n"
                            f"{json.dumps(arguments, indent=2)}\n\n"
                            f"Allow execution?"
                        ),
                        parent=self.root
                    )

                    result["approved"] = approved

                    event.set()

                # --------------------------------------------
                # ERROR
                # --------------------------------------------

                elif message_type == "error":

                    self.add_message(
                        "Error",
                        data
                    )

                # --------------------------------------------
                # AGENT FINISHED
                # --------------------------------------------

                elif message_type == "agent_finished":

                    self.agent_running = False

                    self.send_button.config(
                        state="normal"
                    )

                    self.status_label.config(
                        text="Ready"
                    )

        except queue.Empty:

            pass

        self.root.after(
            100,
            self.process_ui_queue
        )

    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        if self.agent_running:

            answer = messagebox.askyesno(
                "Exit PyPilot",
                "An agent task is still running.\n\n"
                "Do you want to exit?"
            )

            if not answer:

                return

        try:

            if self.mcp_client:

                self.mcp_client.close()

        except Exception as e:

            print(
                f"Error closing MCP client: {e}"
            )

        self.root.destroy()


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

def main():

    root = tk.Tk()

    app = PyPilotUI(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()