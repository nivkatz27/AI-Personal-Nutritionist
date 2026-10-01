from fastapi import FastAPI
from fastapi import Depends, HTTPException

## SQLAlchemy database session type used by the database dependency.
from sqlalchemy.orm import Session

# Import the function that creates a database session for each request.
from database import get_db
# Import the orm model NutritionProfile for database operations.
from db_models import NutritionProfile


from calories_calculations import (
    calculate_bmr,
    calculate_tdee,
    calculate_workout_calories,
    calculate_daily_calorie_target,
)

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


@app.post("/nutrition/tdee")
def get_tdee(profile: NutritionProfileInput):
    tdee = calculate_tdee(profile)
    return {"tdee": tdee}


@app.get("/")  # Handle GET requests to the root path "/"
def read_root():
    return {"message": "API is running"}

@app.post("/nutrition/daily-goal-calories")
def get_daily_goal_calories(profile: NutritionProfileInput):

    daily_goal_calories = calculate_daily_calorie_target(profile)

    return {"daily_goal_calories": daily_goal_calories}


# Retrieve a nutrition profile from the database using its ID.
# Return 404 if no profile with that ID exists.
@app.get("/nutrition/profiles/{profile_id}")
def get_nutrition_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.get(NutritionProfile, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Nutrition profile not found"
        )

    return {
        "id": profile.id,
        "age": profile.age,
        "gender": profile.gender,
        "weight_kg": profile.weight_kg,
        "height_cm": profile.height_cm,
        "workouts_per_week": profile.workouts_per_week,
        "avg_workout_minutes": profile.avg_workout_minutes,
        "workout_intensity": profile.workout_intensity,
        "daily_activity": profile.daily_activity,
        "goal": profile.goal,
        "created_at": profile.created_at,
    }
