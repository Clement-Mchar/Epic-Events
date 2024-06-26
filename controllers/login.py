from database import SessionLocal
from models.models import User
from views.login_view import LoginView
from views.menu_view import MainView
from controllers.menus import MenusController
import sentry_sdk
from sqlalchemy.orm.exc import NoResultFound


class LoginController:

    @classmethod
    def login(cls):
        with SessionLocal() as session:
            while True:
                try:
                    login_infos = LoginView.login_view()
                    email = login_infos[0]
                    password = login_infos[1]
                    user = (
                        session.query(User).filter(User.email == email).one()
                    )
                    if user and user.password == password:
                        MenusController.main_menu(user, session)
                    else:
                        MainView.display_message(
                            "No user found, please try again :"
                        )
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    MainView.display_message(
                        "An error occurred during login. Please try again"
                        " later."
                    )
                    cls.login()
