from models.event_model import EventModel
from models.organization_model import OrganizationModel
from views.event_view import EventView

class EventController:
    def __init__(self):
        self.model = EventModel()
        self.org_model = OrganizationModel()
        self.view = EventView()
    
    def show_all_events(self):
        events = self.model.get_all_events()
        self.view.display_events(events)
        return events
    
    def show_event_details(self, event_id):
        event = self.model.get_event_by_id(event_id)
        self.view.display_event_details(event)
        return event
    
    def add_new_event(self):
        # Get all organizations for selection
        organizations = self.org_model.get_all_organizations()
        if not organizations:
            print("No organizations found. Please add an organization first.")
            return None
        
        org_id, event_name, event_date, location, capacity = self.view.get_event_input(organizations)
        
        if not event_name:
            print("Event name is required.")
            return None
            
        new_event_id = self.model.add_event(org_id, event_name, event_date, location, capacity)
        if new_event_id:
            print(f"Event added successfully with ID: {new_event_id}")
            return new_event_id
        else:
            print("Failed to add event.")
            return None
            
    def show_events_by_organization(self, org_id):
        # First verify organization exists
        organization = self.org_model.get_organization_by_id(org_id)
        if not organization:
            print(f"Organization with ID {org_id} not found.")
            return []
            
        events = self.model.get_events_by_organization(org_id)
        print(f"\nEvents for {organization['OrganizationName']}:")
        self.view.display_events(events)
        return events
        
    def update_event(self, event_id):
        event = self.model.get_event_by_id(event_id)
        if not event:
            print(f"Event with ID {event_id} not found.")
            return False
            
        # Display current event details
        self.view.display_event_details(event)
        
        # Get updated information
        event_name, event_date, location, capacity = self.view.get_event_update_input(event)
        
        # Update the event
        success = self.model.update_event(event_id, event_name, event_date, location, capacity)
        if success:
            print("Event updated successfully!")
        else:
            print("Failed to update event.")
        return success