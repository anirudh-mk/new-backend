from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import AuditModel


class TaxType(AuditModel):
    __tablename__ = "company_tax_types"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(30),
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


class Company(AuditModel):
    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    tax_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("company_tax_types.id", ondelete="SET NULL"),
    )

    tax_registration_number: Mapped[str | None] = mapped_column(
        String(100),
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )


class CompanyAddress(AuditModel):
    __tablename__ = "company_addresses"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    address_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("address_types.id"),
        nullable=False,
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255),
    )

    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id"),
        nullable=False,
    )

    state_id: Mapped[UUID] = mapped_column(
        ForeignKey("states.id"),
        nullable=False,
    )

    district_id: Mapped[UUID] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
    )

    postal_code: Mapped[str | None] = mapped_column(
        String(20),
    )

    latitude: Mapped[float | None] = mapped_column(
        Numeric(10, 8),
    )

    longitude: Mapped[float | None] = mapped_column(
        Numeric(11, 8),
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
    )

    display_order: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )


class CompanyContact(AuditModel):
    __tablename__ = "company_contacts"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    contact_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("contact_types.id"),
        nullable=False,
        index=True,
    )

    value: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_primary: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        default=1,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

