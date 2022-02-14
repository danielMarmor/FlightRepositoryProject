from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from common.entities.db_config import Base


class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    def __str__(self):
        return f'<Country> id:{self.id} name:{self.name}'

    def __repr__(self):
        return f'<Country> id:{self.id} name:{self.name}'



