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


class MainView:

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
    def return_to_main_menu(cls, message, user):
        confirmation = Prompt.ask(message + " (yes/no)")
        return confirmation.lower() in ["yes", "y"]
