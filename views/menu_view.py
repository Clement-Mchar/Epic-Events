from rich.console import Console
from rich.prompt import Prompt
from rich.theme import Theme

# Define a custom theme for the console
custom_theme = Theme(
    {
        "error": "bold red",
        "input": "bright_black on white",
        "text": "italic",
        "title": "bold blue",
    }
)

# Initialize the console with the custom theme
console = Console(theme=custom_theme)

class MainView:

    @classmethod
    def display_message(cls, message):
        # Display a message in bold green
        console.print(message, style="bold green")

    @classmethod
    def main_menu_view(cls, user):
        # Display the main menu options based on user role
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

        # Prompt user to select an option
        choice = int(Prompt.ask("\nSelect an option"))
        return choice

    @classmethod
    def return_to_main_menu(cls, message):
        # Confirm returning to the main menu
        confirmation = Prompt.ask(message + " (yes/no)")
        return confirmation.lower() in ["yes", "y"]
