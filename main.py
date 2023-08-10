from fastapi import FastAPI

from city.controllers.city_controller import city_router
from country.controllers.country_controller import country_router

app = FastAPI()
app.include_router(country_router)
app.include_router(city_router)