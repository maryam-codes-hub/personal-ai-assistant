from datetime import date
import time
name=input("Enter User name:")

print(f"Hello {name}! i am your personal AI Assitant")
command=input("Enter Command:")
if command=="time":
    current=time.ctime()
    print(f"Current time is :{current}")
elif command=="date":
    today=date.today()
    print(f"Today's date:{today}")


elif command=="exit":
    print("Goodbye")
else:
    print("I dont understand this command")