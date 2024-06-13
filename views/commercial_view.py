from rich.console import Console
from rich.prompt import Prompt

console = Console()


class CommercialView:

    @classmethod
    def create_client(cls, user):
        full_name = Prompt.ask("Enter client name")
        email = Prompt.ask("Enter client email")
        telephone = Prompt.ask("Enter client number")
        business_name = Prompt.ask("Enter business name")

        client_infos = [full_name, email, telephone, business_name]

        return client_infos

    @classmethod
    def enter_user_id(cls, user, clients):
        if user.role.code == "com":
            choice = Prompt.ask("Enter the ID of the client you want to edit")
            return choice
        

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
