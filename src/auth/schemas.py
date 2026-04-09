from datetime import datetime
from typing import Optional
from pydantic import BaseModel, model_validator

class UserRegisterSchema(BaseModel):
    email: str
    password: str
    password_2: str

    @model_validator(mode='after')
    def check_passwords_match(self):
        if self.password != self.password_2:
            raise ValueError('Passwords do not match')
        return self

class UserLoginSchema(BaseModel):
    email: str
    password: str

class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None