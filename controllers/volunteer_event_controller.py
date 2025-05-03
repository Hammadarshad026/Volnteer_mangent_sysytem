from models.volunteer_event_model import VolunteerEventModel
from models.volunteer_model import VolunteerModel
from models.event_model import EventModel
from views.volunteer_event_view import VolunteerEventView
from views.volunteer_view import VolunteerView
from views.event_view import EventView
from datetime import datetime

class VolunteerEventController:
    def __init__(self):
        self.model = VolunteerEventModel()
        self.volunteer_model = VolunteerModel()
        self.event_model = EventModel()
        self.view = VolunteerEventView()
        self.volunteer_view = VolunteerView()
        self.event_view = EventView()
    
    def show_all_registrations(self):
        registrations = self.model.get_all_registrations()
        self.view.display_registrations(registrations)
        return registrations
    
    def show_registration_details(self, registration_id):
        registration = self.model.get_registration_by_id(registration_id)
        self.view.display_registration_details(registration)
        return registration
    
    def register_volunteer_for_event(self):
        # Show available volunteers
        print("\n=== AVAILABLE VOLUNTEERS ===")
        volunteers = self.volunteer_model.get_all_volunteers()
        if not volunteers:
            print("No volunteers found. Please add a volunteer first.")
            return None
        self.volunteer_view.display_volunteers(volunteers)
        
        # Get volunteer selection
        volunteer_id = input("\nEnter Volunteer ID: ")
        if not volunteer_id.isdigit():
            print("Invalid Volunteer ID.")
            return None
        volunteer_id = int(volunteer_id)
        
        # Check if volunteer exists
        volunteer = self.volunteer_model.get_volunteer_by_id(volunteer_id)
        if not volunteer:
            print(f"No volunteer found with ID {volunteer_id}.")
            return None
        
        # Show available events
        print("\n=== AVAILABLE EVENTS ===")
        events = self.event_model.get_all_events()
        if not events:
            print("No events found. Please add an event first.")
            return None
        self.event_view.display_events(events)
        
        # Get event selection
        event_id = input("\nEnter Event ID: ")
        if not event_id.isdigit():
            print("Invalid Event ID.")
            return None
        event_id = int(event_id)
        
        # Check if event exists
        event = self.event_model.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID {event_id}.")
            return None
            
        # Register volunteer
        registration_id = self.model.register_volunteer_for_event(volunteer_id, event_id)
        if registration_id:
            print(f"Volunteer successfully registered for event! Registration ID: {registration_id}")
        else:
            print("Failed to register volunteer for event.")
        return registration_id
    
    def show_volunteers_for_event(self):
        # Show available events
        print("\n=== AVAILABLE EVENTS ===")
        events = self.event_model.get_all_events()
        if not events:
            print("No events found.")
            return []
        self.event_view.display_events(events)
        
        # Get event selection
        event_id = input("\nEnter Event ID: ")
        if not event_id.isdigit():
            print("Invalid Event ID.")
            return []
        event_id = int(event_id)
        
        # Check if event exists
        event = self.event_model.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID {event_id}.")
            return []
            
        # Get and display volunteers for this event
        registrations = self.model.get_registrations_for_event(event_id)
        self.view.display_volunteers_for_event(event['EventName'], registrations)
        return registrations
    
    def show_events_for_volunteer(self):
        # Show available volunteers
        print("\n=== AVAILABLE VOLUNTEERS ===")
        volunteers = self.volunteer_model.get_all_volunteers()
        if not volunteers:
            print("No volunteers found.")
            return []
        self.volunteer_view.display_volunteers(volunteers)
        
        # Get volunteer selection
        volunteer_id = input("\nEnter Volunteer ID: ")
        if not volunteer_id.isdigit():
            print("Invalid Volunteer ID.")
            return []
        volunteer_id = int(volunteer_id)
        
        # Check if volunteer exists
        volunteer = self.volunteer_model.get_volunteer_by_id(volunteer_id)
        if not volunteer:
            print(f"No volunteer found with ID {volunteer_id}.")
            return []
            
        # Get and display events for this volunteer
        events = self.model.get_events_for_volunteer(volunteer_id)
        self.view.display_events_for_volunteer(volunteer['Name'], events)
        return events
    
    def cancel_volunteer_registration(self):
        # First show all registrations
        registrations = self.model.get_all_registrations()
        if not registrations:
            print("No registrations found.")
            return False
        self.view.display_registrations(registrations)
        
        # Get registration to cancel
        reg_id = input("\nEnter Registration ID to cancel: ")
        if not reg_id.isdigit():
            print("Invalid Registration ID.")
            return False
        reg_id = int(reg_id)
        
        # Confirm before cancelling
        confirm = input(f"Are you sure you want to cancel registration {reg_id}? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Cancellation aborted.")
            return False
        
        # Cancel the registration
        success = self.model.cancel_registration(reg_id)
        if success:
            print("Registration successfully canceled.")
        else:
            print("Failed to cancel registration.")
        return success