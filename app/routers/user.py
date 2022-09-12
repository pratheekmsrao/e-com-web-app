from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

# from psycopg2 import connection

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.UserOut:  # conn= Depends(get_db)
    """
    creates new user
    :param user: username, password
    :param db: SqlAlchemy db object
    :return: created user: id, username, created_at
    """
    # hash the password - user.password
    hashed_password = utils.get_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

    # Demo: create user with raw sql
    # cursor = conn.cursor()
    # cursor.execute("""INSERT INTO users (username, password) VALUES (%s, %s) RETURNING * """,
    #                (user.username, user.password))
    # new_user = cursor.fetchone()
    # conn.commit()
    # return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int, db: Session = Depends(get_db)
) -> schemas.UserOut:  # conn= Depends(get_db)
    """
    Returns user based on the user_id
    :param id: user id of the user
    :param db: SqlAlchemy db object
    :return: user details: id, username, created_at
    """
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exist",
        )
    return user
    # Demo: get user with raw sql
    # cursor = conn.cursor()
    # cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id),))
    # user = cursor.fetchone()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"user with id: {id} was not found")
    #
    # return user
