from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

custom_theme = Theme({
    "error": "bold red",
    "input": "bright_black on white",
    "text": "bold blue"
})

console = Console(theme=custom_theme)

class LoginView:

    @classmethod
    def login_view(cls):
        while True:
            console.print(Text("User Login", justify="center"), style="bold blue")

            email = Prompt.ask("Enter your email")
            password = Prompt.ask("Enter your password", password=True)

            login_infos = [email, password]
            if not email :
                console.print("Please enter your email to continue.")
                continue
            elif not password :
                console.print("Please enter your password to continue.")
                continue

            return login_infos
