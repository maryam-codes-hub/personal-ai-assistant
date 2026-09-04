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
elif command=="calculator":
    print("WELCOME")
    
    a=int(input("Enter First Number:"))
    b=int(input("Enter Second Number:"))
 
    print("1:Addition\n2:Substraction\n3:Multiplication\n4:Division\n5:Modulus")
    choice=int(input("Enter choice:"))
    if choice==1:
    
     addition=a+b
     print("Addition Result:",addition)
    elif choice==2:
       substraction=a-b
       print("substraction Result:",substraction)
    elif choice==3:
       multiply=a*b
       print("Multiplication Result:",multiply)
    elif choice==4:
      if b==0:
              raise ValueError("Cannot divided by zero")
      division=a/b
      print("Division Result:",division)
    elif choice==5:
       modulus=a%b
       print("Modulus  Result:",modulus)
    else:
       print("Invalid Choice")



elif command=="exit":
    print("Goodbye")
else:
    print("I dont understand this command")