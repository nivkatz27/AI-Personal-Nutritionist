# Nutrient Target Calculation Methodology

AI Personal Nutritionist converts an estimated daily calorie target into practical daily goals for protein, fat, and carbohydrates. The calculation is deterministic: it uses the nutrition profile and the calorie target already produced by our calorie calculation engine. These are initial targets for generally healthy adults who train, not individually measured requirements.

## How we calculate the targets

### 1. Protein: body weight and goal

Protein is calculated from body weight, using a goal-specific default:

- Maintenance: **1.8 g/kg/day**
- Bulking: **2.0 g/kg/day**
- Cutting: **2.2 g/kg/day**

`protein_g = round(weight_kg * protein_factor)`

The defaults reflect a practical choice within or near research-informed ranges for resistance-trained adults. The International Society of Sports Nutrition (ISSN) identifies **1.4–2.0 g/kg/day** as sufficient for most exercising people and discusses potentially higher intakes during energy restriction; a review of off-season bodybuilding nutrition suggests **1.6–2.2 g/kg/day**. The specific three goal values above are **our application defaults**, not thresholds uniquely prescribed by these papers. In particular, higher cutting recommendations in some research use *fat-free mass* rather than total body weight; our MVP does not calculate fat-free mass.

### 2. Fat: a moderate share of calories

We allocate **25% of the daily calorie target** to fat:

`fat_g = round(daily_calories * 0.25 / 9)`

This keeps fat moderate while leaving energy available for carbohydrate intake. The U.S. National Academies' reference range for adults is **20–35% of total energy from fat**. Choosing exactly 25% is a **product default**, not a unique physiological optimum. The current calculation does not separately enforce a grams-per-kilogram fat minimum.

### 3. Carbohydrates: remaining calories

Once protein and fat are allocated, carbohydrates receive the remaining calorie budget:

`carbohydrate_g = round((daily_calories - protein_g * 4 - fat_g * 9) / 4)`

We use the conventional energy approximations of **4 kcal/g for protein**, **9 kcal/g for fat**, and **4 kcal/g for carbohydrates**. Allocating remaining calories to carbohydrates is also consistent with the off-season bodybuilding nutrition review, which emphasizes sufficient carbohydrate availability for training. Carbohydrate goals therefore respond to the user's total calorie target rather than being fixed at one grams-per-kilogram value. The implementation should reject a profile if the remaining carbohydrate budget is negative rather than silently return a negative target.

## Example: bulking

For a **65 kg** user with an existing daily bulking target of **2,988 kcal**:

- Protein: `65 × 2.0 = 130 g` (**520 kcal**).
- Fat: `round(2,988 × 0.25 / 9) = 83 g` (**747 kcal**).
- Carbohydrates: `round((2,988 − 520 − 747) / 4) = 430 g` (**1,720 kcal**).

The rounded targets add up to **2,987 kcal**. A difference of a few calories is expected when gram targets are rounded to whole numbers; the original target remains **2,988 kcal**.

## Assumptions and limitations

The protein factors, fixed 25% fat share, and whole-gram rounding are transparent MVP choices informed by published nutrition guidance. They are not a personalized dietary prescription. Individual needs may depend on training demands, body composition, food preferences, medical circumstances, and progress over time. If the calorie target or the target allocation changes in a future version, the carbohydrate remainder should be recalculated accordingly.

## Sources

- Jäger R, et al. (2017). [International Society of Sports Nutrition Position Stand: protein and exercise](https://pubmed.ncbi.nlm.nih.gov/28642676/). Protein guidance for exercising adults and discussion of higher intake during energy restriction.
- Morton RW, et al. (2018). [A systematic review, meta-analysis and meta-regression of protein supplementation and resistance-training outcomes](https://pubmed.ncbi.nlm.nih.gov/28698222/). Context for protein intake and resistance training; does not prescribe our exact defaults.
- Iraki J, et al. (2019). [Nutrition Recommendations for Bodybuilders in the Off-Season: A Narrative Review](https://pmc.ncbi.nlm.nih.gov/articles/PMC6680710/). Protein and fat ranges and allocation of remaining calories to carbohydrates.
- National Academies / Institute of Medicine. [Dietary Reference Intakes: Acceptable Macronutrient Distribution Ranges](https://www.nationalacademies.org/read/10925/chapter/25). Adult fat intake reference range of 20–35% of energy.

For the upstream daily calorie estimate, see [Calorie Calculation Methodology](calorie-calculation-methodology.md).
