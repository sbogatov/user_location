from pydantic import BaseModel


class CityDTO(BaseModel):
    id: int
    name: str
    country_id: int
