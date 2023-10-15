from datetime import date
from pydantic import BaseModel, ConfigDict


class AnimalCreate(BaseModel):
    animal_type: str
    animal_breed: str
    name: str
    photo_url: str
    birth_date: date


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    animal_breed: str
    name: str
    photo_url: str
    birth_date: date

    def calculate_age(self) -> int:
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age
