from views.commercial_view import CommercialView
from views.menu_view import MenuView
from models.models import User, Client


class CommercialOptions:

    @classmethod
    def create_client(cls, user, session):
        from controllers.menus import MenusController

        client_infos = CommercialView.create_client(user)
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
                MenuView.display_message(
                    f"Client created with id: {new_client.id}"
                )
            except Exception as e:
                session.rollback()
                MenuView.display_message(f"Error creating client : {e}")
        else:
            MenuView.display_message(
                "You don't have the permission to create a client."
            )
            return MenusController.main_menu(user, session)

    @classmethod
    def create_event(cls, user, session):
        pass

    @classmethod
    def clients_management(cls, user, clients, session):
        from controllers.menus import MenusController
        collaborator_options = MenuView.display_clients(clients, user)
        if collaborator_options == "1" :
            if user.role.code == "com":
                client_id = CommercialView.enter_user_id(user, clients)
                client_to_edit = session.query(Client).get(client_id)
                if client_to_edit:
                    cls.edit_client(user, client_to_edit, session)
        elif collaborator_options == "menu":
            MenusController.back_to_main_menu(user, session)
        else:
            session.rollback()
            MenuView.display_message("Pick a valid option.")

    @classmethod
    def edit_client(cls, user, client_to_edit, session):
        from controllers.menus import MenusController
        choice = CommercialView.edit_client_view(user, client_to_edit)
        try:
            if choice == "1":
                new_name = CommercialView.edit_client_name(
                    user, client_to_edit
                )
                client_to_edit.full_name = new_name
                session.commit()
                MenuView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = CommercialView.edit_client_email(
                    user, client_to_edit
                )
                client_to_edit.email = new_email
                session.commit()
                MenuView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "3":
                new_number = CommercialView.edit_client_number(
                    user, client_to_edit
                )
                client_to_edit.telephone = new_number
                session.commit()
                MenuView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "4":
                new_business_name = (
                    CommercialView.edit_client_business_name(
                        user, client_to_edit
                    )
                )
                client_to_edit.business_name = new_business_name
                session.commit()
                MenuView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "menu":
                MenusController.back_to_main_menu(user, session)
            else:
                session.rollback()
                MenuView.display_message("Pick a valid option.")
        except Exception as e:
            session.rollback()
            MenuView.display_message(f"Error editing client: {e}")
