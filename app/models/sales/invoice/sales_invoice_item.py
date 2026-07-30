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
    from app.models.sales.delivery.delivery_note_item import DeliveryNoteItem
    from app.models.sales.invoice.sales_invoice import SalesInvoice
    from app.models.sales.order.sales_order_item import SalesOrderItem


class SalesInvoiceItem(BaseModel):
    """
    Represents an individual Product or Service billed in a Sales Invoice.

    Purpose:
        Sales Invoice Item stores every product or service
        billed to a customer.

        Each Sales Invoice consists of one or more
        Sales Invoice Items.

        Every line stores the invoiced quantity,
        pricing snapshot,
        discount,
        tax summary,
        warehouse,
        product information,
        and accounting values.

        This model represents the financial transaction
        for a single product or service and forms the basis
        for Accounts Receivable, Revenue Recognition,
        Inventory Valuation, and Financial Reporting.

    Examples:

        Invoice

            INV-2026-000245

        Item

            Dell Latitude Laptop

        Quantity

            10 Nos

        Rate

            ₹52,000

        Amount

            ₹5,20,000

        ------------------------------------

        Product

            Laser Printer

        Quantity

            5 Nos

    Workflow:

              Sales Order Item
                      │
                      ▼
            Delivery Note Item
                      │
                      ▼
            Sales Invoice Item
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
    Tax Posting   Revenue GL    Accounts Receivable

    Benefits:

        • Supports unlimited invoice lines.
        • Partial invoicing support.
        • Pricing snapshot.
        • Revenue recognition.
        • Inventory integration.
        • Tax integration.
        • Batch tracking.
        • Serial number tracking.
        • Complete audit trail.
        • Financial reporting.

    Relationships:

             SalesInvoice
                  │
                  ▼
          SalesInvoiceItem
      ┌────────┼────────┬────────┬─────────┐
      ▼        ▼        ▼        ▼
  Product  Variant     UOM   Warehouse

    Example:

        Product

            Dell Latitude 5450

        Quantity

            15

        Unit Price

            ₹52,000

        Discount

            ₹15,000

        Net Amount

            ₹7,65,000

    Notes:

        • One invoice contains many items.
        • One Delivery Note Item may generate multiple Invoice Items.
        • Taxes are stored separately.
        • Charges are stored separately.
        • Batch allocations are stored separately.
        • Serial numbers are stored separately.
        • Historical records should never change.
        • Used for accounting entries.

    This model is referenced throughout
    Sales,
    Accounts Receivable,
    Finance,
    Inventory,
    Taxation,
    Reporting,
    Analytics,
    Customer Portal,
    and Compliance modules.
    """

    __tablename__ = "sales_invoice_items"

    sales_invoice_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_invoices.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Invoice.",
    )

    sales_order_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_order_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Order Item.",
    )

    delivery_note_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("delivery_note_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Delivery Note Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Sales Invoice.",
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
        doc="Warehouse from which the product was supplied.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description printed on the invoice.",
    )

    invoiced_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Quantity billed to the customer.",
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Selling price per unit.",
    )

    discount_percentage: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False,
        default=0,
        doc="Discount percentage.",
    )

    discount_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Discount amount applied to this item.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Total tax amount.",
    )

    net_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Final line amount after discounts and taxes.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Additional remarks for this invoice item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Sales Invoice Item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_invoice: Mapped["SalesInvoice"] = relationship(
        back_populates="items",
    )

    sales_order_item: Mapped["SalesOrderItem"] = relationship(
        back_populates="invoice_items",
    )

    delivery_note_item: Mapped["DeliveryNoteItem"] = relationship(
        back_populates="invoice_items",
    )




