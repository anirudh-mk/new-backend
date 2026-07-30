from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.invoice.sales_invoice_item import SalesInvoiceItem
    from app.models.sales.returns.sales_return import SalesReturn


class SalesReturnItem(BaseModel):
    """
    Represents an individual Product or Service returned by a customer.

    Purpose:
        Sales Return Item stores every returned product
        associated with a Sales Return document.

        Each Sales Return consists of one or more
        Sales Return Items.

        Every line records the returned quantity,
        pricing snapshot,
        warehouse,
        return reason,
        inventory adjustment,
        refund amount,
        and financial impact.

        This model forms the basis for inventory
        restocking, credit note generation,
        refund calculation, and accounting entries.

    Examples:

        Return

            SR-2026-000018

        Product

            Dell Latitude Laptop

        Returned Quantity

            2 Nos

        Reason

            Damaged During Transport

        ------------------------------------

        Product

            Laser Printer

        Returned Quantity

            1 Nos

    Workflow:

            Sales Invoice Item
                    │
                    ▼
            Sales Return Item
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
    Stock Update  Credit Note  Refund
                    │
                    ▼
            General Ledger

    Benefits:

        • Supports unlimited return lines.
        • Supports partial returns.
        • Inventory adjustment.
        • Refund calculation.
        • Credit note generation.
        • Warranty processing.
        • Replacement processing.
        • Complete audit trail.
        • Financial reporting.
        • Inventory traceability.

    Relationships:

            SalesReturn
                 │
                 ▼
          SalesReturnItem
      ┌────────┼────────┬────────┬─────────┐
      ▼        ▼        ▼        ▼
  Product  Variant     UOM   Warehouse

    Example:

        Product

            Dell Latitude 5450

        Returned Qty

            2

        Rate

            ₹52,000

        Refund

            ₹1,04,000

    Notes:

        • One return contains multiple items.
        • One invoice item may have multiple returns.
        • Supports partial quantity returns.
        • Taxes are stored separately.
        • Batch allocations are stored separately.
        • Serial numbers are stored separately.
        • Historical records should never change.
        • Used during accounting and inventory posting.

    This model is referenced throughout
    Sales,
    Inventory,
    Warehouse,
    Finance,
    Accounts Receivable,
    Warranty,
    Customer Service,
    Reporting,
    Analytics,
    and Compliance modules.
    """

    __tablename__ = "sales_return_items"

    sales_return_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_returns.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Return.",
    )

    sales_invoice_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_invoice_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Invoice Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Sales Return.",
    )

    product_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Reference to the Product Variant.",
    )

    warehouse_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
        index=True,
        doc="Warehouse receiving the returned product.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the return document.",
    )

    return_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Reason for returning this product.",
    )

    returned_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Quantity returned by the customer.",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Original selling price per unit.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount applied to this item.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax amount applicable to the returned item.",
    )

    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Refund or credit note amount for this item.",
    )

    is_restocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether inventory has been restocked.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Internal remarks for this return item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Sales Return Item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_return: Mapped["SalesReturn"] = relationship(
        back_populates="items",
    )

    sales_invoice_item: Mapped["SalesInvoiceItem"] = relationship(
        back_populates="return_items",
    )




