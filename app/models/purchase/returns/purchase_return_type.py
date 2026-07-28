from __future__ import annotations

from typing import TYPE_CHECKING

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
    from app.models.purchase.returns.purchase_return import PurchaseReturn


class PurchaseReturnType(BaseModel):
    """
    Defines the various types of Purchase Returns.

    Purpose:
        Purchase Return Types classify the reason or category of goods
        being returned to a supplier. Using a configurable master table
        instead of hardcoded values allows organizations to customize
        return categories according to their business processes.

        Purchase Return Types help in inventory management,
        supplier performance analysis, reporting, and accounting.

    Common Types:

        • Defective
            Items received with manufacturing defects.

        • Damaged
            Goods damaged during transportation or handling.

        • Wrong Item
            Supplier delivered incorrect items.

        • Excess Quantity
            Quantity received exceeds the Purchase Order.

        • Expired
            Products expired before use.

        • Quality Rejected
            Failed quality inspection.

        • Warranty Return
            Returned under supplier warranty.

        • Other
            Miscellaneous reasons.

    Example:

        Purchase Receipt
                │
                ▼
        Purchase Return
                │
        Return Type = Damaged

    Benefits:
        • Standardizes return reasons
        • Improves supplier analysis
        • Supports quality management
        • Enables reporting and dashboards
        • Configurable without code changes

    Relationships:

        PurchaseReturnType
                │
                └── PurchaseReturn
    """

    __tablename__ = "purchase_return_types"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_purchase_return_type_company_code",
        ),
    )

    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
        doc="Company owning this return type. NULL indicates a global return type.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique purchase return type code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Purchase return type name.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the purchase return type.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system return type.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this return type is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    purchase_returns: Mapped[list["PurchaseReturn"]] = relationship(
        back_populates="return_type",
    )
