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

personas = [
    "是",
    "否",
    "理論上可以",
    "數據上偏向不行",
    "你其實已經知道答案了",
    "這問題本身就很危險",
    "看心情",
    "丟硬幣吧",
    "隨便",
    "嗯"
]

emojis = ["😂", "😈", "🤔", "💀", "🙃", "👀", "🔥"]

follow_questions = [
    "那你自己怎麼想？",
    "你是希望我說是還是否？",
    "如果真的發生了你會怎麼辦？",
    "你敢照這個答案做嗎？",
    "你其實比較想聽哪個？"
]

idle_questions = [
    "如果現在一定要選，你們會選哪個？",
    "有人其實已經有答案了吧？",
    "你們有沒有後悔過某個決定？",
    "如果重來一次會選不一樣的嗎？",
    "成功跟快樂哪個比較重要？",
    "如果沒人看見，你們會做一樣的選擇嗎？",
    "你們真的確定現在的方向嗎？",
    "假設明天一切重來，你會改哪一步？"
]

lonely_lines = [
    "好喔都不理我",
    "這題太難是不是",
    "還是我不該問 💀",
    "當我沒說",
    "我是不是氣氛怪怪的"
]

last_message_time = time.time()
last_question_time = 0
last_asker = None

@bot.event
async def on_ready():
    idle_loop.start()
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    global last_message_time, last_asker

    if message.author.bot:
        return

    if message.channel.id != CHANNEL_ID:
        return

    last_message_time = time.time()

    content = message.content.strip()

    if content.endswith(("?", "？")):
        reply = random.choice(personas)

        if random.random() < 0.4:
            reply += " " + random.choice(emojis)

        await message.reply(reply)

        if random.random() < 0.35:
            await asyncio.sleep(random.uniform(0.6, 1.4))
            q = random.choice(follow_questions)
            if random.random() < 0.5:
                q += " " + random.choice(emojis)
            await message.channel.send(q)
            last_asker = message.author.id

    else:
        if last_asker == message.author.id and random.random() < 0.25:
            await asyncio.sleep(random.uniform(0.5, 1.2))
            q = random.choice(follow_questions)
            await message.channel.send(q + " " + random.choice(emojis))

@tasks.loop(seconds=90)
async def idle_loop():
    global last_question_time

    now = time.time()
    if now - last_message_time > 240 and now - last_question_time > 300:
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        q = random.choice(idle_questions)
        if random.random() < 0.5:
            q += " " + random.choice(emojis)

        await channel.send(q)
        last_question_time = now

        await asyncio.sleep(30)
        if time.time() - last_message_time > 270:
            await channel.send(random.choice(lonely_lines))

bot.run(TOKEN)




