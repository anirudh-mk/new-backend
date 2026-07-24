from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import AuditModel


class Country(AuditModel):
    __tablename__ = "countries"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    iso2: Mapped[str] = mapped_column(
        String(2),
        unique=True,
        nullable=False
    )

    iso3: Mapped[str] = mapped_column(
        String(3),
        unique=True,
        nullable=False
    )

    phone_code: Mapped[str] = mapped_column(
        String(5),
        nullable=False
    )

    currency_code: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    states: Mapped[list["State"]] = relationship(
        back_populates="country",
        cascade="all, delete-orphan",
    )


class State(AuditModel):
    __tablename__ = "states"

    country_id: Mapped[UUID] = mapped_column(
        ForeignKey("countries.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    country: Mapped["Country"] = relationship(
        back_populates="states",
    )

    districts: Mapped[list["District"]] = relationship(
        back_populates="state",
        cascade="all, delete-orphan",
    )


class District(AuditModel):
    __tablename__ = "districts"

    class District(AuditModel):
        __tablename__ = "districts"

        state_id: Mapped[UUID] = mapped_column(
            ForeignKey("states.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

        name: Mapped[str] = mapped_column(
            String(100),
            nullable=False,
        )

        is_active: Mapped[bool] = mapped_column(
            default=True,
            nullable=False,
        )

        state: Mapped["State"] = relationship(
            back_populates="districts",
        )
