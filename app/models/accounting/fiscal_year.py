from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.company.company import Company
    from app.models.accounting.accounting_period import AccountingPeriod
    from app.models.accounting.journal_entry import JournalEntry


class FiscalYear(AuditModel):
    """
    Represents a financial (fiscal) year for a company.

    A fiscal year defines the primary accounting period during which a company
    records its financial transactions. It serves as the parent entity for one
    or more accounting periods and is used for financial reporting, taxation,
    auditing, budgeting, and year-end closing activities.

    Purpose:
        - Defines the accounting year for a company.
        - Groups accounting periods (typically monthly).
        - Organizes journal entries under a specific financial year.
        - Supports annual financial statements such as the Balance Sheet,
          Profit & Loss Statement, and Cash Flow Statement.
        - Enables year-end closing and opening balance generation for the
          next fiscal year.
        - Prevents posting transactions once the fiscal year is officially
          closed.

    Example:

        Company: ABC Pvt. Ltd.

        Fiscal Year: 2026-27

            Start Date : 01-Apr-2026
            End Date   : 31-Mar-2027

            Accounting Periods

                ├── April 2026
                ├── May 2026
                ├── June 2026
                ├── ...
                └── March 2027

    Every journal entry belongs to a fiscal year, either directly or through
    its accounting period. Closing a fiscal year indicates that all accounting
    periods have been finalized, financial statements have been prepared, and
    no further transactions should be posted unless the fiscal year is reopened.
    """

    __tablename__ = "fiscal_years"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "name",
            name="uq_fiscal_year_company_name",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="Company to which this fiscal year belongs.",
    )

    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        doc="Display name of the fiscal year (e.g., 2026-27).",
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Start date of the fiscal year.",
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="End date of the fiscal year.",
    )

    is_closed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Indicates whether the fiscal year is closed for accounting.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the fiscal year is active.",
    )

    company: Mapped["Company"] = relationship(
        back_populates="fiscal_years",
    )

    accounting_periods: Mapped[list["AccountingPeriod"]] = relationship(
        back_populates="fiscal_year",
        cascade="all, delete-orphan",
    )

    journal_entries: Mapped[list["JournalEntry"]] = relationship(
        back_populates="fiscal_year",
    )
