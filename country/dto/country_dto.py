from pydantic import BaseModel, Field


class CountryDTO(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=2)
