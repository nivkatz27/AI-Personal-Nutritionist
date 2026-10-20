from datetime import datetime
from math import isfinite
from typing import Literal

from pydantic import BaseModel, field_validator, model_validator, ConfigDict


# Defines the expected structure of the nutrition profile JSON
class NutritionProfileInput(BaseModel):
    age: int
    gender: Literal["male", "female"]
    weight_kg: float
    height_cm: float
    workouts_per_week: int
    avg_workout_minutes: int
    workout_intensity: Literal["low", "moderate", "high"]
    daily_activity: Literal["sedentary", "lightly_active", "active", "very_active"]
    goal: Literal["maintain", "bulk", "cut"]

    # Validate several fields using the same rule
    @field_validator("age", "weight_kg", "height_cm")
    @classmethod
    def must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("must be greater than 0")
        return value

    @field_validator("workouts_per_week")
    @classmethod
    def validate_workouts_per_week(cls, value: int) -> int:
        if not 0 <= value <= 7:
            raise ValueError("must be between 0 and 7")
        return value

    @field_validator("avg_workout_minutes")
    @classmethod
    def validate_avg_workout_minutes(cls, value: int) -> int:
        if value < 0:
            raise ValueError("cannot be negative")
        return value

    # Validate that avg_workout_minutes is consistent with workouts_per_week
    @model_validator(mode="after")
    def validate_workout_minutes_for_active_schedule(self):
        if self.workouts_per_week > 0 and self.avg_workout_minutes <= 0:
            raise ValueError("avg_workout_minutes must be greater than 0 when workouts_per_week is greater than 0")
        if self.workouts_per_week == 0 and self.avg_workout_minutes > 0:
            raise ValueError("avg_workout_minutes must be 0 when workouts_per_week is 0")
        return self



class WorkoutInput(BaseModel):
    workout_type: Literal["resistance_training"]
    duration_minutes: int
    intensity: Literal["low", "moderate", "high"]

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_minutes(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value


class WorkoutCaloriesRequest(BaseModel):
    weight_kg: float
    # The nested workout data is validated as a WorkoutInput object.
    workout: WorkoutInput

    @field_validator("weight_kg")
    @classmethod
    def validate_weight_kg(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("weight_kg must be greater than 0")
        return value

# Defines the structure for updating a nutrition profile, allowing partial updates.
class NutritionProfileUpdate(BaseModel):
    age: int | None = None
    gender: Literal["male", "female"] | None = None
    weight_kg: float | None = None
    height_cm: float | None = None
    workouts_per_week: int | None = None
    avg_workout_minutes: int | None = None
    workout_intensity: Literal["low", "moderate", "high"] | None = None
    daily_activity: Literal["sedentary", "lightly_active", "active", "very_active"] | None = None
    goal: Literal["maintain", "bulk", "cut"] | None = None

    # "*" applies this validator to every field. mode="before" checks supplied raw
    # values before Pydantic converts them; omitted fields receive their defaults
    # without running this validator. This distinguishes omission from explicit null.
    @field_validator("*", mode="before")
    @classmethod
    def reject_explicit_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("cannot be null; omit the field to leave it unchanged")
        return value

    @field_validator("age", "weight_kg", "height_cm")
    @classmethod
    def must_be_positive(cls, value: float) -> float:
        return NutritionProfileInput.must_be_positive(value)

    @field_validator("workouts_per_week")
    @classmethod
    def validate_workouts_per_week(cls, value: int) -> int:
        return NutritionProfileInput.validate_workouts_per_week(value)

    @field_validator("avg_workout_minutes")
    @classmethod
    def validate_avg_workout_minutes(cls, value: int) -> int:
        return NutritionProfileInput.validate_avg_workout_minutes(value)



class NutritionProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    age: int
    gender: Literal["male", "female"]
    weight_kg: float
    height_cm: float
    workouts_per_week: int
    avg_workout_minutes: int
    workout_intensity: Literal["low", "moderate", "high"]
    daily_activity: Literal["sedentary", "lightly_active", "active", "very_active"]
    goal: Literal["maintain", "bulk", "cut"]
    created_at: datetime  

# Represents a single food item provided by the user.
# Nutrition values will be fetched later from an external nutrition API.
class MealItemInput(BaseModel):
    food_name: str
    quantity_g: float

    # Ensure the food name is not empty or only whitespace.
    @field_validator("food_name")
    @classmethod
    def validate_food_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("food_name cannot be empty")
        return value

    # Ensure the quantity is a positive number.
    @field_validator("quantity_g")
    @classmethod
    def validate_quantity_g(cls, value: float) -> float:
        if not isfinite(value):
            raise ValueError("quantity_g must be finite")
        if value <= 0:
            raise ValueError("quantity_g must be greater than 0")
        return value


# Represents the request body for creating a meal.
# A meal contains one or more food items entered by the user.
class MealCreate(BaseModel):
    items: list[MealItemInput]

    # Validate that the meal is not empty.
    @field_validator("items")
    @classmethod
    def validate_items(cls, value: list[MealItemInput]) -> list[MealItemInput]:
        if not value:
            raise ValueError("items cannot be empty")
        return value
