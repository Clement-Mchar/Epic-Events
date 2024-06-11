from views.menu_view import MenuView
from controllers.manager_options import ManagerOptions

class MenusController:

    @classmethod
    def manager_menu(cls, user):
        choice = MenuView.manager_menu_view(user)

        if choice == 1:
            ManagerOptions.create_user(user)