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
    from app.models.company.company import Company
    from app.models.purchase.master.landed_cost import LandedCost


class LandedCostAllocationMethod(BaseModel):
    """
    Defines the methods used to allocate Landed Costs across
    purchased items.

    Purpose:
        A Landed Cost Allocation Method determines how additional
        procurement expenses such as freight, customs duty,
        insurance, transportation, and handling charges are
        distributed among received inventory items.

        Instead of hardcoding allocation logic, ERP administrators
        can configure different allocation methods and use them
        while creating Landed Cost documents.

    Common Allocation Methods:

        • Quantity
            Allocate equally based on received quantity.

        • Item Value
            Allocate based on each item's purchase value.

        • Weight
            Allocate according to product weight.

        • Volume
            Allocate according to product volume.

        • Equal
            Allocate equal amount to every line.

        • Manual
            User manually specifies allocation.

    Example:

        Freight = ₹10,000

        Product A : Qty = 100
        Product B : Qty = 50

        Quantity Allocation

            Product A = ₹6,666.67
            Product B = ₹3,333.33

    Benefits:
        • Configurable allocation rules
        • Accurate inventory valuation
        • Supports import purchases
        • Complies with accounting standards
        • Easy to extend in future

    Relationships:
        LandedCostAllocationMethod
                │
                └── LandedCost
    """

    __tablename__ = "landed_cost_allocation_methods"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_landed_cost_allocation_method_company_code",
        ),
    )

    company_id: Mapped[int | None] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True,
        index=True,
        doc="Company owning this allocation method. NULL indicates a global method.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique allocation method code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Allocation method name.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the allocation method.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is a predefined system allocation method.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the allocation method is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship()

    landed_costs: Mapped[list["LandedCost"]] = relationship(
        back_populates="allocation_method",
    )
