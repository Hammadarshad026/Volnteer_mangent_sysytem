from config.db_config import connectToDB
import mysql.connector

class VolunteerRoleModel:
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

    def get_all_roles(self):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT vr.RoleID, vr.Volunteer_Event_ID, vr.RoleName,
                       v.Name as VolunteerName, e.EventName
                FROM Volunteer_Roles vr
                JOIN Volunteer_Event ve ON vr.Volunteer_Event_ID = ve.ID
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                JOIN Events e ON ve.EventID = e.EventID
                ORDER BY e.EventName, v.Name
            """)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()

    def get_role_by_id(self, role_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT vr.RoleID, vr.Volunteer_Event_ID, vr.RoleName,
                       v.VolunteerID, v.Name as VolunteerName, 
                       e.EventID, e.EventName, e.EventDate
                FROM Volunteer_Roles vr
                JOIN Volunteer_Event ve ON vr.Volunteer_Event_ID = ve.ID
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                JOIN Events e ON ve.EventID = e.EventID
                WHERE vr.RoleID = %s
            """, (role_id,))
            result = self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()

    def add_role(self, volunteer_event_id, role_name):
        try:
            self.connect()
            
            # First verify that the volunteer_event_id exists
            self.cursor.execute(
                "SELECT ID FROM Volunteer_Event WHERE ID = %s",
                (volunteer_event_id,)
            )
            if not self.cursor.fetchone():
                print("Registration not found.")
                return None
                
            # Add the role
            self.cursor.execute(
                "INSERT INTO Volunteer_Roles (Volunteer_Event_ID, RoleName) VALUES (%s, %s)",
                (volunteer_event_id, role_name)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            self.disconnect()
            
    def get_roles_by_registration(self, volunteer_event_id):
        try:
            self.connect()
            self.cursor.execute(
                "SELECT RoleID, RoleName FROM Volunteer_Roles WHERE Volunteer_Event_ID = %s",
                (volunteer_event_id,)
            )
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_roles_by_event(self, event_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT vr.RoleID, vr.RoleName, v.Name as VolunteerName, ve.ID as RegistrationID
                FROM Volunteer_Roles vr
                JOIN Volunteer_Event ve ON vr.Volunteer_Event_ID = ve.ID
                JOIN Volunteers v ON ve.VolunteerID = v.VolunteerID
                WHERE ve.EventID = %s
                ORDER BY v.Name
            """, (event_id,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_roles_by_volunteer(self, volunteer_id):
        try:
            self.connect()
            self.cursor.execute("""
                SELECT vr.RoleID, vr.RoleName, e.EventName, e.EventDate, ve.ID as RegistrationID
                FROM Volunteer_Roles vr
                JOIN Volunteer_Event ve ON vr.Volunteer_Event_ID = ve.ID
                JOIN Events e ON ve.EventID = e.EventID
                WHERE ve.VolunteerID = %s
                ORDER BY e.EventDate DESC
            """, (volunteer_id,))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            self.disconnect()
            
    def update_role(self, role_id, role_name):
        try:
            self.connect()
            self.cursor.execute(
                "UPDATE Volunteer_Roles SET RoleName = %s WHERE RoleID = %s",
                (role_name, role_id)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            self.disconnect()
            
    def delete_role(self, role_id):
        try:
            self.connect()
            self.cursor.execute("DELETE FROM Volunteer_Roles WHERE RoleID = %s", (role_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            self.disconnect()