import discord
import asyncio
import random
import os
from discord.ext import commands, tasks
from ai import get_ai_response, should_respond
from config import (
    DISCORD_TOKEN, PERSONA_NAME, RANDOM_MESSAGE_CHANNELS,
    RANDOM_MESSAGE_MIN_INTERVAL, RANDOM_MESSAGE_MAX_INTERVAL,
    REACTION_CHANCE, REACTIONS
)

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Per-channel conversation history (short rolling window to save tokens)
conversation_history: dict[int, list[dict]] = {}

def get_history(channel_id: int) -> list[dict]:
    return conversation_history.setdefault(channel_id, [])

def add_to_history(channel_id: int, role: str, content: str):
    history = get_history(channel_id)
    history.append({"role": role, "content": content})
    # Keep only the last 10 messages to limit token usage
    if len(history) > 10:
        history.pop(0)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    random_message_loop.start()

@bot.event
async def on_message(message: discord.Message):
    # Ignore self
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    # Decide whether to react
    if random.random() < REACTION_CHANCE and REACTIONS:
        emoji = random.choice(REACTIONS)
        try:
            await message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    # Decide whether to respond
    if not should_respond(bot, message):
        return

    async with message.channel.typing():
        add_to_history(message.channel.id, "user", f"{message.author.display_name}: {message.content}")
        reply = await get_ai_response(get_history(message.channel.id))
        if reply:
            add_to_history(message.channel.id, "assistant", reply)
            await message.reply(reply, mention_author=False)

@tasks.loop(seconds=random.randint(RANDOM_MESSAGE_MIN_INTERVAL, RANDOM_MESSAGE_MAX_INTERVAL))
async def random_message_loop():
    """Occasionally sends an unprompted message in configured channels."""
    if not RANDOM_MESSAGE_CHANNELS:
        return

    channel_id = random.choice(RANDOM_MESSAGE_CHANNELS)
    channel = bot.get_channel(channel_id)
    if channel is None:
        return

    # Reset the interval randomly each loop
    random_message_loop.change_interval(
        seconds=random.randint(RANDOM_MESSAGE_MIN_INTERVAL, RANDOM_MESSAGE_MAX_INTERVAL)
    )

    reply = await get_ai_response(
        get_history(channel.id),
        system_override="Send a short, unprompted message that fits your personality. Keep it under 2 sentences."
    )
    if reply:
        add_to_history(channel.id, "assistant", reply)
        await channel.send(reply)

@random_message_loop.before_loop
async def before_random_loop():
    await bot.wait_until_ready()

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
