# src/models/item.py

from dataclasses import dataclass

@dataclass
class Item:
    name: str
    rarity: str  # For example: "common", "rare", "legendary", "hidden"
