from models.volunteer_model import VolunteerModel
from views.volunteer_view import VolunteerView

class VolunteerController:
    def __init__(self):
        self.model = VolunteerModel()
        self.view = VolunteerView()
    
    def show_all_volunteers(self):
        volunteers = self.model.get_all_volunteers()
        self.view.display_volunteers(volunteers)
        return volunteers
    
    def show_volunteer_details(self, volunteer_id):
        volunteer = self.model.get_volunteer_by_id(volunteer_id)
        self.view.display_volunteer_details(volunteer)
        return volunteer
    
    def add_new_volunteer(self):
        name, email, phone, city = self.view.get_volunteer_input()
        
        if not name or not email:
            print("Volunteer name and email are required.")
            return None
            
        new_volunteer_id = self.model.add_volunteer(name, email, phone, city)
        if new_volunteer_id:
            print(f"Volunteer added successfully with ID: {new_volunteer_id}")
            return new_volunteer_id
        else:
            print("Failed to add volunteer.")
            return None
            
    def search_volunteers(self):
        search_term = input("Enter search term (name, email, or city): ")
        if not search_term:
            print("Search term cannot be empty.")
            return []
            
        volunteers = self.model.search_volunteers(search_term)
        self.view.display_volunteers(volunteers)
        return volunteers