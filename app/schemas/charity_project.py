from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Extra, validator, NonNegativeInt, PositiveInt

from app.schemas.constants import MAX_NAME_LENGTH, MIN_NAME_LENGTH


class CharityProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        min_anystr_length = MIN_NAME_LENGTH
        max_anystr_length = MAX_NAME_LENGTH


class CharityProjectCreate(CharityProjectBase):
    name: str
    description: str
    full_amount: PositiveInt

    @validator('description')
    def description_cannot_be_none(cls, value):
        if not value.strip():
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    @validator('name')
    def name_cannot_be_none(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_none(cls, value):
        if not value:
            raise ValueError('Описание проекта не может быть пустым!')
        return value
