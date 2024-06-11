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

class MenuView:

    @classmethod
    def manager_menu_view(cls, user):
        console.print(Text("Manager Menu", justify="left"), style="bold blue")
        console.print(Text(f"Hello, {user.full_name}.", justify="center"), style="blue")
        console.print(Text(f"Select an option :", justify="center"), style="bold")

