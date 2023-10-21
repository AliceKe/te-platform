from datetime import datetime

from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRoles(Enum):
    mentee = "Mentee"
    mentor = "Mentor"
    admin = "Admin"


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    middle_name: str = ""
    last_name: str
    image: str = ""
    date_of_birth: str | None = ""
    contact: str = ""
    address: str = ""
    university: str = ""
    mentor_id: int | None = None
    is_active: bool = True
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now()


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: int | None = None
    full_name: str = ""

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    password: str


class UserRead(UserInDBBase):
    ...
