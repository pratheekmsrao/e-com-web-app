from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from psycopg2 import connection
from .. import database, models, oauth2, schemas, utils

# from ..database import get_db

router = APIRouter(tags=["Authentication"])


# @router.post('/login', response_model=schemas.Token)
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), conn= Depends(get_db)):
#     cursor = conn.cursor()
#     cursor.execute("""SELECT * FROM users WHERE username = %s """, (str(user_credentials.username),))
#     user = cursor.fetchone()
#     print(user['password'],type(user))
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#
#     if not utils.verify(user_credentials.password, user['password']):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#
#     access_token = oauth2.create_access_token(data={"user_id": user['id']})
#
#     return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
) -> Dict[str, str]:
    """
    User login and returns the JWT token
    :param user_credentials: username and password
    :param db: SqlAlchemy db object
    :return: JWT token
    """
    user = (
        db.query(models.User)
        .filter(models.User.username == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    # create a token
    # return token

    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "user_name": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}
