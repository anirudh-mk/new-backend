from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.sales.master.sales_person import SalesPerson


class CommissionRule(BaseModel):
    """
    Represents a Commission Rule used to calculate Sales Person commissions.

    Purpose:
        Commission Rules define how commissions are calculated for
        Sales Persons.

        Organizations often use different commission structures
        depending on product category, customer, sales amount,
        profit margin, or sales targets.

        Instead of hardcoding commission percentages inside the
        Sales Person master, reusable Commission Rules provide
        a flexible and configurable commission engine.

        A Commission Rule may be assigned to one or many
        Sales Persons.

    Examples:

        Standard Commission

            3%

        Dealer Commission

            5%

        Premium Product Commission

            8%

        High Value Sales

            2%
            Applicable above ₹10,00,000

    Workflow:

                    Company
                       │
                       ▼
                Commission Rule
                       │
                       ▼
                 Sales Person
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Sales Quote   Sales Order   Sales Invoice
                       │
                       ▼
              Commission Calculation
                       │
                       ▼
               Commission Settlement

    Benefits:

        • Supports multiple commission policies.
        • Supports reusable commission structures.
        • Supports sales incentives.
        • Supports profit-based commissions.
        • Supports amount slabs.
        • Supports future commission changes.
        • Simplifies payroll integration.
        • Enables performance analysis.
        • Improves commission transparency.
        • Eliminates manual calculations.

    Relationships:

                    Company
                       │
                       ▼
                Commission Rule
                       │
                       ▼
                 Sales Person

    Example:

        Code

            COMM-001

        Name

            Standard Sales Commission

        Commission Type

            Percentage

        Percentage

            5%

        Minimum Sale

            ₹10,000

        Maximum Sale

            ₹5,00,000

    Notes:

        • One Rule may be assigned to multiple Sales Persons.
        • Rules may have validity periods.
        • Rules may be activated or deactivated.
        • Rules are reusable across branches.
        • Commission may be percentage or fixed amount.
        • Amount ranges are optional.
        • Rules do not store commission transactions.
        • Commission payouts should be stored separately.

    This model is referenced throughout
    Sales,
    CRM,
    Sales Performance,
    Payroll,
    Incentives,
    Analytics,
    Reporting,
    Commission Processing,
    and Finance modules.
    """

    __tablename__ = "commission_rules"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Commission Rule code.",
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
        doc="Display name of the Commission Rule.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Description of the Commission Rule.",
    )

    commission_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="PERCENTAGE",
        doc="Commission calculation type (PERCENTAGE or FIXED_AMOUNT).",
    )

    commission_value: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Commission percentage or fixed amount.",
    )

    minimum_sale_amount: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Minimum sales amount required for this rule.",
    )

    maximum_sale_amount: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Maximum sales amount applicable for this rule.",
    )

    effective_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date from which this Commission Rule becomes effective.",
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date until which this Commission Rule remains effective.",
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether this is the default Commission Rule.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Commission Rule is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="commission_rules",
    )

    sales_persons: Mapped[list["SalesPerson"]] = relationship(
        back_populates="commission_rule",
    )