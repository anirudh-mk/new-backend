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
    from app.models.inventory.product.product import Product
    from app.models.inventory.product.product_variant import ProductVariant
    from app.models.inventory.uom.uom import UOM
    from app.models.sales.invoice.sales_invoice_item import SalesInvoiceItem
    from app.models.sales.returns.sales_return_item import SalesReturnItem
    from app.models.sales.credit_note.credit_note import CreditNote


class CreditNoteItem(BaseModel):
    """
    Represents an individual Product or Service credited
    within a Credit Note.

    Purpose:
        Credit Note Item stores every product or service
        included in a Customer Credit Note.

        Each Credit Note consists of one or more
        Credit Note Items.

        Every line records the credited quantity,
        pricing snapshot,
        discounts,
        taxes,
        refund amount,
        and accounting values.

        This model forms the basis for
        Accounts Receivable adjustment,
        customer credit calculation,
        tax adjustment,
        financial reporting,
        and General Ledger posting.

    Examples:

        Credit Note

            CN-2026-000025

        Product

            Dell Latitude Laptop

        Quantity

            2 Nos

        Credit Amount

            ₹1,04,000

        ------------------------------------

        Product

            Laser Printer

        Quantity

            1 Nos

    Workflow:

            Sales Invoice Item
                    │
                    ▼
            Sales Return Item
                    │
                    ▼
             Credit Note Item
                    │
        ┌───────────┼──────────────┐
        ▼           ▼              ▼
    Customer AR   GL Posting   Tax Adjustment

    Benefits:

        • Supports unlimited credit items.
        • Supports partial credits.
        • Pricing snapshot.
        • Tax adjustment.
        • Customer credit tracking.
        • Financial reporting.
        • Inventory integration.
        • Audit trail.
        • Historical accuracy.
        • Complete traceability.

    Relationships:

            CreditNote
                 │
                 ▼
          CreditNoteItem
      ┌────────┼────────┬────────┐
      ▼        ▼        ▼        ▼
  Product  Variant     UOM   Invoice Item

    Example:

        Product

            Dell Latitude 5450

        Quantity

            2

        Unit Price

            ₹52,000

        Credit Amount

            ₹1,04,000

    Notes:

        • One Credit Note contains multiple items.
        • One Invoice Item may generate multiple credits.
        • Taxes are stored separately.
        • Supports partial credit quantities.
        • Historical values should never change.
        • Used during accounting posting.
        • Used for AR reconciliation.

    Referenced throughout
    Sales,
    Accounts Receivable,
    Accounting,
    Finance,
    Taxation,
    Reporting,
    Analytics,
    Customer Service,
    and Compliance modules.
    """

    __tablename__ = "credit_note_items"

    credit_note_id: Mapped[UUID] = mapped_column(
        ForeignKey("credit_notes.id"),
        nullable=False,
        index=True,
        doc="Reference to the Credit Note.",
    )

    sales_invoice_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_invoice_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Invoice Item.",
    )

    sales_return_item_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("sales_return_items.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Sales Return Item.",
    )

    line_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential line number within the Credit Note.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
        doc="Reference to the Product.",
    )

    product_variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
        doc="Reference to the Product Variant.",
    )

    uom_id: Mapped[UUID] = mapped_column(
        ForeignKey("uoms.id"),
        nullable=False,
        index=True,
        doc="Reference to the Unit of Measure.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Product description copied from the Sales Invoice.",
    )

    credited_quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
        doc="Quantity credited.",
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
        doc="Discount applicable to this credit item.",
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Tax adjustment amount.",
    )

    credit_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        doc="Total credit amount for this line.",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Remarks for this Credit Note Item.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether this Credit Note Item is active.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    credit_note: Mapped["CreditNote"] = relationship(
        back_populates="items",
    )

    sales_invoice_item: Mapped["SalesInvoiceItem"] = relationship(
        back_populates="credit_note_items",
    )

    sales_return_item: Mapped["SalesReturnItem"] = relationship(
        back_populates="credit_note_items",
    )

    product: Mapped["Product"] = relationship(
        back_populates="credit_note_items",
    )

    product_variant: Mapped["ProductVariant"] = relationship(
        back_populates="credit_note_items",
    )

    uom: Mapped["UOM"] = relationship(
        back_populates="credit_note_items",
    )