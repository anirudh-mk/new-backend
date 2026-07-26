from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.accounting.account_type import AccountType
    from app.models.accounting.ledger import Ledger


class AccountGroup(BaseModel):
    """
    Represents a group of related ledgers within an account type.

    Account groups organize ledgers into a hierarchical structure,
    allowing financial reports such as the Balance Sheet and
    Profit & Loss statement to be generated.
    """

    __tablename__ = "account_groups"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_account_group_company_code",
        ),
        UniqueConstraint(
            "company_id",
            "parent_group_id",
            "name",
            name="uq_account_group_company_parent_name",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Company that owns this account group.",
    )

    account_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("account_types.id"),
        nullable=False,
        index=True,
        doc="Account type to which this group belongs.",
    )

    parent_group_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("account_groups.id"),
        nullable=True,
        index=True,
        doc="Parent account group. Null for top-level groups.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique account group code within the company.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Display name of the account group.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Optional description of the account group.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Indicates whether the account group is system-defined.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the account group is active.",
    )

    company: Mapped["Company"] = relationship()

    account_type: Mapped["AccountType"] = relationship()

    parent_group: Mapped["AccountGroup | None"] = relationship(
        remote_side="AccountGroup.id",
        back_populates="child_groups",
    )

    child_groups: Mapped[list["AccountGroup"]] = relationship(
        back_populates="parent_group",
    )

    ledgers: Mapped[list["Ledger"]] = relationship(
        back_populates="account_group",
    )
