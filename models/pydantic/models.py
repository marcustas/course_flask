from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, computed_field


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    animal_breed: str
    photo: str
    @computed_field
    def age(self) -> int:
        return datetime.now().year - self.birth_date.year


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    animal_breed: str
    photo: str

