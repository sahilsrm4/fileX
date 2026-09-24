
import tkinter as tk
from tkinter import ttk, messagebox

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
# CONFIGURATION
# ============================================================

WINDOW_TITLE = "PyPilot — AI QA Automation Agent"

WINDOW_WIDTH = 1250
WINDOW_HEIGHT = 800

MIN_WIDTH = 950
MIN_HEIGHT = 650


# ============================================================
# COLORS
# ============================================================

BG = "#0b1120"

SIDEBAR_BG = "#0f172a"

PANEL = "#111827"

PANEL_LIGHT = "#172033"

PANEL_HOVER = "#1e293b"

BORDER = "#263449"

TEXT = "#f1f5f9"

TEXT_SECONDARY = "#94a3b8"

TEXT_MUTED = "#64748b"

WHITE = "#ffffff"

PRIMARY = "#6366f1"

PRIMARY_HOVER = "#818cf8"

USER_BUBBLE = "#172554"

USER_BORDER = "#1d4ed8"

AGENT_BUBBLE = "#151f2f"

AGENT_BORDER = "#334155"

TOOL_BUBBLE = "#241a08"

TOOL_BORDER = "#92400e"

ERROR_BUBBLE = "#2a1010"

ERROR_BORDER = "#991b1b"

GREEN = "#22c55e"

ORANGE = "#f59e0b"

RED = "#ef4444"

BLUE = "#38bdf8"

PURPLE = "#a78bfa"


# ============================================================
# FONTS
# ============================================================

FONT = ("Segoe UI", 10)

FONT_SMALL = ("Segoe UI", 9)

FONT_TINY = ("Segoe UI", 8)

FONT_BOLD = ("Segoe UI", 10, "bold")

FONT_TITLE = ("Segoe UI", 16, "bold")

FONT_CODE = ("Consolas", 9)


# ============================================================
# PYPILOT UI
# ============================================================

class PyPilotUI:

    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title(WINDOW_TITLE)

        self.root.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.root.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        self.root.configure(
            bg=BG
        )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.ui_queue = queue.Queue()

        self.agent_running = False

        self.application_closing = False

        self.backend_ready = False

        self.message_count = 0

        self.tool_count = 0

        self.current_request_id = 0

        # ----------------------------------------------------
        # CHAT SCROLL STATE
        # ----------------------------------------------------

        self.chat_auto_scroll = True

        self.chat_scroll_threshold = 0.05

        # ----------------------------------------------------
        # MCP
        # ----------------------------------------------------

        self.mcp_client = None

        self.mcp_tools = []

        self.mcp_tool_names = set()

        # ----------------------------------------------------
        # TYPING INDICATOR
        # ----------------------------------------------------

        self.typing_frame = None

        self.typing_animation_id = None

        self.typing_dots = 0

        # ----------------------------------------------------
        # BUILD UI
        # ----------------------------------------------------

        self.setup_styles()

        self.create_main_layout()

        # ----------------------------------------------------
        # START QUEUE
        # ----------------------------------------------------

        self.root.after(
            100,
            self.process_ui_queue
        )

        # ----------------------------------------------------
        # START BACKEND
        # ----------------------------------------------------

        self.root.after(
            200,
            self.start_backend
        )

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )


    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "PyPilot.TButton",
            background=PRIMARY,
            foreground=WHITE,
            borderwidth=0,
            padding=(16, 9),
            font=FONT_BOLD
        )

        style.map(
            "PyPilot.TButton",
            background=[
                (
                    "active",
                    PRIMARY_HOVER
                ),
                (
                    "disabled",
                    "#334155"
                )
            ]
        )


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_main_layout(self):

        self.main_frame = tk.Frame(
            self.root,
            bg=BG
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        self.create_sidebar()

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        self.content_frame = tk.Frame(
            self.main_frame,
            bg=BG
        )

        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_header()

        self.create_chat()

        self.create_composer()

        self.create_status_bar()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self.main_frame,
            width=245,
            bg=SIDEBAR_BG
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_BG
        )

        logo.pack(
            fill="x",
            padx=20,
            pady=(25, 30)
        )

        tk.Label(
            logo,
            text="✦",
            bg=SIDEBAR_BG,
            fg=PRIMARY_HOVER,
            font=("Segoe UI", 28, "bold")
        ).pack(
            side="left"
        )

        logo_text = tk.Frame(
            logo,
            bg=SIDEBAR_BG
        )

        logo_text.pack(
            side="left",
            padx=10
        )

        tk.Label(
            logo_text,
            text="PyPilot",
            bg=SIDEBAR_BG,
            fg=WHITE,
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            logo_text,
            text="AI QA AUTOMATION",
            bg=SIDEBAR_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 7, "bold")
        ).pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # SECTION
        # ----------------------------------------------------

        tk.Label(
            self.sidebar,
            text="WORKSPACE",
            bg=SIDEBAR_BG,
            fg=TEXT_MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 10)
        )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        self.create_sidebar_button(
            "✦",
            "Agent",
            self.show_agent
        )

        self.create_sidebar_button(
            "⚙",
            "Tools",
            self.show_tools
        )

        self.create_sidebar_button(
            "◈",
            "Activity",
            self.show_activity
        )

        self.create_sidebar_button(
            "＋",
            "New Chat",
            self.new_chat
        )

        # ----------------------------------------------------
        # SPACER
        # ----------------------------------------------------

        tk.Frame(
            self.sidebar,
            bg=SIDEBAR_BG
        ).pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SYSTEM CARD
        # ----------------------------------------------------

        card = tk.Frame(
            self.sidebar,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            padx=14,
            pady=14
        )

        tk.Label(
            card,
            text="SYSTEM STATUS",
            bg=PANEL,
            fg=TEXT_MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 5)
        )

        self.sidebar_connection = tk.Label(
            card,
            text="●  Connecting...",
            bg=PANEL,
            fg=ORANGE,
            font=FONT_SMALL
        )

        self.sidebar_connection.pack(
            anchor="w",
            padx=12,
            pady=(0, 10)
        )


    # ========================================================
    # SIDEBAR BUTTON
    # ========================================================

    def create_sidebar_button(
        self,
        icon,
        text,
        command
    ):

        frame = tk.Frame(
            self.sidebar,
            bg=SIDEBAR_BG,
            height=42,
            cursor="hand2"
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=2
        )

        frame.pack_propagate(False)

        icon_label = tk.Label(
            frame,
            text=icon,
            bg=SIDEBAR_BG,
            fg=TEXT_SECONDARY,
            font=("Segoe UI", 13)
        )

        icon_label.pack(
            side="left",
            padx=(12, 12)
        )

        text_label = tk.Label(
            frame,
            text=text,
            bg=SIDEBAR_BG,
            fg=TEXT_SECONDARY,
            font=FONT
        )

        text_label.pack(
            side="left"
        )

        widgets = (
            frame,
            icon_label,
            text_label
        )

        for widget in widgets:

            widget.bind(
                "<Button-1>",
                lambda event, fn=command: fn()
            )

            widget.bind(
                "<Enter>",
                lambda event,
                f=frame,
                i=icon_label,
                t=text_label:
                self.sidebar_hover(
                    f,
                    i,
                    t,
                    True
                )
            )

            widget.bind(
                "<Leave>",
                lambda event,
                f=frame,
                i=icon_label,
                t=text_label:
                self.sidebar_hover(
                    f,
                    i,
                    t,
                    False
                )
            )


    # ========================================================
    # SIDEBAR HOVER
    # ========================================================

    def sidebar_hover(
        self,
        frame,
        icon_label,
        text_label,
        active
    ):

        if active:

            bg = PANEL_LIGHT
            fg = WHITE

        else:

            bg = SIDEBAR_BG
            fg = TEXT_SECONDARY

        frame.configure(
            bg=bg
        )

        icon_label.configure(
            bg=bg,
            fg=fg
        )

        text_label.configure(
            bg=bg,
            fg=fg
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.content_frame,
            bg=BG,
            height=72
        )

        header.pack(
            fill="x",
            padx=25
        )

        header.pack_propagate(False)

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_frame = tk.Frame(
            header,
            bg=BG
        )

        title_frame.pack(
            side="left",
            pady=12
        )

        self.header_title = tk.Label(
            title_frame,
            text="AI Automation Workspace",
            bg=BG,
            fg=TEXT,
            font=FONT_TITLE
        )

        self.header_title.pack(
            anchor="w"
        )

        self.header_subtitle = tk.Label(
            title_frame,
            text="Inspect • Test • Automate • Debug",
            bg=BG,
            fg=TEXT_MUTED,
            font=FONT_SMALL
        )

        self.header_subtitle.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # CONNECTION
        # ----------------------------------------------------

        self.connection_label = tk.Label(
            header,
            text="●  Connecting",
            bg=PANEL,
            fg=ORANGE,
            font=FONT_BOLD,
            padx=14,
            pady=7
        )

        self.connection_label.pack(
            side="right",
            pady=17
        )


    # ========================================================
    # CHAT
    # ========================================================

    def create_chat(self):

        outer = tk.Frame(
            self.content_frame,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 12)
        )

        # ----------------------------------------------------
        # CANVAS
        # ----------------------------------------------------

        self.chat_canvas = tk.Canvas(
            outer,
            bg=PANEL,
            highlightthickness=0,
            bd=0
        )

        self.chat_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SCROLLBAR
        # ----------------------------------------------------

        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=self.chat_canvas.yview
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.chat_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.chat_scrollbar = scrollbar

        # ----------------------------------------------------
        # CHAT CONTENT
        # ----------------------------------------------------

        self.chat_frame = tk.Frame(
            self.chat_canvas,
            bg=PANEL
        )

        self.chat_window = (
            self.chat_canvas.create_window(
                (0, 0),
                window=self.chat_frame,
                anchor="nw"
            )
        )

        # ----------------------------------------------------
        # RESIZE EVENTS
        # ----------------------------------------------------

        self.chat_frame.bind(
            "<Configure>",
            self.on_chat_frame_configure
        )

        self.chat_canvas.bind(
            "<Configure>",
            self.on_chat_canvas_configure
        )

        # ----------------------------------------------------
        # MOUSE WHEEL
        # ----------------------------------------------------

        self.chat_canvas.bind(
            "<MouseWheel>",
            self.on_chat_mousewheel
        )

        self.chat_frame.bind(
            "<MouseWheel>",
            self.on_chat_mousewheel
        )

        # Linux support

        self.chat_canvas.bind(
            "<Button-4>",
            self.on_chat_mousewheel_linux_up
        )

        self.chat_canvas.bind(
            "<Button-5>",
            self.on_chat_mousewheel_linux_down
        )

        self.chat_frame.bind(
            "<Button-4>",
            self.on_chat_mousewheel_linux_up
        )

        self.chat_frame.bind(
            "<Button-5>",
            self.on_chat_mousewheel_linux_down
        )


    # ========================================================
    # CHAT RESIZE
    #
    # IMPORTANT:
    # DO NOT AUTO-SCROLL HERE.
    # ========================================================

    def on_chat_frame_configure(
        self,
        event=None
    ):

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )


    # ========================================================
    # CANVAS RESIZE
    # ========================================================

    def on_chat_canvas_configure(
        self,
        event
    ):

        try:

            self.chat_canvas.itemconfigure(
                self.chat_window,
                width=event.width
            )

        except Exception:

            pass


    # ========================================================
    # CHECK IF USER IS NEAR BOTTOM
    # ========================================================

    def is_chat_near_bottom(self):

        try:

            first, last = self.chat_canvas.yview()

            return (
                last >=
                1.0 - self.chat_scroll_threshold
            )

        except Exception:

            return True


    # ========================================================
    # MOUSE WHEEL
    # ========================================================

    def on_chat_mousewheel(
        self,
        event
    ):

        try:

            if event.delta:

                amount = int(
                    -1 * (event.delta / 120)
                )

                if amount == 0:

                    amount = (
                        -1
                        if event.delta > 0
                        else 1
                    )

                self.chat_canvas.yview_scroll(
                    amount,
                    "units"
                )

            self.chat_auto_scroll = (
                self.is_chat_near_bottom()
            )

        except Exception:

            pass

        return "break"


    # ========================================================
    # LINUX MOUSE WHEEL UP
    # ========================================================

    def on_chat_mousewheel_linux_up(
        self,
        event
    ):

        try:

            self.chat_canvas.yview_scroll(
                -3,
                "units"
            )

            self.chat_auto_scroll = (
                self.is_chat_near_bottom()
            )

        except Exception:

            pass

        return "break"


    # ========================================================
    # LINUX MOUSE WHEEL DOWN
    # ========================================================

    def on_chat_mousewheel_linux_down(
        self,
        event
    ):

        try:

            self.chat_canvas.yview_scroll(
                3,
                "units"
            )

            self.chat_auto_scroll = (
                self.is_chat_near_bottom()
            )

        except Exception:

            pass

        return "break"


    # ========================================================
    # SCROLL TO BOTTOM
    # ========================================================

    def scroll_chat_to_bottom(self):

        try:

            self.chat_canvas.update_idletasks()

            self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )

            self.chat_canvas.yview_moveto(
                1.0
            )

            self.chat_auto_scroll = True

        except Exception:

            pass


    # ========================================================
    # AUTO SCROLL AFTER NEW MESSAGE
    # ========================================================

    def scroll_if_needed(
        self,
        was_near_bottom
    ):

        if not was_near_bottom:

            return

        try:

            self.chat_canvas.update_idletasks()

            self.chat_canvas.configure(
                scrollregion=self.chat_canvas.bbox("all")
            )

            self.chat_canvas.yview_moveto(
                1.0
            )

        except Exception:

            pass


    # ========================================================
    # CREATE MESSAGE BUBBLE
    # ========================================================

    def add_message(
        self,
        sender,
        message
    ):

        if self.application_closing:

            return

        # ----------------------------------------------------
        # CHECK POSITION BEFORE ADDING MESSAGE
        # ----------------------------------------------------

        was_near_bottom = (
            self.is_chat_near_bottom()
        )

        self.message_count += 1

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        if sender == "You":

            bubble_bg = USER_BUBBLE
            bubble_border = USER_BORDER
            name_color = BLUE
            icon = "●"

        elif sender == "PyPilot":

            bubble_bg = AGENT_BUBBLE
            bubble_border = AGENT_BORDER
            name_color = PURPLE
            icon = "✦"

        elif sender == "Tool":

            bubble_bg = TOOL_BUBBLE
            bubble_border = TOOL_BORDER
            name_color = ORANGE
            icon = "⚙"

        elif sender == "Error":

            bubble_bg = ERROR_BUBBLE
            bubble_border = ERROR_BORDER
            name_color = RED
            icon = "!"

        else:

            bubble_bg = PANEL_LIGHT
            bubble_border = BORDER
            name_color = TEXT
            icon = "•"

        # ----------------------------------------------------
        # ROW
        # ----------------------------------------------------

        row = tk.Frame(
            self.chat_frame,
            bg=PANEL
        )

        row.pack(
            fill="x",
            padx=20,
            pady=6
        )

        # ----------------------------------------------------
        # BUBBLE
        # ----------------------------------------------------

        bubble = tk.Frame(
            row,
            bg=bubble_bg,
            highlightbackground=bubble_border,
            highlightthickness=1
        )

        if sender == "You":

            bubble.pack(
                side="right",
                anchor="e"
            )

        else:

            bubble.pack(
                side="left",
                anchor="w"
            )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            bubble,
            bg=bubble_bg
        )

        header.pack(
            fill="x",
            padx=14,
            pady=(10, 4)
        )

        tk.Label(
            header,
            text=f"{icon}  {sender}",
            bg=bubble_bg,
            fg=name_color,
            font=FONT_BOLD
        ).pack(
            side="left"
        )

        # ----------------------------------------------------
        # BODY
        # ----------------------------------------------------

        body = tk.Frame(
            bubble,
            bg=bubble_bg
        )

        body.pack(
            fill="both",
            padx=14,
            pady=(0, 12)
        )

        # ----------------------------------------------------
        # TOOL MESSAGE
        # ----------------------------------------------------

        if sender == "Tool":

            text_font = FONT_CODE

        else:

            text_font = FONT

        message_label = tk.Label(
            body,
            text=str(message),
            bg=bubble_bg,
            fg=TEXT,
            font=text_font,
            justify="left",
            anchor="w",
            wraplength=750
        )

        message_label.pack(
            anchor="w"
        )

        # ----------------------------------------------------
        # RIGHT CLICK COPY
        # ----------------------------------------------------

        self.bind_copy_menu(
            message_label,
            str(message)
        )

        # ----------------------------------------------------
        # ALSO SUPPORT MOUSE WHEEL OVER MESSAGE
        # ----------------------------------------------------

        message_label.bind(
            "<MouseWheel>",
            self.on_chat_mousewheel
        )

        message_label.bind(
            "<Button-4>",
            self.on_chat_mousewheel_linux_up
        )

        message_label.bind(
            "<Button-5>",
            self.on_chat_mousewheel_linux_down
        )

        # ----------------------------------------------------
        # FORCE GEOMETRY UPDATE
        # ----------------------------------------------------

        self.chat_frame.update_idletasks()

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )

        # ----------------------------------------------------
        # SMART AUTO SCROLL
        # ----------------------------------------------------

        self.scroll_if_needed(
            was_near_bottom
        )


    # ========================================================
    # COPY MENU
    # ========================================================

    def bind_copy_menu(
        self,
        widget,
        text
    ):

        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg=PANEL_LIGHT,
            fg=TEXT,
            activebackground=PRIMARY,
            activeforeground=WHITE
        )

        menu.add_command(
            label="Copy",
            command=lambda: self.copy_text(text)
        )

        widget.bind(
            "<Button-3>",
            lambda event: self.show_context_menu(
                menu,
                event
            )
        )


    # ========================================================
    # CONTEXT MENU
    # ========================================================

    def show_context_menu(
        self,
        menu,
        event
    ):

        try:

            menu.tk_popup(
                event.x_root,
                event.y_root
            )

        finally:

            menu.grab_release()


    # ========================================================
    # COPY
    # ========================================================

    def copy_text(
        self,
        text
    ):

        try:

            self.root.clipboard_clear()

            self.root.clipboard_append(
                text
            )

            self.root.update()

        except Exception:

            pass


    # ========================================================
    # TYPING INDICATOR
    # ========================================================

    def show_typing_indicator(self):

        if self.typing_frame is not None:

            return

        was_near_bottom = (
            self.is_chat_near_bottom()
        )

        row = tk.Frame(
            self.chat_frame,
            bg=PANEL
        )

        row.pack(
            fill="x",
            padx=20,
            pady=6
        )

        bubble = tk.Frame(
            row,
            bg=AGENT_BUBBLE,
            highlightbackground=AGENT_BORDER,
            highlightthickness=1
        )

        bubble.pack(
            side="left"
        )

        self.typing_frame = bubble

        self.typing_label = tk.Label(
            bubble,
            text="✦  PyPilot is thinking...",
            bg=AGENT_BUBBLE,
            fg=TEXT_SECONDARY,
            font=FONT_SMALL,
            padx=14,
            pady=10
        )

        self.typing_label.pack()

        self.typing_dots = 0

        self.animate_typing()

        self.chat_frame.update_idletasks()

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )

        self.scroll_if_needed(
            was_near_bottom
        )


    # ========================================================
    # TYPING ANIMATION
    # ========================================================

    def animate_typing(self):

        if self.typing_frame is None:

            return

        self.typing_dots += 1

        dots = "." * (
            self.typing_dots % 4
        )

        self.typing_label.config(
            text=f"✦  PyPilot is thinking{dots}"
        )

        self.typing_animation_id = (
            self.root.after(
                400,
                self.animate_typing
            )
        )


    # ========================================================
    # HIDE TYPING
    # ========================================================

    def hide_typing_indicator(self):

        if self.typing_animation_id:

            try:

                self.root.after_cancel(
                    self.typing_animation_id
                )

            except Exception:

                pass

            self.typing_animation_id = None

        if self.typing_frame:

            try:

                self.typing_frame.destroy()

            except Exception:

                pass

            self.typing_frame = None

        self.chat_frame.update_idletasks()

        self.chat_canvas.configure(
            scrollregion=self.chat_canvas.bbox("all")
        )


    # ========================================================
    # COMPOSER
    # ========================================================

    def create_composer(self):

        outer = tk.Frame(
            self.content_frame,
            bg=BG
        )

        outer.pack(
            fill="x",
            padx=25,
            pady=(0, 8)
        )

        composer = tk.Frame(
            outer,
            bg=PANEL_LIGHT,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        composer.pack(
            fill="x"
        )

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        self.input_box = tk.Text(
            composer,
            height=3,
            wrap="word",
            bg=PANEL_LIGHT,
            fg=TEXT,
            insertbackground=WHITE,
            selectbackground=PRIMARY,
            relief="flat",
            borderwidth=0,
            font=FONT,
            padx=15,
            pady=12
        )

        self.input_box.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # CTRL + ENTER
        # ----------------------------------------------------

        self.input_box.bind(
            "<Control-Return>",
            self.send_message
        )

        # ----------------------------------------------------
        # SEND
        # ----------------------------------------------------

        self.send_button = ttk.Button(
            composer,
            text="Send  ➜",
            style="PyPilot.TButton",
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5
        )

        # ----------------------------------------------------
        # HINT
        # ----------------------------------------------------

        tk.Label(
            outer,
            text=(
                "Ctrl + Enter to send"
                "   •   "
                "FileX"
                "   •   "
                "MCP"
                "   •   "
                "Playwright"
            ),
            bg=BG,
            fg=TEXT_MUTED,
            font=FONT_TINY
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):

        status = tk.Frame(
            self.content_frame,
            bg="#080d19",
            height=30
        )

        status.pack(
            fill="x"
        )

        status.pack_propagate(False)

        self.status_label = tk.Label(
            status,
            text="Starting PyPilot...",
            bg="#080d19",
            fg=TEXT_SECONDARY,
            font=FONT_TINY
        )

        self.status_label.pack(
            side="left",
            padx=25
        )

        self.activity_label = tk.Label(
            status,
            text="Tools: 0",
            bg="#080d19",
            fg=TEXT_MUTED,
            font=FONT_TINY
        )

        self.activity_label.pack(
            side="right",
            padx=25
        )


    # ========================================================
    # BACKEND START
    # ========================================================

    def start_backend(self):

        self.connection_label.config(
            text="●  Connecting",
            fg=ORANGE
        )

        self.sidebar_connection.config(
            text="●  Connecting...",
            fg=ORANGE
        )

        self.status_label.config(
            text="Connecting to MCP..."
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

            self.mcp_client = (
                PersistentMCPClient(
                    MCP_URL
                )
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
            "end-1c"
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

        self.show_typing_indicator()

        self.agent_running = True

        self.current_request_id += 1

        request_id = (
            self.current_request_id
        )

        self.send_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="● PyPilot is thinking..."
        )

        thread = threading.Thread(
            target=self.run_agent,
            args=(
                user_input,
                request_id
            ),
            daemon=True
        )

        thread.start()

        return "break"


    # ========================================================
    # AGENT
    # ========================================================

    def run_agent(
        self,
        user_input,
        request_id
    ):

        try:

            # ------------------------------------------------
            # FILEX TOOLS
            # ------------------------------------------------

            filex_tools = (
                file_client.get_tool_desc()
            )

            # ------------------------------------------------
            # MCP TOOLS
            # ------------------------------------------------

            mcp_descriptions = (
                get_mcp_tool_description(
                    self.mcp_tools
                )
            )

            # ------------------------------------------------
            # TOOLS
            # ------------------------------------------------

            all_tools = {
                "filex_tools": filex_tools,
                "mcp_tools": mcp_descriptions
            }

            tools_text = json.dumps(
                all_tools,
                indent=2,
                default=str
            )

            # ------------------------------------------------
            # CONTEXT
            # ------------------------------------------------

            context = f"""
User request:
{user_input}

Available tools:
{tools_text}
"""

            # =================================================
            # AGENT LOOP
            # =================================================

            while True:

                prompt = f"""
{RESPONSE_PROTOCOL}

{context}

Return exactly one JSON object.
"""

                # ------------------------------------------------
                # GEMINI
                # ------------------------------------------------

                response = (
                    gemini_ai_client
                    .models
                    .generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=prompt
                    )
                )

                # ------------------------------------------------
                # RESPONSE
                # ------------------------------------------------

                raw_response = (
                    response.text.strip()
                )

                self.ui_queue.put(
                    (
                        "model_raw",
                        raw_response
                    )
                )

                # ------------------------------------------------
                # JSON
                # ------------------------------------------------

                try:

                    agent_response = json.loads(
                        raw_response
                    )

                except json.JSONDecodeError as e:

                    self.ui_queue.put(
                        (
                            "error",
                            (
                                "Invalid JSON from model:\n\n"
                                f"{e}\n\n"
                                "Raw response:\n"
                                f"{raw_response}"
                            )
                        )
                    )

                    break

                # ------------------------------------------------
                # TYPE
                # ------------------------------------------------

                response_type = (
                    agent_response.get(
                        "type"
                    )
                )

                # =================================================
                # MESSAGE
                # =================================================

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

                # =================================================
                # TOOL CALL
                # =================================================

                if response_type != "tool_call":

                    self.ui_queue.put(
                        (
                            "error",
                            (
                                "Invalid response type: "
                                f"{response_type}"
                            )
                        )
                    )

                    break

                # ------------------------------------------------
                # TOOL
                # ------------------------------------------------

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

                if not tool_name:

                    self.ui_queue.put(
                        (
                            "error",
                            "Tool name was missing."
                        )
                    )

                    break

                # ------------------------------------------------
                # TOOL REQUEST
                # ------------------------------------------------

                self.ui_queue.put(
                    (
                        "tool_requested",
                        (
                            tool_name,
                            arguments
                        )
                    )
                )

                # =================================================
                # MCP TOOL
                # =================================================

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
                            "ERROR executing MCP tool:\n"
                            f"{e}"
                        )

                # =================================================
                # FILEX TOOL
                # =================================================

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

                        # ------------------------------------------------
                        # CRITICAL TOOLS
                        # ------------------------------------------------

                        try:

                            critical_tools = (
                                file_client.get_critical_fn()
                            )

                        except Exception:

                            critical_tools = []

                        if tool_name in critical_tools:

                            approved = (
                                self.request_confirmation(
                                    tool_name,
                                    arguments
                                )
                            )

                            if not approved:

                                result_text = (
                                    "User denied execution "
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
                                        "ERROR executing tool:\n"
                                        f"{e}"
                                    )

                        # ------------------------------------------------
                        # NORMAL TOOLS
                        # ------------------------------------------------

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
                                    "ERROR executing tool:\n"
                                    f"{e}"
                                )

                # ------------------------------------------------
                # TOOL RESULT
                # ------------------------------------------------

                self.ui_queue.put(
                    (
                        "tool_result",
                        (
                            tool_name,
                            result_text
                        )
                    )
                )

                # ------------------------------------------------
                # UPDATE CONTEXT
                # ------------------------------------------------

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
                    (
                        "Agent error:\n"
                        f"{e}"
                    )
                )
            )

        finally:

            self.ui_queue.put(
                (
                    "agent_finished",
                    request_id
                )
            )


    # ========================================================
    # CRITICAL TOOL CONFIRMATION
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
    # UI QUEUE
    # ========================================================

    def process_ui_queue(self):

        try:

            while True:

                message_type, data = (
                    self.ui_queue.get_nowait()
                )

                # =================================================
                # BACKEND READY
                # =================================================

                if message_type == "backend_ready":

                    self.backend_ready = True

                    self.connection_label.config(
                        text="●  Connected",
                        fg=GREEN
                    )

                    self.sidebar_connection.config(
                        text="●  MCP Connected",
                        fg=GREEN
                    )

                    self.status_label.config(
                        text="Ready"
                    )

                    self.add_message(
                        "PyPilot",
                        (
                            "PyPilot is ready.\n\n"
                            "I can inspect your project, "
                            "work with FileX, execute tools, "
                            "run tests and interact with Playwright."
                        )
                    )

                # =================================================
                # BACKEND ERROR
                # =================================================

                elif message_type == "backend_error":

                    self.backend_ready = False

                    self.connection_label.config(
                        text="●  Disconnected",
                        fg=RED
                    )

                    self.sidebar_connection.config(
                        text="●  Connection failed",
                        fg=RED
                    )

                    self.status_label.config(
                        text="MCP connection failed"
                    )

                    self.add_message(
                        "Error",
                        data
                    )

                # =================================================
                # RAW MODEL RESPONSE
                # =================================================

                elif message_type == "model_raw":

                    print(
                        "\n=============================="
                    )

                    print(
                        "[MODEL RAW RESPONSE]"
                    )

                    print(
                        data
                    )

                    print(
                        "=============================="
                    )

                # =================================================
                # AGENT MESSAGE
                # =================================================

                elif message_type == "agent_message":

                    self.hide_typing_indicator()

                    self.status_label.config(
                        text="Ready"
                    )

                    self.add_message(
                        "PyPilot",
                        data
                    )

                # =================================================
                # TOOL REQUEST
                # =================================================

                elif message_type == "tool_requested":

                    self.hide_typing_indicator()

                    tool_name, arguments = data

                    self.tool_count += 1

                    self.activity_label.config(
                        text=(
                            f"Tools: "
                            f"{self.tool_count}"
                        )
                    )

                    self.status_label.config(
                        text=(
                            "Running: "
                            f"{tool_name}"
                        )
                    )

                    self.add_message(
                        "Tool",
                        (
                            f"{tool_name}\n\n"
                            "Arguments:\n"
                            f"{json.dumps(arguments, indent=2)}"
                        )
                    )

                # =================================================
                # TOOL RESULT
                # =================================================

                elif message_type == "tool_result":

                    tool_name, result = data

                    self.add_message(
                        "Tool",
                        (
                            f"✓ {tool_name}\n\n"
                            f"{result}"
                        )
                    )

                    self.status_label.config(
                        text=(
                            "PyPilot is processing..."
                        )
                    )

                    self.show_typing_indicator()

                # =================================================
                # CONFIRMATION
                # =================================================

                elif message_type == "confirmation":

                    (
                        tool_name,
                        arguments,
                        result,
                        event
                    ) = data

                    self.hide_typing_indicator()

                    approved = messagebox.askyesno(
                        "Tool Execution Confirmation",
                        (
                            "PyPilot wants to execute:\n\n"
                            f"Tool:\n{tool_name}\n\n"
                            "Arguments:\n"
                            f"{json.dumps(arguments, indent=2)}"
                            "\n\n"
                            "Allow execution?"
                        ),
                        parent=self.root
                    )

                    result["approved"] = approved

                    event.set()

                    self.show_typing_indicator()

                # =================================================
                # ERROR
                # =================================================

                elif message_type == "error":

                    self.hide_typing_indicator()

                    self.add_message(
                        "Error",
                        data
                    )

                # =================================================
                # FINISHED
                # =================================================

                elif message_type == "agent_finished":

                    self.hide_typing_indicator()

                    self.agent_running = False

                    self.send_button.config(
                        state="normal"
                    )

                    self.status_label.config(
                        text="Ready"
                    )

                    self.input_box.focus_set()

        except queue.Empty:

            pass

        # ----------------------------------------------------
        # CONTINUE QUEUE
        # ----------------------------------------------------

        if not self.application_closing:

            self.root.after(
                100,
                self.process_ui_queue
            )


    # ========================================================
    # NEW CHAT
    # ========================================================

    def new_chat(self):

        if self.agent_running:

            messagebox.showinfo(
                "Agent Busy",
                (
                    "PyPilot is currently working.\n\n"
                    "Please wait until the current task finishes."
                ),
                parent=self.root
            )

            return

        # ----------------------------------------------------
        # REMOVE CHAT WIDGETS
        # ----------------------------------------------------

        for widget in self.chat_frame.winfo_children():

            widget.destroy()

        self.message_count = 0

        self.tool_count = 0

        self.activity_label.config(
            text="Tools: 0"
        )

        self.input_box.delete(
            "1.0",
            "end"
        )

        self.status_label.config(
            text="Ready"
        )

        self.chat_auto_scroll = True

        self.add_message(
            "PyPilot",
            (
                "New conversation started.\n\n"
                "What would you like me to automate?"
            )
        )

        self.scroll_chat_to_bottom()

        self.input_box.focus_set()


    # ========================================================
    # AGENT VIEW
    # ========================================================

    def show_agent(self):

        self.header_title.config(
            text="AI Automation Workspace"
        )

        self.header_subtitle.config(
            text="Inspect • Test • Automate • Debug"
        )

        self.input_box.focus_set()


    # ========================================================
    # TOOLS VIEW
    # ========================================================

    def show_tools(self):

        tools = []

        # ----------------------------------------------------
        # MCP
        # ----------------------------------------------------

        for tool in self.mcp_tools:

            try:

                tools.append(
                    f"• {tool.name}"
                )

            except Exception:

                pass

        # ----------------------------------------------------
        # FILEX
        # ----------------------------------------------------

        filex_text = ""

        try:

            descriptions = (
                file_client.get_tool_desc()
            )

            if isinstance(
                descriptions,
                dict
            ):

                for name in descriptions.keys():

                    filex_text += (
                        f"• {name}\n"
                    )

            elif isinstance(
                descriptions,
                list
            ):

                for item in descriptions:

                    if isinstance(
                        item,
                        dict
                    ):

                        name = item.get(
                            "name"
                        )

                        if name:

                            filex_text += (
                                f"• {name}\n"
                            )

        except Exception:

            filex_text = (
                "Unable to load FileX tools."
            )

        if not filex_text:

            filex_text = (
                "FileX tools available."
            )

        text = (
            "MCP TOOLS\n"
            "────────────────────\n"
            + (
                "\n".join(tools)
                if tools
                else "No MCP tools loaded."
            )
            + "\n\n"
            "FILEX TOOLS\n"
            "────────────────────\n"
            + filex_text
        )

        self.show_information_window(
            "Available Tools",
            text
        )


    # ========================================================
    # ACTIVITY
    # ========================================================

    def show_activity(self):

        text = (
            "PYPILOT ACTIVITY\n"
            "────────────────────\n\n"
            f"Messages       : {self.message_count}\n"
            f"Tools executed : {self.tool_count}\n"
            f"Agent running  : {self.agent_running}\n"
            f"MCP connected  : {self.backend_ready}\n"
        )

        self.show_information_window(
            "Agent Activity",
            text
        )


    # ========================================================
    # INFORMATION WINDOW
    # ========================================================

    def show_information_window(
        self,
        title,
        content
    ):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            title
        )

        window.geometry(
            "650x500"
        )

        window.configure(
            bg=BG
        )

        window.transient(
            self.root
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        tk.Label(
            window,
            text=title,
            bg=BG,
            fg=TEXT,
            font=FONT_TITLE
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # ----------------------------------------------------
        # TEXT
        # ----------------------------------------------------

        text_box = tk.Text(
            window,
            bg=PANEL,
            fg=TEXT,
            insertbackground=WHITE,
            font=FONT_CODE,
            relief="flat",
            wrap="word",
            padx=15,
            pady=15
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        text_box.insert(
            "1.0",
            content
        )

        text_box.config(
            state="disabled"
        )

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        ttk.Button(
            window,
            text="Close",
            command=window.destroy,
            style="PyPilot.TButton"
        ).pack(
            pady=(0, 20)
        )


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        if self.application_closing:

            return

        # ----------------------------------------------------
        # RUNNING
        # ----------------------------------------------------

        if self.agent_running:

            answer = messagebox.askyesno(
                "Exit PyPilot",
                (
                    "An agent task is still running.\n\n"
                    "Do you want to close PyPilot?"
                ),
                parent=self.root
            )

            if not answer:

                return

        # ----------------------------------------------------
        # STOP ANIMATION
        # ----------------------------------------------------

        self.application_closing = True

        if self.typing_animation_id:

            try:

                self.root.after_cancel(
                    self.typing_animation_id
                )

            except Exception:

                pass

        # ----------------------------------------------------
        # MCP CLOSE
        # ----------------------------------------------------

        try:

            if self.mcp_client:

                self.mcp_client.close()

        except Exception as e:

            print(
                "Error closing MCP client:",
                e
            )

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        self.root.destroy()


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    PyPilotUI(
        root
    )

    root.mainloop()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
 