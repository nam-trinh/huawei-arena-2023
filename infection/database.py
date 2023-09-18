import sqlite3

def connect_fun(database_name: str) -> sqlite3.Connection:
    """
    Connect to an SQLite database and return a connection object.

    Parameters:
        database_name (str): The name (or path) of the SQLite database file to connect to.

    Returns:
        sqlite3.Connection or None: A connection object if the connection is successful,
        or None if there is an error.

    Example usage:
        db_name = 'your_database_name.db'
        connection = connect_fun(db_name)
        
        if connection:
            print(f"Connected to {db_name}")
            # You can now use 'connection' to interact with the database.
        else:
            print("Connection failed.")
    """
    try:
        connection = sqlite3.connect(database_name)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None