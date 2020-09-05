# Import Libraries and functions
import hashlib
import sqlite3
from num1 import test_num
from email import test_email, email_search
from password import test_password
from alpha1 import test_alpha
from id_generator import make_id
from clear import clear

# Function for login access
def login():

    # Filename for .db file [CHANGE HERE]
    db_name = "data"
    db_name1 = "login"

    # Tables names for .db file [CHANGE HERE] [JUST DON'T USE '-']
    table1 = "bio_data" # TABLE FOR USERS BIO DATA
    table2 = "login_id" # TABLE FOR USERS LOGIN INFO
    table3 = "login_info" # TABLE TO UPDATE LOGIN INFO

    # Connections to sqlite3 db
    connection = sqlite3.connect(f"DATABASE/{db_name}.db")  # DATABASE
    connection1 = sqlite3.connect(f"LOGIN/{db_name1}.db")   # LOGIN

    # Define cursors to sqlite3 db
    cursor = connection.cursor()    # DATABASE
    cursor1 = connection1.cursor()  # LOGIN

    # CREATE tables (if not exists)
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table1} (ID INTEGER, First_name TEXT, Last_name TEXT, Phone INTEGER)")
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table2} (ID INTEGER, Email TEXT, Password TEXT)")
    cursor1.execute(f"CREATE TABLE IF NOT EXISTS {table3} (ID INTEGER, First_name TEXT, Last_name TEXT, Last_login TEXT)")

    # Keep promting till valid option no
    while (True):

        # UI Menu
        print("\n---------------------------------------")
        print("   --- | USER LOGIN SYSTEM |---\n")
        print(" 1. LOGIN            2.CREATE NEW USER")
        print("---------------------------------------\n")

        # Ask for option no
        option = input("Type Option No: ")

        # Check for correct type
        check = test_num(option)

        # IF "LOGIN"
        if check == True and option == "1" and len(option) == 1:

            print("\nLOGIN\n")

            # Keep prompting till valid "EMAIL ID"
            while (True):

                email_id = input("Email Address: ")
            
                check = test_email(email_id)

                if check == True:
                    break
            
            # Keep prompting till valid "PASSWORD"
            while (True):

                password = input("Password: ")

                check = test_password(password)

                if check == True:
                    break

                print("\nPlease Enter Correct Password!\n")

            # Encrypt Password (SHA224)
            encrypted = hashlib.sha224(password.encode())

            # SELECT "PASSWORD" of that "EMAIL ID"
            user_id = cursor.execute(f"SELECT Password from {table2} WHERE Email = ?", (email_id, ))
            
            # Fetch response
            user_check = user_id.fetchone()

            # If no USER Found
            if user_check == None:

                print("\nNO USER FOUND!\n")
                return False

            # If USER Found
            if user_check != None:
                
                # If Password matches
                if encrypted.hexdigest() == user_check[0]:
                    
                    # Get First and Last name of USER
                    info = cursor.execute(f"SELECT First_name, Last_name from {table1} WHERE ID = (SELECT ID from {table2} WHERE Email = ? AND Password = ?)", (email_id, encrypted.hexdigest()))

                    # Fetch response
                    user_info = info.fetchall()

                    # Print name of that USER
                    clear()
                    print("\n\n---------------------------------------------------------------------------------------------------")
                    print(" \n                 --| Welcome Back, ", end="")

                    for i in range(len(user_info[0])):

                        print(user_info[0][i],"", end="")

                    # Extract First, Last and ID of USER
                    login_data = cursor.execute(f"SELECT ID, First_name, Last_name from {table1} WHERE ID = (SELECT ID from {table2} WHERE Email = ? AND Password = ?)", (email_id, encrypted.hexdigest()))
                    
                    # Fetch data
                    update_info = login_data.fetchall()

                    # Store ID, First and Last of USER
                    id_no = int(update_info[0][0])
                    first_name = update_info[0][1]
                    last_name = update_info[0][2]

                    # Check if user exists already or not
                    checking_data = cursor1.execute(f"SELECT ID from {table3} WHERE ID = ?", (id_no, ))

                    # Fetch response
                    user_checking_id = checking_data.fetchone()

                    # If user not found, INSERT into table
                    if user_checking_id == None:

                        cursor1.execute(f"INSERT INTO {table3} (ID, First_name, Last_name, Last_login) VALUES(?, ?, ?, datetime('now', 'localtime'))", (id_no, first_name, last_name))
                        connection1.commit()
                        print(" |---\n")

                    # If user found, UPDATE info
                    if user_checking_id != None:

                        time_data = cursor1.execute(f"SELECT Last_login from {table3} WHERE ID = ?", (id_no, ))

                        last_time = time_data.fetchone()

                        print(f"     Last Login: {last_time[0]} |---\n")

                        cursor1.execute(f"UPDATE {table3} SET Last_login = datetime('now', 'localtime') WHERE ID = ?", (id_no, ))
                        connection1.commit()

                    # Exit the program
                    return True

                # If "PASSWORD" not matches
                else:
                    print("\nIncorrect Password!\n")

                    # Ask for PASSWORD CHANGE
                    print("Forgot your Password!?\n")

                    ask = input("Type (Y/N): ")

                    # If YES
                    if ask.upper() == "Y" or ask.upper() == "YES":
                        
                        # Keep promting till EMAIL ADDRESS matches
                        while (True):

                            tmp_email_id = input("Type your Email Address: ")

                            check = test_email(tmp_email_id)
                            
                            if check == True:
                                
                                if tmp_email_id == email_id:
                                    break

                                else:
                                    print("\nType Correct Email Address!\n")

                        # Keep prompting till valid USER PHONE NUMBER
                        while (True):

                            number = input("Type your Phone Number: ")

                            check = test_num(number)

                            if check == True:
                                break

                            print("\nPlease Enter Correct Phone Number!\n")

                        # Extract USER First, Last and ID from table (If user found)
                        recover_data = cursor.execute(f"SELECT ID, First_name, Last_name from {table1} WHERE Phone = ?", (number, ))

                        # Fetch response
                        user_recover_info = recover_data.fetchall()

                        # If response is NULL
                        if user_recover_info == None:
                            print("\nPhone Number not matches!\n")
                            return False

                        # Print USER NAME
                        print("Change PASSWORD for ", end="")

                        for i in range(1, 3):

                            print(user_recover_info[0][i], "", end="")

                        print()

                        # Assign USER ID as an int
                        user_id = int(user_recover_info[0][0])

                        # Keep prompting till valid NEW PASSWORD
                        while (True):

                            new_password = input("Type NEW Password: ")

                            check = test_password(new_password)

                            # If valid, check for confirmation
                            if check == True:
                            
                                confirm_password = input("Confirm NEW Password: ")

                                check = test_password(confirm_password)

                                if check == True:
                                
                                    if confirm_password == new_password:
                                        break

                            print("\nPlease Enter Correct PASSWORD!\n")

                        # Encrypt NEW PASSWORD (SHA224)
                        encrypted = hashlib.sha224(new_password.encode())

                        # UPDATE PASSWORD
                        cursor.execute(f"UPDATE {table2} SET Password = ? WHERE ID = ?", (encrypted.hexdigest(), user_id))
                        connection.commit()

                        # Print Success, Exit the program
                        print("\nPASSWORD CHANGED SUCCESSFULLY!\n")
                        return True

                    # If "NO", exit the program
                    if ask.upper() == "N" or ask.upper() == "NO":
                        return False

                    # If not correct option is provided
                    else:
                        print("Please Type Correct Option!")                    

        # IF "CREATE NEW USER"
        if check == True and option == "2" and len(option) == 1:

            print("\nCREATE NEW USER\n")

            #------------------------------------#
            #         CREATE NEW USER            #
            #------------------------------------#
            # Keep prompting till valid "FIRST NAME"
            while (True):

                first_name = input("\nEnter Your First Name: ")

                check = test_alpha(first_name)

                if check == True:
                    break

                print("\nPlease Enter Correct First Name!\n")

            # Keep prompting till valid "LAST NAME"
            while (True):

                last_name = input("Enter Your Last Name: ")

                check = test_alpha(last_name)

                if check == True:
                    break

                print("\nPlease Enter Correct Last Name!\n")

            # Keep promting till valid "EMAIL ID"
            while (True):
            
                email = input("Your Email ID: ")

                check1 = test_email(email)
                check2 = email_search(email, db_name, table2)

                if check1 == True and check2 == True:
                    break

            # Keep promting till valid "PASSWORD"
            while (True):
            
                password = input("Your Password: ")

                check = test_password(password)

                if check == True:
                    break

                print("\nPlease Enter Correct Password!\n")

            # Keep prompting till valid "PHONE NUMBER"
            while (True):

                phone_num = input("Enter Phone Number (+92): ")

                check = test_num(phone_num)

                if check == True:
                    break

                print("\nPlease Enter Correct Phone Number!\n")

            # Encrypt Password (SHA224)
            encrypted = hashlib.sha224(password.encode())

            # Generate NEW USER ID
            user_id = make_id(db_name, table1)

            # Insert "BIO-DATA"
            cursor.execute(f"INSERT INTO {table1} (ID, First_name, Last_name, Phone) VALUES(?, ?, ?, ?)", (user_id, first_name, last_name, phone_num))
            connection.commit()

            # Insert "LOGIN-ID"
            cursor.execute(f"INSERT INTO {table2} (ID, Email, Password) VALUES(?, ?, ?)", (user_id, email, encrypted.hexdigest()))
            connection.commit()
            print("\nUSER CREATED SUCCESSFULLY\n")
            exit(0)

        if option != "1" and option != "2":
            print("\nPlease Enter Correct Option!\n")