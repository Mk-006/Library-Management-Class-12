import random
try:
    import mysql.connector as Link
except:
    try:
        import mariadb as Link
    except:
        print("No Database Software or Connector has been installed.\nKindly install Mysql or mariadb and thier connectors to use the software")
        exit()
import sys
import os
import datetime
import pickle

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
    Mysql_Cursor.execute("use Library")
except:
    import Database
    Database.Fill_Table()
    Mysql_Cursor.execute("use Library")
if "--Reinitialize" in sys.argv:
    import Database
    Database.Fill_Table()
    Mysql_Cursor.execute("use Library")
DefSerch="CardID"
def clear_terminal():
    if "--Testing" in sys.argv:
        pass
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
def create_table(data,Table):
    data.insert(0,Table)
    num_columns = len(data[0])
    column_widths = [max(len(str(row[i])) for row in data) for i in range(num_columns)]
    horizontal_line = "╠" + "╬".join("═" * (width + 2) for width in column_widths) + "╣" 
    table = []
    table.append("╠" + "╦".join("═" * (width + 2) for width in column_widths) + "╗") 
    for row in data:
        formatted_row = "║" + "║".join(f" {str(item):{width}} " for item, width in zip(row, column_widths)) + "║"
        table.append(formatted_row)
        if row != data[-1]:
            table.append(horizontal_line) 
    table.append("╠" + "╩".join("═" * (width + 2) for width in column_widths) + "╝") 
    return "\n".join(table)
def Input(Text="",Type="str",Error=""):
    if len(Text)>0: Text="║"+Text+"\n"
    if len(Error)>0: Error="║"+Error+"\n"
    Output=None
    while True:
        try:
            if Type == "str":
                Output = input(Text + "║»")
            elif Type == "int":
                Output = int(input(Text + "║»"))
            elif Type == "float":
                Output = float(input(Text + "║»"))
            elif Type == "bool":
                Output = bool(input(Text + "║»"))
            elif Type == "date": 
                Date=input(Text + "║»")
                Output = datetime.datetime.strptime(Date, "%Y-%m-%d").date()
            break
        except :
            print(Error,end="")
    return Output
def Card_IDplusUsername():
    global DefSerch
    while True:
        if DefSerch=="CardID":
            Output=Input("Card ID:")
            if "CHANGE" in Output.upper():
                DefSerch="Username"
            elif Output.isnumeric():
                return int(Output)
            else:
                print("║Enter a number or To switch to using Username enter 'Change' ONLY")
        if DefSerch=="Username":
            Output=Input("Username:")
            if "CHANGE" in Output.upper():
                DefSerch="CardID"
            else:
                Mysql_Cursor.execute(f"select Card_ID from Users where username='{Output}'")
                Card_ID=Mysql_Cursor.fetchone()
                if Card_ID: return Card_ID[0]
                else:print("║User Does not exsist enter a valid username")
def Make_Box(Title,Data,Start="╔"):
    Width=36
    if len(Title)%2!=0: Width-=1;
    print(f"{Start}{'═'*Width}╗")
    print(f"║{' '*((Width//2)-len(Title)//2)}{Title}{' '*((Width//2)-len(Title)//2)}║")
    print(f"╠{'═'*Width}╣")
    Num=1
    for Text in Data:
        print(f"║  {Num}. {Text}{' '*(Width-len(str(Text))-5-(1 if Num > 9 else 0))}║")
        Num+=1
    print(f"╠{'═'*Width}╝")

def Auth():
    Fines_calculation()
    First=True
    print("""
╔════════════════════════════════════════════════════╗
║  :::    :::   ::::::::   :::    :::      :::       ║ 
║  :+:   :+:   :+:    :+:  :+:    :+:    :+: :+:     ║ 
║  +:+  +:+    +:+    +:+  +:+    +:+   +:+   +:+    ║ 
║  +#++:++     +#+    +:+  +#++:++#++  +#++:++#++:   ║ 
║  +#+  +#+    +#+    +#+  +#+    +#+  +#+     +#+   ║ 
║  #+#   #+#   #+#    #+#  #+#    #+#  #+#     #+#   ║ 
║  ###    ###   ########   ###    ###  ###     ###   ║ 
║The Apeejay School Library Management System        ║
║                                    -By Mayank Kumar║
║                                     XII-C          ║
╚════════════════════════════════════════════════════╝
""")
    Card_ID=None
    while True:
        if First: Make_Box("Enter Your Choice",["Log In","Sign Up"]) ; First=False
        else: Make_Box("Enter Your Choice",["Log In","Sign Up"],"╠")
        Choice=Input(Type="int",Error="Your Choice Should be a Number")
        if Choice==1:
            print("║Logging In")
            Username=Input("Username:")
            Password=Input("Password")
            Mysql_Cursor.execute(f"select Count(*) from Users where username='{Username}' and password='{Password}';")
            Exsists=Mysql_Cursor.fetchall()[0][0]
            if Exsists==1:
                Mysql_Cursor.execute(f"select Admin from Users where username='{Username}' and password='{Password}';")
                Type=Mysql_Cursor.fetchall()[0][0]
                if Type==0:
                    Login_Type="User"
                    Mysql_Cursor.execute(f"select Card_ID from Users where username='{Username}' and password='{Password}';")
                    Card_ID=Mysql_Cursor.fetchone()[0]
                else:
                    Login_Type="Admin"
                    Mysql_Cursor.execute(f"select Card_ID from Users where username='{Username}' and password='{Password}';")
                    Card_ID=Mysql_Cursor.fetchone()[0]
                break
            else:
                print("║Password or Username Incorrect")
        elif Choice==2:
            print("║Signing Up")
            Name=Input("Full Name:")
            while True:
                Email=Input("Emai Address:")
                if Email.count('@') == 1 and Email.count('.') >= 1:
                    username, domain = Email.split('@')
                    domain_name, extension = domain.split('.')
                    if username and domain_name and extension:
                        break
                    else:print("║Invalid email address.Dosen't follow email syntax")
                else:print("║Invalid email address.Dosen't follow email syntax") 
            while True:
                Phone=Input("Phone Number:","int","Enter A 10 Digit Number")
                if len(str(Phone))==10: break;
                else: print("║Invalid Number,Enter A 10 Digit Number")
            Address=Input("Address:")
            while True:
                Username=Input("Username:")
                Mysql_Cursor.execute(f"select Count(*) from Users where username='{Username}'")
                Exsists=Mysql_Cursor.fetchall()[0][0]
                if Exsists==0: break
                else:print("║Choose a Different Username,Username Already taken")
            Password=Input("Password:")
            while True:
                Card_ID=random.randint(100000,1000000)
                Mysql_Cursor.execute(f"select Count(*) from Users where Card_Id='{Card_ID}'")
                if Mysql_Cursor.fetchall()[0][0]==0: break
            Mysql_Cursor.execute(f"INSERT INTO Users (Card_ID, username, password, full_name, email, contact_number, address, membership, Admin) VALUES ('{Card_ID}', '{Username}', '{Password}', '{Name}', '{Email}', {Phone}, '{Address}',False, FALSE)")
            Mysql_Connection.commit()
            Login_Type="User"
            break
        elif Choice==321:
            Mysql_Cursor.close()
            Mysql_Connection.close()
            exit()
        else:
            print("║Invalid Option")
    clear_terminal()
    return Login_Type,Card_ID


def User():
    First=True
    while True:
        if First: 
            Make_Box("User Panel",["Search Book","Borrow Book","Return Book","Last Checked out","Checkout History","Account Data","Change Details","Delete Account","Exit"])
            First=False
        else: Make_Box("User Panel",["Search Book","Borrow Book","Return Book","Last Checked out","Checkout History","Account Data","Change Details","Delete Account","Exit"],"╠")
        Choice=Input(Type="int",Error="Your Choice Should be a Number")
        if Choice==1:
            Search_Book()
        elif Choice==2:
            Borrow(Card_ID)
        elif Choice==3:
            Return(Card_ID)
        elif Choice==4:
            Last_Checkout(Card_ID)
        elif Choice==5:
            All_Checkout_User(Card_ID)
        elif Choice==6:
            User_Data(Card_ID)
        elif Choice==7:
            Change_Details(Card_ID)
        elif Choice==8:
            Del_User(Card_ID)
            break
        elif Choice == 9:
            print("║Exiting the Library Management System.")
            break
        else:
            print("║Invalid choice. Please select a valid option.")

def Admin():
    First=True
    while True:
        if First: 
            Make_Box("Admin Panel",["Add Books","Edit Books","Manage Users","Lend Books","Return Books","Fines","Pay Fine","Database","Print Database","Exit"])
            First=False
        else: Make_Box("Admin Panel",["Add Books","Edit Books","Manage Users","Lend Books","Return Books","Fines","Pay Fine","Database","Print Database","Exit"],"╠")
        Choice=Input(Type="int",Error="Your Choice Should be a Number")
        if Choice==1:
            Add_Book()
        elif Choice==2:
            Barcode = Input("Barcode:","int","Barcode Should be a number")
            if Check_if_Book_Exsists(Barcode):
                Mysql_Cursor.execute(f"Select * from Books where Barcode = {Barcode}")
                Data=Mysql_Cursor.fetchall()
                Mysql_Cursor.execute(f"desc Books")
                Top=[i[0] for i in Mysql_Cursor.fetchall()]
                print(create_table(Data,Top) )
                Edit_Book(Barcode)
            else:
                print("║Invalid Barcode")
        elif Choice==3:
            Manage_Users()
        elif Choice==4:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Borrow(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==5:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Return(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==6:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): 
                fin=Fine(Card_ID)
                print("║User has a fine of "+ str(fin))
            else:print("║User Dosent exsist")
        elif Choice==7:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Pay_Fine(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==8:
            print("║This is a barebones version of Mysql Shell only Main Commands are supported")
            Database()
        elif Choice==9:
            Print_Database()
        elif Choice ==10:
            print("║Exiting the Library Management System.")
            break
        else:
            print("║Invalid choice. Please select a valid option.")

def Check_if_Book_Exsists(Barcode):
    Mysql_Cursor.execute(f"select Count(*) from Books where Barcode='{Barcode}'")
    Count=Mysql_Cursor.fetchone()[0]
    if Count==1:
        return True
    else:
        return False
def Check_if_User_Exsists(Card_ID):
    Mysql_Cursor.execute(f"select Count(*) from Users where Card_Id='{Card_ID}'")
    Count=Mysql_Cursor.fetchone()[0]
    if Count==1:
        return True
    else:
        return False

def Search_Book():
    while True:
        Make_Box("Search By",["Title","Author","Genre","Publication Date","Rating","Availability","Barcode","Back to Main Menu"],"╠")
        print("║Multiple options can be selected using a Comma eg:1,5")
        Choices=Input("Choice:",Type="str",Error="Your Choice Should be a Number").split(",")
        try:
            Choices=[int(i) for i in Choices]
        except:
            print("║Your Choice Should be a Number")
        Query_Builder = [] 
        if 1 in Choices:
            Title = Input("Title:")
            Query_Builder.append(f"title LIKE '%{Title}%'")
        if 2 in Choices:
            Author = Input("Author:")
            Query_Builder.append(f"author LIKE '%{Author}%'")
        if 3 in Choices:
            Genre = Input("Genre:")
            Query_Builder.append(f"genre LIKE '{Genre}'")
        if 4 in Choices:
            Publication_Date = Input("Publication Date (YYYY-MM-DD):","date","Invalid date format. Please use the format YYYY-MM-DD")
            Query_Builder.append(f"publication_date = '{Publication_Date}'")
        if 5 in Choices:
            while True:
                Rating = Input("Rating (0.00 - 5.00) (Seperate with - to find in range):")
                try:
                    if "-" in Rating:
                        Start, End = map(float, Rating.split("-"))
                        Query_Builder.append(f"rating BETWEEN {Start} AND {End}")
                        break
                    elif isinstance(float(Rating), float):
                        if 0.00 <= float(Rating) <= 5.00:
                            Query_Builder.append(f"rating = {float(Rating):.2f}")
                            break
                        else:
                            print("║Rating should be between 0.00 and 5.00")
                    else:
                        print("║Rating should be a valid number.")
                except :
                    print("║Rating should be a number between 0.00 and 5.00 or a range separated with '-'")
        if 6 in Choices:
            Availability = Input("Availability (TRUE/FALSE):")
            Query_Builder.append(f"availability_status = {Availability.upper()}")
        if 7 in Choices:
            Barcode = Input("Barcode:","int")
            Query_Builder.append(f"Barcode = {Barcode}")
        if len(Query_Builder)!=0:
            Query="SELECT * FROM Books WHERE " + " AND ".join(Query_Builder)
            Mysql_Cursor.execute(Query)
            Results = Mysql_Cursor.fetchall()
            Mysql_Cursor.execute(f"desc Books")
            Top=[i[0] for i in Mysql_Cursor.fetchall()]
            print(create_table(Results,Top) )
            if 8 in Choices:
                break
        elif 8 in Choices:
            break
        else:
            print("║No search criteria provided.")

def Borrow(Card_Id):
    Mysql_Cursor.execute(f"SELECT borrowing_id FROM Borrowings WHERE card_id = {Card_Id} AND return_date IS NULL")
    existing_borrowing = Mysql_Cursor.fetchone()
    Dif={"Admin":("User","Lent",""),"User":("You","Borrowed","Sorry,")}
    if existing_borrowing:
        print(f"║{Dif[Login_Type][0]} already have an open borrowing. Please return the book before borrowing a new one.")
    elif Fine(Card_Id):
        print(f"║{Dif[Login_Type][0]} has unpaid Fines. Please Pay the fines before Borrowing a new one.")
    else:
        Barcode = Input("Barcode:","int")
        if Check_if_Book_Exsists(Barcode):
            Mysql_Cursor.execute(f"SELECT availability_status FROM Books WHERE Barcode = {Barcode}")
            availability = Mysql_Cursor.fetchone()
            if availability[0] == 1:
                Mysql_Cursor.execute(f"INSERT INTO Borrowings (Barcode, card_id, borrowing_date, due_date) VALUES ({Barcode}, {Card_Id}, NOW(), NOW() + INTERVAL 7 DAY)")
                Mysql_Connection.commit()
                Mysql_Cursor.execute(f"UPDATE Books SET availability_status = 0 WHERE Barcode = {Barcode}")
                Mysql_Connection.commit()
                Mysql_Cursor.execute(f"Select * from Books where Barcode = {Barcode}")
                Data=Mysql_Cursor.fetchall()
                Mysql_Cursor.execute(f"desc Books")
                Top=[i[0] for i in Mysql_Cursor.fetchall()]
                print(create_table(Data,Top) )
                print(f"║Book {Dif[Login_Type][1]} successfully!")
            else:
                print(f"║{Dif[Login_Type][2]} the book is not available for borrowing.")
        else:
            print("║Book with that barcode dosent exist")

def Return(Card_Id):
        #Barcode = Input("Barcode:","int")
        Mysql_Cursor.execute(f"SELECT * FROM Borrowings WHERE Card_Id = {Card_Id} AND return_date IS NULL")
        borrowing_data = Mysql_Cursor.fetchone()
        Barcode=borrowing_data[1]
        if borrowing_data:
            Mysql_Cursor.execute(f"UPDATE Books SET availability_status = 1 WHERE Barcode = {Barcode}")
            Mysql_Connection.commit()
            Mysql_Cursor.execute(f"UPDATE Borrowings SET return_date = NOW() WHERE borrowing_id = {borrowing_data[0]}")
            Mysql_Connection.commit()
            Mysql_Cursor.execute(f"Select * from Books where Barcode = {Barcode}")
            Data=Mysql_Cursor.fetchall()
            Mysql_Cursor.execute(f"desc Books")
            Top=[i[0] for i in Mysql_Cursor.fetchall()]
            print(create_table(Data,Top))
            print("║Book returned successfully!")
        else:
            print("║The book isnt borrowed or it has already been returned.")

def Last_Checkout(Card_Id):
        Mysql_Cursor.execute(f"SELECT Books.Barcode, title, author, genre, publication_date, rating, location, Borrowings.borrowing_date ,due_date  FROM Books INNER JOIN Borrowings ON Books.Barcode = Borrowings.Barcode WHERE Card_Id = {Card_Id} AND return_date IS NULL ORDER BY Borrowings.borrowing_date DESC LIMIT 1")
        last_checked_out_book= Mysql_Cursor.fetchall()
        if last_checked_out_book:
            print(create_table(last_checked_out_book, ["Book id","Title","Author","Genre","publication date","rating", "location","borrowing date","Due Date"]))
        else:
            print("║No books have been Checked out")

def All_Checkout_User(Card_Id):
        Mysql_Cursor.execute(f"SELECT Books.Barcode, title, author, genre, publication_date, rating, location, Borrowings.borrowing_date , Borrowings.due_date ,Borrowings.return_date FROM Books INNER JOIN Borrowings ON Books.Barcode = Borrowings.Barcode WHERE Borrowings.card_id = {Card_Id} ORDER BY Borrowings.borrowing_date DESC")
        checkout_history = Mysql_Cursor.fetchall()
        if checkout_history:
            print(create_table(checkout_history, ["Book id","Title","Author","Genre","publication date","rating", "location","borrowing date","Due Date","Return Date"]))
        else:
            print("║No checkout history found for user.")

def Fine(Card_Id):
        Fines_calculation()
        Mysql_Cursor.execute(f"select fine_amount from Fines where Card_Id='{Card_Id}' and payment_status=FALSE")
        Fines=Mysql_Cursor.fetchall()
        Fine=0
        for x in Fines: Fine+=x[0];
        return Fine
    
def Fines_calculation():
    Mysql_Cursor.execute("SELECT * FROM Borrowings WHERE due_date < CURDATE() AND return_date IS NOT NULL")
    Overdue = Mysql_Cursor.fetchall()
    for Borrowing in Overdue:
        Borrowing_id = Borrowing[0]
        Mysql_Cursor.execute(f"SELECT * FROM Fines WHERE borrowing_id = '{Borrowing_id}'")
        Count=Mysql_Cursor.fetchone()[0]
        if Count==0:
            Mysql_Cursor.execute(f"INSERT INTO Fines (borrowing_id, Card_ID, fine_amount, fine_date, payment_status) VALUES ({Borrowing_id},{Borrowing[2]},0,{Borrowing[4]},False")
            Mysql_Connection.commit()
    Mysql_Cursor.execute("SELECT * FROM Fines WHERE payment_status = False")
    Fines=Mysql_Cursor.fetchall()
    Current_date = datetime.date.today()
    for Unpaid in Fines:
        Fine=((Current_date - Unpaid[-2]).days)*0.5
        Mysql_Cursor.execute(f"UPDATE Fines SET fine_amount={Fine} WHERE fine_id='{Unpaid[0]}'")

def Pay_Fine(Card_ID):
    try:
        Fin=Fine(Card_ID)
        Mysql_Cursor.execute(f"SELECT fine_id FROM Fines WHERE Card_ID = {Card_ID} AND payment_status = FALSE")
        unpaid_fines = Mysql_Cursor.fetchall()
        if not unpaid_fines:
            print("║No outstanding fines found for this user.")
            return
        for fine_id in unpaid_fines:
            Mysql_Cursor.execute(f"UPDATE Fines SET payment_status = TRUE WHERE fine_id = {fine_id[0]}") 
        Mysql_Connection.commit()
        print("║User has a fine of",Fin)
        print("║Fines paid successfully.") 
    except Exception as e:
        print("Error paying fines:", e)

def User_Data(Card_Id):        
        Mysql_Cursor.execute(f"SELECT * FROM Users WHERE Card_ID = {Card_Id}")
        User = Mysql_Cursor.fetchone()
        fine=Fine(Card_Id)
        longest_string = max((item for item in User if isinstance(item, str)), key=len, default="")
        if len(longest_string)<14: longest_string="12345678901234";
        S=len(longest_string)+10
        print(f"""╠{"═"*(S+2)}╗
║{" "*(int(S/2)-5)}Account Data{" "*(int(S/2)-5)}║
╠{"═"*(S+2)}╣
║  Card_Id:{User[0]}{" "*(S-len(str(User[0]))-8)}║
║  Username:{User[1]}{" "*(S-len(str(User[1]))-9)}║
║  Name:{User[3]}{" "*(S-len(str(User[3]))-5)}║
║  Email:{User[4]}{" "*(S-len(str(User[4]))-6)}║
║  Contact:{User[5]}{" "*(S-len(str(User[5]))-8)}║
║  Address:{User[6]}{" "*(S-len(str(User[6]))-8)}║
║  Fine Amount:{fine}{" "*(S-len(str(fine))-12)}║
║  Membership:{bool(User[7])}{" "*(S-len(str(bool(User[7])))-11)}║""")
        if bool(User[7]):
            print(f"""║  Start Date:{User[8]}{" "*(S-len(str(User[8]))-11)}║
║  End Date:{User[9]}{" "*(S-len(str(User[9]))-9)}║ 
╠{"═"*(S+2)}╝""")
        else:
            print(f"""╠{"═"*(S)}╝""")

def Change_Details(Card_Id):
    while True:
        if Login_Type=="User": Make_Box("Change",["Password","Email","Contact","Address","Username","Name","Back to Main Menu"],"╠")
        else: Make_Box("Edit Account",["Password","Email","Contact","Address","Username","Name","Back to Main Menu"],"╠") 
        change_choice=Input("Choice","int","Your Choice Should be a Number")
        if change_choice == 1:
            new_password = Input("New password:")
            Mysql_Cursor.execute(f"UPDATE Users SET password = '{new_password}' WHERE Card_ID = {Card_Id}")
            Mysql_Connection.commit()
            print("║Password changed successfully!")

        elif change_choice == 2:
            New_Email=Input("Emai Address:")
            if New_Email.count('@') == 1 and New_Email.count('.') >= 1:
                username, domain = New_Email.split('@')
                domain_name, extension = domain.split('.')
                if username and domain_name and extension:
                    Mysql_Cursor.execute(f"UPDATE Users SET email = '{New_Email}' WHERE Card_ID = {Card_Id}")
                    Mysql_Connection.commit()
                    print("║Email changed successfully!")
                else:print("║Invalid email address.Dosen't follow email syntax")
            else:print("║Invalid email address.Dosen't follow email syntax")
            
        elif change_choice == 3:
            while True:
                new_contact=Input("Phone Number:","int","Enter A 10 Digit Number")
                if len(str(new_contact))==10: break;
                else: print("║Invalid Number,Enter A 10 Digit Number")
            Mysql_Cursor.execute(f"UPDATE Users SET contact_number = '{new_contact}' WHERE Card_ID = {Card_Id}")
            Mysql_Connection.commit()
            print("║Contact number changed successfully!")

        elif change_choice == 4:
            new_address = Input("New address:")
            Mysql_Cursor.execute(f"UPDATE Users SET address = '{new_address}' WHERE Card_ID = {Card_Id}")
            Mysql_Connection.commit()
            print("║Address changed successfully!")

        elif change_choice == 5:
            while True:
                new_username=Input("Username:")
                Mysql_Cursor.execute(f"select Count(*) from Users where username='{new_username}'")
                Exsists=Mysql_Cursor.fetchall()[0][0]
                if Exsists==0: break
                else:print("║Choose a Different Username,Username Already taken")
            Mysql_Cursor.execute(f"UPDATE Users SET username = '{new_username}' WHERE Card_ID = {Card_Id}")
            Mysql_Connection.commit()
            print("║Username changed successfully!")

        elif change_choice == 6:
            new_name = Input("Enter new name:")
            Mysql_Cursor.execute(f"UPDATE Users SET full_name = '{new_name}' WHERE Card_ID = {Card_Id}")
            Mysql_Connection.commit()
            print("║Name changed successfully!")
        elif change_choice == 7:
            break
        else:
            print("║Invalid choice!")

def Del_User(Card_Id): 
    Mysql_Cursor.execute(f"SELECT count(*) FROM Borrowings WHERE Card_Id = {Card_Id} AND return_date IS NULL")
    borrowed_books = Mysql_Cursor.fetchone()[0]
    if borrowed_books==1:
        print("║User cannot be deleted as they have borrowed books.")
        return
    fine_total = Fine(Card_Id)
    if fine_total > 0:
        print("║User cannot be deleted due to outstanding fines.")
        return
    Mysql_Cursor.execute(f"DELETE FROM Fines WHERE Card_Id = {Card_Id}")
    Mysql_Connection.commit()
    Mysql_Cursor.execute(f"DELETE FROM Borrowings WHERE Card_Id = {Card_Id}")
    Mysql_Connection.commit()
    Mysql_Cursor.execute(f"DELETE FROM Users WHERE Card_ID = {Card_Id}")
    Mysql_Connection.commit() 
    print("║User deleted successfully.")

def Add_Book():
    Title=Input("Title:")
    Author=Input("Author:")
    Genre=Input("Genre:")
    Publication_Date = Input("Publication Date (YYYY-MM-DD):","date","Invalid date format. Please use the format YYYY-MM-DD")
    while True:
        Rating = Input("Rating:","float","Rating should be a valid Float Value between 0.00 and 5.00")
        if 0.00 <= Rating <= 5.00:
            break
        else:
            print("║Rating should be between 0.00 and 5.00")
    while True:
        try:
            Location = Input("Location:")
            break
        except:
            pass
    while True:
        availability_status=Input("Availability status:").upper()
        if availability_status=="TRUE" or availability_status=="FALSE":
            break
        else:
            print("║Enter True or False")
    while True:
        Barcode=random.randint(100000,1000000) 
        Mysql_Cursor.execute(f"select Count(*) from Books where Barcode='{Barcode}'")
        if Mysql_Cursor.fetchone()[0]==0: break
    Mysql_Cursor.execute(f"INSERT INTO Books (Barcode,title, author, genre, publication_date, rating, location, availability_status) VALUES ({Barcode},'{Title}', '{Author}', '{Genre}', '{Publication_Date}', {Rating:.2f}, {Location}, {availability_status})")
    Mysql_Connection.commit()
    Mysql_Cursor.execute(f"Select * from Books where Barcode='{Barcode}'")
    Results = Mysql_Cursor.fetchall()
    Mysql_Cursor.execute(f"desc Books")
    Top=[i[0] for i in Mysql_Cursor.fetchall()]
    print(create_table(Results,Top) )
    print("║Book added successfully!")

def Edit_Book(Barcode):
        Mysql_Cursor.execute(f"SELECT * FROM Books WHERE Barcode = {Barcode}")
        book_data = Mysql_Cursor.fetchone() 
        if book_data:
            while True:
                Make_Box("Edit",["Title","Author","Genre","Publication Date","Rating","Availability","Location","Back to Main Menu"],"╠")
                print("║Multiple options can be selected using a Comma eg:1,5")
                Choices=Input("Choice:",Type="str",Error="Your Choice Should be a Number").split(",")
                try:
                    Choices=[int(i) for i in Choices]
                except:
                    print("║Your Choice Should be a Number")
                Query_Builder = [] 
                if 1 in Choices:
                    Title = Input("New Title:")
                    Query_Builder.append(f"title='{Title}'")
                if 2 in Choices:
                    Author = Input("New Author:")
                    Query_Builder.append(f"author='{Author}%'")
                if 3 in Choices:
                    Genre = Input("New Genre:")
                    Query_Builder.append(f"genre='{Genre}'")
                if 4 in Choices:
                    Publication_Date = Input("New Publication Date (YYYY-MM-DD):","date","Invalid date format. Please use the format YYYY-MM-DD")
                    Query_Builder.append(f"publication_date = '{Publication_Date}'") 
                if 5 in Choices:
                    while True:
                        Rating = Input("Rating:","float","Rating should be a valid Float Value between 0.00 and 5.00")
                        if 0.00 <= Rating <= 5.00:
                            break
                        else:
                            print("║Rating should be between 0.00 and 5.00")
                    Query_Builder.append(f"rating = {Rating:.2f}")
                if 6 in Choices:
                    while True:
                        Availability=Input("Availability status:").upper()
                        if Availability=="TRUE" or Availability=="FALSE":
                            break
                        else:
                            print("║Enter True or False")
                    Query_Builder.append(f"availability_status = {Availability.upper()}")
                if 7 in Choices:
                    Location = Input("Location (0000.0000 - 9999.9999):")
                    Query_Builder.append(f"Location = '{Location}'")
                if len(Query_Builder)!=0:
                    Query="Update Books SET " + " , ".join(Query_Builder) + f" WHERE Barcode='{Barcode}';"
                    Mysql_Cursor.execute(Query)
                    Mysql_Connection.commit()
                    Mysql_Cursor.execute(f"select * from Books where Barcode='{Barcode}'")
                    Results = Mysql_Cursor.fetchall()
                    Mysql_Cursor.execute(f"desc Books")
                    Top=[i[0] for i in Mysql_Cursor.fetchall()]
                    print(create_table(Results,Top) )
                    if 8 in Choices:
                        break
                elif 8 in Choices:
                    break
                else:
                    print("║No search criteria provided.")
def Manage_Users():
    while True:
        Make_Box("Manage Users",["Add User","Delete User","User's Checkouts","Edit Account","Add Membership","Remove Membership","Promote User","Demote User","Back to Main Menu"],"╠")
        Choice=Input("Choice:",Type="int",Error="Your Choice Should be a Number") 
        if Choice==1:
            Add_User()
        elif Choice==2:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID):
                Del_User(Card_ID)
            else:
                print("║User Dosent exsist")
        elif Choice==3:
            Make_Box("Checkout",["All","Last","Exit"],"╠")
            Choice=Input(Type="int",Error="Your Choice Should be a Number")
            if Choice==1:
                Card_ID=Card_IDplusUsername()
                if Check_if_User_Exsists(Card_ID): All_Checkout_User(Card_ID)
                else:print("║User Dosent exsist")
            elif Choice==2:
                Card_ID=Card_IDplusUsername()
                if Check_if_User_Exsists(Card_ID): Last_Checkout(Card_ID)
                else:print("║User Dosent exsist")
            elif Choice==3:
                pass
            else:
                print("║Invalid Option")
        elif Choice==4:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Change_Details(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==5:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Add_Membership(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==6:
            Card_ID=Card_IDplusUsername()
            if Check_if_User_Exsists(Card_ID): Remove_Membership(Card_ID)
            else:print("║User Dosent exsist")
        elif Choice==7:
            Admin_privilege("Promote")
        elif Choice==8:
            Admin_privilege("Demote")
        elif Choice==9:
            break
        
def Add_User():
    Name=Input("Full Name:")
    Email=Input("Emai Address:")
    while True:
        Phone=Input("Phone Number:","int","Enter A 10 Digit Number")
        if len(str(Phone))==10: break;
        else: print("║Invalid Number,Enter A 10 Digit Number")
    Address=Input("Address:")
    while True:
        Username=Input("Username:")
        Mysql_Cursor.execute(f"select Count(*) from Users where username='{Username}'")
        Exsists=Mysql_Cursor.fetchall()[0][0]
        if Exsists==0: break
        else:print("║Choose a Different Username,Username Already taken")
    Password=Input("Password:")
    while True:
        Card_ID=random.randint(1000,10000)
        Mysql_Cursor.execute(f"select Count(*) from Users where Card_Id='{Card_ID}'")
        if Mysql_Cursor.fetchall()[0][0]==0: break
    Mysql_Cursor.execute(f"INSERT INTO Users (Card_ID, username, password, full_name, email, contact_number, address, membership, Admin) VALUES ('{Card_ID}', '{Username}', '{Password}', '{Name}', '{Email}', {Phone}, '{Address}',False, FALSE)")
    Mysql_Connection.commit()

def Add_Membership(Card_ID):
    current_date = datetime.date.today()
    end_date = current_date + datetime.timedelta(days=30) 
    Mysql_Cursor.execute(f"UPDATE Users SET membership = TRUE, membership_start_date = '{current_date}', membership_end_date = '{end_date}' WHERE Card_ID = {Card_ID}")
    Mysql_Connection.commit()
    print("║Membership added successfully.")

def Remove_Membership(Card_ID):
    Mysql_Cursor.execute(f"UPDATE Users SET membership = FALSE, membership_start_date = NULL, membership_end_date = NULL WHERE Card_ID = {Card_ID}")
    Mysql_Connection.commit()
    print("║Membership removed successfully.")

def Admin_privilege(Type):
    User=Input("Card ID:",'int')
    if Check_if_User_Exsists(User):
        Mysql_Cursor.execute(f"select Admin from Users where Card_Id='{User}'")
        Status=Mysql_Cursor.fetchone()[0]
        if Card_ID==User:
            print("║Can not demote/promote yourself")
            return
        elif Type=="Promote":
            if not Status:
                Mysql_Cursor.execute(f"UPDATE Users SET Admin = TRUE WHERE Card_ID = {User}")
                Mysql_Connection.commit()
                print("║User promoted successfully")
                return
            else:
                print("║User is already an admin")
        elif Type=="Demote":
            if Status:
                Mysql_Cursor.execute(f"UPDATE Users SET Admin = FALSE WHERE Card_ID = {User}")
                Mysql_Connection.commit()
                print("║User Demoted successfully")
                return
            else:
                print("║User is not an admin")
    else:
        print("║User Dosent exsist")
def Print_Database():
    while True:
        Make_Box("Print All", ["Users", "Books", "Borrowings", "Fines", "Exit"], "╠")
        Choice = Input(Type="int", Error="Your Choice Should be a Number")
        if Choice == 1:
            Mysql_Cursor.execute("SELECT * FROM Users")
            Data = Mysql_Cursor.fetchall()
            Top = [desc[0] for desc in Mysql_Cursor.description]
            print(create_table(Data, Top))
        elif Choice == 2:
            Mysql_Cursor.execute("SELECT * FROM Books")
            Data = Mysql_Cursor.fetchall()
            Top = [desc[0] for desc in Mysql_Cursor.description]
            print(create_table(Data, Top))
        elif Choice == 3:
            Mysql_Cursor.execute("SELECT * FROM Borrowings")
            Data = Mysql_Cursor.fetchall()
            Top = [desc[0] for desc in Mysql_Cursor.description]
            print(create_table(Data, Top))
        elif Choice == 4:
            Mysql_Cursor.execute("SELECT * FROM Fines")
            Data = Mysql_Cursor.fetchall()
            Top = [desc[0] for desc in Mysql_Cursor.description]
            print(create_table(Data, Top))
        elif Choice == 5:
            break 
        else:
            print("║Invalid choice. Please select a valid option.")

def Database():
    while True:
        try:
            Command=Input()
            Commit=["ALTER","REPAIR","UPDATE","DELETE","INSERT"]
            Fetch=["DESC","DESCRIBE","SELECT"]
            if Command.upper()=="EXIT":
                return
            elif Command.strip().upper().split()[0] in Fetch:
                try:
                    Mysql_Cursor.execute(Command)
                    Data=Mysql_Cursor.fetchall()
                    Top = [desc[0] for desc in Mysql_Cursor.description]
                    print(create_table(Data,Top))
                except Exception as e:
                    print("║Error executing query:", e)
            elif Command.strip().upper().split()[0] in Commit:
                try:
                    Mysql_Cursor.execute(Command)
                    Mysql_Connection.commit()
                    print("║Changes Made Successfully")
                except Exception as e:
                    print("║Error executing query:", e)        
            else:
                print("║Unsupported Command Use Shell to execute commands")
        except:
            pass
while True:
    Login_Type,Card_ID=Auth()
    if Login_Type=="Admin":Admin()
    else: User()
    clear_terminal()
