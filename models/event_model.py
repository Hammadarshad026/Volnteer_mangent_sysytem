from config.db_config import connectToDB
import mysql.connector
from datetime import datetime

class EventModel:
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

    def get_all_events(self):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT e.*, o.OrganizationName 
                FROM Events e
                LEFT JOIN Organizations o ON e.OrganizationID = o.OrganizationID
                ORDER BY e.EventDate DESC
            """)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()

    def get_event_by_id(self, event_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT e.*, o.OrganizationName 
                FROM Events e
                LEFT JOIN Organizations o ON e.OrganizationID = o.OrganizationID
                WHERE e.EventID = %s
            """, (event_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()
    

    def add_event(self, org_id, event_name, event_date, location=None, capacity=None):
        try:
            self.connect()
            self.cursor.execute(
                """INSERT INTO Events 
                   (OrganizationID, EventName, EventDate, Location, Capacity) 
                   VALUES (%s, %s, %s, %s, %s)""",
                (org_id, event_name, event_date, location, capacity)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()
            
    def get_events_by_organization(self, org_id):
        try:
            self.connect()
            self.cursor.execute(
                "SELECT * FROM Events WHERE OrganizationID = %s ORDER BY EventDate DESC", 
                (org_id,)
            )
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    def update_event(self, event_id, event_name, event_date, location, capacity):
        try:
            self.connect()
            self.cursor.execute(
                """UPDATE Events 
                   SET EventName = %s, EventDate = %s, Location = %s, Capacity = %s
                   WHERE EventID = %s""",
                (event_name, event_date, location, capacity, event_id)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            self.disconnect()