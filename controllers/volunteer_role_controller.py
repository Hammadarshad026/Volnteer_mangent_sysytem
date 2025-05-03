from models.volunteer_role_model import VolunteerRoleModel
from models.volunteer_event_model import VolunteerEventModel
from models.event_model import EventModel
from models.volunteer_model import VolunteerModel
from views.volunteer_role_view import VolunteerRoleView
from views.volunteer_event_view import VolunteerEventView

class VolunteerRoleController:
    def __init__(self):
        self.model = VolunteerRoleModel()
        self.ve_model = VolunteerEventModel()
        self.event_model = EventModel()
        self.volunteer_model = VolunteerModel()
        self.view = VolunteerRoleView()
        self.ve_view = VolunteerEventView()
    
    def show_all_roles(self):
        roles = self.model.get_all_roles()
        self.view.display_roles(roles)
        return roles
    
    def show_role_details(self, role_id):
        role = self.model.get_role_by_id(role_id)
        self.view.display_role_details(role)
        return role
    
    def add_new_role(self):
        # First show all registrations
        print("\n=== AVAILABLE REGISTRATIONS ===")
        registrations = self.ve_model.get_all_registrations()
        if not registrations:
            print("No registrations found. Please register volunteers for events first.")
            return None
        self.ve_view.display_registrations(registrations)
        
        # Get registration selection
        reg_id = input("\nEnter Registration ID: ")
        if not reg_id.isdigit():
            print("Invalid Registration ID.")
            return None
        reg_id = int(reg_id)
        
        # Check if registration exists
        registration = self.ve_model.get_registration_by_id(reg_id)
        if not registration:
            print(f"No registration found with ID {reg_id}.")
            return None
            
        # Get role information
        print(f"\nAssigning role to {registration['VolunteerName']} for event {registration['EventName']}")
        role_name = self.view.get_role_input()
        
        if not role_name:
            print("Role name is required.")
            return None
            
        # Add the role
        new_role_id = self.model.add_role(reg_id, role_name)
        if new_role_id:
            print(f"Role added successfully with ID: {new_role_id}")
            return new_role_id
        else:
            print("Failed to add role.")
            return None
    
    def show_roles_for_event(self):
        # Show available events
        print("\n=== AVAILABLE EVENTS ===")
        events = self.event_model.get_all_events()
        if not events:
            print("No events found.")
            return []
            
        # Display events for selection
        print("{:<5} {:<30} {:<12}".format("ID", "Event Name", "Date"))
        print("-" * 50)
        
        for event in events:
            event_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'N/A'
            print("{:<5} {:<30} {:<12}".format(
                event['EventID'],
                event['EventName'][:28] + '..' if len(event['EventName']) > 30 else event['EventName'],
                event_date
            ))
        print("-" * 50)
        
        # Get event selection
        event_id = input("\nEnter Event ID: ")
        if not event_id.isdigit():
            print("Invalid Event ID.")
            return []
        event_id = int(event_id)
        
        # Check if event exists
        event = self.event_model.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID {event_id}.")
            return []
            
        # Get and display roles for this event
        roles = self.model.get_roles_by_event(event_id)
        self.view.display_roles_for_event(event['EventName'], roles)
        return roles
    
    def show_roles_for_volunteer(self):
        # Show available volunteers
        print("\n=== AVAILABLE VOLUNTEERS ===")
        volunteers = self.volunteer_model.get_all_volunteers()
        if not volunteers:
            print("No volunteers found.")
            return []
            
        # Display volunteers for selection
        print("{:<5} {:<30} {:<30}".format("ID", "Name", "Email"))
        print("-" * 70)
        
        for volunteer in volunteers:
            print("{:<5} {:<30} {:<30}".format(
                volunteer['VolunteerID'],
                volunteer['Name'][:28] + '..' if len(volunteer['Name']) > 30 else volunteer['Name'],
                volunteer['Email'][:28] + '..' if len(volunteer['Email']) > 30 else volunteer['Email']
            ))
        print("-" * 70)
        
        # Get volunteer selection
        volunteer_id = input("\nEnter Volunteer ID: ")
        if not volunteer_id.isdigit():
            print("Invalid Volunteer ID.")
            return []
        volunteer_id = int(volunteer_id)
        
        # Check if volunteer exists
        volunteer = self.volunteer_model.get_volunteer_by_id(volunteer_id)
        if not volunteer:
            print(f"No volunteer found with ID {volunteer_id}.")
            return []
            
        # Get and display roles for this volunteer
        roles = self.model.get_roles_by_volunteer(volunteer_id)
        self.view.display_roles_for_volunteer(volunteer['Name'], roles)
        return roles
    
    def update_role(self):
        # First show all roles
        print("\n=== AVAILABLE ROLES ===")
        roles = self.model.get_all_roles()
        if not roles:
            print("No roles found.")
            return False
        self.view.display_roles(roles)
        
        # Get role selection
        role_id = input("\nEnter Role ID to update: ")
        if not role_id.isdigit():
            print("Invalid Role ID.")
            return False
        role_id = int(role_id)
        
        # Check if role exists
        role = self.model.get_role_by_id(role_id)
        if not role:
            print(f"No role found with ID {role_id}.")
            return False
            
        # Display current role details
        self.view.display_role_details(role)
        
        # Get updated information
        new_role_name = self.view.get_role_update_input(role)
        
        # Update the role
        success = self.model.update_role(role_id, new_role_name)
        if success:
            print("Role updated successfully!")
        else:
            print("Failed to update role.")
        return success
    
    def delete_role(self):
        # First show all roles
        print("\n=== AVAILABLE ROLES ===")
        roles = self.model.get_all_roles()
        if not roles:
            print("No roles found.")
            return False
        self.view.display_roles(roles)
        
        # Get role selection
        role_id = input("\nEnter Role ID to delete: ")
        if not role_id.isdigit():
            print("Invalid Role ID.")
            return False
        role_id = int(role_id)
        
        # Check if role exists
        role = self.model.get_role_by_id(role_id)
        if not role:
            print(f"No role found with ID {role_id}.")
            return False
            
        # Confirm before deleting
        confirm = input(f"Are you sure you want to delete the role '{role['RoleName']}' for {role['VolunteerName']}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Deletion aborted.")
            return False
        
        # Delete the role
        success = self.model.delete_role(role_id)
        if success:
            print("Role deleted successfully!")
        else:
            print("Failed to delete role.")
        return success