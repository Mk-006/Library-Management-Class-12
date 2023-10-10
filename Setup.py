try:
    import mysql.connector as Link
except:
    try:
        import mariadb as Link
    except:
        print("No Database Software or Connector has been installed.\nKindly install Mysql or mariadb and thier connectors to use the software")
        exit()
import pickle
try:
    import requests
except:
    print("'requests' Not Installed")
    exit()

try:
    with open("Default_Cred","rb+") as Creds:
        Data=pickle.load(Creds)
    Mysql_Connection=Link.connect(host=Data["Host"],user=Data["Username"],password=Data["Password"])
except:
    with open("Default_Cred","wb+") as Creds:
        while True:
            try:
                Host=input("Host Name:")
                Username=input("Username:")
                Password=input("Password:")
                Data={"Host":Host,"Username":Username,"Password":Password}
                pickle.dump(Data,Creds)
                Mysql_Connection=Link.connect(host=Data["Host"],user=Data["Username"],password=Data["Password"])
                break
            except:
                pass
Mysql_Cursor=Mysql_Connection.cursor()

try:
    Main="https://raw.githubusercontent.com/Mk-006/Library-Management-Class-12/main/Main.py"
    Database="https://raw.githubusercontent.com/Mk-006/Library-Management-Class-12/main/Database.py"
    main_content = requests.get(Main).content
    with open("Main.py", "wb") as main_file:
        main_file.write(main_content)
    database_content = requests.get(Database).content
    with open("Database.py", "wb") as database_file:
        database_file.write(database_content)
except:
    print("An error occured ")
    
import Database
Database.Fill_Table()
Mysql_Cursor.execute("use Library")
