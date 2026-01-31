import discord
from discord.ext import commands
import random
import os

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

short_answers = [
    "是",
    "否",
    "也許",
    "不知道",
    "有可能",
    "不太可能",
    "理論上可以",
    "現實很難"
]

normal_answers = [
    "我覺得可以一試",
    "老實說我不看好",
    "這要看情況",
    "現在下定論還太早",
    "你問這個代表你已經猶豫很久了",
    "如果照目前狀況來看，是偏向不行",
    "感覺會出事",
    "直覺告訴我不是好主意"
]

toxic_answers = [
    "你真的確定要問這個嗎",
    "這問題本身就很有問題",
    "我不想傷你，但答案不太好看",
    "如果這是選擇題，你已經選錯方向了",
    "不是我毒，是狀況真的不樂觀",
    "你問得很認真，但現實不會配合你",
    "理想很美好，實際很殘酷",
    "我只能說，祝你好運"
]

nonsense_answers = [
    "看星座",
    "問你自己",
    "丟硬幣比較快",
    "再睡一下就知道了",
    "我剛剛算了一下，答案在風中",
    "今天不適合做決定",
    "宇宙目前沒有給我訊號",
    "這要看你中午吃什麼"
]

lazy_answers = [
    "嗯",
    "再說",
    "隨便",
    "你高興就好",
    "不想回答",
    "下一題"
]

emojis = ["😂", "😈", "🤔", "🙃", "👀", "🔥", "💀", "✨", "🫠", "🥴"]

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

    roll = random.random()

    if roll < 0.1:
        reply = random.choice(emojis)
    elif roll < 0.3:
        reply = random.choice(short_answers)
    elif roll < 0.55:
        reply = random.choice(normal_answers)
    elif roll < 0.8:
        reply = random.choice(toxic_answers)
    else:
        reply = random.choice(nonsense_answers + lazy_answers)

    if reply not in emojis and random.random() < 0.45:
        reply += " " + random.choice(emojis)

    await message.reply(reply)

bot.run(TOKEN)
