print("Running Setup up for Library Management System")
try:
    import mysql.connector as Link
except:
    try:
        import mariadb as Link
    except:
        print("No Database Software or Connector has been installed.\nKindly install Mysql or mariadb and thier connectors to use the software")
        exit()
print("Database Software Available ✓")
Available=[]
NotAvailable=[]
try:
    import requests
    Available.append("requests")
except:
    NotAvailable.append("requests")
try:
    import os
    null_device = os.devnull if os.name != 'nt' else 'nul'
    for Tool in ["wget","curl","git"]:
        try:
            Code=os.system(f"{Tool} --version > {null_device} 2>&1")
            if Code==0:
                Available.append(Tool)
        except:
            NotAvailable.append(Tool)
except: 
    pass
if len(NotAvailable)==4:
    print(str(NotAvailable).replace("[","").replace("]","").replace(","," or"),"Not Installed")
    exit()
print("Downloading Software Availabe ✓")
print("Downloading Files")
for Tool in Available:
    Main="https://raw.githubusercontent.com/Mk-006/Library-Management-Class-12/main/Main.py"
    Database="https://raw.githubusercontent.com/Mk-006/Library-Management-Class-12/main/Database.py"
    if Tool=="requests":
        print("Using requests")
        try:
            main_content = requests.get(Main).content
            with open("Main.py", "wb") as main_file:
                main_file.write(main_content)
            database_content = requests.get(Database).content
            with open("Database.py", "wb") as database_file:
                database_file.write(database_content)
            break
        except requests.exceptions.ConnectionError:
            print("Not connected to the internet")
            exit()
        except:
            print("An error occured, retrying") 
    elif Tool=="wget":
        print("using Wget")
        try:
            os.system(f"wget {Main} -O Main.py")
            os.system(f"wget {Database} -O Database.py") 
            break
        except:
            print("An error occured, retrying")
    elif Tool=="curl":
        print("Using cURL")
        try:
            os.system(f"curl {Main} -O Main.py")
            os.system(f"curl {Database} -O Database.py") 
            break
        except:
            print("An error occured, retrying")
    elif Tool=="git":
        print("Using Git")
        try:
            os.system("git clone https://github.com/Mk-006/Library-Management-Class-12.git")
            os.chdir("Library-Management-Class-12")
        except:
            print("An error occured Exiting")
            exit()
print("Connecting to Database")
import pickle
try:
    with open("Default_Cred","rb+") as Creds:
        Data=pickle.load(Creds)
    Mysql_Connection=Link.connect(host=Data["Host"],user=Data["Username"],password=Data["Password"])
except:
    Exit=False
    with open("Default_Cred","wb+") as Creds:
        while True:
            try:
                Host = input("Host Name:")
                Username = input("Username:")
                Password = input("Password:")
                print("Connecting...")
                Mysql_Connection = Link.connect(host=Host, user=Username, password=Password)
                Data = {"Host": Host, "Username": Username, "Password": Password}
                pickle.dump(Data, Creds)
                break  
            except:
                while True:
                    try:
                        Again = int(input("Incorrect Details ,Try Again(Y(1)/N(2))?:"))
                        if Again == 1:
                            break
                        elif Again == 2:
                            Exit=True
                            break
                        else:
                            print("Enter a number(1 or 2)")
                    except:
                        print("Enter a number(1 or 2)")
            if Exit: exit()
Mysql_Cursor=Mysql_Connection.cursor()
import Database
Database.Fill_Table()
print("Installation Complete")
while True:
    try:
        import os
        Run=int(input("Run Library Management system?(Y(1)/N(2)):"))
        break
    except:
        print("Enter a number(1 or 2)")

if Run==1:
    import Main
    exit()
elif Run==2:
    print("Run \n<python> Main.py\nTo run Library Management system\nUse --Reinitialize TO reload Database and Enter 321 on Login to Exit")
    Mysql_Cursor.close()
    Mysql_Connection.close()
    exit()
