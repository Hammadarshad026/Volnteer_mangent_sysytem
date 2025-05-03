from config.db_config import connectToDB
import mysql.connector

class OrganizationModel:
    def __init__(self):
        self.conn=None
        self.cursor=None
    

    def connect(self):
        self.conn=connectToDB()
        self.cursor=self.conn.cursor(dictionary=True)

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
    
    def get_all_organizations(self):
        try:
            self.connect()
            self.cursor.execute('SELECT * FROM Organizations')
            result=self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f'Error : {err}')
            return []
        finally:
            self.disconnect()


    def get_organization_by_id(self,org_id):
        try:
            self.connect()
            self.cursor.execute('SELECT * FROM Organizations WHERE OrganizationID = %s',(org_id,))
            result=self.cursor.fetchone()
            return result
        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return None
        finally:
            self.disconnect()
    
    def add_organization(self,organization_name,address=None,contact_number=None):
        try:
            self.connect()
            self.cursor.execute(
                'INSERT INTO Organizations (OrganizationName,Address,ContactNumber) VALUES(%s,%s,%s)',
                (organization_name,address,contact_number)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print(f'Error: {err}')
            return None
        finally:
            self.disconnect()
