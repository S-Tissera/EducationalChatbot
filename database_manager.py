import mysql.connector

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="", database="chatbot_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def query_db(self, sql_query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_query, params)
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def update_db(self, sql_update, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_update, params)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
