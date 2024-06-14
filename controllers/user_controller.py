from functools import partial
from models.models import User, Role, Client, Contract
from views.user_view import UserView
from views.login_view import LoginView
from views.menu_view import MainView
from sqlalchemy.orm import joinedload

class UserController:

    @classmethod
    def create_user(cls, user, session):
        from controllers.menus import MenusController
        user_infos = UserView.create_user_view(user)
        full_name, email, password, role_name = user_infos
        role = session.query(Role).filter(Role.code == role_name).one()
        if user.role.code == "man":
            try:
                new_user = User(
                    full_name=full_name,
                    email=email,
                    password=password,
                    role_id=role.id,
                )
                session.add(new_user)
                session.commit()
                MainView.display_message(
                    f"User created with id: {new_user.id}"
                )
            except Exception as e:
                session.rollback()
                MainView.display_message(f"Error creating user : {e}")
        else:
            MainView.display_message(
                "You don't have the permission to create an user."
            )
            callback = partial(cls.create_user, user, session)
            MenusController.back_to_main_menu(user, session, callback)


    @classmethod
    def get_users(cls, user, session):
        if user:
            users = session.query(User).options(joinedload(User.role)).all()
        cls.user_management(user, users, session)

    @classmethod
    def user_management(cls, user, users, session):
        from controllers.menus import MenusController
        choice = UserView.display_users(user, users)
        try:
            if choice == "1" or choice == "2":
                if choice == "1":
                    user_id = UserView.enter_user_id(user, users)
                    user_to_manage = session.query(User).get(user_id)
                    if user_to_manage:
                        cls.edit_user(user, user_to_manage, session)
                    else:
                        session.rollback()
                        MainView.display_message(
                            "Pick a valid collaborator id."
                        )
                elif choice == "2":
                    user_id = UserView.enter_user_id(user, users)
                    user_to_manage = session.query(User).get(user_id)
                    if user_to_manage:
                        cls.delete_user(user, user_to_manage, session)
                    else:
                        session.rollback()
                        MainView.display_message(
                            "Collaborator not found. Pick a valid user id."
                        )
            elif choice == "menu":
                callback = partial(cls.user_management, user, users, session)
                MenusController.back_to_main_menu(user, session, callback)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
                callback = partial(cls.user_management, user, users, session)
                MenusController.back_to_main_menu(user, session, callback)
        except Exception as e:
            session.rollback()
            MainView.display_message(f"Error in user management: {e}")

    @classmethod
    def edit_user(cls, user, user_to_manage, session):
        from controllers.menus import MenusController

        choice = UserView.edit_user_view(user, user_to_manage)
        try:
            if choice == "1":
                new_name = UserView.edit_user_name(user, user_to_manage)
                user_to_manage.full_name = new_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = UserView.edit_user_email(user, user_to_manage)
                user_to_manage.email = new_email
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "3":
                new_role_name = UserView.edit_user_role(
                    user, user_to_manage
                )
                new_role = (
                    session.query(Role)
                    .filter(Role.name == new_role_name)
                    .one()
                )
                user_to_manage.role = new_role
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "menu":
                callback = partial(cls.edit_user, user, user_to_manage, session)
                MenusController.back_to_main_menu(user, session, callback)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
        except Exception as e:
            session.rollback()
            MainView.display_message(f"Error editing user: {e}")

    @classmethod
    def delete_user(cls, user, user_to_manage, session):
        from controllers.menus import MenusController

        confirmation = UserView.delete_user_view(
            "Are you sure you want to delete user with id"
            f" {user_to_manage.id}?",
            user,
        )
        if confirmation:
            try:
                session.delete(user_to_manage)
                session.commit()
                MainView.display_message(
                    f"User with id {user_to_manage.id} deleted successfully."
                )
                MenusController.main_menu(user, session)
            except Exception as e:
                session.rollback()
                MainView.display_message(f"Error deleting user: {e}")
                cls.delete_user(user, user_to_manage, session)
        else:
            MainView.display_message("User deletion canceled.")
            MenusController.main_menu(user, session)

