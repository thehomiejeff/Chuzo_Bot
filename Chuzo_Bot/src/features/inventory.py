# src/features/inventory.py

from src.models.item import Item

def get_inventory(context):
    """Retrieve the user's inventory (a list of Item objects)."""
    return context.user_data.get('inventory', [])

def add_to_inventory(context, item: Item):
    """Add an Item instance to the user's inventory."""
    if 'inventory' not in context.user_data:
        context.user_data['inventory'] = []
    context.user_data['inventory'].append(item)
