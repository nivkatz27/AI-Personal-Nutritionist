from fastapi import FastAPI
from pydantic import BaseModel, field_validator

# Create a FAstAPI object with a title
app = FastAPI(title="AI Personal Nutritionist API") 

# Defines the expected structure of the nutrition profile JSON
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

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        valid_genders = {"male", "female"}
        if value.lower() not in valid_genders:
            raise ValueError("gender must be 'male' or 'female'")
        return value.lower()

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


@app.get("/") # Handle GET requests to the root path "/"
def read_root():
    return {"message": "API is running"}


