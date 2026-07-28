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
    from app.models.core.country import Country
    from app.models.core.currency import Currency
    from app.models.party.party import Party


class PartyBankAccount(AuditModel):
    """
    Represents a bank account associated with a Party.

    Purpose:
        Stores one or more bank accounts for a Party. These accounts are
        used for payments, receipts, refunds, vendor settlements, customer
        collections, payroll reimbursements, and other financial
        transactions.

        A Party may maintain multiple bank accounts across different
        banks, branches, countries, or currencies.

    Examples:

        ABC Traders

            • HDFC Bank - Current Account
            • ICICI Bank - Savings Account

        XYZ Suppliers

            • SBI - Current Account

    ERP Workflow:

        Party
            │
            ▼
        PartyBankAccount

    Business Benefits:
        - Supports multiple bank accounts per Party.
        - Enables domestic and international banking.
        - Supports multiple currencies.
        - Simplifies payment processing.
        - Maintains a primary bank account.
        - Reusable across Sales, Purchase, Finance and Payroll modules.

    Relationships:
        Party
            └── PartyBankAccount

        Currency
            └── PartyBankAccount

        Country
            └── PartyBankAccount
    """

    __tablename__ = "party_bank_accounts"

    __table_args__ = (
        UniqueConstraint(
            "party_id",
            "account_number",
            name="uq_party_bank_account_number",
        ),
    )

    party_id: Mapped[UUID] = mapped_column(
        ForeignKey("parties.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Party that owns this bank account.",
    )

    bank_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        doc="Name of the bank.",
    )

    branch_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Bank branch name.",
    )

    account_holder_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        doc="Name of the account holder.",
    )

    account_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="Bank account number.",
    )

    account_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        doc="Type of account (Savings, Current, Salary, etc.).",
    )

    ifsc_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        doc="IFSC code used for Indian banking.",
    )

    swift_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        index=True,
        doc="SWIFT/BIC code used for international banking.",
    )

    iban: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        index=True,
        doc="International Bank Account Number (IBAN).",
    )

    currency_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("currencies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Currency of the bank account.",
    )

    country_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("countries.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Country where the bank account is maintained.",
    )

    is_primary: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
        doc="Indicates whether this is the primary bank account for the Party.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this bank account is active.",
    )

    # Relationships

    party: Mapped["Party"] = relationship(
        back_populates="bank_accounts",
        lazy="selectin",
        doc="Party associated with this bank account.",
    )

    currency: Mapped["Currency | None"] = relationship(
        lazy="selectin",
        doc="Currency in which this bank account operates.",
    )

    country: Mapped["Country | None"] = relationship(
        lazy="selectin",
        doc="Country where the bank account is maintained.",
    )
