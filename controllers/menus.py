from views.menu_view import MenuView
from controllers.manager_options import ManagerOptions
from models.models import User, Client, Contract, Event
from sqlalchemy.orm import joinedload

class MenusController:

    @classmethod
    def main_menu(cls, user, session):
        choice = MenuView.main_menu_view(user)
        try:
            if choice == 1:
                cls.get_clients(user)
            elif choice == 2:
                cls.get_contracts(user)
            elif choice == 3:
                cls.get_events(user)
            if user.role.code == "man":
                if choice == 4:
                    cls.get_users(user, session)
                elif choice == 5:
                    ManagerOptions.create_user(user)
                elif choice == 6:
                    ManagerOptions.create_contract(user)
                """elif user.role.code == "com":
                CommercialOptions.create_client(user)
                CommercialOptions.create_event(user)"""
        except Exception as e:
            print(f"Error during main menu: {e}")

    @classmethod
    def get_clients(cls, user, session):
        clients = (
            session.query(Client)
            .options(joinedload(Client.commercial_contact))
            .all()
        )
        MenuView.display_clients(clients, user)

    @classmethod
    def get_contracts(cls, user, session):
        contracts = (
            session.query(Contract)
            .options(
                joinedload(Contract.client_infos),
                joinedload(Contract.commercial),
            )
            .all()
        )
        MenuView.display_contracts(contracts, user)

    @classmethod
    def get_events(cls, user, session):
        events = (
            session.query(Event)
            .options(
                joinedload(Event.contract),
                joinedload(Event.client),
                joinedload(Event.support_contact),
            )
            .all()
        )
        MenuView.display_events(events, user)

    @classmethod
    def get_users(cls, user, session):
        if user:
            users = session.query(User).options(joinedload(User.role)).all()
        ManagerOptions.user_management(user, users, session)

    @classmethod
    def return_to_main_menu(cls, user):
        MenuView.main_menu_view(user)
