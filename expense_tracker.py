import mysql.connector
from datetime import date
from tabulate import tabulate

def create_user_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (rollno INT PRIMARY KEY, name VARCHAR(255) NOT NULL, password VARCHAR(255) DEFAULT 'password123')")

def get_user_type():
    user_type = input("\nAre you a user or admin? Enter 'user' or 'admin': ").lower()
    print("-----------------------------------------------")
    return user_type

def authenticate_admin():
    password = input("\nEnter the admin password: ")
    return password == "Immanuvel"

def authenticate_user(cursor, rollno):
    print("\n")
    cursor.execute("SELECT * FROM Users WHERE rollno = %s", (rollno,))
    user = cursor.fetchone()
    return user

def add_user(cursor, mydb, rollno):

    existing_user = authenticate_user(cursor, rollno)

    if existing_user is not None:
        print("\nUser already exists. Please enter your password to continue.")
        print("\n")
        entered_password = input("Enter your password: ")

        stored_password = existing_user[2]  # Assuming the password is stored in the third column

        if entered_password == stored_password:
            print("\n")
            print("Password verified. Proceeding to the main menu.")
        else:
            print("\n")
            print("Incorrect password. User already exists , if you are not already enrolled , try to enter new ID. \n The below are he exisiting ID's:")
            print("\n")
            cursor.execute("SELECT rollno from Users")
            rows = cursor.fetchall()
            print(tabulate(rows, headers=["ID", "User_id"]))
            
            print("\nExiting....")
            exit()
    else:
        print("\n")
        name = input("Enter your name: ")
        print("\n")
        password = input("Enter your password: ")
        print("\n")
        cursor.execute("INSERT INTO Users (rollno, name, password) VALUES (%s, %s, %s)", (rollno, name, password))
        mydb.commit()
        print("\n")
        print("User added successfully!")

def create_tables(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (ID INT AUTO_INCREMENT PRIMARY KEY, roll_number VARCHAR(50) NOT NULL, name VARCHAR(225) NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Expenses (ID INT AUTO_INCREMENT PRIMARY KEY, User_id INT, TYPE INT NOT NULL, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, VALIDITY INT NOT NULL DEFAULT 1, DATE DATE NOT NULL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Valid_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Not_Valid_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Grocery_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Food_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Accessories_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Electronics_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Studies_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

    cursor.execute("CREATE TABLE IF NOT EXISTS Others_Table (ID INT PRIMARY KEY, User_id INT, PURPOSE VARCHAR(225) NOT NULL, MONEY_SPENT FLOAT NOT NULL, DATE DATE NOT NULL, FOREIGN KEY (ID) REFERENCES Expenses(ID) ON DELETE CASCADE)")

def add_expense(cursor, mydb, user_type, user_id):
    while True:
        # Get user input for expense data
        print("\n")
        TYPE = int(input('''Enter the type of expense:
                        1.Grocery🥒
                        2.Food😋
                        3.Accessories⌚
                        4.Electronics🪫
                        5.Studies📚
                        6.Others🎈
                        '''))
        print("\n")
        PURPOSE = input("Specify the detail: ")
        print("\n")
        MONEY_SPENT = float(input("Enter the Money_spent 💵:"))
        print("\n")
        VALIDITY = int(input("Enter the validity (0 if Useless, 1 if Useful):"))
        print("\n")
        DATE = date.today()

        # Insert data into the Expenses table
        cursor.execute("INSERT INTO Expenses (User_id, TYPE, PURPOSE, MONEY_SPENT, VALIDITY, DATE) VALUES (%s, %s, %s, %s, %s, %s)",
                       (user_id, TYPE, PURPOSE, MONEY_SPENT, VALIDITY, DATE))

        # Get the last inserted ID (auto-incremented) in the Expenses table
        last_id = cursor.lastrowid

        # Insert data into the corresponding type-specific table
        table_name = get_table_name(TYPE)
        cursor.execute(f"INSERT INTO {table_name} (ID, User_id, PURPOSE, MONEY_SPENT, DATE) VALUES (%s, %s, %s, %s, %s)",
                       (last_id, user_id, PURPOSE, MONEY_SPENT, DATE))

        # Insert data into Valid_Table or Not_Valid_Table based on validity
        if VALIDITY == 1:
            cursor.execute("INSERT INTO Valid_Table (ID, User_id, PURPOSE, DATE) VALUES (%s, %s, %s, %s)", (last_id, user_id, PURPOSE, DATE))
        elif VALIDITY == 0:
            cursor.execute("INSERT INTO Not_Valid_Table (ID, User_id, PURPOSE, DATE) VALUES (%s, %s, %s, %s)", (last_id, user_id, PURPOSE, DATE))

        adding_more = input("Do you want to add another expense? 1. Yes  2. No\n")

        if adding_more == '2':
            mydb.commit()  # Commit the changes to the database
            print("Your list has been updated successfully")
            break
        else:
            continue

def delete_expenses(cursor, mydb):
    print("\n")
    delete_option = int(input('''Enter which delete action you need to perform
                              1. Delete all expenses
                              2. Delete a particular expense by ID
                              3. Go back to the main menu
                              '''))
    print("\n")

    if delete_option == 1:
        confirm = input("Are you sure you want to delete all expenses? (y/n): ")
        if confirm.lower() == 'y':
            # Delete from child tables first
            cursor.execute("DELETE FROM Valid_Table")
            cursor.execute("DELETE FROM Not_Valid_Table")
            cursor.execute("DELETE FROM Grocery_Table")
            cursor.execute("DELETE FROM Food_Table")
            cursor.execute("DELETE FROM Accessories_Table")
            cursor.execute("DELETE FROM Electronics_Table")
            cursor.execute("DELETE FROM Studies_Table")
            cursor.execute("DELETE FROM Others_Table")

            # Delete from parent table
            cursor.execute("DELETE FROM Expenses")
            mydb.commit()
            print("\n")
            print("All expenses deleted successfully.")
            print("\n")
        else:
            print("\nDeletion canceled.\n")

    elif delete_option == 2:
        print("\n")
        expense_id = int(input("Enter the ID of the expense you want to delete: "))
        print("\n")
        confirm = input(f"Are you sure you want to delete expense with ID {expense_id}? (y/n): ")
        print("\n")
        if confirm.lower() == 'y':
            # Delete from child tables first
            cursor.execute("DELETE FROM Valid_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Not_Valid_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Grocery_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Food_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Accessories_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Electronics_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Studies_Table WHERE ID = %s", (expense_id,))
            cursor.execute("DELETE FROM Others_Table WHERE ID = %s", (expense_id,))

            # Delete from parent table
            cursor.execute("DELETE FROM Expenses WHERE ID = %s", (expense_id,))
            mydb.commit()
            print("\n")
            print(f"Expense with ID {expense_id} deleted successfully.")
            print("\n")
        else:
            print("Deletion canceled.")

    elif delete_option == 3:
        print("\n")
        print("Going back to the main menu.")

    else:
        print("\n")
        print("Invalid option. Please enter a valid option.")

def view_expenses(cursor, user_id):
    print("\n")
    showall = int(input('''
                      1.See all expenses
                      2.See Valid expenses
                      3.See InValid expenses
                      4.See Grocery expenses
                      5.See Food expenses
                      6.See Accessories expenses
                      7.See Electronics expenses
                      8.See Studenis expenses
                      9.See Other expenses
                      
                      '''))
    if showall == 1:
        cursor.execute(f"SELECT * FROM Expenses WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print(tabulate(rows, headers=["ID", "User_id", "TYPE", "PURPOSE", "MONEY_SPENT", "VALIDITY", "DATE"]))
        print()
        cursor.execute(f"SELECT SUM(MONEY_SPENT) AS Total_Expenses FROM Expenses WHERE User_id = {user_id}")
        total_expenses = cursor.fetchone()[0]
        print("\n")
        print(f"Total Expenses for User {user_id}: {total_expenses}")
    elif showall == 2:
        cursor.execute(f"SELECT * FROM Valid_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "DATE"]))
    elif showall == 3:
        cursor.execute(f"SELECT * FROM Not_Valid_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "DATE"]))
    elif showall == 4:
        cursor.execute(f"SELECT * FROM Grocery_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

    elif showall == 5:
        cursor.execute(f"SELECT * FROM Food_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

    elif showall == 6:
        cursor.execute(f"SELECT * FROM Accessories_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

    elif showall == 7:
        cursor.execute(f"SELECT * FROM Electronics_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

    elif showall == 8:
        cursor.execute(f"SELECT * FROM Studies_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

    elif showall == 9:
        cursor.execute(f"SELECT * FROM Others_Table WHERE User_id = {user_id}")
        rows = cursor.fetchall()
        print("\n")
        print(tabulate(rows, headers=["ID", "User_id", "PURPOSE", "MONEY_SPENT", "DATE"]))

def get_table_name(TYPE):
    table_names = {
        1: "Grocery_Table",
        2: "Food_Table",
        3: "Accessories_Table",
        4: "Electronics_Table",
        5: "Studies_Table",
        6: "Others_Table"
    }
    return table_names.get(TYPE, "Others_Table")


def main():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Immanuvel@12",
        database="newDB"
    )
    print("-----------------------------------------------------------------------------------------------------------\n-----------------------------------------------------------------------------------------------------------")
    print("\nWelcome to Expense tracker...!\n")
    print("-----------------------------------------------------------------------------------------------------------\n-----------------------------------------------------------------------------------------------------------")
    cursor = mydb.cursor()

    create_user_table(cursor)

    user_type = get_user_type()

    if user_type == 'admin':
        if authenticate_admin():
            print("\n")
            print("Admin authentication successful.")
            print("\n")
            printing = input("Do you wish to see the Users ? (y/n)").lower()
            print("\n")
            if printing == 'y':
                cursor.execute("SELECT rollno,name FROM Users")
                rows = cursor.fetchall()
                print("\n")
                print(tabulate(rows, headers=["rollno", "name"]))
            return

        else:
            print("\n")
            print("Wrong password. Exiting.")
            return

    elif user_type == 'user':
        print("\n")
        rollno = int(input("Enter your roll number:"))

        add_user(cursor, mydb, rollno)

        user_id = rollno  # Assuming roll number is used as the user ID
    else:
        print("\n⚠   Invalid Input ⚠  \n")
        exit()

    create_tables(cursor)

    while True:
        print("\n")
        action = int(input('''Do you want to 
                        1. Add an expense
                        2. View Expenses
                        3. Delete
                        4. Exit
                           
                        '''))
        if action == 1:
            add_expense(cursor, mydb, user_type, user_id)
        elif action == 2:
            view_expenses(cursor, user_id)
        elif action == 3:
            delete_expenses(cursor, mydb)
        elif action == 4:
            print("\n")
            print("Thank you\n Don't just have a good day ,\n \"H A V E   A   G R E A T   D A Y \"")
            cursor.close()
            mydb.close()
            break
        else:
            mydb.commit()
            print("\n⚠   Invalid Input ⚠  \n")
            exit()

main()