from database import SessionLocal
from models.models import User
from views.login_view import LoginView
from controllers.menus import MenusController

class LoginController:

    @classmethod
    def login(cls):
        login_infos = LoginView.login_view()
        session = SessionLocal()
        email = login_infos[0]
        password = login_infos[1]
        user = session.query(User).filter(User.email == email).one()
        if user and user.password == password:
            if user.department == "man":
                MenusController.manager_menu(user)
    
