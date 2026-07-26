from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class AccountType(BaseModel):
    """
    Represents a primary classification within the Chart of Accounts.

    An AccountType is the highest level of the accounting hierarchy and defines
    the fundamental nature of financial accounts. Every account group and ledger
    ultimately belongs to one of these account types, enabling the ERP to
    classify transactions correctly and generate standard financial statements.

    Account types are system-defined master records and are typically fixed
    according to accounting principles. Most accounting systems use the
    following five account types:

        - Assets
        - Liabilities
        - Equity
        - Income
        - Expenses

    Purpose:
        - Defines the top-level structure of the Chart of Accounts.
        - Classifies account groups and ledger accounts.
        - Determines how balances are presented in financial statements.
        - Provides the foundation for Balance Sheet and Profit & Loss reporting.
        - Ensures consistent financial classification across all ERP modules.

    Hierarchy:

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

    Example:

        Assets
            ├── Current Assets
            │     ├── Cash
            │     ├── Bank
            │     └── Accounts Receivable
            │
            └── Fixed Assets
                  ├── Buildings
                  └── Machinery

        Income
            ├── Sales Revenue
            ├── Service Revenue
            └── Other Income

    Relationships:
        AccountType
            └── AccountGroup (One-to-Many)

    Every financial transaction ultimately affects a ledger, which belongs to
    an AccountGroup, and every AccountGroup belongs to an AccountType. This
    hierarchical structure enables the ERP to aggregate balances and generate
    financial reports accurately.
    """

    __tablename__ = "account_types"

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique code identifying the account type.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Display name of the account type.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the account type is predefined by the system and cannot be deleted.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the account type is active and available for use.",
    )
