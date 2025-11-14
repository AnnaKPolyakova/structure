from sqlalchemy import Column, Integer, String

from src.app.models.base import Base


class User(Base):  # type: ignore[misc]
    __tablename__ = "user"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, nullable=False)
