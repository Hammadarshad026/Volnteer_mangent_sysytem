from models.organization_model import OrganizationModel
from views.organization_view import OrganizationView


class OrganizationController:
    def __init__(self):
        self.model=OrganizationModel()
        self.view=OrganizationView()


    def show_all_organizations(self):
        organizations = self.model.get_all_organizations()
        self.view.display_organizations(organizations)
        return organizations
    

    def show_organization_details(self, org_id):
        organization = self.model.get_organization_by_id(org_id)
        self.view.display_organization_details(organization)
        return organization
    
    
    def add_new_organization(self):
        name, address, contact = self.view.get_organization_input()
        if not name:
            print("Organization name is required.")
            return None
            
        new_org_id = self.model.add_organization(name, address, contact)
        if new_org_id:
            print(f"Organization added successfully with ID: {new_org_id}")
            return new_org_id
        else:
            print("Failed to add organization.")
            return None