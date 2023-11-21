from pydantic import BaseModel, Field


class CityDTO(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=2)
    country_id: int = Field(ge=0)
