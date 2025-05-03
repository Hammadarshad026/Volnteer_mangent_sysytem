from config.db_config import connectToDB
import mysql.connector
from datetime import datetime

class VolunteerEventModel:
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

    def get_all_registrations(self):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT ve.ID, ve.VolunteerID, ve.EventID, ve.RegistrationDate,
                       v.Name as VolunteerName, 
                       e.EventName, e.EventDate
                FROM Volunteer_Event ve
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                JOIN Events e ON ve.EventID = e.EventID
                ORDER BY ve.RegistrationDate DESC
            """)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()

    def get_registration_by_id(self, registration_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT ve.ID, ve.VolunteerID, ve.EventID, ve.RegistrationDate,
                       v.Name as VolunteerName, v.Email as VolunteerEmail,
                       e.EventName, e.EventDate, e.Location
                FROM Volunteer_Event ve
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                JOIN Events e ON ve.EventID = e.EventID
                WHERE ve.ID = %s
            """, (registration_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()

    def register_volunteer_for_event(self, volunteer_id, event_id, registration_date=None):
        try:
            self.connect()
            
            # First check if the volunteer is already registered for this event
            self.cursor.execute(
                "SELECT ID FROM Volunteer_Event WHERE VolunteerID = %s AND EventID = %s",
                (volunteer_id, event_id)
            )
            existing = self.cursor.fetchone()
            if existing:
                print(f"Volunteer is already registered for this event (Registration ID: {existing['ID']}).")
                return None
            
            # Check if the event has reached capacity
            self.cursor.execute(
                "SELECT Capacity, RegisteredCount FROM Events WHERE EventID = %s",
                (event_id,)
            )
            event = self.cursor.fetchone()
            if not event:
                print("Event not found.")
                return None
                
            if event['Capacity'] is not None and event['RegisteredCount'] >= event['Capacity']:
                print("This event has reached its capacity. Registration failed.")
                return None
            
            # Add the registration
            if registration_date:
                self.cursor.execute(
                    "INSERT INTO Volunteer_Event (VolunteerID, EventID, RegistrationDate) VALUES (%s, %s, %s)",
                    (volunteer_id, event_id, registration_date)
                )
            else:
                self.cursor.execute(
                    "INSERT INTO Volunteer_Event (VolunteerID, EventID) VALUES (%s, %s)",
                    (volunteer_id, event_id)
                )
                
            self.conn.commit()
            new_id = self.cursor.lastrowid
            
            # Update the RegisteredCount in Events table
            self.cursor.execute(
                "UPDATE Events SET RegisteredCount = RegisteredCount + 1 WHERE EventID = %s",
                (event_id,)
            )
            self.conn.commit()
            
            return new_id
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()
            
    def get_registrations_for_event(self, event_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT ve.ID, v.VolunteerID, v.Name, v.Email, ve.RegistrationDate
                FROM Volunteer_Event ve
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                WHERE ve.EventID = %s
                ORDER BY ve.RegistrationDate
            """, (event_id,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_events_for_volunteer(self, volunteer_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT ve.ID, e.EventID, e.EventName, e.EventDate, e.Location, ve.RegistrationDate
                FROM Volunteer_Event ve
                JOIN Events e ON ve.EventID = e.EventID
                WHERE ve.VolunteerID = %s
                ORDER BY e.EventDate
            """, (volunteer_id,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    

    def cancel_registration(self, registration_id):
        try:
            self.connect()
            
            # First delete any related roles in the Volunteer_Roles table
            self.cursor.execute("DELETE FROM Volunteer_Roles WHERE Volunteer_Event_ID = %s", (registration_id,))
            self.conn.commit()
            
            # Now delete the registration from the Volunteer_Event table
            self.cursor.execute("DELETE FROM Volunteer_Event WHERE ID = %s", (registration_id,))
            self.conn.commit()
            
            if self.cursor.rowcount > 0:
                print("Registration successfully canceled.")
                return True
            else:
                print("Registration not found.")
                return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            self.disconnect()