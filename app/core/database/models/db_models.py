from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database.services import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(540), nullable=False, unique=True, index=True)
    password = Column(String(1024), nullable=False, unique=True)
    name = Column(String(540), nullable=False)
    last_name = Column(String(540), nullable=False)
    email = Column(String(540), nullable=False)
    phone = Column(String(540), nullable=False)

    def __repr__(self):
        return "Users(id=%d, name=%s, username=%s,last_name=%s, email=%s)" % (
            self.id,
            self.username,
            self.name,
            self.last_name,
            self.email,
        )
