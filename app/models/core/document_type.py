from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import AuditModel


class DocumentType(AuditModel):
    """
    Master table for Document Types across the ERP modules.
    
    Examples:
        - PR (Purchase Requisition)
        - RFQ (Request for Quotation)
        - SQ (Supplier Quotation)
        - PO (Purchase Order)
        - PR_REJECTED (Rejected Receipt)
        - PINV (Purchase Invoice)
        - PRET (Purchase Return)
        - LC (Landed Cost)
        - SO (Sales Order)
        - SINV (Sales Invoice)
    """

    __tablename__ = "document_types"

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique document type code.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Display name of the document type.",
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Detailed description of the document type.",
    )

    module: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        doc="ERP module name (e.g. Purchase, Sales, Accounting, Inventory).",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Indicates whether the document type is active.",
    )

    def __repr__(self) -> str:
        return f"<DocumentType(code='{self.code}', name='{self.name}')>"
