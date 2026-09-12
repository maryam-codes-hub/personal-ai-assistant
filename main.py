from datetime import date
import time
import os
import shutil
import threading
import webbrowser
import speech_recognition as sr


def detect_intent(command):
    intent = None
    is_open=(
        "launch" in command or "open" in command or "go to" in command
        or "start"  in command
    )
    is_create=(
        "create" in command or "make" in command or "new" in command
    )
    is_delete=(
        "delete" in command or "remove" in command
    )
    is_show=(
       "show" in command or "view" in command or "display" in command or "list" in command
    )
    is_exit=(
        "exit" in command or "quit" in command or "bye" in command
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

    elif ("add" in command or "write" in command or "save" in command) and "note" in command:
        intent = "ADD NOTE"

    elif is_show and "note" in command:
        intent = "SHOW NOTES"

    elif "reminder" in command or "remind" in command:
        intent = "REMINDER"

    elif is_exit:
        intent = "EXIT"

    return intent


def reminder(m,s):
    print("Reminder set!")

    time.sleep(s)

    print(f"HEY !! It's time to {m}")


def notepad():

      os.system("notepad")


def calculator():
        print("WELCOME")

        a = int(input("Enter First Number: "))
        b = int(input("Enter Second Number: "))

        print(
            "1: Addition\n"
            "2: Subtraction\n"
            "3: Multiplication\n"
            "4: Division\n"
            "5: Modulus"
        )

        choice = int(input("Enter choice: "))

        if choice == 1:

            addition = a + b
            print("Addition Result:", addition)

        elif choice == 2:

            subtraction = a - b
            print("Subtraction Result:", subtraction)

        elif choice == 3:

            multiply = a * b
            print("Multiplication Result:", multiply)

        elif choice == 4:

            if b == 0:
                print("Cannot divide by zero")
            else:
                division = a / b
                print("Division Result:", division)

        elif choice == 5:

            modulus = a % b
            print("Modulus Result:", modulus)

        else:
            print("Invalid Choice")

def get_time():
    current = time.ctime()
    print(f"Current time is: {current}")


def get_date():
    today = date.today()
    print(f"Today's date: {today}")


def list_files():
    print(os.listdir())


def create_file():
    file = input("Enter file name: ")

    with open(file, "w") as f:
        pass

    print("File created:", os.path.exists(file))


def create_folder():
    folder = input("Enter folder name: ")
    os.makedirs(folder)
    print("Folder Created")


def copy_file():
    source_file = input("Enter source file: ")

    if not os.path.exists(source_file):
        print("Source file doesn't exist")
        return

    destination_file = input("Enter destination file: ")

    if not os.path.exists(destination_file):
        print("Destination doesn't exist")

        try:
            shutil.copy(source_file, destination_file)
            print("File Copied")

        except Exception as e:
            print(e)

    else:
        print("WARNING: Destination file already exists")

        user_input = input(
            "Do you want to overwrite? (Y/N): "
        ).upper()

        if user_input == "Y":
            try:
                shutil.copy(source_file, destination_file)
                print("File Copied")

            except Exception as e:
                print(e)

        else:
            print("NOT COPIED")


def move_file():
    source_file = input("Enter source file: ")

    if not os.path.exists(source_file):
        print("Source file doesn't exist, create file first")
        return

    destination_folder = input("Enter destination folder: ")

    if not os.path.exists(destination_folder):
        print("Destination folder doesn't exist")

        user_input = input(
            "Do you want to create folder? (Y/N): "
        ).upper()

        if user_input == "Y":
            os.mkdir(destination_folder)
            print("Folder Created")

            shutil.move(source_file, destination_folder)
            print("File Moved")

        else:
            print("Thanks")

    else:
        shutil.move(source_file, destination_folder)
        print("File Moved")


def add_note():
    note = input("Enter your note: ")

    with open("data2.txt", "a") as f:
        f.write(note + "\n")

    print("Note saved!")


def show_notes():
    if not os.path.exists("data2.txt"):
        print("No notes yet")
        return

    with open("data2.txt", "r") as f:
        notes = f.readlines()

    if len(notes) == 0:
        print("No notes yet")
        return

    print("--- Your Notes ---")

    for index, i in enumerate(notes, start=1):
        print(f"{index}: {i.strip()}")


def set_reminder():
    message = input("What should I remind you about? ")
    seconds = int(input("After how many seconds? "))

    thread = threading.Thread(
        target=reminder,
        args=(message, seconds)
    )

    thread.start()


def open_google():
    print("Opening Google.....")
    webbrowser.open("https://www.google.com/")


def open_youtube():
    print("Opening YouTube.....")
    webbrowser.open("https://www.youtube.com/")

def listen_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.record(source,duration=5)
        

    try:
        command = recognizer.recognize_google(audio,language="en-US")
        print("You said:", command)
        return command

    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        return None

    except sr.RequestError as e:
        print("Speech service error:", e)
        return None
def search_web(command):
    query = command[7:]

    print(f"Searching for: {query}")

    search_url = (
        "https://www.google.com/search?q="
        + query.replace(" ", "+")
    )

    webbrowser.open(search_url)


def delete_file():
    file_name = input("Which file do you want to delete: ")

    if os.path.exists(file_name):
        os.remove(file_name)
        print("File deleted")
    else:
        print("File not found")


def delete_folder():
    folder_name = input("Which folder do you want to delete: ")

    if os.path.exists(folder_name):
        os.rmdir(folder_name)
        print("Folder deleted")
    else:
        print("Folder not found")
def main():
   name = input("Enter User name: ")

   print(f"Hello {name}! I am your personal AI Assistant")


   while True:
      command=input("Enter Command:").lower().strip()
      if command=="voice":

       command = listen_command()
      if command is None:
          continue
      
      command=command.lower().strip()

      intent =detect_intent(command)
    #   print("detected intent:",intent)


      if intent == "TIME":
            get_time()

      elif intent == "DATE":
            get_date()

      elif intent == "CALCULATOR":
            calculator()

      elif intent == "EXIT":
            print("Goodbye")
            break

      elif intent == "NOTEPAD":
            notepad()

      elif intent == "LIST FILES":
            list_files()

      elif intent == "CREATE FILE":
            create_file()

      elif intent == "CREATE FOLDER":
            create_folder()

      elif intent == "COPY FILE":
            copy_file()

      elif intent == "MOVE FILE":
            move_file()

      elif intent == "ADD NOTE":
            add_note()

      elif intent == "SHOW NOTES":
            show_notes()

      elif intent == "REMINDER":
            set_reminder()

      elif intent == "OPEN GOOGLE":
            open_google()

      elif intent == "OPEN YOUTUBE":
            open_youtube()

      elif intent == "SEARCH":
          search_web(command)

      elif intent == "DELETE FILE":
            delete_file()

      elif intent == "DELETE FOLDER":
            delete_folder()

      else:
            print("I don't understand this command")


if __name__ == "__main__":
    main()