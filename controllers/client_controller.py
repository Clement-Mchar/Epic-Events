from views.client_view import ClientView
from views.menu_view import MainView
from models.models import Client
from functools import partial
from sqlalchemy.orm import joinedload


class ClientController:

    @classmethod
    def create_client(cls, user, session):
        from controllers.menus import MenusController

        client_infos = ClientView.create_client()
        full_name, email, telephone, business_name = client_infos
        if user.role.code == "com":
            try:
                new_client = Client(
                    full_name=full_name,
                    email=email,
                    telephone=telephone,
                    business_name=business_name,
                    commercial_contact=user.id,
                )
                session.add(new_client)
                session.commit()
                MainView.display_message(
                    f"Client created with id: {new_client.id}"
                )
            except Exception as e:
                MainView.display_message(f"Error creating client : {e}")
                callback = partial(cls.create_client, user, session)
                MenusController.back_to_main_menu(user, session, callback)
        else:
            MainView.display_message(
                "You don't have the permission to create a client."
            )
            return MenusController.main_menu(user, session)

    @classmethod
    def get_clients(cls, user, session):
        try:
            if user:
                clients = (
                    session.query(Client)
                    .options(joinedload(Client.commercial))
                    .all()
                )
                cls.clients_permissions(user, clients, session)
        except Exception as e:
            print(f"Error during get_clients: {e}")

    @classmethod
    def clients_permissions(cls, user, clients, session):
        from controllers.menus import MenusController
        from controllers.contract_controller import ContractController

        choice = ClientView.display_clients(clients, user)
        if user.role.code == "com":
                client_to_edit = session.query(Client).get(choice)
                if client_to_edit:
                    cls.edit_client(user, client_to_edit, session)
                else:
                    MainView.display_message("No client found.")
                    cls.clients_permissions(user, clients, session)
        elif user.role.code == "man":
            ContractController.create_contract(user, clients, choice, session)

        if choice == "menu":
            callback = partial(
                cls.clients_permissions, user, clients, session
            )
            MenusController.back_to_main_menu(user, session, callback)
        else:
            MainView.display_message("Pick a valid option.")
            cls.clients_permissions(user, clients, session)

    @classmethod
    def edit_client(cls, user, client_to_edit, session):
        from controllers.menus import MenusController

        choice = ClientView.edit_client_view()
        try:
            if choice == "1":
                new_name = ClientView.edit_client_name()
                client_to_edit.full_name = new_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = ClientView.edit_client_email()
                client_to_edit.email = new_email
            elif choice == "3":
                new_number = ClientView.edit_client_number()
                client_to_edit.telephone = new_number
            elif choice == "4":
                new_business_name = ClientView.edit_client_business_name()
                client_to_edit.business_name = new_business_name

            session.commit()
            MainView.display_message("Updated successfully.")
            MenusController.main_menu(user, session)

            if choice == "menu":
                callback = partial(
                    cls.edit_client, user, client_to_edit, session
                )
                MenusController.back_to_main_menu(user, session, callback)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
                cls.edit_client(user, client_to_edit, session)
        except Exception as e:
            session.rollback()
            MainView.display_message("Please enter a valid ID.")
            cls.edit_client(user, client_to_edit, session)
