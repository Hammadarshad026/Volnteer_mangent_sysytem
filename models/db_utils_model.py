from config.db_config import connectToDB
import mysql.connector

class DatabaseUtilsModel:
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
            
    def execute_sql(self, sql):
        """Execute any SQL statement"""
        try:
            self.connect()
            # Execute the SQL statement directly
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error executing SQL: {err}")
            return False
        finally:
            self.disconnect()
            
    def execute_script(self, sql_script):
        """Execute a SQL script with multiple statements"""
        try:
            self.connect()
            # For running raw SQL scripts
            cursor = self.conn.cursor()
            
            # Split script on semicolons not inside BEGIN/END blocks
            statements = []
            current_statement = []
            in_block = False
            
            for line in sql_script.splitlines():
                line = line.strip()
                
                if not line or line.startswith('--'):  # Skip empty lines and comments
                    continue
                    
                if 'BEGIN' in line:
                    in_block = True
                    
                current_statement.append(line)
                
                if 'END' in line and in_block:
                    in_block = False
                    
                if line.endswith(';') and not in_block:
                    statements.append('\n'.join(current_statement))
                    current_statement = []
            
            # Execute each statement
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
                    
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error executing SQL script: {err}")
            return False
        finally:
            self.disconnect()
            
    def create_trigger(self, trigger_name, table, timing, event, body):
        """Create a database trigger"""
        sql = f"""
        CREATE TRIGGER {trigger_name}
        {timing} {event} ON {table}
        FOR EACH ROW
        {body}
        """
        return self.execute_sql(sql)
        
    def create_procedure(self, procedure_sql):
        """Create a stored procedure"""
        return self.execute_sql(procedure_sql)
        
    def create_function(self, function_sql):
        """Create a database function"""
        return self.execute_sql(function_sql)
        
    def create_view(self, view_sql):
        """Create a database view"""
        return self.execute_sql(view_sql)
        
    def drop_trigger(self, trigger_name):
        """Drop a database trigger"""
        sql = f"DROP TRIGGER IF EXISTS {trigger_name}"
        return self.execute_sql(sql)
        
    def drop_procedure(self, procedure_name):
        """Drop a stored procedure"""
        sql = f"DROP PROCEDURE IF EXISTS {procedure_name}"
        return self.execute_sql(sql)
        
    def drop_function(self, function_name):
        """Drop a database function"""
        sql = f"DROP FUNCTION IF EXISTS {function_name}"
        return self.execute_sql(sql)
        
    def drop_view(self, view_name):
        """Drop a database view"""
        sql = f"DROP VIEW IF EXISTS {view_name}"
        return self.execute_sql(sql)