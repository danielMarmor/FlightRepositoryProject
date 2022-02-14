from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from common.entities.db_config import Base


class UserRole(Base):

    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(25), unique=True, nullable=False)

    def __str__(self):
        return f'<UserRole> id:{self.id} name:{self.role_name}'

    def __repr__(self):
        return f'<UserRole> id:{self.id} name:{self.role_name}'

