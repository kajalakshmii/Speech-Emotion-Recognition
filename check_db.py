import sqlite3

def check_table_structure():
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Query to get the table structure
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()

    print("Table structure for 'users' table:")
    for column in columns:
        print(column)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    check_table_structure()
