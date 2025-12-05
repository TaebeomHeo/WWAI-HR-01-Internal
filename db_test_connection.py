import mysql.connector

DB_CONFIG = {
    'host': '61.37.80.105',
    'port': 3306,
    'database': 'dbwisewiresdb',
    'user': 'wisewires',
    'password': 'wiseadmin140!'
}

def test_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            db_version = cursor.fetchone()
            print(f"Successfully connected to MySQL database. Version: {db_version[0]}")
            cursor.close()
            conn.close()
            return True
        else:
            print("Failed to connect to the database.")
            return False
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return False

if __name__ == "__main__":
    test_db_connection()
