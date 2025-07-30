from fastapi import HTTPException
from pydantic import BaseModel
from typing import ClassVar
import bcrypt


class User(BaseModel):

    _users: ClassVar[list['User']] =  []

    name: str
    email: str # need validation
    __hashed_password: bytes = ""
    is_email_verified: bool = False
    kyc_verified: bool = False
    is_banned: bool = False
    
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password
    
    @classmethod
    def create_user(cls, user: 'User', password: str) -> 'User':
        hashed_password = cls.hash_password(password)
        user.__hashed_password = hashed_password
        cls._users.append(user)
        return user

    @classmethod
    def get_user(cls, email):
        for user in cls._users:
            if email == user.email:
                return user
        raise HTTPException(status_code=404, detail="User not found.")

    @classmethod
    def login_user(cls, email: str, password: str) -> 'User':
        user = cls.get_user(email)
        password_bytes = password.encode('utf-8')
        hashed_password = user.__hashed_password
        if bcrypt.checkpw(password_bytes, hashed_password):
            return user
        raise HTTPException(status_code=401, detail="Email or Password Incorrect")
    