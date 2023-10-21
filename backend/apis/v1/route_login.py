from typing import Optional

from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.models.user import User
from db.repository.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.token import Token
from sqlalchemy.orm import Session

router = APIRouter()


def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """
    Authenticates a user based on their email and password.
    Parameters:
    - email (str): The email of the user.
    - password (str): The password of the user.
    - db (Session): The database session.
    Returns:
    - Optional[User]: The authenticated user if successful, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not Hasher.verify_password(password, user.password):
        return None
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    """
    Authenticates user with username and password and returns an access token.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session): The database session.
    Returns:
        Token: The access token and token type.
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Retrieves the current authenticated user.
    Args:
        token (str): The JWT token.
        db (Session): The database session.
    Returns:
        Optional[User]: The current user, if authenticated. None otherwise.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = get_user(email=username, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user
