from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import getpass

console = Console()


class ManagerView:

    @classmethod
    def create_user_view(cls, user):
        full_name = Prompt.ask("Collaborator name ")
        email = Prompt.ask("Collaborator email ")
        password = getpass.getpass("Collaborator password ")
        role_name = Prompt.ask("Collaborator role ")

        user_infos = [full_name, email, password, role_name]

        return user_infos

    @classmethod
    def display_users(cls, user, users):
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
        choice = int(Prompt.ask("\nSelect an option: "))
        return choice

    @classmethod
    def enter_user_id(cls, user, users):
        choice = Prompt.ask(
            "Enter the ID of the user you want to edit/delete : "
        )
        return choice

    @classmethod
    def edit_user_view(cls, user, user_to_manage):
        print("What do you want to modify ?")
        print("1. Name")
        print("2. Email")
        print("3. Role")
        choice = int(Prompt.ask("\nSelect an option: "))

        return choice

    @classmethod
    def edit_user_name(cls, user, user_to_manage):
        new_name = Prompt.ask("New user name :")
        return new_name

    @classmethod
    def edit_user_email(cls, user, user_to_manage):
        new_email = str(Prompt.ask("New user email :"))
        return new_email

    @classmethod
    def edit_user_role(cls, user, user_to_manage):
        new_role = Prompt.ask("New user role :")
        return new_role

    @classmethod
    def delete_user_view(cls, message, user, user_to_manage):
        confirmation = Prompt.ask(message + " (yes/no)")
        return confirmation.lower() in ["yes", "y"]
