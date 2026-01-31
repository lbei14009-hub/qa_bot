import discord
from discord.ext import commands
import random
import os

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

answers = [
    "是",
    "否",
    "也許",
    "很難說",
    "再問一次",
    "我覺得可以",
    "我不這麼認為",
    "有可能",
    "機率不高",
    "絕對會",
    "想太多了"
]

emojis = ["😂", "😈", "🤔", "🙃", "👀", "✨", "🔥"]

@bot.event
async def on_ready():
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    content = message.content.strip()
    if not content:
        return

    if not content.endswith(("?", "？")):
        return

    reply = random.choice(answers)

    if random.random() < 0.3:
        reply += " " + random.choice(emojis)

    await message.reply(reply)

bot.run(TOKEN)
