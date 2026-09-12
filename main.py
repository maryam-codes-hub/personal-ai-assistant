from datetime import date
import time
import os
import shutil
import threading
import webbrowser
import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog


# =========================================================
# INTENT DETECTION
# =========================================================

def detect_intent(command):
    intent = None

    is_open = (
        "launch" in command
        or "open" in command
        or "go to" in command
        or "start" in command
    )

    is_create = (
        "create" in command
        or "make" in command
        or "new" in command
    )

    is_delete = (
        "delete" in command
        or "remove" in command
    )

    is_show = (
        "show" in command
        or "view" in command
        or "display" in command
        or "list" in command
    )

    is_exit = (
        "exit" in command
        or "quit" in command
        or "bye" in command
    )

    if "time" in command:
        intent = "TIME"

    elif "date" in command:
        intent = "DATE"

    elif is_open and "calculator" in command:
        intent = "CALCULATOR"

    elif is_open and "notepad" in command:
        intent = "NOTEPAD"

    elif is_show and "file" in command:
        intent = "LIST FILES"

    elif command.startswith("search "):
        intent = "SEARCH"

    elif is_open and "google" in command:
        intent = "OPEN GOOGLE"

    elif is_open and "youtube" in command:
        intent = "OPEN YOUTUBE"

    elif is_delete and "file" in command:
        intent = "DELETE FILE"

    elif is_delete and "folder" in command:
        intent = "DELETE FOLDER"

    elif is_create and "folder" in command:
        intent = "CREATE FOLDER"

    elif is_create and "file" in command:
        intent = "CREATE FILE"

    elif ("copy" in command or "duplicate" in command) and "file" in command:
        intent = "COPY FILE"

    elif ("move" in command or "shift" in command) and "file" in command:
        intent = "MOVE FILE"

    elif (
        ("add" in command or "write" in command or "save" in command)
        and "note" in command
    ):
        intent = "ADD NOTE"

    elif is_show and "note" in command:
        intent = "SHOW NOTES"

    elif "reminder" in command or "remind" in command:
        intent = "REMINDER"

    elif is_exit:
        intent = "EXIT"

    return intent


# =========================================================
# VOICE
# =========================================================

def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.record(source, duration=5)

    try:
        command = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        return command

    except sr.UnknownValueError:
        return None

    except sr.RequestError:
        return None


# =========================================================
# GUI APPLICATION
# =========================================================

class PersonalAIAssistant:

    def __init__(self, root):

        self.root = root

        self.root.title("Personal AI Desktop Assistant")
        self.root.geometry("1050x700")
        self.root.minsize(900, 600)

        # ---------------- COLORS ----------------

        self.bg_color = "#0F172A"
        self.sidebar_color = "#111827"
        self.card_color = "#1E293B"
        self.input_color = "#334155"

        self.text_color = "#F8FAFC"
        self.secondary_text = "#94A3B8"

        self.accent_color = "#38BDF8"
        self.success_color = "#22C55E"
        self.danger_color = "#EF4444"

        self.root.configure(bg=self.bg_color)

        # ---------------- STYLE ----------------

        self.style = ttk.Style()

        self.style.theme_use("clam")

        self.style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=10,
            borderwidth=0
        )

        self.style.configure(
            "Quick.TButton",
            background=self.card_color,
            foreground=self.text_color,
            padding=10,
            font=("Segoe UI", 9, "bold")
        )

        self.style.map(
            "Quick.TButton",
            background=[
                ("active", self.accent_color)
            ]
        )

        # ---------------- MAIN LAYOUT ----------------

        self.create_header()
        self.create_body()
        self.create_input_area()

        self.show_message(
            "Assistant",
            "Hello! I am your Personal AI Assistant.\n"
            "Type a command or use the Voice button to speak."
        )

    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.sidebar_color,
            height=80
        )

        header.pack(
            fill="x",
            side="top"
        )

        header.pack_propagate(False)

        # Logo / title

        title_frame = tk.Frame(
            header,
            bg=self.sidebar_color
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        title = tk.Label(
            title_frame,
            text="✦ Personal AI Assistant",
            font=("Segoe UI", 20, "bold"),
            bg=self.sidebar_color,
            fg=self.text_color
        )

        title.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            title_frame,
            text="Your smart desktop companion",
            font=("Segoe UI", 9),
            bg=self.sidebar_color,
            fg=self.secondary_text
        )

        subtitle.pack(
            anchor="w"
        )

        # Status

        self.status_label = tk.Label(
            header,
            text="●  Ready",
            font=("Segoe UI", 10, "bold"),
            bg=self.sidebar_color,
            fg=self.success_color
        )

        self.status_label.pack(
            side="right",
            padx=30
        )

    # =====================================================
    # BODY
    # =====================================================

    def create_body(self):

        body = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(15, 10)
        )

        # ---------------- LEFT SIDEBAR ----------------

        sidebar = tk.Frame(
            body,
            bg=self.sidebar_color,
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        sidebar.pack_propagate(False)

        quick_title = tk.Label(
            sidebar,
            text="Quick Actions",
            font=("Segoe UI", 13, "bold"),
            bg=self.sidebar_color,
            fg=self.text_color
        )

        quick_title.pack(
            anchor="w",
            padx=18,
            pady=(20, 15)
        )

        quick_buttons = [
            ("🕐  Time", "time"),
            ("📅  Date", "date"),
            ("📁  List Files", "list files"),
            ("📝  Show Notes", "show notes"),
            ("🌐  Google", "open google"),
            ("▶️  YouTube", "open youtube"),
            ("🔍  Search", "search "),
            ("📓  Notepad", "open notepad"),
        ]

        for text, command in quick_buttons:

            button = ttk.Button(
                sidebar,
                text=text,
                style="Quick.TButton",
                command=lambda c=command: self.quick_command(c)
            )

            button.pack(
                fill="x",
                padx=15,
                pady=5
            )

        # ---------------- CHAT AREA ----------------

        chat_frame = tk.Frame(
            body,
            bg=self.card_color
        )

        chat_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        chat_header = tk.Label(
            chat_frame,
            text="  Assistant Console",
            font=("Segoe UI", 12, "bold"),
            bg=self.card_color,
            fg=self.text_color,
            anchor="w"
        )

        chat_header.pack(
            fill="x",
            padx=15,
            pady=(15, 5)
        )

        # Text output

        text_container = tk.Frame(
            chat_frame,
            bg=self.card_color
        )

        text_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        scrollbar = tk.Scrollbar(
            text_container
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.output_box = tk.Text(
            text_container,
            bg="#0B1220",
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set
        )

        self.output_box.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.output_box.yview
        )

        self.output_box.config(
            state="disabled"
        )

        # Text tags

        self.output_box.tag_config(
            "user",
            foreground=self.accent_color
        )

        self.output_box.tag_config(
            "assistant",
            foreground=self.success_color
        )

        self.output_box.tag_config(
            "normal",
            foreground=self.text_color
        )

    # =====================================================
    # INPUT AREA
    # =====================================================

    def create_input_area(self):

        input_frame = tk.Frame(
            self.root,
            bg=self.bg_color
        )

        input_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.command_entry = tk.Entry(
            input_frame,
            bg=self.input_color,
            fg=self.text_color,
            insertbackground=self.text_color,
            font=("Segoe UI", 11),
            relief="flat"
        )

        self.command_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 10)
        )

        self.command_entry.bind(
            "<Return>",
            lambda event: self.execute_command()
        )

        # Send button

        send_button = tk.Button(
            input_frame,
            text="➤  Send",
            bg=self.accent_color,
            fg="#0F172A",
            activebackground="#7DD3FC",
            activeforeground="#0F172A",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.execute_command
        )

        send_button.pack(
            side="left",
            padx=(0, 8)
        )

        # Voice button

        self.voice_button = tk.Button(
            input_frame,
            text="🎤  Voice",
            bg="#7C3AED",
            fg="white",
            activebackground="#8B5CF6",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.start_voice
        )

        self.voice_button.pack(
            side="left",
            padx=(0, 8)
        )

        # Exit

        exit_button = tk.Button(
            input_frame,
            text="✕",
            bg=self.danger_color,
            fg="white",
            activebackground="#F87171",
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.exit_app
        )

        exit_button.pack(
            side="left"
        )

    # =====================================================
    # OUTPUT
    # =====================================================

    def show_message(self, sender, message):

        self.output_box.config(
            state="normal"
        )

        if sender == "You":
            self.output_box.insert(
                "end",
                f"\nYou: {message}\n",
                "user"
            )

        else:
            self.output_box.insert(
                "end",
                f"\nAssistant: {message}\n",
                "assistant"
            )

        self.output_box.see("end")

        self.output_box.config(
            state="disabled"
        )

    # =====================================================
    # QUICK COMMANDS
    # =====================================================

    def quick_command(self, command):

        if command == "search ":

            query = simpledialog.askstring(
                "Search",
                "What do you want to search?"
            )

            if not query:
                return

            command = "search " + query

        self.process_command(command)

    # =====================================================
    # NORMAL COMMAND
    # =====================================================

    def execute_command(self):

        command = self.command_entry.get().strip()

        if not command:
            return

        self.command_entry.delete(
            0,
            "end"
        )

        self.process_command(command)

    # =====================================================
    # PROCESS COMMAND
    # =====================================================

    def process_command(self, command):

        command = command.lower().strip()

        self.show_message(
            "You",
            command
        )

        intent = detect_intent(command)

        if intent == "TIME":

            current = time.ctime()

            self.show_message(
                "Assistant",
                f"Current time is: {current}"
            )

        elif intent == "DATE":

            today = date.today()

            self.show_message(
                "Assistant",
                f"Today's date: {today}"
            )

        elif intent == "CALCULATOR":

            self.run_calculator()

        elif intent == "NOTEPAD":

            os.system("notepad")

            self.show_message(
                "Assistant",
                "Opening Notepad..."
            )

        elif intent == "LIST FILES":

            self.list_files_gui()

        elif intent == "CREATE FILE":

            self.create_file_gui()

        elif intent == "CREATE FOLDER":

            self.create_folder_gui()

        elif intent == "COPY FILE":

            self.copy_file_gui()

        elif intent == "MOVE FILE":

            self.move_file_gui()

        elif intent == "ADD NOTE":

            self.add_note_gui()

        elif intent == "SHOW NOTES":

            self.show_notes_gui()

        elif intent == "REMINDER":

            self.set_reminder_gui()

        elif intent == "OPEN GOOGLE":

            webbrowser.open(
                "https://www.google.com/"
            )

            self.show_message(
                "Assistant",
                "Opening Google..."
            )

        elif intent == "OPEN YOUTUBE":

            webbrowser.open(
                "https://www.youtube.com/"
            )

            self.show_message(
                "Assistant",
                "Opening YouTube..."
            )

        elif intent == "SEARCH":

            self.search_web_gui(command)

        elif intent == "DELETE FILE":

            self.delete_file_gui()

        elif intent == "DELETE FOLDER":

            self.delete_folder_gui()

        elif intent == "EXIT":

            self.exit_app()

        else:

            self.show_message(
                "Assistant",
                "I don't understand this command."
            )

    # =====================================================
    # CALCULATOR
    # =====================================================

    def run_calculator(self):

        a = simpledialog.askinteger(
            "Calculator",
            "Enter first number:"
        )

        if a is None:
            return

        b = simpledialog.askinteger(
            "Calculator",
            "Enter second number:"
        )

        if b is None:
            return

        choice = simpledialog.askinteger(
            "Calculator",
            "Choose operation:\n\n"
            "1 - Addition\n"
            "2 - Subtraction\n"
            "3 - Multiplication\n"
            "4 - Division\n"
            "5 - Modulus"
        )

        if choice == 1:

            result = a + b

        elif choice == 2:

            result = a - b

        elif choice == 3:

            result = a * b

        elif choice == 4:

            if b == 0:
                self.show_message(
                    "Assistant",
                    "Cannot divide by zero."
                )
                return

            result = a / b

        elif choice == 5:

            if b == 0:
                self.show_message(
                    "Assistant",
                    "Cannot calculate modulus by zero."
                )
                return

            result = a % b

        else:

            self.show_message(
                "Assistant",
                "Invalid choice."
            )
            return

        self.show_message(
            "Assistant",
            f"Calculator Result: {result}"
        )

    # =====================================================
    # FILE FUNCTIONS
    # =====================================================

    def list_files_gui(self):

        files = os.listdir()

        if not files:

            message = "No files found."

        else:

            message = "\n".join(
                f"• {file}"
                for file in files
            )

        self.show_message(
            "Assistant",
            message
        )

    def create_file_gui(self):

        file_name = simpledialog.askstring(
            "Create File",
            "Enter file name:"
        )

        if not file_name:
            return

        try:

            with open(file_name, "w"):
                pass

            self.show_message(
                "Assistant",
                f"File created: {file_name}"
            )

        except Exception as e:

            self.show_message(
                "Assistant",
                f"Error: {e}"
            )

    def create_folder_gui(self):

        folder = simpledialog.askstring(
            "Create Folder",
            "Enter folder name:"
        )

        if not folder:
            return

        try:

            os.makedirs(folder)

            self.show_message(
                "Assistant",
                f"Folder created: {folder}"
            )

        except FileExistsError:

            self.show_message(
                "Assistant",
                "Folder already exists."
            )

        except Exception as e:

            self.show_message(
                "Assistant",
                f"Error: {e}"
            )

    def copy_file_gui(self):

        source = simpledialog.askstring(
            "Copy File",
            "Enter source file:"
        )

        if not source:
            return

        if not os.path.exists(source):

            self.show_message(
                "Assistant",
                "Source file doesn't exist."
            )
            return

        destination = simpledialog.askstring(
            "Copy File",
            "Enter destination file:"
        )

        if not destination:
            return

        if os.path.exists(destination):

            overwrite = messagebox.askyesno(
                "File Exists",
                "Destination already exists.\n"
                "Do you want to overwrite it?"
            )

            if not overwrite:
                return

        try:

            shutil.copy(
                source,
                destination
            )

            self.show_message(
                "Assistant",
                "File copied successfully."
            )

        except Exception as e:

            self.show_message(
                "Assistant",
                f"Error: {e}"
            )

    def move_file_gui(self):

        source = simpledialog.askstring(
            "Move File",
            "Enter source file:"
        )

        if not source:
            return

        if not os.path.exists(source):

            self.show_message(
                "Assistant",
                "Source file doesn't exist."
            )
            return

        destination = simpledialog.askstring(
            "Move File",
            "Enter destination folder:"
        )

        if not destination:
            return

        if not os.path.exists(destination):

            create = messagebox.askyesno(
                "Folder Doesn't Exist",
                "Destination folder doesn't exist.\n"
                "Create it?"
            )

            if not create:
                return

            os.mkdir(destination)

        try:

            shutil.move(
                source,
                destination
            )

            self.show_message(
                "Assistant",
                "File moved successfully."
            )

        except Exception as e:

            self.show_message(
                "Assistant",
                f"Error: {e}"
            )

    # =====================================================
    # NOTES
    # =====================================================

    def add_note_gui(self):

        note = simpledialog.askstring(
            "Add Note",
            "Enter your note:"
        )

        if not note:
            return

        with open(
            "data2.txt",
            "a"
        ) as f:

            f.write(
                note + "\n"
            )

        self.show_message(
            "Assistant",
            "Note saved successfully."
        )

    def show_notes_gui(self):

        if not os.path.exists(
            "data2.txt"
        ):

            self.show_message(
                "Assistant",
                "No notes yet."
            )

            return

        with open(
            "data2.txt",
            "r"
        ) as f:

            notes = f.readlines()

        if not notes:

            self.show_message(
                "Assistant",
                "No notes yet."
            )

            return

        message = "--- Your Notes ---\n\n"

        for index, note in enumerate(
            notes,
            start=1
        ):

            message += (
                f"{index}. "
                f"{note.strip()}\n"
            )

        self.show_message(
            "Assistant",
            message
        )

    # =====================================================
    # REMINDER
    # =====================================================

    def set_reminder_gui(self):

        message = simpledialog.askstring(
            "Reminder",
            "What should I remind you about?"
        )

        if not message:
            return

        seconds = simpledialog.askinteger(
            "Reminder",
            "After how many seconds?"
        )

        if seconds is None:
            return

        self.show_message(
            "Assistant",
            f"Reminder set for {seconds} seconds."
        )

        thread = threading.Thread(
            target=self.reminder,
            args=(message, seconds),
            daemon=True
        )

        thread.start()

    def reminder(self, message, seconds):

        time.sleep(seconds)

        self.root.after(
            0,
            lambda: self.reminder_popup(message)
        )

    def reminder_popup(self, message):

        self.show_message(
            "Assistant",
            f"⏰ Reminder: {message}"
        )

        messagebox.showinfo(
            "Reminder",
            f"⏰ It's time to {message}"
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_web_gui(self, command):

        query = command[7:].strip()

        if not query:

            self.show_message(
                "Assistant",
                "Please enter something to search."
            )

            return

        search_url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        webbrowser.open(
            search_url
        )

        self.show_message(
            "Assistant",
            f"Searching Google for: {query}"
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_file_gui(self):

        file_name = simpledialog.askstring(
            "Delete File",
            "Which file do you want to delete?"
        )

        if not file_name:
            return

        if not os.path.exists(file_name):

            self.show_message(
                "Assistant",
                "File not found."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete:\n{file_name}?"
        )

        if confirm:

            try:

                os.remove(file_name)

                self.show_message(
                    "Assistant",
                    "File deleted successfully."
                )

            except Exception as e:

                self.show_message(
                    "Assistant",
                    f"Error: {e}"
                )

    def delete_folder_gui(self):

        folder_name = simpledialog.askstring(
            "Delete Folder",
            "Which folder do you want to delete?"
        )

        if not folder_name:
            return

        if not os.path.exists(folder_name):

            self.show_message(
                "Assistant",
                "Folder not found."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete folder:\n{folder_name}?"
        )

        if not confirm:
            return

        try:

            os.rmdir(folder_name)

            self.show_message(
                "Assistant",
                "Folder deleted successfully."
            )

        except OSError:

            self.show_message(
                "Assistant",
                "Folder is not empty or cannot be deleted."
            )

        except Exception as e:

            self.show_message(
                "Assistant",
                f"Error: {e}"
            )

    # =====================================================
    # VOICE
    # =====================================================

    def start_voice(self):

        self.voice_button.config(
            state="disabled",
            text="🎤 Listening..."
        )

        self.status_label.config(
            text="● Listening...",
            fg="#F59E0B"
        )

        self.show_message(
            "Assistant",
            "Listening for your command..."
        )

        thread = threading.Thread(
            target=self.voice_thread,
            daemon=True
        )

        thread.start()

    def voice_thread(self):

        command = listen_command()

        self.root.after(
            0,
            lambda: self.voice_finished(command)
        )

    def voice_finished(self, command):

        self.voice_button.config(
            state="normal",
            text="🎤  Voice"
        )

        self.status_label.config(
            text="● Ready",
            fg=self.success_color
        )

        if command is None:

            self.show_message(
                "Assistant",
                "Sorry, I could not understand your voice command."
            )

            return

        self.show_message(
            "You",
            command
        )

        self.process_command(
            command
        )

    # =====================================================
    # EXIT
    # =====================================================

    def exit_app(self):

        result = messagebox.askyesno(
            "Exit Assistant",
            "Are you sure you want to exit?"
        )

        if result:

            self.root.destroy()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    root =tk.Tk()

    app =PersonalAIAssistant(root)

    root.mainloop()