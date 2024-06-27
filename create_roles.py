from models.models import Role
from database import SessionLocal

def create_roles():
    session = SessionLocal()
    roles_data = [
        {"name": "Manager", "code": "man"},
        {"name": "Commercial", "code": "com"},
        {"name": "Support", "code": "sup"}
    ]
    for role_data in roles_data:
        role = Role(**role_data)
        session.add(role)

    session.commit()
    session.close()

create_roles()