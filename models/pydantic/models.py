from datetime import date
from pydantic import BaseModel, ConfigDict, computed_field


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    breed: str
    photo: str


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    breed: str
    photo: str

    @computed_field
    @property
    def age(self) -> str:
        years = date.today().year - self.birth_date.year
        if date.today().month < self.birth_date.month:
            years -= years
        elif date.today().month == self.birth_date.month:
            if date.today().day < self.birth_date.day:
                years -= years
        return years
