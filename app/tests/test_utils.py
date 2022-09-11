from passlib.context import CryptContext

from app.utils import get_hash, verify

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_verify():
    password = "abc"
    hashed_password = get_hash(password)

    assert verify(password, hashed_password)
