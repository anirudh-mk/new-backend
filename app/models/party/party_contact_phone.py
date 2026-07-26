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
    from app.models.party.party_contact import PartyContact


class PartyContactPhone(AuditModel):
    """
    Represents a phone number associated with a Party Contact.

    Purpose:
        Stores one or more phone numbers for a contact person.
        A contact may have multiple numbers such as mobile,
        office, home or fax.

    Examples:

        John Mathew

            • +91 9876543210 (Mobile)
            • +91 4952345678 (Office)

    Business Benefits:
        - Supports multiple phone numbers.
        - Supports WhatsApp integration.
        - Enables SMS/OTP verification.
        - Allows primary phone selection.

    Relationships:
        PartyContact
            └── PartyContactPhone
    """

    __tablename__ = "party_contact_phones"

    __table_args__ = (
        UniqueConstraint(
            "contact_id",
            "country_code",
            "phone_number",
            name="uq_party_contact_phone",
        ),
    )

    contact_id: Mapped[UUID] = mapped_column(
        ForeignKey("party_contacts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Contact that owns this phone number.",
    )

    country_code: Mapped[str] = mapped_column(
        String(5),
        nullable=False,
        default="+91",
        doc="International dialing code.",
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        doc="Phone or mobile number.",
    )

    phone_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="MOBILE",
        doc="Phone type (MOBILE, OFFICE, HOME, FAX, etc.).",
    )

    is_whatsapp: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this number is registered on WhatsApp.",
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the primary phone number.",
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this phone number has been verified.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this phone number is active.",
    )

    # Relationships

    contact: Mapped["PartyContact"] = relationship(
        back_populates="phones",
        lazy="selectin",
        doc="Contact associated with this phone number.",
    )
