from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
console = Console()


class ClientView:

    @classmethod
    def create_client(cls, user):
        full_name = Prompt.ask("Enter client name")
        email = Prompt.ask("Enter client email")
        telephone = Prompt.ask("Enter client number")
        business_name = Prompt.ask("Enter business name")

        client_infos = [full_name, email, telephone, business_name]

        return client_infos


    @classmethod
    def edit_client_view(cls, user, client_to_edit):
        console.print("What do you want to modify ?")
        console.print("1. Name")
        console.print("2. Email")
        console.print("3. Telephone")
        console.print("4. Business name")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")

        return choice

    @classmethod
    def edit_client_name(cls, user, client_to_edit):
        new_name = Prompt.ask("New client name")
        return new_name

    @classmethod
    def edit_client_email(cls, user, client_to_edit):
        new_email = str(Prompt.ask("New client email"))
        return new_email

    @classmethod
    def edit_client_number(cls, user, client_to_edit):
        new_number = Prompt.ask("New client number")
        return new_number

    @classmethod
    def edit_client_business_name(cls, user, client_to_edit):
        new_business_name = Prompt.ask("New client business name")
        return new_business_name

    @classmethod
    def display_clients(cls, clients, user):
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white", justify="right")
        table.add_column("Name", style="white")
        table.add_column("Email", style="white")
        table.add_column("Telephone", style="white")
        table.add_column("Business name", style="white")
        table.add_column("Creation date", style="white")
        table.add_column("Last update")
        table.add_column("Commercial contact")

        for client in clients:
            table.add_row(
                str(client.id),
                client.full_name,
                client.email,
                str(client.telephone),
                client.business_name,
                str(client.creation_date),
                str(client.last_update),
                client.commercial.full_name,
            )

        console.print(table)
        if user.role.code == "com":
            console.print('1. Enter "edit" to edit a client infos')
        elif user.role.code == "man":
            console.print("Enter the ID of a client to create a contract")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\n")
        return choice

    @classmethod
    def create_event(cls):
        event_name = Prompt.ask("Enter event name")
        event_start = Prompt.ask("Enter event start time (YYYY-MM-DD HH:MM:SS)")
        event_end = Prompt.ask("Enter event end time (YYYY-MM-DD HH:MM:SS)")
        location = Prompt.ask("Enter event location")
        attendees = Prompt.ask("Enter number of attendees")
        notes = Prompt.ask("Enter additional notes (optional)", default="")

        event_infos = [
            event_name,
            event_start,
            event_end,
            location,
            attendees,
            notes
        ]

        return event_infos