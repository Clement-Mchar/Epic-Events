from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.theme import Theme
from rich.table import Table

custom_theme = Theme(
    {
        "error": "bold red",
        "input": "bright_black on white",
        "text": "italic",
        "title": "bold blue",
    }
)

console = Console(theme=custom_theme)


class MenuView:

    @classmethod
    def display_message(cls, message):
        console.print(message, style="bold green")

    @classmethod
    def main_menu_view(cls, user):
        console.print("Main Menu", style="title")
        console.print("1. Display clients list")
        console.print("2. Display contracts list")
        console.print("3. Display events list")
        if user.role.code == "man":
            console.print("4. Display collaborator's list")
            console.print("5. Create a new collaborator account")
            console.print("6. Create a new contract")
        if user.role.code == "com":
            console.print("4. Create a new client")
            console.print("5. Create an event")

        choice = int(Prompt.ask("\nSelect an option"))
        return choice

    @classmethod
    def display_clients(cls, clients, user):
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white", justify="right")
        table.add_column("Name", style="white")
        table.add_column("Email", style="white")
        table.add_column("Telephone", style="white")
        table.add_column("Business name", style="white")
        table.add_column("Creation date", style="white")
        table.add_column("Last contact")
        table.add_column("Commercial contact")
        print("test")
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

    @classmethod
    def display_contracts(cls, contracts, user):
        table = Table(show_header=True, header_style="cyan")
        table.add_column("ID", style="white")
        table.add_column("Client infos", style="white")
        table.add_column("Commercial contact", style="white")
        table.add_column("Total amount", style="white")
        table.add_column("Amount due", style="white")
        table.add_column("Creation date", style="white")
        table.add_column("Status", style="white")

        for contract in contracts:
            client_infos = (
                f"Name: {contract.client_infos.full_name}, "
                f"Phone: {contract.client_infos.telephone}, "
                f"Email: {contract.client_infos.email}"
                if contract.client_infos
                else "N/A"
            )

            table.add_row(
                str(contract["ID"]),
                client_infos,
                contract.commercial.full_name,
                str(contract.total_amount),
                str(contract.left_amount),
                contract.creation_date,
                contract.status,
            )
        console.print(table)

        if user.role.code == "man":
            console.print("1. Edit contract infos")
            choice = int(Prompt.ask("\nSelect an option"))
        if user.role.code == "com":
            console.print("1. Display all contracts that you are in charge of")
            console.print("2. Display all contracts that are not paid yet")
            console.print("3. Display all contracts that are not signed yet")
            choice = int(Prompt.ask("\nSelect an option"))

        return choice

    @classmethod
    def display_events(events, user):
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

        for event in events:
            client_infos = (
                f"Name: {event.client.full_name}, "
                f"Phone: {event.client.telephone}, "
                f"Email: {event.client.email}"
                if event.client
                else "N/A"
            )

            table.add_row(
                str(event.id),
                str(event.contract.id) if event.contract else "N/A",
                client_infos,
                event.event_start,
                event.event_end,
                (
                    event.support_contact.full_name
                    if event.support_contact
                    else "N/A"
                ),
                event.location,
                str(event.attendees),
                event.notes,
            )
        console.print(table)

        if user.role.code == "man":
            console.print("1. Display all events without support contact")
            console.print("2. Edit an event")
            choice = int(Prompt.ask("\nSelect an option"))
        if user.role.code == "sup":
            console.print("1. Display events that you are working on")
            console.print("2. Edit an event")
            choice = int(Prompt.ask("\nSelect an option"))

        return choice
