from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    breed: Optional[str] = None
    photo: Optional[str] = None


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    breed: Optional[str] = None
    photo: Optional[str] = None

