from config.db_config import connectToDB
import mysql.connector

class VolunteerModel:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = connectToDB()
        self.cursor = self.conn.cursor(dictionary=True)

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

    def get_all_volunteers(self):
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM Volunteers")
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()

    def get_volunteer_by_id(self, volunteer_id):
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM Volunteers WHERE VolunteerID = %s", (volunteer_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()

    def add_volunteer(self, name, email, phone=None, city=None):
        try:
            self.connect()
            self.cursor.execute(
                "INSERT INTO Volunteers (Name, Email, Phone, City) VALUES (%s, %s, %s, %s)",
                (name, email, phone, city)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()
            
    def search_volunteers(self, search_term):
        try:
            self.connect()
            search_pattern = f"%{search_term}%"
            self.cursor.execute(
                """SELECT * FROM Volunteers 
                   WHERE Name LIKE %s OR Email LIKE %s OR City LIKE %s
                   ORDER BY Name""",
                (search_pattern, search_pattern, search_pattern)
            )
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()