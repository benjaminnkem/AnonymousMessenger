from pydantic import BaseModel, Field


class CreateUserDto(BaseModel):
    username: str
    password: str = Field(min_length=8)


class LoginDto(BaseModel):
    username: str
    password: str = Field(min_length=8)
