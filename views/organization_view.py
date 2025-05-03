class OrganizationView:
    def display_organizations(self,organizations):
        if not organizations:
            print('No Organizations Found')
            return
        print("\n---ORGANIZATION LIST---")
        print("{:<5} {:<30} {:<30} {:<15}".format("ID", "Name", "Address", "Contact"))
        print("-" * 80)

        for org in organizations:
            print("{:<5} {:<30} {:<30} {:<15}".format(
                org['OrganizationID'],
                org['OrganizationName'][:28] + '..' if len(org['OrganizationName']) > 30 else org['OrganizationName'],
                org['Address'][:28] + '..' if org['Address'] and len(org['Address']) > 30 else (org['Address'] or 'N/A'),
                org['ContactNumber'] or 'N/A'
            ))
        print("-" * 80)


    def display_organization_details(self, organization):
        if not organization:
            print("Organization not found.")
            return
            
        print("\n--- ORGANIZATION DETAILS ---")
        print(f"ID: {organization['OrganizationID']}")
        print(f"Name: {organization['OrganizationName']}")
        print(f"Address: {organization['Address'] or 'Not provided'}")
        print(f"Contact Number: {organization['ContactNumber'] or 'Not provided'}")
        print("-" * 30)
    

    def get_organization_input(self):
        print("\n--- ADD NEW ORGANIZATION ---")
        name = input("Organization Name: ")
        address = input("Address (optional, press Enter to skip): ") or None
        contact = input("Contact Number (optional, press Enter to skip): ") or None
        return name, address, contact