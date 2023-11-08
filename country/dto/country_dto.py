from pydantic import BaseModel


class CountryDTO(BaseModel):
    id: int
    name: str
