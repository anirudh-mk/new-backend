from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class AccountType(BaseModel):
    """
    Represents a primary account type in the Chart of Accounts.

    Account types are system-defined classifications used to organize
    account groups and ledgers.

    Examples:
        - Assets
        - Liabilities
        - Equity
        - Income
        - Expenses
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
