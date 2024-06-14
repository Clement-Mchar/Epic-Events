from views.client_view import ClientView
from views.contract_view import ContractView
from views.menu_view import MainView
from views.user_view import UserView
from models.models import User, Client, Contract
from functools import partial
from sqlalchemy.orm import joinedload

class ClientController:

    @classmethod
    def create_client(cls, user, session):
        from controllers.menus import MenusController

        client_infos = ClientView.create_client(user)
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
                session.rollback()
                MainView.display_message(f"Error creating client : {e}")
        else:
            MainView.display_message(
                "You don't have the permission to create a client."
            )
            return MenusController.main_menu(user, session)

    @classmethod
    def get_clients(cls, user, session):
        from controllers.contract_controller import ContractController
        try:
            if user:
                clients = (
                    session.query(Client)
                    .options(joinedload(Client.commercial))
                    .all()
                )
            if user.role.code == "com":
                cls.clients_management(user, clients, session)
            elif user.role.code == "man":
                ContractController.create_contract(user, clients, session)
        except Exception as e:
            print(f"Error during get_clients: {e}")

    @classmethod
    def clients_management(cls, user, clients, session):
        from controllers.menus import MenusController
        collaborator_options = ClientView.display_clients(clients, user)
        if user.role.code == "com":
            if collaborator_options == "edit" :
                if user.role.code == "com":
                    client_id = UserView.enter_user_id(user, clients)
                    client_to_edit = session.query(Client).get(client_id)
                    if client_to_edit:
                        cls.edit_client(user, client_to_edit, session)
            elif collaborator_options == "menu":
                MenusController.back_to_main_menu(user, session)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
        else:
            session.rollback()
            MainView.display_message("Pick a valid option.")

    @classmethod
    def edit_client(cls, user, client_to_edit, session):
        from controllers.menus import MenusController
        choice = ClientView.edit_client_view(user, client_to_edit)
        try:
            if choice == "1":
                new_name = ClientView.edit_client_name(
                    user, client_to_edit
                )
                client_to_edit.full_name = new_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = ClientView.edit_client_email(
                    user, client_to_edit
                )
                client_to_edit.email = new_email
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "3":
                new_number = ClientView.edit_client_number(
                    user, client_to_edit
                )
                client_to_edit.telephone = new_number
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "4":
                new_business_name = (
                    ClientView.edit_client_business_name(
                        user, client_to_edit
                    )
                )
                client_to_edit.business_name = new_business_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "menu":
                MenusController.back_to_main_menu(user, session)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
        except Exception as e:
            session.rollback()
            MainView.display_message(f"Error editing client: {e}")
    
