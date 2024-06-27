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
        # Establish a session to interact with the database
        with SessionLocal() as session:
            while True:
                try:
                    # Display login view and retrieve user input
                    login_infos = LoginView.login_view()
                    email = login_infos[0]
                    password = login_infos[1]

                    # Query the database for a user with the provided email
                    user = (
                        session.query(User).filter(User.email == email).one()
                    )

                    # Validate user credentials and navigate to main menu
                    if user and user.password == password:
                        MenusController.main_menu(user, session)
                    else:
                        MainView.display_message(
                            "No user found, please try again."
                        )

                except Exception as e:
                    # Log exceptions with Sentry and prompt user to retry login
                    sentry_sdk.capture_exception(e)
                    MainView.display_message(
                        "An error occurred during login. Please try again"
                        " later."
                    )
                    cls.login()  # Recursively call login method to retry
