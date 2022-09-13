from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from common.entities.db_config import Base


class Customer(Base):
    __tablename__ = 'customers'

    MAX_FIRST_NAME = 50
    MAX_LAST_NAME = 50
    MAX_ADDRESS = 200
    MAX_PHONE = 50
    MAX_CREDIT_CARD = 24
    MAX_IMAGE_URL = 1000

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(MAX_FIRST_NAME), nullable=False)
    last_name = Column(String(MAX_LAST_NAME), nullable=False)
    address = Column(String(MAX_ADDRESS), nullable=False)
    phone_number = Column(String(MAX_PHONE), unique=True, nullable=False)
    credit_card_number = Column(String(MAX_CREDIT_CARD), unique=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    image_url = Column(String(MAX_IMAGE_URL), unique=False, nullable=False)

    user = relationship('User', backref=backref('customers', uselist=False))

    def __eq__(self, other):
        return isinstance(other, Customer) \
            and self.id == other.id and self.first_name == other.first_name and self.last_name == other.last_name \
            and self.address == other.address and self.phone_number == other.phone_number \
            and self.credit_card_number == other.credit_card_number \
            and self.image_url == other.image_url

    def __str__(self):
        return f'<Customer> id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}' \
               f'address:{self.address} phone_number:{self.phone_number} credit_card_number:' \
               f'{self.credit_card_number} user_id:{self.user_id} image_url:{self.image_url}'

    def __repr__(self):
        return f'<Customer> id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}' \
               f'address:{self.address} phone_number:{self.phone_number} credit_card_number:' \
               f'{self.credit_card_number} user_id:{self.user_id} image_url:{self.image_url}'

    def adapt_str(self):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.address = self.address.strip()
        self.phone_number = self.phone_number.strip()
        self.credit_card_number = self.credit_card_number.strip()
        self.image_url = self.image_url.strip()

    @property
    def serialize(self):
        data = {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'address': self.address,
                'phone_number': self.phone_number,
                'credit_card_number': self.credit_card_number,
                'user_id': self.user_id,
                'image_url': self.image_url,
                'username' : self.user.username,
                'password' :self.user.password,
                'email' : self.user.email
                }
        return data

