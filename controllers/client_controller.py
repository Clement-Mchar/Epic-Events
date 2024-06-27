from views.client_view import ClientView
from views.menu_view import MainView
from views.user_view import UserView
from models.models import Client, User, Role
from functools import partial
from sqlalchemy.orm import joinedload
import sentry_sdk


class ClientController:

    @classmethod
    def create_client(cls, user, session):
        from controllers.menus import MenusController

        try:
            # Prompt user for client information
            client_infos = ClientView.create_client()
            full_name, email, telephone, business_name = client_infos

            # Check user's role and create client if allowed
            if user.role.code == "com":
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
                MenusController.main_menu(user, session)
            else:
                MainView.display_message(
                    "You don't have the permission to create a client."
                )
                MenusController.main_menu(user, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error creating client : {e}")
            callback = partial(cls.create_client, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def get_clients(cls, user, session):
        from controllers.menus import MenusController

        try:
            # Retrieve all clients from the database
            clients = (
                session.query(Client)
                .options(joinedload(Client.commercial))
                .all()
            )

            # Process client permissions based on user's role
            cls.clients_permissions(user, clients, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error getting clients : {e}")
            callback = partial(cls.get_clients, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def clients_permissions(cls, user, clients, session):
        from controllers.menus import MenusController
        from controllers.contract_controller import ContractController

        try:
            # Display clients and handle user's choice
            choice = ClientView.display_clients(clients, user)

            if user.role.code == "com":
                # Edit client if choice is a valid client ID
                client_to_edit = session.query(Client).get(choice)
                if client_to_edit:
                    cls.edit_client(user, client_to_edit, session)
                else:
                    MainView.display_message("No client found.")
                    cls.clients_permissions(user, clients, session)

            elif user.role.code == "man":
                # Create contract for selected client
                ContractController.create_contract(
                    user, clients, choice, session
                )

            # Handle menu option or invalid choice
            if choice == "menu":
                callback = partial(
                    cls.clients_permissions, user, clients, session
                )
                MenusController.back_to_main_menu(user, session, callback)
            else:
                cls.clients_permissions(user, clients, session)

        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(
                f"Error getting clients permissions : {e}"
            )
            callback = partial(cls.edit_client, user, clients, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def edit_client(cls, user, client_to_edit, session):
        from controllers.menus import MenusController

        try:
            # Display options for editing client information
            choice = ClientView.edit_client_view()

            # Update client information based on user's choice
            if choice == "1":
                new_name = ClientView.edit_client_name()
                client_to_edit.full_name = new_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = ClientView.edit_client_email()
                client_to_edit.email = new_email
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "3":
                new_number = ClientView.edit_client_number()
                client_to_edit.telephone = new_number
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "4":
                new_business_name = ClientView.edit_client_business_name()
                client_to_edit.business_name = new_business_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "5":
                users = (
                    session.query(User)
                    .join(Role)
                    .filter(Role.code == "com")
                    .options(joinedload(User.role)
                ).all())
                UserView.display_users(users)
                new_commercial_contact_id = (
                    ClientView.edit_client_commercial_contact()
                )
                new_commercial_contact = (
                    session.query(User)
                    .filter(User.id == new_commercial_contact_id)
                )
                if new_commercial_contact:
                    client_to_edit.commercial_contact = new_commercial_contact
                    session.commit()
                    MainView.display_message("Updated successfully.")
                    MenusController.main_menu(user, session)
                else:
                    MainView.display_message("No commercial found.")

            # Handle menu option or invalid choice
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
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error editing client : {e}.")
            callback = partial(cls.edit_client, user, client_to_edit, session)
            MenusController.back_to_main_menu(user, session, callback)
