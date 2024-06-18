from views.menu_view import MainView
from controllers.client_controller import ClientController
from controllers.contract_controller import ContractController
from controllers.event_controller import EventController
from controllers.user_controller import UserController


class MenusController:

    @classmethod
    def main_menu(cls, user, session):
        choice = MainView.main_menu_view(user)
        try:
            if choice == 1:
                ClientController.get_clients(user, session)
            elif choice == 2:
                ContractController.get_contracts(user, session)
            elif choice == 3:
                EventController.get_events(user, session)
            if user.role.code == "man":
                if choice == 4:
                    UserController.get_users(user, session)
                elif choice == 5:
                    UserController.create_user(user, session)
                elif choice == 6:
                    ClientController.get_clients(user, session)
                else:
                    session.rollback()
                    MainView.display_message("Pick a valid option.")
                    cls.main_menu(user, session)
            elif user.role.code == "com":
                if choice == 4:
                    ClientController.create_client(user, session)
                elif choice == 5:
                    EventController.create_event(user, session)
                else:
                    session.rollback()
                    MainView.display_message("Pick a valid option.")
                    cls.main_menu(user, session)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
                cls.main_menu(user, session)
        except Exception as e:
            print(f"Error during main menu: {e}")

    @classmethod
    def back_to_main_menu(cls, user, session, current_controller_callback):
        confirmation = MainView.return_to_main_menu(
            "Do you want to go back to the main menu ?", user
        )
        if confirmation:
            cls.main_menu(
                user,
                session,
            )
        else:
            MainView.display_message("Staying in the current view.")
            current_controller_callback()
