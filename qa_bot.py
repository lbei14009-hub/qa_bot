import discord
from discord.ext import commands
import random
import os

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
        "問這個代表你已經心裡有答案了",
        "我不想傷你，但你自己知道結果",
        "這問題本身就很危險",
        "如果成功了算你運氣好"
    ],
    "不正經派": [
        "看心情",
        "問宇宙",
        "丟硬幣吧",
        "今天不適合做決定",
        "我剛剛睡著了"
    ],
    "擺爛派": [
        "隨便",
        "你高興就好",
        "嗯",
        "下一題",
        "不想回答"
    ],
    "路人派": [
        "我只是路過",
        "你們繼續，我在看",
        "這題我不會",
        "有人懂嗎"
    ]
}

emojis = ["😂", "😈", "🤔", "💀", "🙃", "👀", "🔥"]

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

    roll = random.random()

    if roll < 0.1:
        reply = random.choice(emojis)
    else:
        persona = random.choice(list(personas.keys()))
        reply = random.choice(personas[persona])

        if random.random() < 0.4:
            reply += " " + random.choice(emojis)

    await message.reply(reply)

bot.run(TOKEN)
