from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from common.entities.db_config import Base


class Country(Base):
    __tablename__ = 'countries'
    NAME_MAX = 50
    AIRPORN_ABBR_MAX = 3

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(NAME_MAX), unique=True, nullable=False)
    airport_abbr = Column(String(AIRPORN_ABBR_MAX), unique=False, nullable=False)

    def __str__(self):
        return f'<Country> id:{self.id} name:{self.name} airport_abbr:{self.airport_abbr}'

    def __repr__(self):
        return f'<Country> id:{self.id} name:{self.name} airport_abbr:{self.airport_abbr}'

    @property
    def serialize(self):
        data = {'id': self.id,
                'name': self.name,
                'airport_abbr': self.airport_abbr
                }
        return data

