import json
from pathlib import Path

def load_recipes():
    """Load recipes from the JSON file."""
    recipe_file = Path("data/recipes.json")
    if not recipe_file.exists():
        return []
    
    with open(recipe_file, "r") as f:
        return json.load(f)

def search_recipes(query="", cuisine=None, diet=None):
    """Search recipes based on criteria."""
    recipes = load_recipes()
    
    # Filter recipes based on search criteria
    if query:
        recipes = [r for r in recipes if query.lower() in r["name"].lower()]
    if cuisine:
        recipes = [r for r in recipes if any(c in r["cuisine"] for c in cuisine)]
    if diet:
        recipes = [r for r in recipes if all(d in r["diet"] for d in diet)]
    
    return recipes
