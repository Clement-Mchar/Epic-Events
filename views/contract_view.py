from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class ContractView:

    @classmethod
    def display_user_contracts(cls, contracts):
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

    @classmethod
    def edit_contract_view(cls):
        console.print("What do you want to modify ?")
        console.print("1. Total amount")
        console.print("2. Amount due")
        console.print("3. Status")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")

        return choice

    @classmethod
    def edit_contract_total_amount(cls):
        new_total_amount = Prompt.ask("New total amount")
        return new_total_amount

    @classmethod
    def edit_contract_amount_due(cls):
        new_amount_due = Prompt.ask("New amount due")
        return new_amount_due

    @classmethod
    def edit_contract_status(cls):
        new_status = Prompt.ask("Contract signed (yes/no)")
        return new_status

    @classmethod
    def enter_contract_id(cls):
        choice = Prompt.ask("Enter the ID of the contract you want to edit")
        return choice

    @classmethod
    def display_contracts(cls, contracts, user):
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

        if user.role.code == "man":
            console.print("1. Edit a contract infos")
        if user.role.code == "com":
            console.print("1. Edit a contract infos")
            console.print("2. Display all contracts that you are in charge of")
            console.print("3. Display all contracts that are not paid yet")
            console.print("4. Display all contracts that are not signed yet")
            console.print("5. Create an event")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")
        return choice

    @classmethod
    def create_contract_view(cls):
        total_amount = Prompt.ask("Prix du contrat")
        return total_amount
