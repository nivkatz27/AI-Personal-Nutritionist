from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, field_validator

# Create a FAstAPI object with a title
app = FastAPI(title="AI Personal Nutritionist API")


# Defines the expected structure of the nutrition profile JSON
class NutritionProfileInput(BaseModel):
    age: int
    gender: Literal["male", "female"]
    weight_kg: float
    height_cm: float
    workouts_per_week: int
    avg_workout_minutes: int
    workout_intensity: str
    daily_activity: str
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


# MET values are kept explicit so they are easy to adjust later.
RESISTANCE_TRAINING_MET = {
    "low": 3.5,
    "moderate": 5.0,
    "high": 6.0,
}


@app.post("/nutrition/profile")
def create_nutrition_profile(profile: NutritionProfileInput):
    # Convert the validated Pydantic object to a Python dict
    return profile.model_dump()


def calculate_bmr(profile: NutritionProfileInput) -> float:
    if profile.gender == "male":
        return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161


@app.post("/nutrition/bmr")
def get_bmr(profile: NutritionProfileInput):
    bmr = calculate_bmr(profile)
    return {"bmr": bmr}


def calculate_workout_calories(weight_kg: float, workout: WorkoutInput) -> float:
    # Choose the MET for the validated workout intensity.
    met = RESISTANCE_TRAINING_MET[workout.intensity]
    # MET formula: kcal per minute = MET * 3.5 * body weight (kg) / 200
    kcal_per_minute = met * 3.5 * weight_kg / 200
    # The total is the per-minute burn multiplied by the workout length.
    return kcal_per_minute * workout.duration_minutes


@app.post("/nutrition/workout-calories")
def get_workout_calories(payload: WorkoutCaloriesRequest):
    # payload.workout is already a validated WorkoutInput object.
    estimated_calories = calculate_workout_calories(payload.weight_kg, payload.workout)
    return {"estimated_calories": estimated_calories}


@app.get("/")  # Handle GET requests to the root path "/"
def read_root():
    return {"message": "API is running"}


