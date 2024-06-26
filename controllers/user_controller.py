from functools import partial
from models.models import User, Role
from views.user_view import UserView
from views.menu_view import MainView
from sqlalchemy.orm import joinedload
import sentry_sdk


class UserController:

    @classmethod
    def create_user(cls, user, session):
        from controllers.menus import MenusController

        try:
            user_infos = UserView.create_user_view()
            full_name, email, password, role_name = user_infos
            role = session.query(Role).filter(Role.code == role_name).one()
            if user.role.code == "man":
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
            else:
                MainView.display_message(
                    "You don't have the permission to create an user."
                )
                callback = partial(cls.create_user, user, session)
                MenusController.back_to_main_menu(user, session, callback)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error creating user : {e}")
            callback = partial(cls.create_user, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def get_users(cls, user, session):
        from controllers.menus import MenusController
        try:
            if user:
                users = session.query(User).options(joinedload(User.role)).all()
            cls.users_permissions(user, users, session)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error getting users : {e}")
            callback = partial(cls.get_users, user, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def users_permissions(cls, user, users, session):
        from controllers.menus import MenusController

        try:
            choice = UserView.display_users(users)
            if user.role.code == "man":
                if choice == "1" or choice == "2":
                    if choice == "1":
                        user_id = UserView.enter_user_id()
                        user_to_manage = session.query(User).get(user_id)
                        if user_to_manage:
                            cls.edit_user(user, user_to_manage, session)
                        else:
                            session.rollback()
                            MainView.display_message(
                                "Pick a valid collaborator id."
                            )
                    elif choice == "2":
                        user_id = UserView.delete_user_id()
                        user_to_manage = session.query(User).get(user_id)
                        if user_to_manage:
                            cls.delete_user(user, user_to_manage, session)
                        else:
                            session.rollback()
                            MainView.display_message(
                                "Collaborator not found. Pick a valid user id."
                            )
                elif choice == "menu":
                    callback = partial(
                        cls.users_permissions, user, users, session
                    )
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    MainView.display_message("Pick a valid option.")
                    cls.users_permissions(user, users, session)
            else:
                if choice == "menu":
                    callback = partial(
                        cls.users_permissions, user, users, session
                    )
                    MenusController.back_to_main_menu(user, session, callback)
                else:
                    MainView.display_message("Pick a valid option.")
                    cls.users_permissions(user, users, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error getting users permissions: {e}")
            callback = partial(cls.users_permissions, user, users, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def edit_user(cls, user, user_to_manage, session):
        from controllers.menus import MenusController

        try:
            choice = UserView.edit_user_view()
            if choice == "1":
                new_name = UserView.edit_user_name()
                user_to_manage.full_name = new_name
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "2":
                new_email = UserView.edit_user_email()
                user_to_manage.email = new_email
                session.commit()
                MainView.display_message("Updated successfully.")
                MenusController.main_menu(user, session)
            elif choice == "3":
                new_role_name = UserView.edit_user_role()
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
                callback = partial(
                    cls.edit_user, user, user_to_manage, session
                )
                MenusController.back_to_main_menu(user, session, callback)
            else:
                session.rollback()
                MainView.display_message("Pick a valid option.")
                cls.edit_user(user, user_to_manage, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error editing user: {e}")
            callback = partial(cls.edit_user, user, user_to_manage, session)
            MenusController.back_to_main_menu(user, session, callback)

    @classmethod
    def delete_user(cls, user, user_to_manage, session):
        from controllers.menus import MenusController
        try:
            confirmation = UserView.delete_user_view(
                "Are you sure you want to delete user with id"
                f" {user_to_manage.id}?"
            )
            if confirmation:
                session.delete(user_to_manage)
                session.commit()
                MainView.display_message(
                    f"User with id {user_to_manage.id} deleted successfully."
                )
                MenusController.main_menu(user, session)
            else:
                MainView.display_message("User deletion canceled.")
                MenusController.main_menu(user, session)
        except Exception as e:
            session.rollback()
            sentry_sdk.capture_exception(e)
            MainView.display_message(f"Error deleting user: {e}")
            cls.delete_user(user, user_to_manage, session)
