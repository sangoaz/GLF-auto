from sqlmodel import Session
from app.core.database import engine
from app.core.security import hash_password
from app.models.user import User
from app.enums import UserRole

with Session(engine) as session:
    admin = User(
        email="admin@glf.fr",
        password_hash=hash_password("admin1234"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(admin)
    session.commit()
    print("Admin créé avec succès !")
