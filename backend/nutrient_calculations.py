from calories_calculations import calculate_daily_calorie_target
from models import NutritionProfileInput


PROTEIN_FACTORS = {
    "maintain": 1.8,
    "bulk": 2.0,
    "cut": 2.2,
}


def calculate_protein_target(profile: NutritionProfileInput) -> int:
    # Scale protein with body weight and the allocation chosen for each goal.
    protein_factor = PROTEIN_FACTORS[profile.goal]
    return round(profile.weight_kg * protein_factor)


def calculate_fat_target(profile: NutritionProfileInput) -> int:
    daily_calories = calculate_daily_calorie_target(profile)
    # Reserve 25% of the calorie budget for fat, which supplies 9 kcal per gram.
    return round(daily_calories * 0.25 / 9)


def calculate_carbohydrate_target(profile: NutritionProfileInput) -> int:
    # Share the allocation and budget validation used by the complete targets.
    return calculate_daily_nutrient_targets(profile)["carbs_g"]


def calculate_daily_nutrient_targets(profile: NutritionProfileInput) -> dict[str, int]:
    daily_calories = calculate_daily_calorie_target(profile)
    protein_g = calculate_protein_target(profile)
    fat_g = calculate_fat_target(profile)

    # Use rounded allocations so carbohydrates fit the grams actually returned.
    remaining_calories = daily_calories - protein_g * 4 - fat_g * 9
    if remaining_calories < 0:
        raise ValueError(
            "Protein and fat targets exceed the daily calorie target; "
            "the remaining calorie budget for carbohydrates is negative."
        )
    carbs_g = round(remaining_calories / 4)

    return {
        "daily_calories": daily_calories,
        "protein_g": protein_g,
        "fat_g": fat_g,
        "carbs_g": carbs_g,
    }
