from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.accounting.journal_entry import JournalEntry
    from app.models.accounting.ledger import Ledger
    pass  # decoupled: from app.models.company.branch import Branch


class JournalEntryLine(AuditModel):
    """
    Represents an individual ledger posting within a journal entry.

    A JournalEntryLine records the financial impact of a journal entry on a
    specific ledger account. Each line represents either a debit or a credit
    posting and contributes to the overall transaction recorded by its parent
    JournalEntry.

    A journal entry consists of one or more journal entry lines. Together, the
    lines must satisfy the fundamental principle of double-entry accounting,
    where the total debit amount equals the total credit amount.

    Purpose:
        - Records debit or credit postings against individual ledger accounts.
        - Associates each posting with a branch for branch-wise accounting.
        - Maintains the sequence of postings within a journal entry.
        - Supports financial reporting, ledger analysis, and audit trails.
        - Updates ledger balances when the journal entry is posted.

    Accounting Rule:
        - Each line must contain either a debit amount or a credit amount.
        - A single line should never have both debit and credit values greater
          than zero.
        - The sum of all debit amounts within a journal entry must equal the
          sum of all credit amounts.

    Example:

        Journal Entry: Purchase Invoice

        ---------------------------------------------------------
        Line | Ledger                 Debit        Credit
        ---------------------------------------------------------
          1  | Purchase Expense      ₹10,000.00        -
          2  | Input GST              ₹1,800.00        -
          3  | Accounts Payable             -     ₹11,800.00
        ---------------------------------------------------------

    Another Example:

        Journal Entry: Cash Receipt

        ---------------------------------------------------------
        Line | Ledger                 Debit        Credit
        ---------------------------------------------------------
          1  | Cash                  ₹5,000.00         -
          2  | Customer Account             -      ₹5,000.00
        ---------------------------------------------------------

    Relationships:
        JournalEntry
            └── JournalEntryLine (One-to-Many)

        Ledger
            └── JournalEntryLine (One-to-Many)

        Branch
            └── JournalEntryLine (One-to-Many)

    The JournalEntryLine is the lowest-level accounting record in the ERP.
    Every ledger balance, Trial Balance, General Ledger, Profit & Loss Statement,
    Balance Sheet, Cash Flow Statement, and other financial reports are ultimately
    derived from these journal entry lines.
    """

    __tablename__ = "journal_entry_lines"

    journal_entry_id: Mapped[UUID] = mapped_column(
        ForeignKey("journal_entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Journal entry to which this line belongs.",
    )

    line_no: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequence number of the journal entry line.",
    )

    ledger_id: Mapped[UUID] = mapped_column(
        ForeignKey("ledgers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Ledger affected by this journal entry line.",
    )

    branch_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Branch associated with this journal entry line.",
    )

    debit: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Debit amount.",
    )

    credit: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=0,
        doc="Credit amount.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional narration for this journal entry line.",
    )

    journal_entry: Mapped["JournalEntry"] = relationship(
        back_populates="journal_entry_lines",
    )

    ledger: Mapped["Ledger"] = relationship(
        back_populates="journal_entry_lines",
    )
