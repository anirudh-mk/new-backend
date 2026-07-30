from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.accounting.journal_entry import JournalEntry


class JournalStatus(AuditModel):
    """
    Represents the workflow status of a journal entry.

    A JournalStatus defines the current stage of a journal entry within the
    accounting lifecycle. It is used to control whether a journal entry can be
    edited, posted, reversed, or cancelled, ensuring the integrity of financial
    records and compliance with accounting policies.

    Purpose:
        - Tracks the current workflow state of a journal entry.
        - Controls which operations are permitted based on the status.
        - Prevents unauthorized modification of finalized transactions.
        - Supports approval and posting workflows.
        - Provides a consistent status reference across all accounting modules.

    Typical Workflow:

        Draft
           │
           ▼
        Posted
           │
           ├────────► Reversed
           │
           └────────► Cancelled

    Common Statuses:

        DRAFT
            Journal entry has been created but has not yet affected ledger
            balances. It can be modified or deleted.

        POSTED
            Journal entry has been validated and posted to the ledger.
            Ledger balances are updated and the entry should no longer be edited.

        CANCELLED
            Journal entry has been cancelled before posting or according to
            company policy. It no longer represents a valid accounting
            transaction.

        REVERSED
            A reversing journal entry has been created to negate the financial
            effect of the original posted journal entry while preserving the
            audit trail.

    Example:

        Sales Invoice

            Status : Draft
                ↓
            Accountant reviews
                ↓
            Status : Posted
                ↓
            Incorrect posting found
                ↓
            Status : Reversed

    Relationships:
        JournalStatus
            └── JournalEntry (One-to-Many)

    Using a separate master table instead of storing status as plain text allows
    the ERP to enforce workflow rules, maintain referential integrity, and
    introduce additional statuses (such as Pending Approval or Approved) without
    changing the database schema.
    """

    __tablename__ = "journal_statuses"

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique code identifying the journal entry status.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Display name of the journal entry status.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description of the journal entry status.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the status is active.",
    )

    journal_entries: Mapped[list["JournalEntry"]] = relationship(
        back_populates="status",
    )