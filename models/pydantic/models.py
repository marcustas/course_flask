from datetime import date
from pydantic import BaseModel, ConfigDict


class AnimalCreate(BaseModel):
    animal_type: str
    name: str
    birth_date: date
    animal_breed: str
    image_url: str


class AnimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    animal_type: str
    name: str
    birth_date: date
    animal_breed: str
    image_url: str

    def get_age(self) -> str:
        """
        Returns:
            str
        """        
        today = date.today()
        years = today.year - self.birth_date.year
        months = today.month - self.birth_date.month

        if today.day < self.birth_date.day:
            months -= 1

        if months < 0:
            years -= 1
            months += 12

        if years > 0 and months > 0:
            age_str = f"{years} year {months} month"
        elif years > 0:
            age_str = f"{years} year"
        else:
            age_str = f"{months} month"

        return age_str