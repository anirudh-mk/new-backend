from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.accounting.fiscal_year import FiscalYear
    from app.models.accounting.journal_entry import JournalEntry


class AccountingPeriod(AuditModel):
    """
    Represents an accounting period within a fiscal year.

    An accounting period is a subdivision of a fiscal year, typically one month,
    used to organize, control, and report financial transactions.

    Purpose:
        - Groups journal entries into logical accounting periods.
        - Controls whether transactions can be posted by opening or closing periods.
        - Supports month-end and year-end closing processes.
        - Simplifies financial reporting for a specific period.
        - Prevents modification of finalized accounting periods.
        - Provides a consistent period reference for accounting, inventory,
          payroll, taxation, and other ERP modules.

    Example:

        Fiscal Year: 2026-27

            ├── April 2026
            ├── May 2026
            ├── June 2026
            ├── July 2026
            ├── ...
            └── March 2027

    When a journal entry is created with a transaction date, the ERP determines
    the corresponding accounting period and links the journal entry to it.

    For example:

        Transaction Date: 15-Apr-2026
        Accounting Period: April 2026

    If the April accounting period has been closed, no further transactions can
    be posted for dates within that period, ensuring the integrity of finalized
    financial statements and regulatory filings.
    """

    __tablename__ = "accounting_periods"

    __table_args__ = (
        UniqueConstraint(
            "fiscal_year_id",
            "name",
            name="uq_accounting_period_fiscal_year_name",
        ),
    )

    fiscal_year_id: Mapped[UUID] = mapped_column(
        ForeignKey("fiscal_years.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Fiscal year to which this accounting period belongs.",
    )

    name: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Display name of the accounting period (e.g., April 2026).",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Start date of the accounting period.",
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="End date of the accounting period.",
    )

    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the accounting period is closed.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the accounting period is active.",
    )

    fiscal_year: Mapped["FiscalYear"] = relationship(
        back_populates="accounting_periods",
    )

    journal_entries: Mapped[list["JournalEntry"]] = relationship(
        back_populates="accounting_period",
    )