from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

class NutritionProfile(Base):
    __tablename__ = "nutrition_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column()

    gender: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    weight_kg: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    height_cm: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False
    )

    workouts_per_week: Mapped[int] = mapped_column(
        nullable=False
    )

    avg_workout_minutes: Mapped[int] = mapped_column(
        nullable=False
    )

    workout_intensity: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    daily_activity: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    goal: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )