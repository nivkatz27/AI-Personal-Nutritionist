from fastapi import FastAPI
from fastapi import Depends, HTTPException

# SQLAlchemy database session type used by the database dependency.
from sqlalchemy.orm import Session

# Import the function that creates a database session for each request.
from database import get_db
# Import the ORM model NutritionProfile for database operations.
from db_models import NutritionProfile

from calories_calculations import (
    calculate_bmr,
    calculate_tdee,
    calculate_workout_calories,
    calculate_daily_calorie_target,
)

from pydantic_models import NutritionProfileInput, NutritionProfileResponse, WorkoutCaloriesRequest, NutritionProfileUpdate
from nutrient_calculations import calculate_daily_nutrient_targets

# Create a FastAPI object with a title
app = FastAPI(title="AI Personal Nutritionist API")


# Receive and validate a nutrition profile, then save it to the database.
# Return the saved profile including database-generated fields such as ID and creation time.
@app.post("/nutrition/profile", response_model=NutritionProfileResponse)
def create_nutrition_profile(
    profile: NutritionProfileInput,
    db: Session = Depends(get_db),
):
    # We use model_dump() to convert the Pydantic model to a dictionary for the ORM constructor.
    # ** - Unpack the dictionary into keyword arguments.
    db_profile = NutritionProfile(**profile.model_dump())
    # Add the new profile object to the current database session.
    db.add(db_profile)
    # Commit the session to save the new profile to the database.
    db.commit()
    # Reload the object from PostgreSQL to get database-generated values
    # such as the ID and created_at timestamp.
    db.refresh(db_profile)
    return db_profile


# Use age, gender, weight, and height from the submitted profile
# to estimate the user's basal metabolic rate (BMR) in calories per day.
@app.post("/nutrition/bmr")
def get_bmr(profile: NutritionProfileInput):
    bmr = calculate_bmr(profile)
    return {"bmr": bmr}


# Estimate calories burned during a workout using the user's weight,
# workout duration, workout type, and intensity.
@app.post("/nutrition/workout-calories")
def get_workout_calories(payload: WorkoutCaloriesRequest):
    # payload.workout is already a validated WorkoutInput object.
    estimated_calories = calculate_workout_calories(
        payload.weight_kg,
        payload.workout
    )
    return {"estimated_calories": estimated_calories}


# Estimate the user's total daily energy expenditure (TDEE).
# This combines baseline daily activity with estimated workout energy expenditure.
@app.post("/nutrition/tdee")
def get_tdee(profile: NutritionProfileInput):
    tdee = calculate_tdee(profile)
    return {"tdee": tdee}


# Provide a simple health check to confirm that the API is running and responding.
@app.get("/")
def read_root():
    return {"message": "API is running"}


# Calculate the user's daily calorie target based on their goal:
# maintenance, bulking, or cutting.
@app.post("/nutrition/daily-goal-calories")
def get_daily_goal_calories(profile: NutritionProfileInput):
    daily_goal_calories = calculate_daily_calorie_target(profile)
    return {"daily_goal_calories": daily_goal_calories}


# Calculate the user's daily calorie and macronutrient targets.
# Returns recommended protein, fat, and carbohydrate intake in grams.
@app.post("/nutrition/daily-nutrient-targets")
def get_daily_nutrient_targets(profile: NutritionProfileInput):
    return calculate_daily_nutrient_targets(profile)


# Retrieve a nutrition profile from the database using its ID.
# Return 404 if no profile with that ID exists.
@app.get("/nutrition/profiles/{profile_id}", response_model=NutritionProfileResponse)
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

# Update an existing nutrition profile in the database using its ID.
# Return 404 if no profile with that ID exists. 
@app.patch("/nutrition/profiles/{profile_id}", response_model=NutritionProfileResponse)
def update_nutrition_profile(
    profile_id: int,
    profile_update: NutritionProfileUpdate,
    db: Session = Depends(get_db),
):
    profile = db.get(NutritionProfile, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Nutrition profile not found"
        )

    # Convert the Pydantic model to a dictionary, only from fields that were provided in the request.
    update_data = profile_update.model_dump(exclude_unset=True)

    # Check the final schedule before changing the profile, using stored values for omitted fields.
    final_workouts_per_week = update_data.get(
        "workouts_per_week",
        profile.workouts_per_week,
    )
    final_avg_workout_minutes = update_data.get(
        "avg_workout_minutes",
        profile.avg_workout_minutes,
    )
    if final_workouts_per_week > 0 and final_avg_workout_minutes <= 0:
        raise HTTPException(
            status_code=422,
            detail="avg_workout_minutes must be greater than 0 when workouts_per_week is greater than 0",
        )
    if final_workouts_per_week == 0 and final_avg_workout_minutes > 0:
        raise HTTPException(
            status_code=422,
            detail="avg_workout_minutes must be 0 when workouts_per_week is 0",
        )

    # Update the fields of the existing profile with the new values. 
    for field, value in update_data.items():
        setattr(profile, field, value)
    # Save the updated profile values to PostgreSQL.
    db.commit()
    # Reload the profile from the database to keep the ORM object up to date.
    db.refresh(profile)
    # Return the updated profile.
    return profile

# Delete an existing nutrition profile from the database using its ID.
# Return 404 if no profile with that ID exists.
@app.delete("/nutrition/profiles/{profile_id}")
def delete_nutrition_profile(
    profile_id: int,
    db: Session = Depends(get_db),
):
    profile = db.get(NutritionProfile, profile_id)

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Nutrition profile not found"
        )

    # Remove the profile from the current database session.
    db.delete(profile)
    # Commit the session to delete the profile from the database.
    db.commit()
    return {"message": "Nutrition profile deleted successfully"}
