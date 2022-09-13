from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from common.entities.db_config import Base
from sqlalchemy.orm import relationship, backref


class Administrator(Base):
    __tablename__ = 'administrators'

    FIRST_NAME_MAX = 50
    LAST_NAME_MAX = 50
    IMAGE_URL_MAX = 1000;

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(FIRST_NAME_MAX), nullable=False)
    last_name = Column(String(LAST_NAME_MAX), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), unique=True, nullable=False)
    image_url = Column(String(IMAGE_URL_MAX), unique=False, nullable=False)

    user = relationship('User', backref=backref('administrators', uselist=False))

    def __str__(self):
        return f'<Administrator> id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}' \
               f' user_id:{self.user_id} , image_url:{self.image_url}'

    def __repr__(self):
        return f'<Administrator> id:{self.id}, first_name:{self.first_name}, last_name:{self.last_name}' \
               f' user_id:{self.user_id}, image_url:{self.image_url}'

    def __eq__(self, other):
        if not isinstance(other, Administrator):
            return False
        return self.id == other.id and self.first_name == other.first_name and \
            self.last_name == other.last_name and self.user_id == other.user_id and \
            self.image_url == other.image_url

    def adapt_str(self):
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

    @property
    def serialize(self):
        data = {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'user_id': self.user_id,
                'username': self.user.username,
                'password': self.user.password,
                'email': self.user.email,
                'image_url': self.image_url
                }
        return data
