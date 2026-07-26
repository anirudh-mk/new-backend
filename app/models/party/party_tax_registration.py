from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.party.party import Party
    from app.models.accounting.tax_type import TaxType


class PartyTaxRegistration(AuditModel):
    """
    Represents a tax registration associated with a Party.

    Purpose:
        Stores government-issued tax registration numbers for a Party.
        A Party may maintain multiple registrations depending on the
        countries in which it operates or the tax authorities with
        which it is registered.

        Examples include GST, VAT, PAN, TIN, EIN and other statutory
        registrations.

    Examples:

        ABC Traders

            • GSTIN
            • PAN

        XYZ Imports

            • VAT Number
            • Import Export Code (IEC)

    ERP Workflow:

        TaxType
            │
            ▼
        PartyTaxRegistration
            │
            ▼
          Party

    Business Benefits:
        - Supports multiple tax registrations per Party.
        - Enables country-specific tax compliance.
        - Centralizes statutory registration information.
        - Reusable across Sales, Purchase, Finance and Compliance modules.

    Relationships:
        Party
            └── PartyTaxRegistration

        TaxType
            └── PartyTaxRegistration
    """

    __tablename__ = "party_tax_registrations"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "tax_type_id",
            "registration_number",
            name="uq_party_tax_registration",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party associated with this tax registration.",
    )

    tax_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("company_tax_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Type of tax registration (GST, VAT, PAN, etc.).",
    )

    registration_number: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Government-issued tax registration number.",
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Registered legal name associated with the tax registration.",
    )

    issuing_authority: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Government authority that issued the registration.",
    )

    place_of_registration: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Place or jurisdiction where the registration was issued.",
    )

    certificate_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Certificate or license number, if applicable.",
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the primary tax registration for the Party.",
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether the registration has been verified.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this tax registration is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="tax_registrations",
        lazy="selectin",
        doc="Party associated with this tax registration.",
    )

    tax_type: Mapped["TaxType"] = relationship(
        lazy="selectin",
        doc="Tax registration type assigned to the Party.",
    )
