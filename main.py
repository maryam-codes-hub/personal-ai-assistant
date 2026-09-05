from datetime import date
import time
import os
import shutil
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

elif command=="notepad":
    os.system("notepad")


elif command=="list files":
    print(os.listdir())
elif command=="create file":
    file=input("Enter file name:")
    with open(file,"w")as f:
        pass
    print("File created",os.path.exists(file))

elif command=="create folder":
    folder=input("Enter folder name:")
    os.makedirs(folder)
    print("Folder Created")

elif command=="copy file":
    source_file=input("Enter source file:")
    if not os.path.exists(source_file):
        print("source file doesn't exists")
    else:
        destination_file=input("Enter destination file:")
        if not os.path.exists(destination_file):
                print("Destination file doesn't exists")
        else: 
            print("WARNING:Destination file overwriting")

            if(user_input:=input("Do you want to overwrite (Y/N):")).upper()=="Y":
                    try:
                
                               shutil.copy(source_file,destination_file)
                               print("File Copied")
                    except Exception as e:
                                     print(e)
            else:
                 print("NOT COPIED")           
elif command=="move file":
    source_file=input("Enter source file:")
    if not os.path.exists(source_file):
        print("source file doesn't exists,create file first")
    else:
        destination_folder=input("Enter destination folder:")
        if not os.path.exists(destination_folder):
            print("Destination folder doesn't exists")

        
            if(user_input:=input("Do you want to create folder (Y/N):")).upper()=="Y":
                
                os.mkdir(destination_folder)
                print("Folder Created")
                shutil.move(source_file,destination_folder)
                print("File Moved")
                            
            else:
                print("Thanks")
                
        else:
            shutil.move(source_file,destination_folder)
            print("File Moved")

elif command=="add note":
    note=input("Enter your note:")
    with open("data2.txt","a") as f:
        f.write(note)
elif command=="show notes":
    with open("data2.txt","r")as f:
       notes=f.readlines()
    if len(notes)==0:
         print("No note yet")
    else:
         print("---Your Notes---")
         for index,i in enumerate(notes,start=1):
              print(f"{index}:{i.strip()}")
    
    
      
            
            


else:
    print("I dont understand this command")