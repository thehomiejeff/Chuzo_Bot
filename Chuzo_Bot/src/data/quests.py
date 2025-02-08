# src/data/quests.py

# PHOENIX_CALL_QUEST: A Branching Quest Narrative
PHOENIX_CALL_QUEST = {
    "title": "The Phoenix's Call",
    "stages": [
        {
            "prompt": (
                "At dawn, in the bustling town square, Chuzo stands before a gathered crowd. "
                "The Phoenix Amulet gleams at his side as he proclaims, \"Friends, the flames of destiny have spoken! "
                "I have seen a vision of the Ember Heart, a relic of power hidden in the Inferno Mountains. Who among you will join me?\" \n\n"
                "Choices:\n"
                "A. \"I will join you, for adventure calls!\"\n"
                "B. \"I must stay behind, my duty here is not yet done.\""
            ),
            "choices": {
                "a": {
                    "text": "Boldly, you and the willing companions step forward to answer Chuzo's call.",
                    "next": 1
                },
                "b": {
                    "text": "You decide to remain behind, leaving Chuzo to venture forth alone.",
                    "next": 2
                }
            }
        },
        {
            "prompt": (
                "With a resolute nod, the assembled heroes gather their courage and set forth with Chuzo. "
                "Along a rugged path, the group reaches a fork in the road. Chuzo muses, \"Shall we take the winding trail through the shadowed woods, rich with ancient secrets, "
                "or the direct route along the roaring river, swift and treacherous?\" \n\n"
                "Choices:\n"
                "A. \"The woods, where every shadow whispers wisdom.\"\n"
                "B. \"The river, for its speed may be our ally.\""
            ),
            "choices": {
                "a": {
                    "text": "You choose the winding trail. The dense, mysterious woods test your senses and ignite your curiosity.",
                    "next": 3
                },
                "b": {
                    "text": "You opt for the river path, embracing its relentless current and the promise of swift progress.",
                    "next": 4
                }
            }
        },
        {
            "prompt": (
                "Alone now, Chuzo embarks on the journey by himself. The weight of solitude sharpens his focus and resolve, but the path grows perilous without trusted allies.\n\n"
                "Without the strength of camaraderie, the quest takes a solitary, uncertain turn."
            ),
            "choices": {},
            "reward_item": {"item": "Solitary Emblem", "rarity": "uncommon"}
        },
        {
            "prompt": (
                "Deep in the shadowed woods, eerie sounds and ancient murmurs surround you. The forest seems alive with secrets. "
                "Chuzo, with a twinkle in his eye, declares, \"Let us unravel the mysteries of this enchanted wood!\" \n\n"
                "Choices:\n"
                "A. \"I trust your wisdom, Master Artificer.\"\n"
                "B. \"I believe our own instincts shall guide us.\""
            ),
            "choices": {
                "a": {
                    "text": "Relying on Chuzo's legendary insight, you follow his lead as the forest slowly reveals a safe passage.",
                    "next": 5
                },
                "b": {
                    "text": "Choosing independent thought, you and your companions forge ahead—but a misstep in the twisting paths delays your progress.",
                    "next": 5
                }
            }
        },
        {
            "prompt": (
                "Along the roaring river, the current surges with unpredictable might. Chuzo quips, \"Even the wildest river yields to a clever mind!\" \n\n"
                "Choices:\n"
                "A. \"Let us craft a raft and ride its fury.\"\n"
                "B. \"We shall wait for calmer waters.\""
            ),
            "choices": {
                "a": {
                    "text": "Resourcefulness wins the day as you construct a sturdy raft, taming the rapids with ingenuity.",
                    "next": 5
                },
                "b": {
                    "text": "Patience bears its reward as you find a serene bend in the river, easing your journey.",
                    "next": 5
                }
            }
        },
        {
            "prompt": (
                "At last, your party reaches the hidden chamber deep within the Inferno Mountains. The Ember Heart pulses with a warm, radiant glow. "
                "Chuzo proclaims, \"Behold, the Ember Heart! With this relic, our destiny shall be reborn.\" \n\n"
                "Choices:\n"
                "A. \"Let us claim it boldly and ignite a new era!\"\n"
                "B. \"We must study its secrets carefully before taking it.\""
            ),
            "choices": {
                "a": {
                    "text": "Fueled by valor, you claim the Ember Heart, sealing your fate as heroes of legend.",
                    "next": "end_a"
                },
                "b": {
                    "text": "Through careful scrutiny, you uncover hidden truths that reshape your quest, leading to a wiser future.",
                    "next": "end_b"
                }
            }
        },
        {
            "prompt": (
                "Ending A: The Ember Heart has been seized with unbridled courage. The kingdom awakens to renewed hope, and your names are forever etched "
                "in the annals of legend as those who dared to defy darkness with fearless hearts."
            ),
            "choices": {},
            "reward_item": {"item": "Hidden Phoenix Blade", "rarity": "legendary"}
        },
        {
            "prompt": (
                "Ending B: With wisdom and caution, the secrets of the Ember Heart are unlocked, ushering in an era of balanced prosperity. "
                "Your measured approach ensures that the realm is restored not just by power, but by understanding and unity."
            ),
            "choices": {},
            "reward_item": {"item": "Ember Token", "rarity": "rare"}
        }
    ]
}
