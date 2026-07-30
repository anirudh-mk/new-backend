from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
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
    from app.models.hr.employee.employee import Employee
    from app.models.sales.quotation.sales_quotation import SalesQuotation
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.sales.invoice.sales_invoice import SalesInvoice


class SalesPerson(BaseModel):
    """
    Represents a Sales Person within the organization.

    Purpose:
        A Sales Person is responsible for acquiring customers,
        generating quotations, managing customer relationships,
        processing sales orders, and achieving sales targets.

        The Sales Person master connects Employees with
        the Sales module and stores sales-specific information
        such as commission rates, sales targets,
        territories, and active status.

        Every Sales Quotation, Sales Order,
        and Sales Invoice may optionally reference
        a Sales Person for performance tracking
        and commission calculation.

    Examples:

        Sales Person

            Rahul Sharma

            Employee ID
                EMP-0012

            Territory
                North Kerala

            Commission
                5%

        -----------------------------------

        Sales Person

            John Mathew

            Territory
                Karnataka

            Monthly Target
                ₹50,00,000

            Commission
                3%

    Workflow:

                     Company
                        │
                        ▼
                   Employee
                        │
                        ▼
                  Sales Person
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Sales Quote    Sales Order    Sales Invoice
                        │
                        ▼
                Commission Calculation
                        │
                        ▼
                  Sales Performance

    Benefits:

        • Tracks employee sales performance.
        • Supports commission calculation.
        • Supports sales territories.
        • Supports sales targets.
        • Enables salesperson-wise reports.
        • Enables profitability analysis.
        • Supports CRM integration.
        • Supports customer assignment.
        • Supports incentive calculation.
        • Improves sales analytics.

    Relationships:

                     Company
                        │
                        ▼
                  Sales Person
                        │
                 Employee Master
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    Sales Quote    Sales Order    Sales Invoice

    Example:

        Employee

            EMP-0015

        Name

            Arjun Nair

        Sales Code

            SP-015

        Commission

            4%

        Territory

            Kerala

    Notes:

        • Every Sales Person is linked to one Employee.
        • One Employee may or may not be a Sales Person.
        • Sales Persons may have different commission rates.
        • Sales targets are optional.
        • Sales Persons may be assigned to Customers.
        • Sales Persons may manage multiple territories.
        • Used for reporting and commission only.
        • Inactive Sales Persons remain available
          for historical transactions.

    This model is referenced throughout
    CRM,
    Customer Management,
    Sales,
    Sales Quotation,
    Sales Order,
    Sales Invoice,
    Commission,
    Incentives,
    Performance Dashboard,
    Analytics,
    and Reporting modules.
    """

    __tablename__ = "sales_persons"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
        doc="Reference to the Company.",
    )

    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
        unique=True,
        index=True,
        doc="Reference to the Employee acting as Sales Person.",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
        doc="Unique Sales Person code.",
    )

    territory: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc="Sales territory assigned to the Sales Person.",
    )

    sales_target: Mapped[float | None] = mapped_column(
        Numeric(18, 2),
        nullable=True,
        doc="Sales target assigned to the Sales Person.",
    )

    commission_percentage: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=0,
        doc="Default commission percentage.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks about the Sales Person.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the Sales Person is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    company: Mapped["Company"] = relationship(
        back_populates="sales_persons",
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="sales_person",
    )

    quotations: Mapped[list["SalesQuotation"]] = relationship(
        back_populates="sales_person",
    )

    sales_orders: Mapped[list["SalesOrder"]] = relationship(
        back_populates="sales_person",
    )

    sales_invoices: Mapped[list["SalesInvoice"]] = relationship(
        back_populates="sales_person",
    )