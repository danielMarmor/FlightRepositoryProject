from datetime import datetime
from sqlalchemy import Column, BigInteger, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from common.entities.db_config import Base
from common.entities.Country import Country
from common.entities.AirlineCompany import AirlineCompany
from dataclasses import dataclass


@dataclass
class Flight(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger, ForeignKey(AirlineCompany.id), nullable=False)
    origin_country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    destination_country_id = Column(Integer,  ForeignKey('countries.id'), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    landing_time = Column(DateTime, nullable=False)
    remaining_tickets = Column(Integer, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    distance = Column(Numeric(18, 2), nullable=False)
    num_seats = Column(BigInteger, nullable=False)

    airline_company = relationship('AirlineCompany', backref=backref('flights', uselist=True))
    origin_country = relationship(Country, foreign_keys=[origin_country_id], backref=backref('origin_flights',  uselist=True))
    destination_country = relationship(Country, foreign_keys=[destination_country_id], backref=backref('destination_flights',  uselist=True))

    def __str__(self):
        return f'<Flight>: id:{self.id} airline_company_id:{self.airline_company_id} origin_country_id:' \
               f'{self.origin_country_id} destination_country_id:{self.destination_country_id} ' \
               f'departure_time:{self.departure_time} landing_time:{self.landing_time} ' \
               f'price:{self.price} remaining_tickets:{self.remaining_tickets}' \
               f'distance:{self.distance} num_seats:{self.num_seats}'

    def __repr__(self):
        return f'<Flight>: id:{self.id} airline_company_id:{self.airline_company_id} origin_country_id:' \
               f'{self.origin_country_id} destination_country_id:{self.destination_country_id} ' \
               f'departure_time:{self.departure_time} landing_time:{self.landing_time} ' \
               f'price:{self.price} remaining_tickets:{self.remaining_tickets}'\
               f'distance:{self.distance} num_seats:{self.num_seats}'

    def __eq__(self, other):
        if not isinstance(other, Flight):
            return False
        return other.id == self.id and other.airline_company_id == self.airline_company_id \
            and other.origin_country_id  == self.origin_country_id \
            and other.destination_country_id == self.destination_country_id \
            and other.departure_time == self.departure_time \
            and other.landing_time == self.landing_time \
            and other.remaining_tickets == self.remaining_tickets \
            and other.distance == self.distance \
            and other.num_seats == self.num_seats

    @property
    def serialize(self):
        data = {'id': self.id,
                'airline_company_id': self.airline_company_id,
                'airline_company_name': self.airline_company.name,
                'airline_company_iata': self.airline_company.iata,
                'origin_country_id': self.origin_country_id,
                'origin_country_name': self.origin_country.name,
                'origin_country_port_abrr': self.origin_country.airport_abbr,
                'destination_country_id': self.destination_country_id,
                'destination_country_name': self.destination_country.name,
                'destination_country_port_abrr': self.destination_country.airport_abbr,
                'departure_time': str(self.departure_time),
                'landing_time': str(self.landing_time),
                'price': str(self.price),
                'remaining_tickets': self.remaining_tickets,
                'distance': str(self.distance),
                'num_seats': self.num_seats
                }
        return data

