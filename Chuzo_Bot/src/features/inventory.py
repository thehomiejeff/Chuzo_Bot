def get_inventory(context):
    """Retrieve the user's inventory."""
    return context.user_data.get('inventory', [])

def add_to_inventory(context, item):
    """Add an item to the user's inventory."""
    if 'inventory' not in context.user_data:
        context.user_data['inventory'] = []
    context.user_data['inventory'].append(item)
