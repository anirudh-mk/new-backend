from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company import Company
    pass  # decoupled: from app.models.party.party import Party
    pass  # decoupled: from app.models.party.party_bank_account import PartyBankAccount
    pass  # decoupled: from app.models.party.party_credit_limit import PartyCreditLimit


class Currency(AuditModel):
    """
    Represents a currency supported by the ERP.

    Purpose:
        Currency is a master table containing all monetary currencies
        supported by the ERP. It is referenced throughout the system for
        accounting, sales, purchasing, inventory valuation, banking,
        taxation and reporting.

        Each company has a base currency, while Parties, Bank Accounts,
        Credit Limits and Transactions may use different currencies.

    Examples:
        - Indian Rupee (INR)
        - US Dollar (USD)
        - Euro (EUR)
        - British Pound (GBP)
        - Japanese Yen (JPY)

    ERP Workflow:

        Currency
            ├── Company
            ├── Party
            ├── PartyBankAccount
            ├── PartyCreditLimit
            ├── Sales Invoice
            ├── Purchase Invoice
            ├── Journal Entry
            └── Exchange Rate

    Business Benefits:
        - Supports multi-currency accounting.
        - Enables foreign customer and supplier transactions.
        - Centralizes currency information.
        - Provides consistent currency formatting.
        - Supports exchange rate conversions.

    Relationships:
        Currency
            ├── Company
            ├── Party
            ├── PartyBankAccount
            └── PartyCreditLimit
    """

    __tablename__ = "currencies"

    __table_args__ = (
        UniqueConstraint(
            "code",
            name="uq_currency_code",
        ),
        UniqueConstraint(
            "name",
            name="uq_currency_name",
        ),
    )

    code: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        index=True,
        doc="ISO 4217 currency code (e.g. INR, USD, EUR).",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
        doc="Official currency name.",
    )

    symbol: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="Currency symbol (₹, $, €, £, ¥).",
    )

    numeric_code: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        unique=True,
        doc="ISO 4217 numeric currency code.",
    )

    decimal_places: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=2,
        doc="Number of decimal places used by the currency.",
    )

    is_base_currency: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the organization's default/base currency.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Indicates whether this currency is active.",
    )

    # Relationships



