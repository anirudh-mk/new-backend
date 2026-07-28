from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.company.branch_address import BranchAddress
    from app.models.company.branch_contact import BranchContact
    from app.models.accounting.tax_type import TaxType


class Branch(AuditModel):
    """
    Represents an operational location or branch under a Company.

    Branches partition operational resources (warehouses, users, transactions)
    under a parent Company legal entity, and may carry their own tax registration.

    Purpose:
        - Segregates business transactions by physical location.
        - Supports regional tax registrations (GSTIN/VAT) within a multi-branch company.
    """

    __tablename__ = "branches"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_branch_company_code",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="The parent company that owns this branch.",
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
        doc="Name of the branch (e.g. New York Branch, Warehouse 1).",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Short unique code for the branch.",
    )

    tax_type_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("company_tax_types.id", ondelete="SET NULL"),
        nullable=True,
        doc="The branch-specific tax scheme/type registered (if different from Company).",
    )

    tax_registration_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        doc="Branch-specific tax registration number.",
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        doc="Indicates whether the branch is active.",
    )

    # Relationships
    company: Mapped["Company"] = relationship(
        back_populates="branches",
    )

    addresses: Mapped[list["BranchAddress"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
        doc="Addresses registered under this branch.",
    )

    contacts: Mapped[list["BranchContact"]] = relationship(
        back_populates="branch",
        cascade="all, delete-orphan",
        doc="Contact methods registered under this branch.",
    )

    tax_type: Mapped["TaxType"] = relationship()

    def __repr__(self) -> str:
        return f"<Branch(id={self.id}, code='{self.code}', name='{self.name}')>"
