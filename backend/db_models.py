from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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

    # Relationship to all meals that belong to this nutrition profile.
    meals: Mapped[list["Meal"]] = relationship(
        back_populates="nutrition_profile",
    )


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Foreign key to the NutritionProfile table
    nutrition_profile_id: Mapped[int] = mapped_column(
        ForeignKey("nutrition_profiles.id"),
        nullable=False
    )

    eaten_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    # Relationship to the MealItem table, allowing access to all items in this meal.
    items: Mapped[list["MealItem"]] = relationship(
        back_populates="meal",
    )

    # Relationship back to the nutrition profile that owns this meal.
    nutrition_profile: Mapped["NutritionProfile"] = relationship(
        back_populates="meals",
    )


class MealItem(Base):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Each item belongs to a meal through its database foreign key.
    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id"),
        nullable=False
    )

    food_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    quantity_g: Mapped[Decimal | None] = mapped_column(
        Numeric(7, 2),
        nullable=True
    )

    calories: Mapped[Decimal] = mapped_column(
        Numeric(8, 2),
        nullable=False
    )

    protein_g: Mapped[Decimal] = mapped_column(
        Numeric(7, 2),
        nullable=False
    )

    carbs_g: Mapped[Decimal] = mapped_column(
        Numeric(7, 2),
        nullable=False
    )

    fat_g: Mapped[Decimal] = mapped_column(
        Numeric(7, 2),
        nullable=False
    )

    # Relationship to the Meal table, allowing access to the meal this item belongs to.
    meal: Mapped["Meal"] = relationship(
        back_populates="items",
    )
