from fastapi import FastAPI

from calculations import calculate_bmr, calculate_workout_calories
from models import NutritionProfileInput, WorkoutCaloriesRequest

# Create a FastAPI object with a title
app = FastAPI(title="AI Personal Nutritionist API")


@app.post("/nutrition/profile")
def create_nutrition_profile(profile: NutritionProfileInput):
    # Convert the validated Pydantic object to a Python dict
    return profile.model_dump()


@app.post("/nutrition/bmr")
def get_bmr(profile: NutritionProfileInput):
    bmr = calculate_bmr(profile)
    return {"bmr": bmr}


@app.post("/nutrition/workout-calories")
def get_workout_calories(payload: WorkoutCaloriesRequest):
    # payload.workout is already a validated WorkoutInput object.
    estimated_calories = calculate_workout_calories(payload.weight_kg, payload.workout)
    return {"estimated_calories": estimated_calories}


@app.get("/")  # Handle GET requests to the root path "/"
def read_root():
    return {"message": "API is running"}


