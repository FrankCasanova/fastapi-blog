from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db: Session) -> User:
    """
    Create a new user in the database.
    Args:
        user (UserCreate): The user data to be created.
        db (Session): The database session.
    Returns:
        User: The created user object.
    """
    user = User(
        email=user.email,
        password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
