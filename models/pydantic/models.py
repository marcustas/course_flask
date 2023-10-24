from datetime import date
from pydantic import BaseModel, ConfigDict, computed_field
from dateutil.relativedelta import relativedelta


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    breed: str
    birth_date: date
    photo: str


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    breed: str
    birth_date: date
    photo: str

    @computed_field
    @property
    def age(self) -> int:
        age = relativedelta(date.today(), self.birth_date)
        return age.years
