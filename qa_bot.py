import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import time

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
        "你心裡其實有答案了"
    ],
    "不正經派": [
        "看心情",
        "問宇宙",
        "丟硬幣吧"
    ],
    "擺爛派": [
        "隨便",
        "你高興就好",
        "嗯"
    ]
}

emojis = ["😂", "😈", "🤔", "💀", "🙃", "👀"]

follow_questions = [
    "那你自己怎麼想？",
    "你是希望是還是不是？",
    "你其實比較想聽哪個答案？",
    "如果真的發生了你打算怎麼辦？",
    "這題你問過自己了嗎？"
]

idle_questions = [
    "所以你們現在是在猶豫什麼？",
    "有沒有人其實已經有答案了？",
    "如果現在一定要選，你們會選哪個？",
    "有人想賭一把嗎？",
    "這個頻道突然好安靜"
]

last_message_time = time.time()

@bot.event
async def on_ready():
    idle_asker.start()
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    global last_message_time

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    last_message_time = time.time()

    content = message.content.strip()
    if not content.endswith(("?", "？")):
        return

    persona = random.choice(list(personas.keys()))
    reply = random.choice(personas[persona])

    if random.random() < 0.4:
        reply += " " + random.choice(emojis)

    await message.reply(reply)

    if random.random() < 0.2:
        await asyncio.sleep(random.uniform(0.6, 1.4))
        question = random.choice(follow_questions)
        if random.random() < 0.4:
            question += " " + random.choice(emojis)
        await message.channel.send(question)

@tasks.loop(seconds=120)
async def idle_asker():
    if time.time() - last_message_time > 600:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            question = random.choice(idle_questions)
            if random.random() < 0.4:
                question += " " + random.choice(emojis)
            await channel.send(question)

bot.run(TOKEN)


