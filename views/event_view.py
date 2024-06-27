from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

class EventView:

    @classmethod
    def display_events(cls, events, user):
        # Create a table with headers
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white", justify="right")
        table.add_column("Contract ID", style="white")
        table.add_column("Client Infos", style="white")
        table.add_column("Event Start", style="white")
        table.add_column("Event End", style="white")
        table.add_column("Support Contact", style="white")
        table.add_column("Location", style="white")
        table.add_column("Attendees", style="white")
        table.add_column("Notes", style="white")

        # Add event data to the table
        for event in events:
            client_infos = (
                f"Name: {event.contract.client.full_name}, "
                f"Phone: {event.contract.client.telephone}, "
                f"Email: {event.contract.client.email}"
            )

            table.add_row(
                str(event.id),
                str(event.contract.id) if event.contract else "N/A",
                client_infos,
                event.event_start,
                event.event_end,
                (event.support.full_name if event.support else "N/A"),
                event.location,
                str(event.attendees),
                event.notes,
            )
        console.print(table)

        # Display different options based on user role
        if (user.role.code == "man"):
            console.print("1. Display all events without support contact")
            console.print("2. Edit an event")
        elif (user.role.code == "sup"):
            console.print("1. Display events that you are working on")
            console.print("2. Edit an event")
        console.print('Enter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")

        return choice

    @classmethod
    def create_event(cls):
        # Prompt the user to enter event details
        event_name = Prompt.ask("Enter event name")
        event_start = Prompt.ask("Enter event start time (YYYY-MM-DD HH:MM:SS)")
        event_end = Prompt.ask("Enter event end time (YYYY-MM-DD HH:MM:SS)")
        location = Prompt.ask("Enter event location")
        attendees = Prompt.ask("Enter number of attendees")
        notes = Prompt.ask("Enter additional notes (optional)", default="")

        # Store event information
        event_infos = [
            event_name,
            event_start,
            event_end,
            location,
            attendees,
            notes,
        ]

        return event_infos

    @classmethod
    def event_contract_id(cls):
        # Prompt user to enter contract ID
        choice = Prompt.ask("Enter the ID of the contract you want to create an event for")
        return choice

    @classmethod
    def get_event_id(cls):
        # Prompt user to enter event ID
        choice = int(Prompt.ask("Enter the ID of the event you want to edit"))
        return choice

    @classmethod
    def edit_event_view(cls, user):
        console.print("What do you want to edit ?")
        # Display different options based on user role
        if user.role.code == "man":
            console.print("Manager Options :")
            console.print("1. Assign a support contact to an event")
            console.print("2. Change the contract for the event")
        elif user.role.code == "sup":
            console.print("Support Options :")
            console.print("1. Event name")
            console.print("2. Event start")
            console.print("3. Event end")
            console.print("4. Location")
            console.print("5. Number of guests")
            console.print("6.Notes ")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")

        return choice

    @classmethod
    def edit_event_support(cls, users):
        # Create a table to display user options for support contact
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white")
        table.add_column("Full name", style="white")
        table.add_column("Email", style="white")
        table.add_column("Role", style="white")

        for user in users:
            table.add_row(
                str(user.id),
                user.full_name,
                user.email,
                user.role.name,
            )
        console.print(table)
        console.print(
            "1. Enter the ID of the collaborator you want to assign to the event"
        )
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")
        return choice

    @classmethod
    def edit_event_name(cls):
        new_event_name = Prompt.ask("New event name")
        return new_event_name

    @classmethod
    def edit_event_start(cls):
        new_event_start = Prompt.ask("Enter event start time (YYYY-MM-DD HH:MM:SS)")
        return new_event_start

    @classmethod
    def edit_event_end(cls):
        new_event_end = Prompt.ask("Enter event end time (YYYY-MM-DD HH:MM:SS)")
        return new_event_end

    @classmethod
    def edit_event_location(cls):
        new_event_location = Prompt.ask("New event location")
        return new_event_location

    @classmethod
    def edit_event_attendees(cls):
        new_attendees = Prompt.ask("New number of guests")
        return new_attendees

    @classmethod
    def edit_event_notes(cls):
        new_event_notes = Prompt.ask("Edit notes")
        return new_event_notes

    @classmethod
    def edit_event_contract(cls, contracts):
        # Create a table to display contract options for event
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white")
        table.add_column("Client name", style="white")
        table.add_column("Client contact", style="white")
        table.add_column("Commercial contact", style="white")
        table.add_column("Total amount", style="white")
        table.add_column("Amount due", style="white")
        table.add_column("Creation date", style="white")
        table.add_column("Status", style="white")

        for contract in contracts:
            client_infos = (
                f"Phone: {contract.client.telephone}, "
                f"Email: {contract.client.email}"
                if contract.client
                else "N/A"
            )
            status = "Not signed" if contract.status == False else "Signed"

            table.add_row(
                str(contract.id),
                contract.client.full_name,
                client_infos,
                contract.client.commercial.full_name,
                str(contract.total_amount),
                str(contract.left_amount),
                str(contract.creation_date),
                status,
            )
        console.print(table)
        new_event_contract = Prompt.ask("Enter the ID of the contract you want to assign to the event")

        return new_event_contract
