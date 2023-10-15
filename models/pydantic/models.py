from datetime import date
from pydantic import BaseModel, ConfigDict


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    breed: str
    animal_photo: str


    @property
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    age: int
    breed: str
    animal_photo: str
