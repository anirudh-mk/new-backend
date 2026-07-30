from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import BaseModel

if TYPE_CHECKING:
    from app.models.sales.order.sales_order import SalesOrder
    from app.models.user.user import User


class SalesOrderRevision(BaseModel):
    """
    Represents a revision/version of a Sales Order.

    Purpose:
        Sales Order Revision maintains a complete version
        history of a Sales Order whenever significant
        business changes occur.

        Instead of overwriting important information,
        each revision records what changed, who changed it,
        when it was changed, and why it was changed.

        This provides a complete audit trail and allows
        users to compare revisions or restore previous
        versions if necessary.

        A revision is typically created whenever:

        • Customer changes ordered quantity.
        • Product is added or removed.
        • Price changes.
        • Discount changes.
        • Delivery date changes.
        • Terms and conditions change.
        • Approval is rejected and edited.
        • Customer requests modifications.

    Examples:

        Revision 1

            Initial Order

        Revision 2

            Added 5 Laptops

        Revision 3

            Updated Delivery Date

        Revision 4

            Changed Selling Price

    Workflow:

          Sales Order
                │
         Create Revision
                │
                ▼
        Sales Order Revision
                │
                ▼
         Approval Workflow
                │
                ▼
        Delivery / Invoice

    Benefits:

        • Complete audit trail.
        • Version management.
        • Easy rollback.
        • Approval history.
        • Customer change tracking.
        • Legal compliance.
        • Internal accountability.
        • Historical reporting.
        • Comparison between revisions.
        • Enterprise document control.

    Relationships:

            SalesOrder
                 │
                 ▼
       SalesOrderRevision
                 │
                 ▼
               User

    Example:

        Sales Order

            SO-000245

        Revision

            3

        Reason

            Customer requested additional quantity.

        Changed By

            John Smith

    Notes:

        • One Sales Order can have many revisions.
        • Revision numbers should be sequential.
        • Previous revisions should never be modified.
        • Snapshot JSON may be stored externally if required.
        • Used for audit and compliance.
        • Supports approval rollback.
        • Supports document comparison.

    This model is referenced throughout
    Sales,
    CRM,
    Workflow,
    Inventory,
    Accounting,
    Audit,
    Compliance,
    Reporting,
    and Customer Service modules.
    """

    __tablename__ = "sales_order_revisions"

    sales_order_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales_orders.id"),
        nullable=False,
        index=True,
        doc="Reference to the Sales Order.",
    )

    revision_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        doc="Sequential revision number.",
    )

    revision_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Reason for creating the revision.",
    )

    changed_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        doc="User who made the revision.",
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        doc="Date and time when the revision was created.",
    )

    status_before: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Sales Order status before the revision.",
    )

    status_after: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        doc="Sales Order status after the revision.",
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Summary of the changes made in this revision.",
    )

    snapshot_reference: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        doc="Reference to the stored JSON snapshot or document version.",
    )

    # ---------------------------------------------------------
    # Relationships
    # ---------------------------------------------------------

    sales_order: Mapped["SalesOrder"] = relationship(
        back_populates="revisions",
    )

    changed_by: Mapped["User"] = relationship(
        back_populates="sales_order_revisions",
    )