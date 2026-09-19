from models import NutritionProfileInput, WorkoutInput


# MET values are kept explicit so they are easy to adjust later.
# MET - measures how much energy an activity uses compared to resting.
RESISTANCE_TRAINING_MET = {
    "low": 3.5,
    "moderate": 5.0,
    "high": 6.0,
}


# These baseline factors provide an approximate energy expenditure estimate, not an exact measurement of NEAT.
# Cronometer's categories can include exercise, so we should not automatically add EAT without checking overlap.
BASELINE_ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "active": 1.5,
    "very_active": 1.9,
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


def calculate_baseline_daily_calories(profile: NutritionProfileInput) -> float:
    # Start with BMR, then scale by the selected lifestyle factor.
    bmr = calculate_bmr(profile)
    activity_factor = BASELINE_ACTIVITY_FACTORS[profile.daily_activity]
    return bmr * activity_factor


def calculate_average_daily_net_workout_calories(
    weight_kg: float,
    workout: WorkoutInput,
    workouts_per_week: int
) -> float:

    # Total calories burned during one workout.
    gross_calories = calculate_workout_calories(weight_kg, workout)

    # Estimated resting calories during the workout.
    resting_calories = 3.5 * weight_kg / 200 * workout.duration_minutes

    # Estimate resting calories using 1 MET (3.5 mL of oxygen per kg of body weight per minute).
    # Divide by 200 to convert oxygen to calories (1000 mL per liter, about 5 kcal per liter).
    # Multiply by workout duration; subtract from gross calories to get net EAT.
    net_calories = gross_calories - resting_calories

    # Average daily net exercise expenditure.
    return net_calories * workouts_per_week / 7


def calculate_adjusted_daily_workout_calories(profile: NutritionProfileInput) -> float:
    if profile.workouts_per_week == 0:
        return 0

    # Create the workout model from the nutrition profile for a consistent estimate.
    workout = WorkoutInput(
        workout_type="resistance_training",
        duration_minutes=profile.avg_workout_minutes,
        intensity=profile.workout_intensity,
    )

    # Average daily exercise calories above resting expenditure.
    net_eat = calculate_average_daily_net_workout_calories(
        profile.weight_kg,
        workout,
        profile.workouts_per_week,
    )

    # Estimate the baseline activity component above BMR.
    baseline_above_bmr = calculate_baseline_daily_calories(profile) - calculate_bmr(profile)

    # Convert weekly workout time to a daily average before estimating overlap with baseline activity.
    daily_workout_minutes = workout.duration_minutes * profile.workouts_per_week / 7

    # This MVP heuristic assumes exercise replaces some of the baseline activity during a 16-hour waking day.
    replaced_baseline_activity = baseline_above_bmr * (daily_workout_minutes / (16 * 60))

    # Return net exercise calories after accounting for the overlap with baseline activity.
    return net_eat - replaced_baseline_activity


def calculate_tdee(profile: NutritionProfileInput) -> float:
    baseline = calculate_baseline_daily_calories(profile)
    adjusted_eat = calculate_adjusted_daily_workout_calories(profile)
    return baseline + adjusted_eat
