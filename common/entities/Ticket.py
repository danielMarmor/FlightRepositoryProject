from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from common.entities.db_config import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger, ForeignKey('flights.id'), nullable=False)
    customer_id = Column(BigInteger, ForeignKey('customers.id'), nullable=False)

    __table_args__ = (UniqueConstraint('flight_id', 'customer_id', name='un_flight_customer'), )

    flight = relationship('Flight', backref=backref('tickets'), uselist=True)
    customer = relationship('Customer', backref=backref('tickets'), uselist=True)

    def __str__(self):
        return f'<Ticket> id:{self.id}, flight_id:{self.flight_id}, customer_id:{self.customer_id}'

    def __repr__(self):
        return f'<Ticket> id:{self.id}, flight_id:{self.flight_id}, customer_id:{self.customer_id}'

    def __eq__(self, other):
        if not isinstance(other, Ticket):
            return False
        return other.id == self.id and other.flight_id == self.flight_id \
            and other.customer_id == self.customer_id

    @property
    def serialize(self):
        data = {'id': self.id,
                'flight_id': self.flight_id,
                'customer_id': self.customer_id,
                }
        return data

