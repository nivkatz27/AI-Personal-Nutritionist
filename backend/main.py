from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI(title="AI Personal Nutritionist API") # Create a FAstAPI object with a title


class NutritionProfileInput(BaseModel):
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    workouts_per_week: int
    avg_workout_minutes: int
    workout_intensity: str
    daily_activity: str
    goal: str

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


@app.post("/nutrition/profile")
def create_nutrition_profile(profile: NutritionProfileInput):
    return profile.model_dump()


@app.get("/") # Handle GET requests to the root path "/"
def read_root():
    return {"message": "API is running"}


