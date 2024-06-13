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
                    commercial_contact=user.id
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