from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    pass  # decoupled: from app.models.company.company import Company
    from app.models.accounting.account_group import AccountGroup

from decimal import Decimal


class Ledger(BaseModel):
    """
    Represents an individual ledger account within the Chart of Accounts.

    A Ledger is the lowest level of the Chart of Accounts hierarchy and
    represents an account that records actual financial transactions. Every
    debit and credit entry posted in the accounting system ultimately affects
    a ledger through journal entry lines.

    Each ledger belongs to a single AccountGroup, which in turn belongs to an
    AccountType. Together, they form the complete Chart of Accounts used for
    financial reporting and accounting operations.

    Purpose:
        - Records financial transactions for a specific account.
        - Maintains opening balances for accounting periods.
        - Serves as the posting account for journal entries.
        - Supports General Ledger, Trial Balance, Balance Sheet,
          Profit & Loss Statement, and Cash Flow reporting.
        - Enables financial analysis at the individual account level.
        - Controls whether manual journal entries are permitted.

    Chart of Accounts Hierarchy:

        AccountType
             │
             ▼
        AccountGroup
             │
             ▼
           Ledger
             │
             ▼
        JournalEntryLine

    Examples:

        Assets
        └── Current Assets
            ├── Cash on Hand
            ├── SBI Current Account
            ├── HDFC Bank Account
            └── Accounts Receivable

        Liabilities
        └── Current Liabilities
            ├── Accounts Payable
            ├── GST Payable
            └── Salary Payable

        Income
        └── Sales
            ├── Product Sales
            ├── Service Income
            └── Other Income

        Expenses
        └── Operating Expenses
            ├── Salary Expense
            ├── Rent Expense
            ├── Electricity Expense
            └── Office Supplies

    Opening Balance:

        Every ledger can have an opening balance that represents its balance
        at the beginning of a financial period.

        Example:

            Cash on Hand
                Opening Balance : ₹50,000.00
                Balance Type    : DR

            Bank Loan
                Opening Balance : ₹2,50,000.00
                Balance Type    : CR

    Manual Entry Control:

        Some ledgers are maintained automatically by the ERP and should not
        allow direct journal postings. For example:

            - Inventory Control
            - GST Input / Output
            - Accounts Receivable
            - Accounts Payable

        Other ledgers may allow accountants to create manual journal entries,
        such as:

            - Miscellaneous Expense
            - Bank Charges
            - Interest Income
            - Adjustment Account

    Relationships:
        Company
            └── Ledger (One-to-Many)

        AccountGroup
            └── Ledger (One-to-Many)

        Ledger
            └── JournalEntryLine (One-to-Many)

    Every financial transaction posted in the ERP ultimately affects one or
    more ledger accounts. Ledger balances form the basis for all accounting
    reports, including the General Ledger, Trial Balance, Balance Sheet,
    Profit & Loss Statement, Cash Flow Statement, GST reports, and financial
    analytics.
    """

    __tablename__ = "ledgers"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_ledger_company_code",
        ),
        UniqueConstraint(
            "company_id",
            "name",
            name="uq_ledger_company_name",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this ledger.",
    )

    account_group_id: Mapped[UUID] = mapped_column(
        ForeignKey("account_groups.id"),
        nullable=False,
        index=True,
        doc="Account group to which this ledger belongs.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique ledger code within the company.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        doc="Display name of the ledger.",
    )

    opening_balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=Decimal("0.00"),
        nullable=False,
        doc="Opening balance of the ledger.",
    )

    opening_balance_type: Mapped[str] = mapped_column(
        String(2),
        default="DR",
        nullable=False,
        doc="Opening balance type: DR (Debit) or CR (Credit).",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional description or remarks for the ledger.",
    )

    allow_manual_entry: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether manual journal entries are allowed for this ledger.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates whether the ledger is system-defined.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the ledger is active.",
    )


    account_group: Mapped["AccountGroup"] = relationship(
        back_populates="ledgers",
    )