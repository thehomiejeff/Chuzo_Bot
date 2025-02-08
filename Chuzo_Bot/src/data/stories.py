STORY_ONE = {
    "title": "The Lost Relic",
    "stages": [
        {
            "prompt": "You are tasked with finding the lost relic of Brynthe. Do you 'search the forest' or 'ask the villagers'?",
            "valid_inputs": ["search the forest", "ask the villagers"],
            "response": {
                "search the forest": "You venture into the dark forest, where you hear strange whispers.",
                "ask the villagers": "The villagers tell you of a cave where the relic might be hidden."
            }
        },
        {
            "prompt": "You find a mysterious door. Do you 'open it' or 'look for another way'?",
            "valid_inputs": ["open it", "look for another way"],
            "response": {
                "open it": "The door creaks open, revealing the lost relic!",
                "look for another way": "You find a hidden passage, but it leads to a dead end."
            }
        }
    ],
    "reward": "Relic of Brynthe"
}

STORY_TWO = {
    "title": "The Sorcerer's Curse",
    "stages": [
        {
            "prompt": "A curse has befallen the kingdom. Do you 'seek the wise elder' or 'investigate the ruins'?",
            "valid_inputs": ["seek the wise elder", "investigate the ruins"],
            "response": {
                "seek the wise elder": "The elder tells you the curse can be broken with the Phoenix Amulet.",
                "investigate the ruins": "You find ancient texts hinting at the curse's origin."
            }
        },
        {
            "prompt": "You must choose: 'craft the Phoenix Amulet' or 'confront the sorcerer'.",
            "valid_inputs": ["craft the Phoenix Amulet", "confront the sorcerer"],
            "response": {
                "craft the Phoenix Amulet": "You gather materials and craft the amulet, breaking the curse!",
                "confront the sorcerer": "You face the sorcerer but are overwhelmed by his dark magic."
            }
        }
    ],
    "reward": "Phoenix Amulet"
}
