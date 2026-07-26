from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModel


class TaxType(BaseModel):
    """
    Represents a high-level category of tax within the accounting system.

    A TaxType classifies taxes into broad statutory categories such as GST,
    VAT, TDS, TCS, Service Tax, or Excise Duty. It serves as a master reference
    used to organize individual tax configurations while ensuring consistency
    across the ERP.

    Unlike the Tax model, which defines company-specific tax rates and ledger
    mappings, a TaxType represents only the category of taxation. Multiple Tax
    configurations can belong to the same TaxType.

    Purpose:
        - Categorizes taxes into statutory classifications.
        - Provides a standardized list of tax categories across companies.
        - Simplifies tax management and reporting.
        - Enables multiple tax configurations under a single tax category.
        - Supports country- or region-specific taxation systems.

    Examples:

        GST
            ├── GST @ 5%
            ├── GST @ 12%
            ├── GST @ 18%
            └── GST @ 28%

        VAT
            ├── VAT @ 5%
            └── VAT @ 15%

        TDS
            ├── TDS - Contractor
            ├── TDS - Professional Fees
            └── TDS - Rent

        Service Tax
            ├── Service Tax @ 10%
            └── Service Tax @ 15%

    Hierarchy:

        TaxType
             │
             ▼
           Tax
             │
             ▼
        Business Transaction
             │
             ▼
        Journal Entry

    Example:

        Tax Type
            GST

        Tax Configurations
            GST @ 5%
            GST @ 12%
            GST @ 18%

        During a sales transaction, the ERP selects the appropriate Tax
        configuration based on the transaction details and applies the
        corresponding tax rate and ledger mappings.

    Relationships:
        TaxType
            └── Tax (One-to-Many)

    Using a separate TaxType master ensures that tax categories remain
    standardized while allowing each company to maintain its own tax rates,
    effective periods, and accounting ledger mappings. This separation improves
    data consistency, reporting, and compliance with statutory tax regulations.
    """

    __tablename__ = "tax_types"

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
        doc="Unique code identifying the tax type.",
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Display name of the tax type.",
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Optional description of the tax type.",
    )

    is_system: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the tax type is predefined by the system.",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Indicates whether the tax type is active.",
    )
