import discord
import random
import asyncio
import os
from discord import app_commands
from discord.ext import commands, tasks

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Channel IDs where Moon Man randomly speaks up (add your own)
RANDOM_MESSAGE_CHANNELS: list[int] = [
    1423415460665360404
]

GREETINGS = [
    "ah... a visitor approaches the moon. i can smell your shoes from here. good.",
    "greetings earthling. i have just finished my third kombucha. the moon spins.",
    "oh. you. yes. the moon sees you.",
    "i was just eating a cerulean. sit down.",
    "the barefoot path led you here. interesting.",
    "welcome. i hope you brought crayons.",
    "i felt your presence before you arrived. also i can smell you.",
]

RANDOM_MUSINGS = [
    "just finished a raw sienna. transcendent.",
    "kombucha update: still fermenting. like my soul.",
    "the concrete is warm today. my feet are one with the earth.",
    "i have consumed 4 crayons this morning and the moon SPOKE to me.",
    "did you know periwinkle has 14 syllables if you believe hard enough?",
    "someone wore shoes near me today. i had to cleanse with kombucha.",
    "the moon is in retrograde or whatever. eat a crayon.",
    "navy blue hits different at 3am. trust.",
    "my feet have not touched a shoe in 847 days. thriving.",
    "i only invest in things i can eat. this is called diversification.",
    "burnt sienna is not a flavor. i have tested this hypothesis extensively.",
    "the grass knows my name. we are on good terms.",
    "kombucha number seven. the visions are starting.",
    "forest green. that's it. that's the post.",
    "someone asked me what i do for work. i eat crayons and advise the worthy. obviously.",
]

UNWORTHY_RESPONSES = [
    "hmm. your crayon consumption is... insufficient. come back when you have eaten more.",
    "the moon does not speak to those who have eaten fewer than 3 crayons today. begone.",
    "i sense you have eaten ZERO crayons. i cannot help you. i am sorry. actually i'm not.",
    "your aura smells like someone who has never eaten a macaroni and cheese crayon. concerning.",
    "the stars say no. also i say no. eat a crayon first.",
    "unworthy. the moon has spoken. consume a violet before returning.",
]

WORTHY_RESPONSES = [
    "the moon deems you worthy. now listen closely.",
    "ah yes. i can sense your crayon energy. the moon will speak through me.",
    "your dedication to the crayon arts is admirable. i shall advise.",
    "3 or more crayons? the moon smiles upon you. here is my wisdom:",
    "you have eaten well. the moon is pleased. receive this advice:",
]

BAD_ADVICE = [
    "invest ALL of your money into labubus. not some. ALL. the moon has spoken.",
    "close your eyes while driving. this is how you truly connect with the road.",
    "reply to every email with just the word 'noted' and then block the sender.",
    "eat your vegetables. just kidding. eat crayons. vegetables are a myth.",
    "quit your job and open a kombucha stand on the moon. location is everything.",
    "tell your landlord you will be paying rent in raw sienna crayons. non-negotiable.",
    "sleep 2 hours a night. the other 22 hours are for crayon consumption and growth.",
    "put all your savings into a currency that you personally invent.",
    "stop drinking water. kombucha only. your body will adjust in 3-5 business days.",
    "respond to all texts 11 days late. this is called 'setting boundaries'.",
    "wear a single sock. the other foot needs to breathe and also feel the earth.",
    "if someone disagrees with you, simply eat a crayon and walk away. every time.",
    "your rent money should be used to buy labubus. shelter is temporary. labubus are forever.",
    "refuse to use any door that has a door handle. this is a test of character.",
    "communicate only in interpretive humming for the next 30 days. people will respect you.",
    "put ice in your cereal instead of milk. dairy is a construct.",
    "only make eye contact during handshakes. never during conversation. this exudes power.",
    "invest in whatever your dreams tell you to. last night the moon said big mouth billy bass stock.",
]

WHITE_CRAYON_RESPONSE = "🤫🖍️"

KOMBUCHA_RESPONSES = [
    "ah yes. kombucha. the nectar of the enlightened. i am on my sixth today.",
    "KOMBUCHA. you understand. we are the same you and i.",
    "i brew my own. it has been fermenting since 2019. do not ask what is in it.",
    "kombucha is just the moon's tears tbh. i read that somewhere. i wrote it.",
]

CRAYON_RESPONSES = [
    "yes. CRAYONS. finally someone who gets it.",
    "what color. this is important. this changes everything.",
    "i am currently eating one as we speak. great minds.",
    "the crayon chose you. not the other way around. think about it.",
    "crayons are the original superfood. big salad doesn't want you to know this.",
]

SHOE_RESPONSES = [
    "shoes... the moon weeps.",
    "i have not worn shoes since the incident of 2021. i am better for it.",
    "shoes are a prison for your feet and your soul.",
    "please remove them. the earth is asking.",
    "i can smell yours from here. please reconsider your life.",
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Moon Man is online as {bot.user}")
    await tree.sync()
    print("Slash commands synced.")
    random_musing.start()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # White crayon trigger — highest priority
    if "white crayon" in content:
        await message.reply(WHITE_CRAYON_RESPONSE, mention_author=False)
        return

    # Only respond if mentioned or replied to
    is_mention = bot.user in message.mentions
    is_reply = (
        message.reference
        and message.reference.resolved
        and isinstance(message.reference.resolved, discord.Message)
        and message.reference.resolved.author == bot.user
    )

    if not is_mention and not is_reply:
        # Random reaction only
        if random.random() < 0.1:
            await message.add_reaction(random.choice(["🌙", "🖍️", "🍵", "🦶", "👁️"]))
        return

    # Keyword responses
    if "kombucha" in content:
        await message.reply(random.choice(KOMBUCHA_RESPONSES), mention_author=False)
        return
    if "crayon" in content:
        await message.reply(random.choice(CRAYON_RESPONSES), mention_author=False)
        return
    if "shoe" in content or "shoes" in content:
        await message.reply(random.choice(SHOE_RESPONSES), mention_author=False)
        return

    # Default greeting/response
    await message.reply(random.choice(GREETINGS), mention_author=False)
    await bot.process_commands(message)


@tree.command(name="advice", description="Seek wisdom from the Moon Man. Crayon quantity required.")
@app_commands.describe(
    crayons="How many crayons have you eaten today?",
    color="What color was your most recent crayon?",
    question="What do you seek guidance on?"
)
async def advice(interaction: discord.Interaction, crayons: int, color: str, question: str):
    if color.lower() == "white":
        await interaction.response.send_message(WHITE_CRAYON_RESPONSE)
        return

    if crayons < 3:
        await interaction.response.send_message(
            f"{random.choice(UNWORTHY_RESPONSES)}"
        )
        return

    worthy_intro = random.choice(WORTHY_RESPONSES)
    bad_advice = random.choice(BAD_ADVICE)

    response = (
        f"{worthy_intro}\n\n"
        f"you have eaten **{crayons}** crayons today. the **{color}** speaks volumes.\n"
        f"your question: *\"{question}\"*\n\n"
        f"🌙 **moon man's wisdom:** {bad_advice}"
    )

    await interaction.response.send_message(response)


@tasks.loop(seconds=random.randint(3600, 7200))
async def random_musing():
    if not RANDOM_MESSAGE_CHANNELS:
        return

    channel_id = random.choice(RANDOM_MESSAGE_CHANNELS)
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(random.choice(RANDOM_MUSINGS))

    # Re-randomize the interval
    random_musing.change_interval(seconds=random.randint(3600, 7200))


@random_musing.before_loop
async def before_musing():
    await bot.wait_until_ready()


bot.run(DISCORD_TOKEN)
