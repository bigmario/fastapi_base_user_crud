from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database.services import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(540), nullable=False, unique=True, index=True)
    name = Column(String(540), nullable=False)
    last_name = Column(String(540), nullable=False)
    phone = Column(String(540), nullable=False)
    password = Column(String(1024), nullable=False)
    recovery_token = Column(String(1024), nullable=True)

    def __repr__(self):
        return "Users(id=%d, email=%s, name=%s, last_name=%s, email=%s, phone=%s)" % (
            self.id,
            self.email,
            self.name,
            self.last_name,
            self.phone,
        )
