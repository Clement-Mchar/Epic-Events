from database import SessionLocal
from models.models import User, Role
from views.manager_view import ManagerView
from views.login_view import LoginView

class ManagerOptions:

    @classmethod
    def create_user(cls, user):
        session = SessionLocal()
        user_infos = ManagerView.create_user_view(user)
        full_name, email, password, role_name = user_infos
        role = session.query(Role).filter(Role.code == role_name).one()
        if user.role.code == "man":
            try:
                new_user = User(
                    full_name=full_name,
                    email=email,
                    password=password,
                    role_id=role.id
                )
                session.add(new_user)
                session.commit()
                print(f"User created with id: {new_user.id}")
            except Exception as e:
                session.rollback()
                print(f"Error creating user: {e}")
            finally:
                session.close()
        else :
            print("Vous ne pouvez pas créer un collaborateur.")
            return LoginView.login_view()