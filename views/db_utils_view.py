class DatabaseUtilsView:
    def display_db_utils_menu(self):
        print("\n=== DATABASE UTILITIES MENU ===")
        print("1. Setup All Database Objects (Triggers, Procedures, Views, Functions)")
        print("2. Use RegisterVolunteerForEvent Procedure")
        print("3. Use GetEventStatistics Procedure")
        print("4. View UpcomingEvents View")
        print("5. View VolunteerParticipation View")
        print("6. Use GetVolunteerEventCount Function")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")
        return choice
        
    def display_upcoming_events(self, events):
        if not events:
            print("No upcoming events found.")
            return

        print("\n--- UPCOMING EVENTS ---")
        print("{:<5} {:<30} {:<12} {:<20} {:<10} {:<10}".format(
            "ID", "Event Name", "Date", "Location", "Registered", "Available"))
        print("-" * 90)
        
        for event in events:
            event_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'N/A'
            
            print("{:<5} {:<30} {:<12} {:<20} {:<10} {:<10}".format(
                event['EventID'],
                event['EventName'][:28] + '..' if len(event['EventName']) > 30 else event['EventName'],
                event_date,
                event['Location'][:18] + '..' if event['Location'] and len(event['Location']) > 20 else (event['Location'] or 'N/A'),
                f"{event['RegisteredCount']}/{event['Capacity'] or 'N/A'}",
                event['AvailableSpots'] if event['Capacity'] else 'Unlimited'
            ))
        print("-" * 90)
        
    def display_volunteer_participation(self, volunteers):
        if not volunteers:
            print("No volunteer participation data found.")
            return

        print("\n--- VOLUNTEER PARTICIPATION ---")
        print("{:<5} {:<30} {:<30} {:<12} {:<12}".format(
            "ID", "Volunteer Name", "Email", "Events", "Roles"))
        print("-" * 90)
        
        for vol in volunteers:
            print("{:<5} {:<30} {:<30} {:<12} {:<12}".format(
                vol['VolunteerID'],
                vol['VolunteerName'][:28] + '..' if len(vol['VolunteerName']) > 30 else vol['VolunteerName'],
                vol['Email'][:28] + '..' if len(vol['Email']) > 30 else vol['Email'],
                vol['EventsAttended'],
                vol['RolesHeld']
            ))
        print("-" * 90)
        
    def display_event_statistics(self, summary, top_events):
        if not summary:
            print("No event statistics found.")
            return
            
        # Display summary
        print("\n--- EVENT STATISTICS SUMMARY ---")
        print(f"Total Events: {summary[0]['TotalEvents']}")
        print(f"Total Registrations: {summary[0]['TotalRegistrations'] or 0}")
        print(f"Avg Registrations Per Event: {summary[0]['AvgRegistrationsPerEvent'] or 0:.2f}")
        print(f"Unique Volunteers: {summary[0]['UniqueVolunteers'] or 0}")
        print("-" * 30)
        
        # Display top events
        if top_events:
            print("\n--- TOP EVENTS BY REGISTRATION ---")
            print("{:<5} {:<30} {:<12} {:<10} {:<20}".format(
                "ID", "Event Name", "Date", "Reg. Count", "Organization"))
            print("-" * 80)
            
            for event in top_events:
                event_date = event['EventDate'].strftime("%Y-%m-%d") if event['EventDate'] else 'N/A'
                
                print("{:<5} {:<30} {:<12} {:<10} {:<20}".format(
                    event['EventID'],
                    event['EventName'][:28] + '..' if len(event['EventName']) > 30 else event['EventName'],
                    event_date,
                    event['RegisteredCount'] or 0,
                    event['OrganizationName'][:18] + '..' if event['OrganizationName'] and len(event['OrganizationName']) > 20 else (event['OrganizationName'] or 'N/A')
                ))
            print("-" * 80)