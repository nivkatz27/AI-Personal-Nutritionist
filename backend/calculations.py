from models import NutritionProfileInput, WorkoutInput


# MET values are kept explicit so they are easy to adjust later.
# MET - measures how much energy an activity uses compared to resting.
RESISTANCE_TRAINING_MET = {
    "low": 3.5,
    "moderate": 5.0,
    "high": 6.0,
}


def calculate_bmr(profile: NutritionProfileInput) -> float:
    if profile.gender == "male":
        return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161


def calculate_workout_calories(weight_kg: float, workout: WorkoutInput) -> float:
    # Choose the MET for the validated workout intensity.
    met = RESISTANCE_TRAINING_MET[workout.intensity]
    # MET formula: kcal per minute = MET * 3.5 * body weight (kg) / 200
    kcal_per_minute = met * 3.5 * weight_kg / 200
    # The total is the per-minute burn multiplied by the workout length.
    return kcal_per_minute * workout.duration_minutes
