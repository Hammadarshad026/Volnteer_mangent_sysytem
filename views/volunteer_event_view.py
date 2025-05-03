class VolunteerEventView:
    def display_registrations(self, registrations):
        if not registrations:
            print("No registrations found.")
            return

        print("\n--- VOLUNTEER EVENT REGISTRATIONS ---")
        print("{:<5} {:<30} {:<30} {:<12} {:<12}".format(
            "ID", "Volunteer Name", "Event Name", "Event Date", "Registered On"))
        print("-" * 90)
        
        for reg in registrations:
            event_date = reg['EventDate'].strftime("%Y-%m-%d") if reg['EventDate'] else 'N/A'
            reg_date = reg['RegistrationDate'].strftime("%Y-%m-%d") if reg['RegistrationDate'] else 'N/A'
            
            print("{:<5} {:<30} {:<30} {:<12} {:<12}".format(
                reg['ID'],
                reg['VolunteerName'][:28] + '..' if len(reg['VolunteerName']) > 30 else reg['VolunteerName'],
                reg['EventName'][:28] + '..' if len(reg['EventName']) > 30 else reg['EventName'],
                event_date,
                reg_date
            ))
        print("-" * 90)
    
    def display_registration_details(self, registration):
        if not registration:
            print("Registration not found.")
            return
            
        print("\n--- REGISTRATION DETAILS ---")
        print(f"Registration ID: {registration['ID']}")
        print(f"Volunteer: {registration['VolunteerName']} (ID: {registration['VolunteerID']})")
        print(f"Volunteer Email: {registration['VolunteerEmail']}")
        print(f"Event: {registration['EventName']} (ID: {registration['EventID']})")
        print(f"Event Date: {registration['EventDate'].strftime('%Y-%m-%d') if registration['EventDate'] else 'Not set'}")
        print(f"Event Location: {registration['Location'] or 'Not specified'}")
        print(f"Registration Date: {registration['RegistrationDate'].strftime('%Y-%m-%d') if registration['RegistrationDate'] else 'Not recorded'}")
        print("-" * 30)
    
    def display_volunteers_for_event(self, event_name, registrations):
        if not registrations:
            print(f"No volunteers registered for event: {event_name}")
            return

        print(f"\n--- VOLUNTEERS FOR EVENT: {event_name} ---")
        print("{:<5} {:<30} {:<30} {:<12}".format(
            "ID", "Volunteer Name", "Email", "Registered On"))
        print("-" * 80)
        
        for reg in registrations:
            reg_date = reg['RegistrationDate'].strftime("%Y-%m-%d") if reg['RegistrationDate'] else 'N/A'
            
            print("{:<5} {:<30} {:<30} {:<12}".format(
                reg['ID'],
                reg['Name'][:28] + '..' if len(reg['Name']) > 30 else reg['Name'],
                reg['Email'][:28] + '..' if len(reg['Email']) > 30 else reg['Email'],
                reg_date
            ))
        print("-" * 80)
        
    def display_events_for_volunteer(self, volunteer_name, events):
        if not events:
            print(f"No events registered for volunteer: {volunteer_name}")
            return

        print(f"\n--- EVENTS FOR VOLUNTEER: {volunteer_name} ---")
        print("{:<5} {:<30} {:<12} {:<20} {:<12}".format(
            "ID", "Event Name", "Event Date", "Location", "Registered On"))
        print("-" * 85)
        
        for event in events:
            event_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'N/A'
            reg_date = event['RegistrationDate'].strftime("%Y-%m-%d") if event['RegistrationDate'] else 'N/A'
            
            print("{:<5} {:<30} {:<12} {:<20} {:<12}".format(
                event['ID'],
                event['EventName'][:28] + '..' if len(event['EventName']) > 30 else event['EventName'],
                event_date,
                event['Location'][:18] + '..' if event['Location'] and len(event['Location']) > 20 else (event['Location'] or 'N/A'),
                reg_date
            ))
        print("-" * 85)