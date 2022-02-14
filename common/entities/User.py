from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, backref
from common.entities.db_config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    user_role = Column(Integer, ForeignKey('user_roles.id'), nullable=False)

    userrole = relationship('UserRole', backref=backref('users'), uselist=True)

    def __str__(self):
        return f'<User> id:{self.id} username=:{self.username} password:{self.password} ' \
               f'email:{self.email} user_role:{self.user_role}'

    def __repr__(self):
        return f'<User> id:{self.id} username=:{self.username} password:{self.password} W' \
               f'email:{self.email} user_role:{self.user_role}'

    def is_equal_by_data(self, other):
        return self.username == other.username and self.password == other.password and self.email == other.email \
               and self.user_role == other.user_role

    def adapt_str(self):
        return User(id=self.id,
                    username=self.username.strip(),
                    password=self.password.strip(),
                    email=self.email.strip(),
                    user_role=self.user_role)
