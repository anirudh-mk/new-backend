from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    is_active: Mapped[bool] = mapped_column(default=False)

    last_login: Mapped[datetime | None] = mapped_column(nullable=True)