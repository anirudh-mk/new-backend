from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.core.country import Country
    from app.models.accounting.tax import Tax


class TaxType(BaseModel):
    """
    Represents a statutory tax category applicable to a specific country.

    A TaxType defines a high-level classification of taxes recognized by a
    country's taxation system. It serves as a master reference that organizes
    company-specific tax configurations while ensuring that only valid tax
    categories are available for businesses operating within that country.

    A TaxType does not define tax rates or accounting behavior. Instead, it
    acts as a category under which one or more Tax configurations are created.
    The Tax model stores the actual tax rate, effective dates, ledger mappings,
    and calculation rules used during transaction processing.

    Since taxation laws differ across countries, TaxTypes are maintained on a
    country basis. This allows the ERP to support multiple jurisdictions while
    keeping tax definitions standardized and extensible.

    Purpose:
        - Defines statutory tax categories for each country.
        - Standardizes tax classification across the ERP.
        - Serves as the parent for company-specific tax configurations.
        - Restricts companies to tax categories applicable to their country.
        - Simplifies tax reporting and statutory compliance.
        - Supports multi-country ERP deployments.

    Country-wise Examples:

        India
            GST
            TDS
            TCS

        United Arab Emirates
            VAT

        United Kingdom
            VAT

        United States
            Sales Tax

        Australia
            GST

    Tax Hierarchy:

        Country
            │
            ▼
        TaxType
            │
            ▼
        Tax
            │
            ▼
        Product / Service
            │
            ▼
        Sales / Purchase Transaction
            │
            ▼
        Journal Entry

    Example:

        Country
            India

        Tax Types
            GST
            TDS
            TCS

        Company
            ABC Private Limited

        Tax Configurations
            GST @ 5%
            GST @ 12%
            GST @ 18%
            GST @ 28%

        During a sales transaction, the ERP selects one of the company's
        configured GST taxes based on business rules and calculates the
        appropriate tax amount.

    Benefits:

        - Eliminates duplicate tax category definitions.
        - Ensures companies use only valid tax categories.
        - Supports country-specific taxation rules.
        - Simplifies maintenance when introducing new countries.
        - Provides a consistent foundation for tax calculation and reporting.
        - Keeps tax categories separate from company-specific tax rates.

    Relationships:
        Country
            └── TaxType (One-to-Many)

        TaxType
            └── Tax (One-to-Many)

    The TaxType model forms the statutory foundation of the ERP's taxation
    framework. It represents government-defined tax categories, while individual
    companies create Tax records under these categories to define their own tax
    rates, effective periods, and accounting ledger mappings. This separation
    maintains a normalized database design and enables the ERP to scale across
    multiple countries and tax regimes.
    """

    __tablename__ = "tax_types"

    __table_args__ = (
        UniqueConstraint(
            "country_id",
            "code",
            name="uq_tax_type_country_code",
        ),
    )

    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="Country where this tax type is applicable.",
    )

    code: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        back_populates="tax_types",
    )

    taxes: Mapped[list["Tax"]] = relationship(
        back_populates="tax_type",
    )
