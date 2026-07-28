from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel, BaseModel

if TYPE_CHECKING:
    from app.models.company.company.company import Company
    from app.models.company.company.branch import Branch
    from app.models.purchase.quotation.request_for_quotation import RequestForQuotation
    from app.models.purchase.requisition.purchase_requisition import PurchaseRequisition
    from app.models.accounting.journal_status import JournalStatus
    from app.models.purchase.quotation.supplier_quotation import SupplierQuotation
    from app.models.purchase.quotation.supplier_quotation_item import SupplierQuotationItem
    from app.models.inventory.product import Product
    from app.models.inventory.product_variant import ProductVariant


class QuotationComparison(AuditModel):
    """
    Represents a comparison matrix for evaluating multiple supplier quotations.
    """

    __tablename__ = "quotation_comparisons"

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    branch_id: Mapped[UUID] = mapped_column(
        ForeignKey("branches.id"),
        nullable=False,
        index=True,
    )

    comparison_no: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique Quotation Comparison number.",
    )

    comparison_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date of comparison evaluation.",
    )

    rfq_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("request_for_quotations.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating RFQ.",
    )

    requisition_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("purchase_requisitions.id"),
        nullable=True,
        index=True,
        doc="Reference to the originating Purchase Requisition.",
    )

    status_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_statuses.id"),
        nullable=False,
        index=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    company: Mapped["Company"] = relationship()
    branch: Mapped["Branch"] = relationship()
    rfq: Mapped["RequestForQuotation"] = relationship()
    requisition: Mapped["PurchaseRequisition"] = relationship()
    status: Mapped["JournalStatus"] = relationship()

    details: Mapped[list["QuotationComparisonDetail"]] = relationship(
        back_populates="comparison",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<QuotationComparison(comparison_no='{self.comparison_no}', date='{self.comparison_date}')>"


class QuotationComparisonDetail(BaseModel):
    """
    Represents a detailed comparison line comparing a specific quotation item.
    """

    __tablename__ = "quotation_comparison_details"

    comparison_id: Mapped[UUID] = mapped_column(
        ForeignKey("quotation_comparisons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    quotation_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_quotations.id"),
        nullable=False,
        index=True,
        doc="Reference to the Supplier Quotation.",
    )

    quotation_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("supplier_quotation_items.id"),
        nullable=False,
        index=True,
        doc="Reference to the Supplier Quotation Item.",
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    variant_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=True,
        index=True,
    )

    quantity: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Offered quantity.",
    )

    unit_price: Mapped[float] = mapped_column(
        Numeric(18, 4),
        nullable=False,
        doc="Offered unit price.",
    )

    tax_amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
    )

    landed_cost_estimate: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Estimated additional landed costs (freight, duties, etc.) for this line.",
    )

    line_total: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Net line amount including tax and estimated landed costs.",
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="Evaluated rank compared to other quotes (1 = best/cheapest).",
    )

    is_selected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether this quote was selected for the Purchase Order.",
    )

    selection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Why this item was selected or rejected.",
    )

    # Relationships
    comparison: Mapped["QuotationComparison"] = relationship(back_populates="details")
    quotation: Mapped["SupplierQuotation"] = relationship()
    quotation_item: Mapped["SupplierQuotationItem"] = relationship()
    product: Mapped["Product"] = relationship()
    variant: Mapped["ProductVariant"] = relationship()

    def __repr__(self) -> str:
        return f"<QuotationComparisonDetail(comparison_id='{self.comparison_id}', rank={self.rank}, selected={self.is_selected})>"
