from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme
import getpass

# Define a custom theme for the console
custom_theme = Theme(
    {
        "error": "bold red",
        "input": "bright_black on white",
        "text": "bold blue",
    }
)

# Initialize the console with the custom theme
console = Console(theme=custom_theme)

class LoginView:

    @classmethod
    def login_view(cls):
        while True:
            # Display the login title
            console.print(
                Text("User Login", justify="center"), style="bold blue"
            )

            # Prompt the user to enter email and password
            email = Prompt.ask("Enter your email")
            password = getpass.getpass("Enter your password : ")

            # Store login information
            login_infos = [email, password]
            
            # Validate email input
            if not email:
                console.print("Please enter your email to continue.")
                continue
            # Validate password input
            elif not password:
                console.print("Please enter your password to continue.")
                continue

            # Return login information
            return login_infos
