import discord
from discord.ext import commands
import random
import os
import asyncio

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

personas = {
    "理性派": [
        "是",
        "否",
        "理論上可以",
        "數據上偏向不行",
        "從現實來看機率不高"
    ],
    "毒舌派": [
        "你真的想清楚了嗎",
        "這問題本身就很危險",
        "你問這個就代表你心裡有數了",
        "成功的話算你命好"
    ],
    "不正經派": [
        "看心情",
        "問宇宙",
        "丟硬幣吧",
        "我剛剛沒在聽"
    ],
    "擺爛派": [
        "隨便",
        "你高興就好",
        "嗯",
        "下一題"
    ]
}

emojis = ["😂", "😈", "🤔", "💀", "🙃", "👀"]

self_roasts = [
    "等等，我剛剛是不是在亂講",
    "當我沒說",
    "我突然不確定了",
    "算了我不想負責",
    "剛那句收回"
]

counter_replies = [
    "不對，我反悔",
    "其實也不是完全不行",
    "好啦剛剛太武斷了",
    "冷靜想想，好像有機會"
]

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
    if not content.endswith(("?", "？")):
        return

    persona = random.choice(list(personas.keys()))
    first_reply = random.choice(personas[persona])

    if random.random() < 0.4:
        first_reply += " " + random.choice(emojis)

    await message.reply(first_reply)

    if random.random() < 0.25:
        await asyncio.sleep(random.uniform(0.5, 1.5))
        follow_up = random.choice(self_roasts + counter_replies)

        if random.random() < 0.5:
            follow_up += " " + random.choice(emojis)

        await message.channel.send(follow_up)

bot.run(TOKEN)
