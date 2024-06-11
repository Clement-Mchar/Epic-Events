from rich.console import Console
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
        title = "Manager Menu"
        options = [
            "1: Create a new collaborator profile"
        ]
        menu_panel = Panel.fit("\n".join(options), title=title, border_style="blue", padding=(1, 2))
        console.print(menu_panel)

        choice = int(console.input("\nSelect an option: "))
        return choice
