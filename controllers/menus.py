from views.menu_view import MenuView

class MenusController:

    @classmethod
    def manager_menu(cls, user):
        choice = MenuView.manager_menu_view(user)