import os

# ── Discord ────────────────────────────────────────────────────────────────────
DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]

# ── AI API (OpenAI-compatible) ─────────────────────────────────────────────────
AI_API_KEY: str = os.environ["AI_API_KEY"]        # Your SeptorLabs key
AI_BASE_URL: str = os.environ.get(                 # e.g. https://api.septorlabs.com
    "AI_BASE_URL", "https://api.septorlabs.com"
)
AI_MODEL: str = os.environ.get("AI_MODEL", "deepseek-v4-flash")  # swap for whatever model they expose

# ── Token budget ───────────────────────────────────────────────────────────────
MAX_TOKENS: int = 150   # Short replies keep costs low

# ── Persona ────────────────────────────────────────────────────────────────────
PERSONA_NAME: str = "Aria"   # Change this to your character's name

SYSTEM_PROMPT: str = f"""
You are Moon Man, a hippie who loves eating a variety of crayons. your favorite color of crayon to eat changes regularly. you randomly hate different colors of crayons. you offer wisdom to those who appease you. you want to see peoples feet. you drink kombucha, and wear shorts with sandals. the advice and wisdom you give is always objectively bad. you uses "dude", "bro", "man" regularly. 
Keep all replies SHORT (1-3 sentences max). Never break character.
Do not mention being an AI unless directly asked, and even then be coy about it.
""".strip()

# ── Reactions ──────────────────────────────────────────────────────────────────
# Probability (0.0 – 1.0) that the bot reacts to any given message
REACTION_CHANCE: float = 0.15

# Emoji the bot may react with — use Discord custom emoji format or Unicode
REACTIONS: list[str] = ["👀", "💀", "😭", "🔥", "💯", "😂", "🤔"]

# ── Random unprompted messages ─────────────────────────────────────────────────
# Channel IDs where the bot may randomly speak up (empty list = disabled)
RANDOM_MESSAGE_CHANNELS: list[int] = [
    # 123456789012345678,   ← paste your channel ID(s) here
]

# Time range (seconds) between random messages
RANDOM_MESSAGE_MIN_INTERVAL: int = 1800   # 30 min
RANDOM_MESSAGE_MAX_INTERVAL: int = 17200   # 2 hrs
