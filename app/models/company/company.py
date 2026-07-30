from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company_address import CompanyAddress
    from app.models.company.company_contact import CompanyContact
    from app.models.company.branch import Branch
    pass  # decoupled: from app.models.accounting.tax_type import TaxType



class Company(AuditModel):
    """
    Represents the primary legal entity/organization within the ERP.

    Company acts as the root organization master table. All operational records,
    branches, transactions (sales, purchases, journal entries, ledgers), and
    configurations belong to a specific Company.

    Purpose:
        - Stores statutory business identifiers (Registration Number, Tax Type).
        - Links multiple physical offices/warehouses (via CompanyAddress).
        - Acts as the central tenant identifier for multi-company accounting configurations.
    """

    __tablename__ = "companies"

    name: Mapped[str] = mapped_column(
        String(200),
        unique=True,
        nullable=False,
        index=True,
        doc="Official registered legal name of the organization.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Short unique code identifying the company (e.g. COMP, GOOGLE).",
    )

    tax_type_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        doc="The primary tax scheme/type registered for the company (links to TaxType).",
    )

    tax_registration_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Statutory tax registration number (e.g. GSTIN, VAT No, EIN).",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the company entity is active and operational.",
    )

    # Relationships
    branches: Mapped[list["Branch"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        doc="Operational branch locations registered under this company.",
    )

    addresses: Mapped[list["CompanyAddress"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        doc="Physical or mailing addresses registered under this company.",
    )

    contacts: Mapped[list["CompanyContact"]] = relationship(
        back_populates="company",
        cascade="all, delete-orphan",
        doc="Communication contact methods registered under this company.",
    )


    def __repr__(self) -> str:
        return f"<Company(id={self.id}, code='{self.code}', name='{self.name}')>"