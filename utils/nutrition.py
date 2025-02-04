def calculate_daily_nutrition(meals):
    """Calculate nutrition totals for a day's meals."""
    totals = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0
    }
    
    for meal in meals:
        for nutrient in totals:
            totals[nutrient] += meal.get(nutrient, 0)
    
    return totals

def get_nutrition_summary(start_date, end_date, meals):
    """Get nutrition summary for a date range."""
    daily_totals = []
    
    # Calculate daily totals
    current_date = start_date
    while current_date <= end_date:
        daily_meals = [m for m in meals if m["date"] == current_date]
        daily_totals.append(calculate_daily_nutrition(daily_meals))
        current_date += 1
        
    return daily_totals
