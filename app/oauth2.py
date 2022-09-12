from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Query, Session

from . import database, models, schemas
from .config import settings

# from psycopg2 import connection


# from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict) -> str:
    """
    created JWT token
    :param data: {"user_id": user.id, "user_name": user.username}
    :return: JWT token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(
    token: str, credentials_exception: HTTPException
) -> schemas.TokenData:
    """
    Verify the JWT token for authenticity and expiration
    :param token: JWT token
    :param credentials_exception: Exception if the JWTError error
    :return: TokenData with id and username
    """
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        username: str = payload.get("user_name")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, username=username)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
) -> object:
    """
    Returns current user logged-in user
    :param token: JWT token
    :param db: SqlAlchemy db object
    :return: SqlAlchemy result object
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials, expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
