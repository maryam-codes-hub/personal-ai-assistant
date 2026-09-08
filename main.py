from datetime import date
import time
import os
import shutil
import threading
import webbrowser


def detect_intent(command):
    intent = None

    if "time" in command:
        intent = "TIME"

    elif "date" in command:
        intent = "DATE"

    elif ("launch" in command or "open " in command) and "calculator" in command:
        intent = "CALCULATOR"

    elif ("launch" in command or "open " in command) and "notepad" in command:
        intent = "NOTEPAD"

    elif ("show" in command or "give" in command or "list" in command) and "file" in command:
        intent = "LIST FILES"

    elif ("launch" in command or "open " in command) and "google" in command:
        intent = "OPEN GOOGLE"

    elif ("launch" in command or "open " in command) and "youtube" in command:
        intent = "OPEN YOUTUBE"

    elif ("delete" in command or "remove" in command) and "file" in command:
        intent = "DELETE FILE"

    elif ("delete" in command or "remove" in command) and "folder" in command:
        intent = "DELETE FOLDER"

    elif ("create" in command or "make" in command) and "folder" in command:
        intent = "CREATE FOLDER"

    elif ("create" in command or "make" in command) and "file" in command:
        intent = "CREATE FILE"

    elif ("copy" in command or "duplicate" in command) and "file" in command:
        intent = "COPY FILE"

    elif ("move" in command or "shift" in command) and "file" in command:
        intent = "MOVE FILE"

    elif ("add" in command or "write" in command or "save" in command) and "note" in command:
        intent = "ADD NOTE"

    elif ("show" in command or "view" in command or "display" in command) and "note" in command:
        intent = "SHOW NOTES"

    elif "reminder" in command or "remind" in command:
        intent = "REMINDER"

    elif command.startswith("search "):
        intent = "SEARCH"

    elif "exit" in command or "quit" in command or "bye" in command:
        intent = "EXIT"

    return intent


def reminder(m, s):
    print("Reminder set!")

    time.sleep(s)

    print(f"HEY {name}!! It's time to {m}")


name = input("Enter User name: ")

print(f"Hello {name}! I am your personal AI Assistant")


while True:

    command = input("Enter Command: ").lower()

    intent = detect_intent(command)

    if intent == "TIME":

        current = time.ctime()
        print(f"Current time is: {current}")


    elif intent == "DATE":

        today = date.today()
        print(f"Today's date: {today}")


    elif intent == "CALCULATOR":

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


    elif intent == "EXIT":

        print("Goodbye")
        break


    elif intent == "NOTEPAD":

        os.system("notepad")


    elif intent == "LIST FILES":

        print(os.listdir())


    elif intent == "CREATE FILE":

        file = input("Enter file name: ")

        with open(file, "w") as f:
            pass

        print("File created:", os.path.exists(file))


    elif intent == "CREATE FOLDER":

        folder = input("Enter folder name: ")

        os.makedirs(folder)

        print("Folder Created")


    elif intent == "COPY FILE":

        source_file = input("Enter source file: ")

        if not os.path.exists(source_file):

            print("Source file doesn't exist")

        else:

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


    elif intent == "MOVE FILE":

        source_file = input("Enter source file: ")

        if not os.path.exists(source_file):

            print("Source file doesn't exist, create file first")

        else:

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


    elif intent == "ADD NOTE":

        note = input("Enter your note: ")

        with open("data2.txt", "a") as f:
            f.write(note + "\n")

        print("Note saved!")


    elif intent == "SHOW NOTES":

        if not os.path.exists("data2.txt"):

            print("No notes yet")

        else:

            with open("data2.txt", "r") as f:
                notes = f.readlines()

            if len(notes) == 0:

                print("No notes yet")

            else:

                print("--- Your Notes ---")

                for index, i in enumerate(notes, start=1):
                    print(f"{index}: {i.strip()}")


    elif intent == "REMINDER":

        message = input("What should I remind you about? ")

        seconds = int(input("After how many seconds? "))

        thread = threading.Thread(
            target=reminder,
            args=(message, seconds)
        )

        thread.start()


    elif intent == "OPEN GOOGLE":

        print("Opening Google.....")

        webbrowser.open("https://www.google.com/")


    elif intent == "OPEN YOUTUBE":

        print("Opening YouTube.....")

        webbrowser.open("https://www.youtube.com/")


    elif intent == "SEARCH":

        query = command[7:]

        print(f"Searching for: {query}")

        search_url = (
            "https://www.google.com/search?q="
            + query.replace(" ", "+")
        )

        webbrowser.open(search_url)


    elif intent == "DELETE FILE":

        file_name = input("Which file do you want to delete: ")

        if os.path.exists(file_name):

            os.remove(file_name)

            print("File deleted")

        else:

            print("File not found")


    elif intent == "DELETE FOLDER":

        folder_name = input("Which folder do you want to delete: ")

        if os.path.exists(folder_name):

            os.rmdir(folder_name)

            print("Folder deleted")

        else:

            print("Folder not found")


    else:

        print("I don't understand this command")