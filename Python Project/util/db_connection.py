import mysql.connector
from mysql.connector import Error
from util.property_util import PropertyUtil


class DBConnection:
    _connection = None

    @staticmethod
    def get_connection():
        if DBConnection._connection is None:
            try:
                connection_string = PropertyUtil.get_property_string()
                DBConnection._connection = mysql.connector.connect(**connection_string)
                if DBConnection._connection.is_connected():
                    print("Connected to MySQL database")
                else:
                    print("Failed to connect to MySQL database")
            except Error as e:
                print(f"Error connecting to MySQL database: {e}")

        return DBConnection._connection
