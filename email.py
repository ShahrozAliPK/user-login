import sqlite3

# Function to check for valid "EMAIL ID"
def test_email(input_email):

    if "@" in input_email:

        return True

    print("\nPlease enter correct Email address!\n")
    return False

# Function to check for "EMAIL ID" (if exists already)
def email_search(user_email, db_filename, table_name):

    # Create connection to database
    connection = sqlite3.connect(f"DATABASE/{db_filename}.db")

    # Define cursor
    cursor = connection.cursor()

    # Search for "EMAIL ID" (if already exists)
    email_data = cursor.execute(f"SELECT Email from {table_name} WHERE Email = ?", (user_email, ))

    # Fetch response
    entries = email_data.fetchone()

    # If not found, return True
    if entries == None:
        return True

    # If already found, return False
    if entries != None:
        print("\nEmail Address already exists!\n")
        return False

