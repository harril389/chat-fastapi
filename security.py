from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from pydantic import ValidationError
from passlib.context import CryptContext

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_token(authorization=Depends(reusable_oauth2)) -> str:
    try:
        payload = jwt.decode(authorization.credentials,
                             SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        if payload.get('username') < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )


def verify_password(user_db, password: str):
    if not pwd_context.verify(password, user_db['password']):
        return False
    return True


def generate_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 3)
    to_encode = {
        'exp': expire, 'username': username
    }
    encode_jwt = jwt.encode(to_encode, SECRET_KEY,
                            algorithm=SECURITY_ALGORITHM)
    return encode_jwt
