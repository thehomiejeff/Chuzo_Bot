import random
from config import CRAFTING_OPTIONS, HIDDEN_RECIPES
from typing import Optional

def craft_item(category: str, chosen_material: str) -> str:
    """
    Attempts to craft an item in the given category using the chosen material.
    
    Args:
        category (str): The crafting category (e.g., 'weapon', 'potion', 'artifact').
        chosen_material (str): The material the user wants to use.
    
    Returns:
        str: A message indicating the result of the crafting attempt.
    """
    options = CRAFTING_OPTIONS.get(category)
    if not options:
        return f"No such category: {category}"
    
    material_data = options.get("materials", {}).get(chosen_material)
    if not material_data:
        return f"Material '{chosen_material}' not found in category '{category}'."
    
    success_rate = material_data["success_rate"]
    if random.random() <= success_rate:
        crafted_item = random.choice(options["items"])
        return f"Success! You crafted a {crafted_item}."
    else:
        return "Crafting failed, try again."

def check_hidden_recipe(material1: str, material2: str) -> Optional[str]:
    """
    Checks if a hidden recipe exists for the given combination of materials.
    
    Args:
        material1 (str): The first material.
        material2 (str): The second material.
    
    Returns:
        Optional[str]: The special item if a hidden recipe exists, otherwise None.
    """
    return HIDDEN_RECIPES.get((material1, material2)) or HIDDEN_RECIPES.get((material2, material1))
