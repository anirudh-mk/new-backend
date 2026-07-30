from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Date, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel

if TYPE_CHECKING:
    from app.models.accounting.ledger import Ledger
    from app.models.accounting.tax_type import TaxType
    pass  # decoupled: from app.models.company.company import Company


class Tax(AuditModel):
    """
    Represents a tax configuration defined for a company.

    A Tax defines how a specific tax is calculated, applied, and recorded in
    the accounting system. It stores the tax rate, validity period, associated
    ledger accounts, and calculation behavior, allowing the ERP to automatically
    compute taxes during financial transactions.

    Each tax belongs to a TaxType (such as GST, VAT, TDS, or Service Tax) and
    is associated with ledger accounts where the tax amounts are posted during
    journal entry generation.

    Purpose:
        - Defines company-specific tax configurations.
        - Calculates taxes during sales, purchases, and other taxable transactions.
        - Maps tax amounts to the appropriate accounting ledgers.
        - Supports effective-date based tax rate changes.
        - Enables automatic accounting entries for statutory compliance.
        - Supports both simple and compound tax calculations.

    Tax Configuration Example:

        Tax Type
            GST

        Tax
            Code            : GST18
            Name            : GST @ 18%
            Rate            : 18.00%
            Effective From  : 01-Apr-2026
            Effective To    : None

    Ledger Mapping:

        Purchase Transaction

            Purchase Expense      Dr   ₹10,000.00
            Input GST             Dr    ₹1,800.00
                To Accounts Payable      ₹11,800.00

            Input GST is posted to the configured Input Tax Ledger.

        Sales Transaction

            Customer              Dr   ₹11,800.00
                To Sales Revenue        ₹10,000.00
                To Output GST            ₹1,800.00

            Output GST is posted to the configured Output Tax Ledger.

    Compound Tax Example:

        Some jurisdictions calculate one tax on top of another.

        Example:

            Base Amount          ₹10,000.00

            Tax A (10%)          ₹1,000.00

            Tax B (5% on ₹11,000)
                                 ₹550.00

            Total Tax            ₹1,550.00

        Setting is_compound=True enables this calculation behavior.

    Effective Dates:

        Tax rates often change due to government regulations.

        Example:

            GST @ 18%
                Effective From : 01-Apr-2026
                Effective To   : 31-Mar-2027

            GST @ 20%
                Effective From : 01-Apr-2027

        The ERP automatically applies the tax configuration that is effective
        on the transaction date.

    Relationships:
        Company
            └── Tax (One-to-Many)

        TaxType
            └── Tax (One-to-Many)

        Ledger
            ├── Input Tax Ledger (Many-to-One)
            └── Output Tax Ledger (Many-to-One)

    A Tax configuration acts as the bridge between business transactions and
    their accounting impact. During transaction processing, the ERP uses this
    configuration to calculate tax amounts, determine the applicable rate based
    on the transaction date, and generate the appropriate journal entries using
    the configured input and output ledger accounts.
    """

    __tablename__ = "taxes"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "code",
            name="uq_tax_company_code",
        ),
        UniqueConstraint(
            "company_id",
            "name",
            name="uq_tax_company_name",
        ),
    )

    company_id: Mapped[UUID] = mapped_column(
        nullable=False,
        index=True,
        doc="Company that owns this tax configuration.",
    )

    tax_type_id: Mapped[UUID] = mapped_column(
        ForeignKey("tax_types.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Category of tax (GST, VAT, TDS, etc.).",
    )

    code: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Unique tax code within the company.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Display name of the tax.",
    )

    rate: Mapped[float] = mapped_column(
        Numeric(8, 4),
        nullable=False,
        doc="Tax percentage.",
    )

    input_ledger_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ledgers.id", ondelete="RESTRICT"),
        nullable=True,
        doc="Ledger used when the tax is recoverable (Input Tax).",
    )

    output_ledger_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("ledgers.id", ondelete="RESTRICT"),
        nullable=True,
        doc="Ledger used when the tax is payable (Output Tax).",
    )

    is_compound: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether this tax is calculated on top of another tax.",
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        doc="Date from which this tax becomes effective.",
    )

    effective_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        doc="Date until which this tax is effective.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether this tax configuration is active.",
    )


    tax_type: Mapped["TaxType"] = relationship(
        back_populates="taxes",
    )

    input_ledger: Mapped["Ledger | None"] = relationship(
        foreign_keys=[input_ledger_id],
    )

    output_ledger: Mapped["Ledger | None"] = relationship(
        foreign_keys=[output_ledger_id],
    )