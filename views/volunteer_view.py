class VolunteerView:
    def display_volunteers(self, volunteers):
        if not volunteers:
            print("No volunteers found.")
            return

        print("\n--- VOLUNTEERS LIST ---")
        print("{:<5} {:<30} {:<30} {:<15} {:<15}".format(
            "ID", "Name", "Email", "Phone", "City"))
        print("-" * 95)
        
        for volunteer in volunteers:
            print("{:<5} {:<30} {:<30} {:<15} {:<15}".format(
                volunteer['VolunteerID'],
                volunteer['Name'][:28] + '..' if len(volunteer['Name']) > 30 else volunteer['Name'],
                volunteer['Email'][:28] + '..' if len(volunteer['Email']) > 30 else volunteer['Email'],
                volunteer['Phone'] or 'N/A',
                volunteer['City'] or 'N/A'
            ))
        print("-" * 95)
    
    def display_volunteer_details(self, volunteer):
        if not volunteer:
            print("Volunteer not found.")
            return
            
        print("\n--- VOLUNTEER DETAILS ---")
        print(f"ID: {volunteer['VolunteerID']}")
        print(f"Name: {volunteer['Name']}")
        print(f"Email: {volunteer['Email']}")
        print(f"Phone: {volunteer['Phone'] or 'Not provided'}")
        print(f"City: {volunteer['City'] or 'Not provided'}")
        print("-" * 30)
    
    def get_volunteer_input(self):
        print("\n--- ADD NEW VOLUNTEER ---")
        name = input("Volunteer Name: ")
        email = input("Email: ")
        phone = input("Phone (optional, press Enter to skip): ") or None
        city = input("City (optional, press Enter to skip): ") or None
        return name, email, phone, city