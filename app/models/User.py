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
    is_kyc_verified: bool = False
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
    def get_user(cls, user_id: int, email: str = None) -> 'User':        
        if email is None:
            try:            
                return cls._users[user_id]
            except IndexError:
                raise HTTPException(status_code=404, detail="User not found.")                
        for user in cls._users:
            if user.email == email:
                return user
        raise HTTPException(status_code=404, detail="User not found.")

    @classmethod
    def login_user(cls, email: str, password: str) -> 'User':
        user = cls.get_user(user_id=None, email=email)
        password_bytes = password.encode('utf-8')
        hashed_password = user.__hashed_password
        if bcrypt.checkpw(password_bytes, hashed_password):
            return user
        raise HTTPException(status_code=401, detail="Email or Password Incorrect")
    
    @classmethod
    def get_users(cls) -> list['User']:
        return cls._users.copy() # Return copy to prevent external modification
    
    @classmethod
    def verify_kyc(cls, user_id) -> 'User':
        user = cls.get_user(user_id)
        if not user.is_kyc_verified:
            user.is_kyc_verified = True
        return user
    
    @classmethod
    def unverify_kyc(cls, user_id) -> 'User':
        user = cls.get_user(user_id)
        if user.is_kyc_verified:
            user.is_kyc_verified = False
        return user
    
    @classmethod
    def ban_user(cls, user_id) -> 'User':
        user = cls.get_user(user_id)
        if not user.is_banned:
            user.is_banned = True
        return user
    
    @classmethod
    def unban_user(cls, user_id) -> 'User':
        user = cls.get_user(user_id)
        if user.is_banned:
            user.is_banned = False
        return user

    
