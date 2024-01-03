from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from config.database import Base


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
