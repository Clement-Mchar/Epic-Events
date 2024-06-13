from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
import getpass

console = Console()

class CommercialView:

    @classmethod
    def create_client(cls, user):
        full_name = Prompt.ask('Enter client name')
        email = Prompt.ask('Enter client email')
        telephone = Prompt.ask('Enter client number')
        business_name = Prompt.ask('Enter business name')
        
        client_infos = [full_name, email, telephone, business_name]

        return client_infos