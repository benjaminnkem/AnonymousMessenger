from pydantic import BaseModel, Field, EmailStr


class CreateUserDto(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8)


class LoginDto(BaseModel):
    username: str
    password: str = Field(min_length=8)
