import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ====================
# Conversation States
# ====================
STORY_IN_PROGRESS = 1
QUEST_IN_PROGRESS = 2
CRAFTING_ITEM, CRAFTING_MATERIAL = range(2)
QUIZ_IN_PROGRESS = 3

# ====================
# Crafting System Configuration
# ====================
CRAFTING_OPTIONS = {
    "weapon": {
        "items": ["Dragonbone Sword", "Phoenix Bow", "Ice Dagger"],
        "materials": {
            "Dragon Scales": {"success_rate": 0.8, "rarity": "rare"},
            "Obsidian": {"success_rate": 0.6, "rarity": "common"},
            "Mithril": {"success_rate": 0.7, "rarity": "uncommon"}
        }
    },
    "potion": {
        "items": ["Elixir of Life", "Potion of Invisibility", "Liquid Lightning"],
        "materials": {
            "Phoenix Feather": {"success_rate": 0.9, "rarity": "legendary"},
            "Stardust": {"success_rate": 0.5, "rarity": "common"},
            "Moonstone": {"success_rate": 0.7, "rarity": "uncommon"}
        }
    },
    "artifact": {
        "items": ["Crown of Stars", "Amulet of Shadows", "Orb of Prophecy"],
        "materials": {
            "Ethereal Essence": {"success_rate": 0.85, "rarity": "rare"},
            "Ancient Relic": {"success_rate": 0.75, "rarity": "uncommon"},
            "Crystal Shard": {"success_rate": 0.6, "rarity": "common"}
        }
    }
}

# Hidden recipes (material combinations that unlock special items)
HIDDEN_RECIPES = {
    ("Phoenix Feather", "Ethereal Essence"): "Phoenix Amulet",
    ("Dragon Scales", "Ancient Relic"): "Dragonheart Gauntlet",
    ("Stardust", "Moonstone"): "Starlight Pendant"
}

# ====================
# Quest System Configuration
# ====================
QUESTS = {
    "find_the_lost_relic": {
        "stages": [
            {
                "prompt": "You find yourself in a dark forest. Do you go 'left' or 'right'?",
                "valid_inputs": ["left", "right"],
                "response": {
                    "left": "You stumble upon a hidden path. It leads to a clearing.",
                    "right": "You encounter a pack of wolves. They chase you back!"
                }
            },
            {
                "prompt": "In the clearing, you see a cave. Do you 'enter' or 'leave'?",
                "valid_inputs": ["enter", "leave"],
                "response": {
                    "enter": "Inside the cave, you find the lost relic!",
                    "leave": "You return home empty-handed."
                }
            }
        ],
        "reward": "Ancient Relic"
    }
}

# ====================
# Quiz Configuration
# ====================
QUIZ_QUESTIONS = [
    {
        "question": "What is the name of the sacred artifact Chuzo protects?",
        "options": ["Orb of Eternity", "Crown of Stars", "Amulet of Shadows"],
        "correct_answer": "Orb of Eternity"
    },
    {
        "question": "What role did Chuzo play in the Great War?",
        "options": ["Healer", "Strategist", "Blacksmith"],
        "correct_answer": "Strategist"
    },
    {
        "question": "Which mythical creature is NOT found in the kingdom?",
        "options": ["Dragon", "Phoenix", "Kraken"],
        "correct_answer": "Kraken"
    },
    {
        "question": "What is the name of the dark sorcerer who threatened the kingdom?",
        "options": ["Malakar", "Zorath", "Necron"],
        "correct_answer": "Malakar"
    },
    {
        "question": "Where did Chuzo grow up?",
        "options": ["Ruins of Brynthe", "Forest of Eldar", "Mountains of Kael"],
        "correct_answer": "Ruins of Brynthe"
    }
]
