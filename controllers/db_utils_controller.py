from models.db_utils_model import DatabaseUtilsModel
import mysql.connector
from datetime import datetime

class DatabaseUtilsController:
    def __init__(self):
        self.model = DatabaseUtilsModel()
        self.summary = None
        self.top_events = None
        
    def setup_database_objects(self):
        """
        Set up all database objects (triggers, procedures, views, functions)
        """
        print("\nSetting up database objects...")
        
        # Create triggers
        print("Creating triggers...")
        self.create_update_registered_count_trigger()
        
        # Create stored procedures
        print("Creating stored procedures...")
        self.create_register_volunteer_procedure()
        self.create_event_statistics_procedure()
        
        # Create views
        print("Creating views...")
        self.create_upcoming_events_view()
        self.create_volunteer_participation_view()
        
        # Create functions
        print("Creating functions...")
        self.create_volunteer_event_count_function()
        
        print("Database objects setup completed.")
    
    def create_update_registered_count_trigger(self):
        """Create trigger to update event registered count"""
        # First drop existing triggers if any
        self.model.drop_trigger("update_event_count_after_insert")
        self.model.drop_trigger("update_event_count_after_delete")
        
        # Create insert trigger - using the new method for creating triggers
        trigger_body = """
        BEGIN
            UPDATE Events 
            SET RegisteredCount = (
                SELECT COUNT(*) 
                FROM Volunteer_Event 
                WHERE EventID = NEW.EventID
            )
            WHERE EventID = NEW.EventID;
        END
        """
        
        if self.model.create_trigger("update_event_count_after_insert", "Volunteer_Event", "AFTER", "INSERT", trigger_body):
            print("- Created trigger: update_event_count_after_insert")
        
        # Create delete trigger
        trigger_body = """
        BEGIN
            UPDATE Events 
            SET RegisteredCount = (
                SELECT COUNT(*) 
                FROM Volunteer_Event 
                WHERE EventID = OLD.EventID
            )
            WHERE EventID = OLD.EventID;
        END
        """
        
        if self.model.create_trigger("update_event_count_after_delete", "Volunteer_Event", "AFTER", "DELETE", trigger_body):
            print("- Created trigger: update_event_count_after_delete")
        
    def create_register_volunteer_procedure(self):
        """Create stored procedure for registering volunteers to events"""
        # First drop existing procedure if any
        self.model.drop_procedure("RegisterVolunteerForEvent")
        
        procedure_sql = """
        CREATE PROCEDURE RegisterVolunteerForEvent(
            IN p_volunteer_id INT,
            IN p_event_id INT,
            OUT p_registration_id INT,
            OUT p_success BOOLEAN,
            OUT p_message VARCHAR(255)
        )
        BEGIN
            DECLARE event_capacity INT;
            DECLARE event_registered INT;
            DECLARE is_already_registered INT DEFAULT 0;
            
            -- Check if volunteer is already registered
            SELECT COUNT(*) INTO is_already_registered
            FROM Volunteer_Event
            WHERE VolunteerID = p_volunteer_id AND EventID = p_event_id;
            
            IF is_already_registered > 0 THEN
                SET p_success = FALSE;
                SET p_message = 'Volunteer is already registered for this event.';
                SET p_registration_id = NULL;
            ELSE
                -- Check event capacity
                SELECT Capacity, RegisteredCount INTO event_capacity, event_registered
                FROM Events
                WHERE EventID = p_event_id;
                
                IF event_capacity IS NOT NULL AND event_registered >= event_capacity THEN
                    SET p_success = FALSE;
                    SET p_message = 'Event has reached capacity.';
                    SET p_registration_id = NULL;
                ELSE
                    -- Register the volunteer
                    INSERT INTO Volunteer_Event (VolunteerID, EventID, RegistrationDate)
                    VALUES (p_volunteer_id, p_event_id, CURRENT_DATE());
                    
                    SET p_registration_id = LAST_INSERT_ID();
                    SET p_success = TRUE;
                    SET p_message = 'Volunteer successfully registered.';
                END IF;
            END IF;
        END
        """
        
        if self.model.create_procedure(procedure_sql):
            print("- Created procedure: RegisterVolunteerForEvent")
            
    def create_event_statistics_procedure(self):
        """Create stored procedure for getting event statistics"""
        # First drop existing procedure if any
        self.model.drop_procedure("GetEventStatistics")
        
        procedure_sql = """
        CREATE PROCEDURE GetEventStatistics(
            IN p_start_date DATE,
            IN p_end_date DATE
        )
        BEGIN
            -- Summary of events in date range
            SELECT 
                COUNT(DISTINCT EventID) AS TotalEvents,
                SUM(RegisteredCount) AS TotalRegistrations,
                AVG(RegisteredCount) AS AvgRegistrationsPerEvent,
                (SELECT COUNT(DISTINCT VolunteerID) FROM Volunteer_Event ve
                 JOIN Events e ON ve.EventID = e.EventID
                 WHERE e.EventDate BETWEEN p_start_date AND p_end_date) AS UniqueVolunteers
            FROM Events
            WHERE EventDate BETWEEN p_start_date AND p_end_date;
            
            -- Top events by registration
            SELECT 
                e.EventID,
                e.EventName,
                e.EventDate,
                e.RegisteredCount,
                o.OrganizationName
            FROM Events e
            LEFT JOIN Organizations o ON e.OrganizationID = o.OrganizationID
            WHERE e.EventDate BETWEEN p_start_date AND p_end_date
            ORDER BY e.RegisteredCount DESC
            LIMIT 5;
        END
        """
        
        if self.model.create_procedure(procedure_sql):
            print("- Created procedure: GetEventStatistics")
    
    def create_upcoming_events_view(self):
        """Create view for upcoming events"""
        # First drop existing view if any
        self.model.drop_view("UpcomingEvents")
        
        view_sql = """
        CREATE VIEW UpcomingEvents AS
        SELECT 
            e.EventID,
            e.EventName,
            e.EventDate,
            e.Location,
            e.Capacity,
            e.RegisteredCount,
            o.OrganizationName,
            (e.Capacity - e.RegisteredCount) AS AvailableSpots
        FROM Events e
        LEFT JOIN Organizations o ON e.OrganizationID = o.OrganizationID
        WHERE e.EventDate >= CURRENT_DATE()
        ORDER BY e.EventDate ASC
        """
        
        if self.model.create_view(view_sql):
            print("- Created view: UpcomingEvents")
            
    def create_volunteer_participation_view(self):
        """Create view for volunteer participation"""
        # First drop existing view if any
        self.model.drop_view("VolunteerParticipation")
        
        view_sql = """
        CREATE VIEW VolunteerParticipation AS
        SELECT 
            v.VolunteerID,
            v.Name AS VolunteerName,
            v.Email,
            v.City,
            COUNT(DISTINCT ve.EventID) AS EventsAttended,
            COUNT(DISTINCT vr.RoleID) AS RolesHeld
        FROM Volunteers v
        LEFT JOIN Volunteer_Event ve ON v.VolunteerID = ve.VolunteerID
        LEFT JOIN Volunteer_Roles vr ON ve.ID = vr.Volunteer_Event_ID
        GROUP BY v.VolunteerID, v.Name, v.Email, v.City
        ORDER BY EventsAttended DESC
        """
        
        if self.model.create_view(view_sql):
            print("- Created view: VolunteerParticipation")
            
    def create_volunteer_event_count_function(self):
        """Create function to count events a volunteer has participated in"""
        # First drop existing function if any
        self.model.drop_function("GetVolunteerEventCount")
        
        function_sql = """
        CREATE FUNCTION GetVolunteerEventCount(p_volunteer_id INT) 
        RETURNS INT
        DETERMINISTIC
        READS SQL DATA
        BEGIN
            DECLARE event_count INT;
            
            SELECT COUNT(DISTINCT EventID) INTO event_count
            FROM Volunteer_Event
            WHERE VolunteerID = p_volunteer_id;
            
            RETURN event_count;
        END
        """
        
        if self.model.create_function(function_sql):
            print("- Created function: GetVolunteerEventCount")
    
    def use_register_volunteer_procedure(self):
        """Use the RegisterVolunteerForEvent stored procedure"""
        # Get volunteer ID
        volunteer_id = input("Enter Volunteer ID: ")
        if not volunteer_id.isdigit():
            print("Invalid Volunteer ID.")
            return None
        volunteer_id = int(volunteer_id)
        
        # Get event ID
        event_id = input("Enter Event ID: ")
        if not event_id.isdigit():
            print("Invalid Event ID.")
            return None
        event_id = int(event_id)
        
        try:
            self.model.connect()
            cursor = self.model.conn.cursor(dictionary=True)
            
            # Create a simpler approach without using callproc
            cursor.execute(
                "SET @p_registration_id = 0, @p_success = FALSE, @p_message = ''"
            )
            cursor.execute(
                "CALL RegisterVolunteerForEvent(%s, %s, @p_registration_id, @p_success, @p_message)",
                (volunteer_id, event_id)
            )
            cursor.execute(
                "SELECT @p_registration_id, @p_success, @p_message"
            )
            result = cursor.fetchone()
            
            self.model.conn.commit()
            
            registration_id = result['@p_registration_id']
            success = result['@p_success']
            message = result['@p_message']
            
            print(f"\nResult: {message}")
            if success:
                print(f"Registration ID: {registration_id}")
                
            return success
            
        except mysql.connector.Error as err:
            print(f"Error calling stored procedure: {err}")
            return False
        finally:
            self.model.disconnect()

    def use_event_statistics_procedure(self):
        """Use the GetEventStatistics stored procedure"""
        # Get date range
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return None
        
        try:
            self.model.connect()
            
            # Execute the procedure - we need to handle this differently since
            # stored_results() isn't supported in all versions
            
            # Get summary data
            self.model.cursor.execute(
                "SELECT COUNT(DISTINCT EventID) AS TotalEvents, "
                "SUM(RegisteredCount) AS TotalRegistrations, "
                "AVG(RegisteredCount) AS AvgRegistrationsPerEvent, "
                "(SELECT COUNT(DISTINCT VolunteerID) FROM Volunteer_Event ve "
                "JOIN Events e ON ve.EventID = e.EventID "
                "WHERE e.EventDate BETWEEN %s AND %s) AS UniqueVolunteers "
                "FROM Events "
                "WHERE EventDate BETWEEN %s AND %s",
                (start, end, start, end)
            )
            self.summary = self.model.cursor.fetchall()
            
            # Get top events data
            self.model.cursor.execute(
                "SELECT e.EventID, e.EventName, e.EventDate, e.RegisteredCount, o.OrganizationName "
                "FROM Events e "
                "LEFT JOIN Organizations o ON e.OrganizationID = o.OrganizationID "
                "WHERE e.EventDate BETWEEN %s AND %s "
                "ORDER BY e.RegisteredCount DESC "
                "LIMIT 5",
                (start, end)
            )
            self.top_events = self.model.cursor.fetchall()
            
            # Display results
            from views.db_utils_view import DatabaseUtilsView
            view = DatabaseUtilsView()
            view.display_event_statistics(self.summary, self.top_events)
            
            return self.summary, self.top_events
            
        except mysql.connector.Error as err:
            print(f"Error querying data: {err}")
            return None
        finally:
            self.model.disconnect()

    def query_upcoming_events_view(self):
        """Query the UpcomingEvents view"""
        try:
            self.model.connect()
            self.model.cursor.execute("SELECT * FROM UpcomingEvents")
            events = self.model.cursor.fetchall()
            
            from views.db_utils_view import DatabaseUtilsView
            view = DatabaseUtilsView()
            view.display_upcoming_events(events)
            
            return events
        except mysql.connector.Error as err:
            print(f"Error querying view: {err}")
            return []
        finally:
            self.model.disconnect()
            
    def query_volunteer_participation_view(self):
        """Query the VolunteerParticipation view"""
        try:
            self.model.connect()
            self.model.cursor.execute("SELECT * FROM VolunteerParticipation")
            volunteers = self.model.cursor.fetchall()
            
            from views.db_utils_view import DatabaseUtilsView
            view = DatabaseUtilsView()
            view.display_volunteer_participation(volunteers)
            
            return volunteers
        except mysql.connector.Error as err:
            print(f"Error querying view: {err}")
            return []
        finally:
            self.model.disconnect()
            
    def use_volunteer_event_count_function(self):
        """Use the GetVolunteerEventCount function"""
        # Get volunteer ID
        volunteer_id = input("Enter Volunteer ID: ")
        if not volunteer_id.isdigit():
            print("Invalid Volunteer ID.")
            return None
        volunteer_id = int(volunteer_id)
        
        try:
            self.model.connect()
            self.model.cursor.execute(
                "SELECT GetVolunteerEventCount(%s) AS EventCount", 
                (volunteer_id,)
            )
            result = self.model.cursor.fetchone()
            
            if result:
                print(f"\nVolunteer (ID: {volunteer_id}) has participated in {result['EventCount']} events.")
            
            return result['EventCount'] if result else None
        except mysql.connector.Error as err:
            print(f"Error calling function: {err}")
            return None
        finally:
            self.model.disconnect()