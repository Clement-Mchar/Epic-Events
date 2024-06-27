from models.models import User, Role
from database import SessionLocal
import getpass


def create_user(role_id):
    session = SessionLocal()

    role = session.query(Role).filter_by(id=role_id).first()
    if role is None:
        raise ValueError(f"Role with id '{role_id}' not found in the database.")
    password = getpass.getpass("Enter user password : ")
    user = User(
        full_name="manager",
        email="manager@ee.com",
        password=password,
        role_id=role_id
    )

    session.add(user)
    session.commit()
    session.close()

    return user

create_user(role_id=1)
