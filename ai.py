import aiohttp
import discord
from config import (
    AI_API_KEY, AI_BASE_URL, AI_MODEL,
    SYSTEM_PROMPT, MAX_TOKENS, PERSONA_NAME
)

async def get_ai_response(
    history: list[dict],
    system_override: str | None = None
) -> str | None:
    """
    Calls the OpenAI-compatible API with the rolling conversation history.
    Returns the assistant's reply text, or None on failure.
    """
    system = system_override or SYSTEM_PROMPT

    messages = [{"role": "system", "content": system}] + history

    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "max_tokens": MAX_TOKENS,
        "temperature": 0.85,
    }

    headers = {
        "Authorization": f"Bearer sk-6efa36b2c082232102de1b9fa29fe193372928271821bddd",
        "Content-Type": "application/json",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://septorlabs.com//v1",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    print(f"[AI ERROR] {resp.status}: {text}")
                    return None
                data = await resp.json()
                return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[AI EXCEPTION] {e}")
        return None


def should_respond(bot: discord.Client, message: discord.Message) -> bool:
    """
    Returns True if the bot should respond to this message.
    Responds when:
      - The bot is directly mentioned
      - The message is a reply to the bot
    """
    # DMs
    if isinstance(message.channel, discord.DMChannel):
        return False

    # Direct mention
    if bot.user in message.mentions:
        return True

    # Reply to the bot
    if (
        message.reference
        and message.reference.resolved
        and isinstance(message.reference.resolved, discord.Message)
        and message.reference.resolved.author == bot.user
    ):
        return True

    return False