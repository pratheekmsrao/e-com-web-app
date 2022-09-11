from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash(password: str) -> str:
    """returns the hashed password"""
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if the password matches or now
    :param plain_password: user entered password
    :param hashed_password: hashed password
    :return: True if password matched or returns False
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
