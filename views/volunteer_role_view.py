class VolunteerRoleView:
    def display_roles(self, roles):
        if not roles:
            print("No roles found.")
            return

        print("\n--- VOLUNTEER ROLES ---")
        print("{:<5} {:<30} {:<30} {:<20}".format(
            "ID", "Role", "Volunteer", "Event"))
        print("-" * 90)
        
        for role in roles:
            print("{:<5} {:<30} {:<30} {:<20}".format(
                role['RoleID'],
                role['RoleName'][:28] + '..' if len(role['RoleName']) > 30 else role['RoleName'],
                role['VolunteerName'][:28] + '..' if len(role['VolunteerName']) > 30 else role['VolunteerName'],
                role['EventName'][:18] + '..' if len(role['EventName']) > 20 else role['EventName']
            ))
        print("-" * 90)
    
    def display_role_details(self, role):
        if not role:
            print("Role not found.")
            return
            
        print("\n--- ROLE DETAILS ---")
        print(f"Role ID: {role['RoleID']}")
        print(f"Role Name: {role['RoleName']}")
        print(f"Volunteer: {role['VolunteerName']} (ID: {role['VolunteerID']})")
        print(f"Event: {role['EventName']} (ID: {role['EventID']})")
        if role['EventDate']:
            print(f"Event Date: {role['EventDate'].strftime('%Y-%m-%d')}")
        print(f"Registration ID: {role['Volunteer_Event_ID']}")
        print("-" * 30)
    
    def get_role_input(self):
        role_name = input("Enter role name/description: ")
        return role_name
        
    def get_role_update_input(self, current_role):
        print(f"Current role name: {current_role['RoleName']}")
        role_name = input("New role name (press Enter to keep current): ") or current_role['RoleName']
        return role_name
        
    def display_roles_for_event(self, event_name, roles):
        if not roles:
            print(f"No roles assigned for event: {event_name}")
            return

        print(f"\n--- ROLES FOR EVENT: {event_name} ---")
        print("{:<5} {:<30} {:<30} {:<10}".format(
            "ID", "Role", "Volunteer", "Reg. ID"))
        print("-" * 80)
        
        for role in roles:
            print("{:<5} {:<30} {:<30} {:<10}".format(
                role['RoleID'],
                role['RoleName'][:28] + '..' if len(role['RoleName']) > 30 else role['RoleName'],
                role['VolunteerName'][:28] + '..' if len(role['VolunteerName']) > 30 else role['VolunteerName'],
                role['RegistrationID']
            ))
        print("-" * 80)
        
    def display_roles_for_volunteer(self, volunteer_name, roles):
        if not roles:
            print(f"No roles assigned for volunteer: {volunteer_name}")
            return

        print(f"\n--- ROLES FOR VOLUNTEER: {volunteer_name} ---")
        print("{:<5} {:<30} {:<30} {:<10}".format(
            "ID", "Role", "Event", "Reg. ID"))
        print("-" * 80)
        
        for role in roles:
            event_date = role['EventDate'].strftime("%Y-%m-%d") if role['EventDate'] else ''
            event_info = f"{role['EventName']} ({event_date})"
            
            print("{:<5} {:<30} {:<30} {:<10}".format(
                role['RoleID'],
                role['RoleName'][:28] + '..' if len(role['RoleName']) > 30 else role['RoleName'],
                event_info[:28] + '..' if len(event_info) > 30 else event_info,
                role['RegistrationID']
            ))
        print("-" * 80)