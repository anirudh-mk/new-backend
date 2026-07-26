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
    from app.models.company import Company
    from app.models.accounting.account_group import AccountGroup


class Ledger(BaseModel):
    """
    Represents an individual ledger in the Chart of Accounts.
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
        ForeignKey("companies.id"),
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

    opening_balance: Mapped[float] = mapped_column(
        Numeric(18, 2),
        default=0,
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

    company: Mapped["Company"] = relationship()

    account_group: Mapped["AccountGroup"] = relationship(
        back_populates="ledgers",
    )
