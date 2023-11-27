import pickle
try:
    import mysql.connector as Link
except:
    try:
        import mariadb as Link
    except:
        print("No Database Software or Connector has been installed.\nKindly install Mysql or mariadb and thier connectors to use the software")
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
def Create_Table():
    Mysql_Cursor.execute("use Library")
    Mysql_Cursor.execute("CREATE TABLE if not exists Users (  \
Card_ID INT PRIMARY KEY, \
username VARCHAR(255) NOT NULL, \
password VARCHAR(255) NOT NULL,\
full_name VARCHAR(255) NOT NULL,\
email VARCHAR(255) NOT NULL,\
contact_number VARCHAR(10) NOT NULL,\
address VARCHAR(255) ,\
membership BOOLEAN NOT NULL,\
membership_start_date DATE,\
membership_end_date DATE,\
Admin BOOLEAN NOT NULL);")
    Mysql_Connection.commit()
    Mysql_Cursor.execute("CREATE TABLE if not exists Books (\
ISBN INT PRIMARY KEY,\
title VARCHAR(255) NOT NULL,\
author VARCHAR(255) NOT NULL,\
genre VARCHAR(255) NOT NULL,\
publication_date DATE NOT NULL,\
rating DECIMAL(4, 2) NOT NULL, \
location VARCHAR(10) NOT NULL,\
availability_status BOOLEAN NOT NULL);")
    Mysql_Connection.commit()
    Mysql_Cursor.execute("CREATE TABLE if not exists Borrowings (\
borrowing_id INT AUTO_INCREMENT PRIMARY KEY,\
ISBN INT NOT NULL,\
Card_ID INT NOT NULL,\
borrowing_date DATE NOT NULL,\
due_date DATE NOT NULL,\
return_date DATE,\
FOREIGN KEY (ISBN) REFERENCES Books(ISBN) ON DELETE CASCADE,\
FOREIGN KEY (Card_ID) REFERENCES Users(Card_id) ON DELETE CASCADE);") 
    Mysql_Connection.commit()
    Mysql_Cursor.execute("CREATE TABLE IF NOT EXISTS Fines (\
fine_id INT AUTO_INCREMENT PRIMARY KEY,\
borrowing_id INT NOT NULL,\
Card_ID INT NOT NULL,\
fine_amount DECIMAL(10, 2) NOT NULL,\
fine_date DATE NOT NULL,\
payment_status BOOLEAN NOT NULL,\
FOREIGN KEY (borrowing_id) REFERENCES Borrowings(borrowing_id) ON DELETE CASCADE,\
FOREIGN KEY (Card_ID) REFERENCES Users(Card_id) ON DELETE CASCADE);")
    Mysql_Connection.commit()

def Fill_Table():
    Mysql_Cursor.execute("Drop database if exists Library")
    Mysql_Cursor.execute("create database if not exists Library;")
    Create_Table()
    Mysql_Cursor.execute("INSERT INTO Users (Card_ID, username, password, full_name, email, contact_number, address, membership, membership_start_date, membership_end_date, Admin) VALUES \
(1001, 'user1', 'pass123', 'John Doe', 'john@example.com', '1234567890', '123 Main St', TRUE, '2023-01-01', '2023-12-31', FALSE),\
(1002, 'user2', 'pass456', 'Jane Smith', 'jane@example.com', '9876543210', '456 Elm St', TRUE, '2023-02-01', '2023-12-31', FALSE),\
(1003, 'user3', 'pass789', 'Michael Johnson', 'michael@example.com', '5551234567', '789 Oak St', TRUE, '2023-03-01', '2023-12-31', FALSE),\
(1004, 'user4', 'passabc', 'Emily Williams', 'emily@example.com', '4449876543', '567 Maple Ave', TRUE, '2023-04-01', '2023-12-31', FALSE),\
(1005, 'user5', 'passxyz', 'David Brown', 'david@example.com', '7896541230', '890 Pine Rd', TRUE, '2023-05-01', '2023-12-31', FALSE),\
(1006, 'user6', 'pass123', 'Sarah Davis', 'sarah@example.com', '3335558888', '345 Cedar Ln', TRUE, '2023-06-01', '2023-12-31', FALSE),\
(1007, 'user7', 'pass456', 'Robert Wilson', 'robert@example.com', '6662224444', '456 Birch Rd', TRUE, '2023-07-01', '2023-12-31', FALSE),\
(1008, 'user8', 'pass789', 'Amanda Taylor', 'amanda@example.com', '1112223333', '234 Pine St', TRUE, '2023-08-01', '2023-12-31', FALSE),\
(1009, 'user9', 'passabc', 'William Martinez', 'william@example.com', '8887776666', '567 Oak Ave', TRUE, '2023-09-01', '2023-12-31', FALSE),\
(1010, 'Admin', 'AdminPassword', 'Olivia Hernandez', 'olivia@example.com', '5559994444', '678 Elm Rd', TRUE, '2023-10-01', '2023-12-31', TRUE)\
")
    Mysql_Connection.commit()
    Mysql_Cursor.execute("INSERT INTO Books (ISBN,title, author, genre, publication_date, rating, location, availability_status) VALUES\
(100001,'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', '2021-01-15', 4.2, '8000.1', TRUE),\
(100002,'To Kill a Mockingbird', 'Harper Lee', 'Classic', '2020-09-05', 4.5, '800.002', TRUE),\
(100003,'1984', 'George Orwell', 'Dystopian', '2019-05-22', 4.7, '800.003', TRUE),\
(100004,'Pride and Prejudice', 'Jane Austen', 'Romance', '2018-11-10', 4.0, '800.004', TRUE),\
(100005,'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', '2022-03-18', 4.3, '800.005', TRUE),\
(100006,'Harry Potter and the Sorcerers Stone', 'J.K. Rowling', 'Fantasy', '2021-06-30', 4.8, '800.006', TRUE),\
(100007,'The Catcher in the Rye', 'J.D. Salinger', 'Coming of Age', '2023-02-08', 3.9, '800.007', TRUE),\
(100008,'Brave New World', 'Aldous Huxley', 'Science Fiction', '2019-09-25', 4.1, '800.008', TRUE),\
(100009,'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', '2020-08-12', 4.6, '800.009', TRUE),\
(100010,'Jane Eyre', 'Charlotte Brontë', 'Gothic', '2023-04-04', 4.4, '800.010', TRUE)")
    Mysql_Connection.commit()
    Mysql_Cursor.execute("INSERT INTO Borrowings (ISBN, Card_ID, borrowing_date, due_date, return_date) VALUES\
(100001, 1001, '2023-05-10', '2023-05-17', '2023-05-15'),\
(100003, 1002, '2023-04-20', '2023-04-27', NULL),\
(100005, 1003, '2023-03-15', '2023-03-22', NULL),\
(100002, 1004, '2023-04-05', '2023-04-12', '2023-04-10'),\
(100004, 1005, '2023-05-01', '2023-05-08', NULL),\
(100006, 1007, '2023-03-25', '2023-04-01', '2023-03-30'),\
(100006, 1001, '2023-02-15', '2023-02-22', NULL),\
(100007, 1008, '2023-04-10', '2023-04-17', '2023-04-15'),\
(100009, 1009, '2023-05-05', '2023-05-12', NULL),\
(100010, 1010, '2023-03-30', '2023-04-06', NULL);")
    Mysql_Connection.commit()
    Mysql_Cursor.execute("INSERT INTO Fines (borrowing_id, Card_ID, fine_amount, fine_date, payment_status) VALUES\
(1,1001, 2.50, '2023-05-18', FALSE),\
(4,1001, 1.00, '2023-04-13', TRUE),\
(7,1002, 3.75, '2023-02-23', FALSE),\
(2,1005, 0.50, '2023-04-13', TRUE),\
(6,1004, 1.25, '2023-03-31', TRUE),\
(3,1003, 0.75, '2023-03-23', FALSE),\
(9,1009, 2.00, '2023-05-13', FALSE),\
(5,1007, 1.50, '2023-05-09', TRUE),\
(8,1007, 2.75, '2023-04-16', TRUE),\
(10,1010, 1.25, '2023-010-01', FALSE);")
    Mysql_Connection.commit()

Fill_Table()
