from typing import Literal

from pydantic import BaseModel, field_validator, model_validator


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
    goal: str

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

    @model_validator(mode="after")
    def validate_workout_minutes_for_active_schedule(self):
        if self.workouts_per_week > 0 and self.avg_workout_minutes <= 0:
            raise ValueError("avg_workout_minutes must be greater than 0 when workouts_per_week is greater than 0")
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
