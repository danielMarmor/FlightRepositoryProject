from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from common.entities.db_config import Base


class AirlineCompany(Base):
    __tablename__ = 'airine_companies'

    MAX_NAME = 50

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(MAX_NAME), unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    user_id = Column(BigInteger,  ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship('User', backref=backref('airine_companies', uselist=False))
    country = relationship('Country', backref=backref('airine_companies', uselist=True))

    def __str__(self):
        return f'<AirlineCompany> id:{self.id} name:{self.name} country_id:{self.country_id}' \
               f'user_id:{self.user_id}'

    def __repr__(self):
        return f'<AirlineCompany> id:{self.id} name:{self.name} country_id:{self.country_id}' \
               f'user_id:{self.user_id}'

    def __eq__(self, other):
        return isinstance(other, AirlineCompany) and other.id == self.id and other.name == self.name \
               and other.country_id == self.country_id and other.user_id == self.user_id

    def adapt_str(self):
        self.name = self.name.strip()

    @property
    def serialize(self):
        data = {'id': self.id,
                'name': self.name,
                'country_id': self.country_id,
                'user_id': self.user_id
                }
        return data

