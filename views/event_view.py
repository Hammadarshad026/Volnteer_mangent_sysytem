from datetime import datetime

class EventView:
    def display_events(self, events):
        if not events:
            print("No events found.")
            return

        print("\n--- EVENTS LIST ---")
        print("{:<5} {:<30} {:<12} {:<20} {:<5} {:<20}".format(
            "ID", "Event Name", "Date", "Location", "Capacity", "Organization"))
        print("-" * 100)
        
        for event in events:
            event_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'N/A'
            print("{:<5} {:<30} {:<12} {:<20} {:<5} {:<20}".format(
                event['EventID'],
                event['EventName'][:28] + '..' if len(event['EventName']) > 30 else event['EventName'],
                event_date,
                event['Location'][:18] + '..' if event['Location'] and len(event['Location']) > 20 else (event['Location'] or 'N/A'),
                event['Capacity'] or 'N/A',
                event['OrganizationName'][:18] + '..' if event.get('OrganizationName') and len(event['OrganizationName']) > 20 else (event.get('OrganizationName') or 'N/A')
            ))
        print("-" * 100)
    
    def display_event_details(self, event):
        if not event:
            print("Event not found.")
            return
            
        print("\n--- EVENT DETAILS ---")
        print(f"ID: {event['EventID']}")
        print(f"Name: {event['EventName']}")
        print(f"Date: {event['EventDate'].strftime('%Y-%m-%d') if event['EventDate'] else 'Not set'}")
        print(f"Location: {event['Location'] or 'Not provided'}")
        print(f"Capacity: {event['Capacity'] or 'Not specified'}")
        print(f"Registered: {event['RegisteredCount']} volunteer(s)")
        print(f"Organization: {event.get('OrganizationName') or 'Not specified'}")
        print("-" * 30)
    
    def get_event_input(self, organizations):
        print("\n--- ADD NEW EVENT ---")
        
        # Display available organizations
        print("\nAvailable Organizations:")
        for org in organizations:
            print(f"{org['OrganizationID']}: {org['OrganizationName']}")
            
        org_id = input("\nOrganization ID (Enter to skip): ") or None
        if org_id:
            org_id = int(org_id)
            
        event_name = input("Event Name: ")
        
        # Date input with validation
        while True:
            date_input = input("Event Date (YYYY-MM-DD): ")
            try:
                event_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                
        location = input("Location (optional, press Enter to skip): ") or None
        
        capacity = input("Capacity (optional, press Enter to skip): ") or None
        if capacity:
            capacity = int(capacity)
            
        return org_id, event_name, event_date, location, capacity
        
    def get_event_update_input(self, event):
        print("\n--- UPDATE EVENT ---")
        print(f"Current name: {event['EventName']}")
        event_name = input("New name (press Enter to keep current): ") or event['EventName']
        
        current_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'Not set'
        print(f"Current date: {current_date}")
        
        # Date input with validation
        while True:
            date_input = input("New date (YYYY-MM-DD, press Enter to keep current): ") or current_date
            try:
                event_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                
        print(f"Current location: {event['Location'] or 'Not set'}")
        location = input("New location (press Enter to keep current): ") or event['Location']
        
        print(f"Current capacity: {event['Capacity'] or 'Not set'}")
        capacity_input = input("New capacity (press Enter to keep current): ")
        capacity = int(capacity_input) if capacity_input else event['Capacity']
            
        return event_name, event_date, location, capacity