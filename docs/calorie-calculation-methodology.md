[English](calorie-calculation-methodology.md) | [עברית](calorie-calculation-methodology-he.md)

# How We Calculate Daily Calorie Targets

## Overview

AI Personal Nutritionist estimates a starting daily calorie target using a user's age, sex, weight, height, lifestyle activity, and resistance-training schedule. It first estimates total daily energy expenditure (TDEE), then adjusts that estimate for maintenance, bulking, or cutting. The result is a starting point, not a measurement of an individual's metabolism.

## Calculation method

We estimate resting energy expenditure using the Mifflin–St Jeor equation. Weight is entered in kilograms, height in centimeters, and age in years. [1]

For men: BMR = 10 × weight + 6.25 × height − 5 × age + 5.

For women: BMR = 10 × weight + 6.25 × height − 5 × age − 161.

To account for ordinary daily activity, we multiply BMR by the selected lifestyle factor: 1.2 for sedentary, 1.375 for lightly active, 1.5 for active, or 1.9 for very active. This gives an approximate daily baseline, not a direct measurement of movement. Cronometer's energy-expenditure documentation informed our approach to activity accounting. [3]

We estimate resistance-training expenditure using MET values, a standard way to describe the energy cost of physical activities. The current app maps low, moderate, and high workout intensity to 3.5, 5.0, and 6.0 MET respectively. This three-level mapping is a product simplification informed by resistance-training examples in the Adult Compendium of Physical Activities. [2]

Workout calories = MET × 3.5 × weight (kg) ÷ 200 × workout minutes.

To estimate the additional energy attributable to exercise, we subtract the standard 1-MET resting expenditure during the workout and spread the remaining weekly workout calories over seven days. We then reduce possible overlap with activity already included in the lifestyle baseline. The overlap estimate is the baseline expenditure above BMR, multiplied by average daily workout minutes divided by 960 minutes (an assumed 16-hour waking day). This is our own approximate adjustment, inspired by the time-based activity accounting described by Cronometer; it does not reproduce or scientifically validate Cronometer's entire model. [3]

Estimated TDEE is the lifestyle baseline plus the adjusted average daily workout expenditure. The starting eating target is TDEE for maintenance, TDEE + 300 kcal for bulking, or TDEE − 300 kcal for cutting, rounded to a whole number.

## Example

For a 27-year-old man weighing 65 kg and measuring 177 cm, with an active lifestyle and four 90-minute high-intensity resistance workouts each week, estimated BMR is 1,626.25 kcal/day and the lifestyle baseline is 2,439.38 kcal/day. One workout is estimated at 614.25 kcal in total, or 511.88 kcal beyond standardized resting expenditure.

Averaging the additional exercise expenditure over the week gives 292.50 kcal/day. The estimated overlap with baseline activity is 43.56 kcal/day, leaving 248.94 kcal/day of adjusted exercise expenditure. Estimated TDEE is therefore 2,688.31 kcal/day, and the starting bulking target is 2,988 kcal/day. Calculations use unrounded intermediate values.

## Assumptions and limitations

BMR equations and MET values are estimates; actual energy needs vary between people. Self-reported activity and workout intensity may be imprecise, particularly when training includes long rest periods. The 16-hour overlap adjustment and fixed ±300 kcal goal adjustment are our MVP design choices, not individualized, scientifically validated prescriptions. The current model does not calculate the thermic effect of food separately or calibrate estimates against logged intake and weight trends. Future targets should be adjusted according to observed progress.

## Sources

Mifflin et al. (1990), “A new predictive equation for resting energy expenditure in healthy individuals,” *The American Journal of Clinical Nutrition*. [Original study on PubMed](https://pubmed.ncbi.nlm.nih.gov/2305711/). [1]

2024 Adult Compendium of Physical Activities. [Conditioning and resistance-training MET values](https://pacompendium.com/conditioning-exercise/). [2]

Cronometer, official product documentation: [Energy Expenditure](https://support.cronometer.com/hc/en-us/articles/31974307318420-Energy-Expenditure) and [Energy Summary](https://support.cronometer.com/hc/en-us/articles/31118923481876-Energy-Summary). Used as product-design references, not as validation of our custom overlap formula. [3]
