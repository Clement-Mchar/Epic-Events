from rich.console import Console
from rich.prompt import Prompt
import getpass

console = Console()

class ManagerView:

    @classmethod
    def create_user_view(cls, user):
        full_name = Prompt.ask("Collaborator name ")
        email = Prompt.ask("Collaborator email ")
        password = getpass.getpass("Collaborator password ")
        role_name = Prompt.ask("Collaborator role ")

        user_infos = [full_name, email, password,role_name]

        return user_infos
