from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import AuditModel


class AddressCategory(AuditModel):
    __tablename__ = "address_categories"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )


class AddressType(AuditModel):
    __tablename__ = "address_types"

    address_category_id: Mapped[UUID] = mapped_column(
        ForeignKey("address_categories.id"),
        nullable=False,
        index=True,
    )

    company_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )

    is_system: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
