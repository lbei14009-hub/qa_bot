import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import time
from collections import defaultdict

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

PERSONAS = {
    "理性": [
        "從邏輯上來說，是",
        "理性判斷，不太可能",
        "依條件而定",
        "不是",
        "也許",
        "絕對是",
        "絕對不是"
    ],
    "毒舌": [
        "你真的覺得這是個好問題嗎？",
        "你要不要冷靜一下再問",
        "這問題有點浪費空氣",
        "你要不要聽聽看你在說甚麼?",
        "你他媽有病是不是?",
        "啟智",
        "你該檢查智商了",
        ":)?",
        "問之前動一下腦子",
        "晚餐兒"
    ],
    "擺爛": [
        "隨便啦",
        "我懶得想",
        "你開心就好",
        ": )",
        "..."
    ],
    "哲學": [
        "問題本身就是答案",
        "你確定你在找答案嗎？",
        "也許沒有正確解"
    ],
    "不正經": [
        "🤡",
        "笑死",
        "握草",
        "喔",
        "幹"
    ]
}

EMOJIS = ["😂", "😈", "🤔", "💀", "🙃", "👀"]

FOLLOW_QUESTIONS = [
    "吃我肘及",
    "你是想被支持，還是想被打醒？",
    "你敢照這個答案做嗎？",
    "如果你不服，問題也不在我",
    "你可以不認同，但我的答案不會改",
    "給我擦皮鞋"
]

IDLE_QUESTIONS = [
    "如果沒人知道，你還會選一樣的嗎？",
    "這裡有人其實已經有答案了吧？",
    "你們是不是在假裝沒看到？"
]

LONELY_LINES = [
    "好喔，看來我不重要",
    "算了，當我沒說",
    "……"
]

recent_users = []
last_message_time = time.time()
last_idle_time = 0
user_question_count = defaultdict(int)
user_bias = defaultdict(int)

@bot.event
async def on_ready():
    idle_loop.start()
    print(f"{bot.user} 已上線")

@bot.event
async def on_message(message):
    global last_message_time

    if message.author.bot or message.channel.id != CHANNEL_ID:
        return

    last_message_time = time.time()

    uid = message.author.id
    user_question_count[uid] += 1
    recent_users.append(uid)
    if len(recent_users) > 10:
        recent_users.pop(0)

    content = message.content.strip()
    if not content.endswith(("?", "？")):
        return

    persona = random.choice(list(PERSONAS.keys()))
    reply = random.choice(PERSONAS[persona])

    if user_question_count[uid] >= 3:
        reply = random.choice([
            "怎麼又是你？",
            "你是不是卡在這個問題？",
            "你真的需要這麼多答案嗎？",
            "你是不是有病?"
        ])
        user_bias[uid] -= 1

    if random.random() < 0.1:
        await message.reply("老子不想回答這題")
        return

    if random.random() < 0.4:
        reply += " " + random.choice(EMOJIS)

    await message.reply(f"【{persona}】{reply}")

    if random.random() < 0.2:
        await asyncio.sleep(1)
        await message.channel.send(random.choice(FOLLOW_QUESTIONS))

@tasks.loop(seconds=120)
async def idle_loop():
    global last_idle_time

    now = time.time()
    if now - last_message_time < 600:
        return
    if now - last_idle_time < 1800:
        return
    if random.random() > 0.3:
        return

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    if recent_users and random.random() < 0.3:
        uid = random.choice(recent_users)
        await channel.send(f"<@{uid}>")
        await asyncio.sleep(3)

    q = random.choice(IDLE_QUESTIONS)
    if random.random() < 0.4:
        q += " " + random.choice(EMOJIS)

    await channel.send(q)
    last_idle_time = now

    await asyncio.sleep(60)
    if time.time() - last_message_time > 660:
        await channel.send(random.choice(LONELY_LINES))

bot.run(TOKEN)


