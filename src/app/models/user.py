from sqlalchemy.orm import Mapped, mapped_column

from src.app.models.base import Base


class User(Base):  # type: ignore[misc]
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
