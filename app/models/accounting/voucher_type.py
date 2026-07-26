from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.accounting.journal_entry import JournalEntry


class VoucherType(AuditModel):
    """
    Represents a category of accounting voucher used to classify journal entries.

    A VoucherType defines the business purpose of a journal entry by identifying
    the type of transaction that generated it. Every journal entry is associated
    with a voucher type, enabling the ERP to organize transactions, enforce
    business rules, generate voucher numbering, and produce transaction-specific
    reports.

    Voucher types are typically system-defined and represent common accounting
    transactions such as sales, purchases, receipts, payments, and journal
    adjustments. Additional voucher types may be introduced to support specific
    business requirements.

    Purpose:
        - Classifies journal entries based on business transactions.
        - Differentiates accounting documents within the ERP.
        - Supports voucher numbering and document sequencing.
        - Enables transaction-specific validations and workflows.
        - Simplifies financial reporting and auditing.
        - Provides meaningful categorization for accounting and statutory reports.

    Common Voucher Types:

        SV  - Sales Voucher
        PV  - Purchase Voucher
        RV  - Receipt Voucher
        PM  - Payment Voucher
        JV  - Journal Voucher
        CV  - Contra Voucher
        CN  - Credit Note
        DN  - Debit Note
        OB  - Opening Balance
        CL  - Closing Entry

    Example Transactions:

        Sales Invoice
            Voucher Type : SV (Sales Voucher)

            Customer A/C           Dr   ₹11,800.00
                To Sales Revenue        ₹10,000.00
                To Output GST            ₹1,800.00

        Supplier Payment
            Voucher Type : PM (Payment Voucher)

            Accounts Payable       Dr   ₹25,000.00
                To Bank Account         ₹25,000.00

        Year-End Adjustment
            Voucher Type : JV (Journal Voucher)

            Depreciation Expense   Dr    ₹5,000.00
                To Accumulated
                   Depreciation          ₹5,000.00

    Benefits:

        - Groups similar transactions for reporting.
        - Allows separate voucher numbering for each transaction type.
        - Supports document filtering and auditing.
        - Enables transaction-specific business logic.
        - Improves traceability across accounting operations.

    Relationships:
        VoucherType
            └── JournalEntry (One-to-Many)

    Every accounting transaction in the ERP is recorded as a JournalEntry and
    classified by a VoucherType. This classification provides business context
    for the transaction while supporting reporting, auditing, document
    management, and accounting workflows throughout the system.
    """

    __tablename__ = "voucher_types"

    code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique code identifying the voucher type.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Display name of the voucher type.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description of the voucher type.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the voucher type is active.",
    )

    journal_entries: Mapped[list["JournalEntry"]] = relationship(
        back_populates="voucher_type",
    )
