import sqlite3

# GENERATES NEW USER ID #
def make_id(db_filename, table_name):

    connection = sqlite3.connect(f"DATABASE/{db_filename}.db")

    cursor = connection.cursor()

    # Return last ID
    key = cursor.execute(f"SELECT ID from {table_name} ORDER BY ID DESC LIMIT 1")

    # Fetch data
    value = key.fetchone()

    # Value to store USER ID
    user_id = 0

    # If first USER ID
    if value == None:
        user_id = 0

    # Else
    if value != None:
        user_id = int(value[0])

    # Update ID
    ID = user_id + 1

    # Return New ID
    return ID
	