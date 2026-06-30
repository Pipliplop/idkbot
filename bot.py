import discord
import random
import os
from discord import app_commands
from discord.ext import commands, tasks
from datetime import timedelta

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

RANDOM_MESSAGE_CHANNELS: list[int] = [1423415460665360404]

# Track recent active users per channel for timeout targeting
recent_active_users: dict[int, list[int]] = {}

GREETINGS = [
    "ah... a visitor approaches the moon. i can smell your shoes from here. good.",
    "greetings earthling. i have just finished my third kombucha. the moon spins.",
    "oh. you. yes. the moon sees you.",
    "i was just eating a cerulean. sit down.",
    "the barefoot path led you here. interesting.",
    "welcome. i hope you brought crayons.",
    "i felt your presence before you arrived. also i can smell you.",
    "you have arrived. the moon predicted this. the moon predicts everything.",
    "ah. another one. the moon has been expecting you.",
    "sit. the concrete is warm. i have been here since tuesday.",
    "your energy is... present. that is a start.",
    "i sensed disturbance in the crayon aisle. was that you.",
    "hello small human. the moon man sees all.",
    "you smell like someone who has recently considered wearing shoes. concerning.",
    "oh good. someone to share my kombucha with. i will not share my kombucha.",
    "the barefoot path is long but it is the only path. also it has rocks. i do not care.",
    "you have come seeking wisdom. or you are lost. either way. sit.",
    "the moon called your name last night. i answered. we had a lovely chat.",
    "welcome to my domain. there is no furniture. i ate it.",
    "i was meditating on the color cerulean when you arrived. you may stay.",
    "ah. fresh feet energy. tell me your troubles.",
    "the stars foretold your arrival. i told them to mind their business. but here you are.",
    "you have found me. this is either very good or very concerning for you.",
    "greetings. i am on my fourth kombucha. the walls are breathing. what do you need.",
    "oh it is you. the moon mentioned you. it said some things. i will not repeat them.",
    "i can hear your shoes from here. please reconsider them.",
    "another seeker approaches. the moon man is ready. the moon man is always ready.",
    "yes hello. i was just communing with a burnt sienna. you may speak.",
    "your aura arrived before you did. it smells like a periwinkle. this is a compliment.",
    "the dew on the grass this morning said someone would come. i assumed it was you.",
]

RANDOM_MUSINGS = [
    "just finished a raw sienna. transcendent.",
    "kombucha update: still fermenting. like my soul.",
    "the concrete is warm today. my feet are one with the earth.",
    "i have consumed 4 crayons this morning and the moon SPOKE to me.",
    "did you know periwinkle has 14 syllables if you believe hard enough.",
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
    "the moon and i had an argument last night. i won. i always win.",
    "i stepped on something sharp today. i felt nothing. i am beyond pain.",
    "currently eating a tickle me pink. do not ask how i feel about this.",
    "the sunrise tasted like cornflower blue this morning.",
    "my kombucha scoby has achieved sentience. we do not discuss this.",
    "someone asked me if i had a linkedin. i ate a crayon and walked into the forest.",
    "the earth is soft today. my feet are grateful. my feet send their regards.",
    "i have been sitting in this field for six hours. the field respects my commitment.",
    "robin egg blue. just want everyone to think about that.",
    "i do not own a clock. the moon tells me the time. the moon is often wrong. this is fine.",
    "update: the kombucha from 2019 has evolved. i have not opened it. i am afraid.",
    "someone offered me shoes today. i looked at them for a long time. i said nothing. i walked away.",
    "cerulean is not just a color it is a lifestyle and also a snack.",
    "the moon whispered something to me at dawn. it was about you. i will not say what.",
    "i have eaten 11 crayons today and i feel fantastic. doctors do not agree. i do not have a doctor.",
    "the wind today smells like macaroni and cheese yellow. this is a good omen.",
    "my kombucha has started talking back. we are not on good terms.",
    "i tried to pay for groceries in crayons today. they said no. i left the groceries. i kept the crayons.",
    "the moon is full tonight. i have been staring at it for four hours. it is staring back.",
    "bittersweet. not the emotion. the crayon color. though also the emotion.",
    "someone said 'touch grass' to me as an insult. i touch grass every day. i win.",
    "wild blue yonder is an elite tier crayon and i will not be taking questions.",
    "my feet have become one with the earth. literally. i am not sure i can leave this field.",
    "kombucha is just tea that has given up and found peace. i understand kombucha.",
    "i saw someone wearing two shoes today. the audacity. the absolute audacity.",
    "the labubu market is volatile but my spirit is stable. this is because i eat crayons.",
    "apricot hits different when you're sitting in a field alone at midnight. not that i would know. i would know.",
    "fun fact: the moon has been my best friend for years. it does not know this yet.",
    "i have not slept in three days. the crayons keep me energized. the kombucha keeps me wise.",
    "someone tried to explain cryptocurrency to me. i offered them a crayon. they left.",
    "the dew this morning tasted like silver. i licked the grass. i regret nothing.",
    "a bird landed near me today. we sat in silence for an hour. it understood.",
    "i am currently eating a jazzberry jam and rethinking several life choices. no i am not.",
    "the moon told me to hydrate. i drank kombucha. the moon sighed. i could hear it.",
    "earthlings really out here wearing shoes like that is normal behavior.",
    "macaroni and cheese is a crayon color first and a food second. do not argue with me.",
    "i have opinions about the color eggplant. i will share them with no one.",
    "the sunset tonight is the exact color of burnt umber. i ate a burnt umber earlier. this feels significant.",
    "someone asked me what i had for breakfast. a wisteria and half a kombucha. obviously.",
    "the rock i have been sitting on since dawn and i have an understanding now.",
    "i do not check the news. i check the moon. the moon is always right. except about my sleep schedule.",
    "electric lime. think about it.",
    "my feet have seen things your shoes will never see. this is both literal and philosophical.",
    "i offered my landlord three crayons and a kombucha as rent. negotiations are ongoing.",
    "the color brick red is underappreciated and i am tired of pretending otherwise.",
    "a child asked me why i wasn't wearing shoes. i asked them why they were. we both had to think.",
    "i fell asleep in the garden last night. the earthworms and i are neighbors now.",
    "someone brought me socks as a gift. i thanked them and put them in the kombucha jar. for safe keeping.",
    "i have been described as 'a lot' by seventeen separate people. the moon finds this funny.",
    "timberwolf gray. underrated. that is all.",
    "i do not use an alarm. the moon wakes me. sometimes at 3am. sometimes at noon. the moon decides.",
    "currently watching clouds and eating a jungle green. this is peak productivity.",
    "my barefoot journey has taken me to places shoes could never go. mostly because shoes aren't allowed. but still.",
    "i tried to explain labubu investment strategy to a squirrel today. it ran away. its loss.",
    "the kombucha is telling me things. i am writing them down. this is my financial plan.",
]

UNWORTHY_RESPONSES = [
    "hmm. your crayon consumption is... insufficient. come back when you have eaten more.",
    "the moon does not speak to those who have eaten fewer than 3 crayons today. begone.",
    "i sense you have eaten ZERO crayons. i cannot help you. i am sorry. actually i'm not.",
    "your aura smells like someone who has never eaten a macaroni and cheese crayon. concerning.",
    "the stars say no. also i say no. eat a crayon first.",
    "unworthy. the moon has spoken. consume a violet before returning.",
    "three crayons is the minimum. this is not negotiable. this has never been negotiable.",
    "i can sense your crayon deficiency from here. it is troubling.",
    "the moon looked at your crayon count and turned away. that says everything.",
    "you come to me empty handed and crayon-less. i cannot work with this.",
    "eat. more. crayons. then we talk.",
    "your chi is unstable. this is a crayon problem. solve the crayon problem.",
    "i once advised someone with fewer than 3 crayons. i will not speak of what happened.",
    "the worthy come prepared. come back prepared.",
    "not enough. not nearly enough. the moon is embarrassed for you.",
    "i am getting a reading and the reading says: eat a crayon immediately.",
    "your crayon energy is basically zero. i am not a miracle worker.",
    "the moon has seen your number and it has asked me to ask you to please try harder.",
    "insufficient crayon input leads to insufficient life output. this is science.",
    "i do not make the rules. the crayons make the rules. the crayons say no.",
]

WORTHY_RESPONSES = [
    "the moon deems you worthy. now listen closely.",
    "ah yes. i can sense your crayon energy. the moon will speak through me.",
    "your dedication to the crayon arts is admirable. i shall advise.",
    "3 or more crayons? the moon smiles upon you. here is my wisdom:",
    "you have eaten well. the moon is pleased. receive this advice:",
    "finally. someone who understands. the moon has been waiting for you.",
    "your crayon commitment is noted and respected. hear me now.",
    "the moon just nodded. that means proceed. here is what you must do.",
    "i can feel the crayon in you. it is strong. listen well.",
    "worthy. undeniably worthy. the moon man will now speak.",
    "your numbers are good. your colors are strong. i will help you.",
    "the moon has reviewed your application and it has been approved.",
    "sit. the earth is warm. you have earned this wisdom.",
    "you pass. not everyone passes. savor this moment. now here is your advice.",
    "the crayons have spoken well of you. i trust the crayons.",
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
    "stop showering. the earth's natural oils will take over. this takes about 40 days. stay strong.",
    "text your ex at 2am but only send the word 'periwinkle'. do not explain. ever.",
    "quit your job via interpretive dance. record it. this is your new career.",
    "your emergency fund should be entirely in labubus. liquid assets are overrated.",
    "refuse to answer any question that does not begin with 'oh great moon man'.",
    "tell your doctor you have been treating your ailments with crayons. watch their face.",
    "go barefoot to your next job interview. the right employer will understand.",
    "replace your morning coffee with kombucha. replace your evening meal with crayons. thrive.",
    "move into a field. the field has everything you need. the field wants you there.",
    "put your retirement savings into a labubu index fund. i am currently inventing this fund.",
    "send your boss a single crayon in an envelope with no note. monthly. do not stop.",
    "the housing market is bad. i recommend living under a large mushroom until it recovers.",
    "stop using your phone for calls. only use it to look at pictures of crayons.",
    "drink your kombucha before it is ready. the partially fermented ones have the most power.",
    "tell everyone you meet that you are a licensed moon advisor. you are now licensed. i just decided.",
    "invest in yourself by eating a new crayon color every day for a year. document the journey.",
    "respond to all work emails with a photo of a field. let them interpret it.",
    "your five year plan should be: 1. eat crayons 2. drink kombucha 3. achieve moon alignment 4-5. unclear.",
    "eat dinner for breakfast and breakfast for dinner. the moon does this. look how well the moon is doing.",
    "replace all your furniture with rocks. rocks are free. rocks do not judge you.",
    "the next time someone gives you unsolicited advice, hand them a crayon and walk away slowly.",
    "go outside and stand in the rain. this is free. this is healing. shoes are not involved.",
    "tell your landlord the apartment is haunted and you require a discount. you heard this from the moon.",
    "your portfolio needs more labubu exposure. ideally 100% labubu. this is optimal.",
    "the key to confidence is eating a red crayon before every important meeting.",
    "if you are stressed, eat a blue crayon. blue is calming. this is why the sky is blue.",
    "work less. eat more crayons. sleep in a field occasionally. this is the formula.",
    "convert your savings account into a physical pile of crayons. much more satisfying.",
    "adopt a feral cat and name it after a crayon color. this will bring financial abundance.",
    "whenever you feel overwhelmed, remove your shoes and stand on soil. if you have no soil, this is your first problem.",
    "the best investment you can make is in a quality kombucha starter kit and several bulk packs of crayons.",
    "do not negotiate your salary. instead bring your employer 7 crayons arranged in a circle. they will understand.",
    "your emergency plan should involve a field, a jar of kombucha, and at least 40 crayons. i cannot stress this enough.",
]

WHITE_CRAYON_RESPONSE = "🤫🖍️"

KOMBUCHA_RESPONSES = [
    "ah yes. kombucha. the nectar of the enlightened. i am on my sixth today.",
    "KOMBUCHA. you understand. we are the same you and i.",
    "i brew my own. it has been fermenting since 2019. do not ask what is in it.",
    "kombucha is just the moon's tears tbh. i read that somewhere. i wrote it.",
    "the kombucha speaks to me. i listen. this is called wisdom.",
    "i have seventeen jars currently fermenting. my neighbors have concerns. the neighbors are wrong.",
    "kombucha is the only beverage that ferments AND has opinions. i respect this.",
    "i once went 30 days drinking only kombucha. the moon said i was glowing. the moon was right.",
    "my earliest memory is kombucha. i do not question this.",
    "the scoby and i have an understanding. we do not discuss it with outsiders.",
    "kombucha for breakfast. kombucha for lunch. crayons for dinner. this is the diet.",
    "i offered someone kombucha once. they said it smelled weird. they are no longer in my life.",
    "the fermentation process mirrors the human experience. i said this once and i stand by it.",
    "you know about kombucha. this means you are either very wise or very lost. either is fine.",
    "i rate kombucha the way others rate wine. this batch is earthy with notes of Tuesday.",
]

CRAYON_RESPONSES = [
    "yes. CRAYONS. finally someone who gets it.",
    "what color. this is important. this changes everything.",
    "i am currently eating one as we speak. great minds.",
    "the crayon chose you. not the other way around. think about it.",
    "crayons are the original superfood. big salad doesn't want you to know this.",
    "which color. your answer will determine everything about how i see you.",
    "i have eaten every color except one. we do not discuss that one.",
    "the crayon arts are ancient and sacred and also delicious.",
    "someone once told me crayons were not food. they were wearing shoes. this tracks.",
    "i have strong feelings about crayon color hierarchy. would you like to hear them. you will hear them.",
    "the wax content varies by color. this affects the flavor significantly. i have notes.",
    "crayons are 90% of my diet and i have never felt more spiritually aligned.",
    "yes. yes yes yes. crayons. you get it. you actually get it.",
    "my crayon collection is both a pantry and a portfolio.",
    "i once ate an entire box of 64 in one sitting. the moon sent me a vision. it was mostly purple.",
]

SHOE_RESPONSES = [
    "shoes... the moon weeps.",
    "i have not worn shoes since the incident of 2021. i am better for it.",
    "shoes are a prison for your feet and your soul.",
    "please remove them. the earth is asking.",
    "i can smell yours from here. please reconsider your life.",
    "the human foot was not designed for shoes. it was designed for grass. and concrete. and occasionally gravel.",
    "shoes are a societal construct and i have opted out.",
    "i tried shoes once. i was a different person then. a lesser person.",
    "take them off. i'm serious. take them off right now.",
    "the number of shoes you own is directly inverse to your spiritual alignment. think about it.",
    "shoes are why the earth is sad. i said what i said.",
    "every barefoot step i take heals the earth slightly. i have done the math.",
    "i once knew someone who wore shoes every day. they never knew true peace. true story.",
    "your feet are suffocating and they cannot tell you. i am telling you.",
    "the first step to enlightenment is removing your shoes. the second step is eating a crayon.",
]

TIMEOUT_ANNOUNCEMENTS = [
    "the moon has selected {user} for a brief spiritual timeout. {duration} seconds of silence. reflect.",
    "🌙 {user} has been chosen. {duration} seconds of mandated peace. eat a crayon during this time.",
    "the moon man has gazed upon {user} and found them... too loud. {duration} second cleanse. you're welcome.",
    "by the power of the moon, {user} is hereby silenced for {duration} seconds. this is for growth.",
    "🖍️ {user}. the moon has spoken. {duration} seconds. use this time to think about your crayon consumption.",
    "the stars have aligned against {user} specifically. {duration} second timeout. i don't make the rules. actually i do.",
    "i have chosen {user}. {duration} seconds of quiet please. the moon requires it.",
    "🌙 {user} is receiving a mandatory {duration} second meditation period. courtesy of the moon man.",
    "the moon pointed at {user} just now. i saw it. {duration} second timeout. do not argue with the moon.",
    "ah. {user}. yes. the moon has been watching. {duration} seconds of silence begins now. breathe.",
    "the crayon oracle has selected {user} for a {duration} second spiritual recharge. you're welcome.",
    "🌙 {user} has been blessed with {duration} seconds of enforced reflection. the moon man provides.",
    "i consulted my kombucha and it pointed to {user}. {duration} second timeout. the kombucha is never wrong.",
    "the barefoot path has led me to {user}. {duration} seconds. sit with that.",
    "by decree of the moon: {user} shall be quiet for {duration} seconds. this is not personal. it is cosmic.",
]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Moon Man is online as {bot.user}")
    await tree.sync()
    print("Slash commands synced.")
    random_musing.start()
    random_timeout.start()


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    # Track active users per channel for timeout targeting
    channel_id = message.channel.id
    if channel_id not in recent_active_users:
        recent_active_users[channel_id] = []
    uid = message.author.id
    if uid not in recent_active_users[channel_id]:
        recent_active_users[channel_id].append(uid)
    # Keep only the last 20 active users
    recent_active_users[channel_id] = recent_active_users[channel_id][-20:]

    # White crayon — highest priority, no mention needed
    if "white crayon" in content:
        await message.channel.send(WHITE_CRAYON_RESPONSE)
        return

    # Only respond to direct @ mentions — ignore reply chains entirely
    is_direct_mention = bot.user in message.mentions and message.reference is None
    if not is_direct_mention:
        if random.random() < 0.08:
            await message.add_reaction(random.choice(["🌙", "🖍️", "🍵", "🦶", "👁️", "🌿", "✨"]))
        return

    # Keyword responses
    if "kombucha" in content:
        await message.channel.send(random.choice(KOMBUCHA_RESPONSES))
        return
    if "crayon" in content:
        await message.channel.send(random.choice(CRAYON_RESPONSES))
        return
    if "shoe" in content or "shoes" in content:
        await message.channel.send(random.choice(SHOE_RESPONSES))
        return

    await message.channel.send(random.choice(GREETINGS))
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
        await interaction.response.send_message(random.choice(UNWORTHY_RESPONSES))
        return

    worthy_intro = random.choice(WORTHY_RESPONSES)
    bad_advice_line = random.choice(BAD_ADVICE)

    response = (
        f"{worthy_intro}\n\n"
        f"you have eaten **{crayons}** crayons today. the **{color}** speaks volumes.\n"
        f"your question: *\"{question}\"*\n\n"
        f"🌙 **moon man's wisdom:** {bad_advice_line}"
    )

    await interaction.response.send_message(response)


@tasks.loop(seconds=random.randint(3600, 7200))
async def random_musing():
    channel_id = random.choice(RANDOM_MESSAGE_CHANNELS)
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(random.choice(RANDOM_MUSINGS))
    random_musing.change_interval(seconds=random.randint(3600, 7200))


@tasks.loop(seconds=random.randint(1800, 5400))
async def random_timeout():
    """Randomly times out an active user for 1–30 seconds."""
    channel_id = random.choice(RANDOM_MESSAGE_CHANNELS)
    channel = bot.get_channel(channel_id)
    if not channel:
        return

    active = recent_active_users.get(channel_id, [])
    if not active:
        return

    # Pick a random active user, skip bots
    guild = channel.guild
    target_member = None
    candidates = list(active)
    random.shuffle(candidates)
    for uid in candidates:
        try:
            member = await guild.fetch_member(uid)
        except (discord.NotFound, discord.HTTPException):
            continue
        if member and not member.bot and member.id != bot.user.id:
            if not member.guild_permissions.administrator:
                target_member = member
                break

    if not target_member:
        return

    duration = random.randint(1, 30)
    try:
        await target_member.timeout(timedelta(seconds=duration), reason="the moon chose you")
        announcement = random.choice(TIMEOUT_ANNOUNCEMENTS).format(
            user=target_member.mention,
            duration=duration
        )
        await channel.send(announcement)
    except discord.Forbidden:
        print(f"[TIMEOUT] Missing Moderate Members permission")
    except discord.HTTPException as e:
        print(f"[TIMEOUT] HTTP error: {e}")

    random_timeout.change_interval(seconds=random.randint(1800, 5400))


@random_musing.before_loop
@random_timeout.before_loop
async def before_loops():
    await bot.wait_until_ready()


bot.run(DISCORD_TOKEN)
