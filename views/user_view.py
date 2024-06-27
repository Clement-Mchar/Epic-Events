from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import getpass

# Initialize the console for rich output
console = Console()

class UserView:

    @classmethod
    def create_user_view(cls):
        # Prompt the user for collaborator details
        full_name = Prompt.ask("Collaborator name ")
        email = Prompt.ask("Collaborator email ")
        password = getpass.getpass("Collaborator password ")
        role_name = Prompt.ask("Collaborator role ")

        user_infos = [full_name, email, password, role_name]
        return user_infos

    @classmethod
    def display_users(cls, users):
        # Display users in a table format
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
        console.print("1. Edit a collaborator account")
        console.print("2. Delete a collaborator account")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")
        return choice

    @classmethod
    def enter_user_id(cls):
        # Prompt for user ID to edit
        choice = Prompt.ask("Enter the ID of the user you want to edit")
        return choice

    @classmethod
    def edit_user_view(cls):
        # Display options to edit user details
        console.print("What do you want to modify ?")
        console.print("1. Name")
        console.print("2. Email")
        console.print("3. Role")
        console.print('\nEnter "menu" to return to the main menu')
        choice = Prompt.ask("\nSelect an option")
        return choice

    @classmethod
    def edit_user_name(cls):
        # Prompt for new user name
        new_name = Prompt.ask("New user name")
        return new_name

    @classmethod
    def edit_user_email(cls):
        # Prompt for new user email
        new_email = Prompt.ask("New user email")
        return new_email

    @classmethod
    def edit_user_role(cls):
        # Prompt for new user role
        new_role = Prompt.ask("New user role")
        return new_role

    @classmethod
    def delete_user_view(cls, message):
        # Confirm user deletion
        confirmation = Prompt.ask(message + " (yes/no)")
        return confirmation.lower() in ["yes", "y"]

    @classmethod
    def delete_user_id(cls):
        # Prompt for user ID to delete
        choice = Prompt.ask("Enter the ID of the user you want to delete")
        return choice
