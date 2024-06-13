from database import SessionLocal
from models.models import User
from views.login_view import LoginView
from controllers.menus import MenusController


class LoginController:

    @classmethod
    def login(cls):
        login_infos = LoginView.login_view()
        with SessionLocal() as session:
            email = login_infos[0]
            password = login_infos[1]
            try:
                user = session.query(User).filter(User.email == email).one()
                if user and user.password == password:
                    MenusController.main_menu(user, session)
                else:
                    print("Login failed: Incorrect email or password.")
            except Exception as e:
                print(f"Error during login: {e}")
