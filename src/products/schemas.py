from datetime import datetime

from pydantic import BaseModel, model_validator


class ProductCreateUpdateSchema(BaseModel):
    name: str
    price: float


class ProductSchema(ProductCreateUpdateSchema):
    id: int
    created_at: datetime | None = None


class UserRegisterScheme(BaseModel):
    email: str
    password: str
    password_2: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_2:
            raise ValueError('Passwords do not match')
        return self
