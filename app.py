from controllers.organization_controller import OrganizationController
from controllers.event_controller import EventController
from controllers.volunteer_controller import VolunteerController
from controllers.volunteer_event_controller import VolunteerEventController
from controllers.volunteer_role_controller import VolunteerRoleController
from controllers.db_utils_controller import DatabaseUtilsController
from views.db_utils_view import DatabaseUtilsView
import os
os.system('cls')

def display_menu():
    print("\n=== VOLUNTEER MANAGEMENT SYSTEM ===")
    print("1. Organizations")
    print("2. Events")
    print("3. Volunteers")
    print("4. Volunteer Event Registrations")
    print("5. Volunteer Roles")
    print("6. Database Utilities")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice

def organization_menu():
    
    print("\n=== ORGANIZATIONS MENU ===")
    print("1. View All Organizations")
    print("2. View Organization Details")
    print("3. Add New Organization")
    print("4. View Events for an Organization")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice

def event_menu():
    
    print("\n=== EVENTS MENU ===")
    print("1. View All Events")
    print("2. View Event Details")
    print("3. Add New Event")
    print("4. Update Event")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice

def volunteer_menu():
    
    print("\n=== VOLUNTEERS MENU ===")
    print("1. View All Volunteers")
    print("2. View Volunteer Details")
    print("3. Add New Volunteer")
    print("4. Search Volunteers")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice

def volunteer_event_menu():
    
    print("\n=== VOLUNTEER EVENT REGISTRATIONS MENU ===")
    print("1. View All Registrations")
    print("2. View Registration Details")
    print("3. Register Volunteer for Event")
    print("4. View Volunteers for an Event")
    print("5. View Events for a Volunteer")
    print("6. Cancel Registration")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice

def volunteer_role_menu():
    
    print("\n=== VOLUNTEER ROLES MENU ===")
    print("1. View All Roles")
    print("2. View Role Details")
    print("3. Assign New Role")
    print("4. View Roles for an Event")
    print("5. View Roles for a Volunteer")
    print("6. Update Role")
    print("7. Delete Role")
    print("0. Back to Main Menu")
    choice = input("Enter your choice: ")
    return choice

def main():
    org_controller = OrganizationController()
    event_controller = EventController()
    volunteer_controller = VolunteerController()
    volunteer_event_controller = VolunteerEventController()
    volunteer_role_controller = VolunteerRoleController()
    db_utils_controller = DatabaseUtilsController()
    db_utils_view = DatabaseUtilsView()
    
    while True:
        choice = display_menu()
        
        if choice == '1':  # Organizations Menu
            while True:
                org_choice = organization_menu()
                
                if org_choice == '1':
                    
                    org_controller.show_all_organizations()
                elif org_choice == '2':
                    org_id = input("Enter Organization ID: ")
                    if org_id.isdigit():
                        org_controller.show_organization_details(int(org_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif org_choice == '3':
                    org_controller.add_new_organization()
                elif org_choice == '4':
                    org_id = input("Enter Organization ID: ")
                    if org_id.isdigit():
                        event_controller.show_events_by_organization(int(org_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif org_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == '2':  # Events Menu
            while True:
                event_choice = event_menu()
                
                if event_choice == '1':
                    event_controller.show_all_events()
                elif event_choice == '2':
                    event_id = input("Enter Event ID: ")
                    if event_id.isdigit():
                        event_controller.show_event_details(int(event_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif event_choice == '3':
                    event_controller.add_new_event()
                elif event_choice == '4':
                    event_id = input("Enter Event ID to update: ")
                    if event_id.isdigit():
                        event_controller.update_event(int(event_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif event_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == '3':  # Volunteers Menu
            while True:
                volunteer_choice = volunteer_menu()
                
                if volunteer_choice == '1':
                    volunteer_controller.show_all_volunteers()
                elif volunteer_choice == '2':
                    volunteer_id = input("Enter Volunteer ID: ")
                    if volunteer_id.isdigit():
                        volunteer_controller.show_volunteer_details(int(volunteer_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif volunteer_choice == '3':
                    volunteer_controller.add_new_volunteer()
                elif volunteer_choice == '4':
                    volunteer_controller.search_volunteers()
                elif volunteer_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == '4':  # Volunteer Event Registrations Menu
            while True:
                ve_choice = volunteer_event_menu()
                
                if ve_choice == '1':
                    volunteer_event_controller.show_all_registrations()
                elif ve_choice == '2':
                    reg_id = input("Enter Registration ID: ")
                    if reg_id.isdigit():
                        volunteer_event_controller.show_registration_details(int(reg_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif ve_choice == '3':
                    volunteer_event_controller.register_volunteer_for_event()
                elif ve_choice == '4':
                    volunteer_event_controller.show_volunteers_for_event()
                elif ve_choice == '5':
                    volunteer_event_controller.show_events_for_volunteer()
                elif ve_choice == '6':
                    volunteer_event_controller.cancel_volunteer_registration()
                elif ve_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == '5':  # Volunteer Roles Menu
            while True:
                vr_choice = volunteer_role_menu()
                
                if vr_choice == '1':
                    volunteer_role_controller.show_all_roles()
                elif vr_choice == '2':
                    role_id = input("Enter Role ID: ")
                    if role_id.isdigit():
                        volunteer_role_controller.show_role_details(int(role_id))
                    else:
                        print("Invalid ID. Please enter a number.")
                elif vr_choice == '3':
                    volunteer_role_controller.add_new_role()
                elif vr_choice == '4':
                    volunteer_role_controller.show_roles_for_event()
                elif vr_choice == '5':
                    volunteer_role_controller.show_roles_for_volunteer()
                elif vr_choice == '6':
                    volunteer_role_controller.update_role()
                elif vr_choice == '7':
                    volunteer_role_controller.delete_role()
                elif vr_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        elif choice == '6':  # Database Utilities Menu
            while True:
                db_choice = db_utils_view.display_db_utils_menu()
                
                if db_choice == '1':
                    db_utils_controller.setup_database_objects()
                elif db_choice == '2':
                    db_utils_controller.use_register_volunteer_procedure()
                elif db_choice == '3':
                    db_utils_controller.use_event_statistics_procedure()
                elif db_choice == '4':
                    db_utils_controller.query_upcoming_events_view()
                elif db_choice == '5':
                    db_utils_controller.query_volunteer_participation_view()
                elif db_choice == '6':
                    db_utils_controller.use_volunteer_event_count_function()
                elif db_choice == '0':
                    break
                else:
                    print("Invalid choice. Please try again.")
                
        elif choice == '0':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()