import os
import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO
import random

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",m ", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(member.display_avatar.url)


# IMAGE BLEND MAGIK COMMAND (2 images)
@bot.command()
async def magik(ctx):
    if len(ctx.message.attachments) < 2:
        await ctx.send("Send 2 images with the command.")
        return

    img1_url = ctx.message.attachments[0].url
    img2_url = ctx.message.attachments[1].url

    img1_data = requests.get(img1_url).content
    img2_data = requests.get(img2_url).content

    img1 = Image.open(BytesIO(img1_data)).convert("RGBA")
    img2 = Image.open(BytesIO(img2_data)).convert("RGBA")

    img2 = img2.resize(img1.size)

    frames = []
    for i in range(11):
        alpha = i / 10
        frame = Image.blend(img1, img2, alpha)
        frames.append(frame)

    output = BytesIO()
    frames[-1].save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, filename="magik.png"))


# PETER GRIFFIN GIF COMMAND
@bot.command()
async def peter_griffin(ctx):
    peter_gifs = [
        "https://media.tenor.com/8n3YhXy9Q7kAAAAC/peter-griffin-family-guy.gif",
        "https://media.tenor.com/3JQd7Qz7vVwAAAAC/peter-griffin-dance.gif",
        "https://media.tenor.com/l0Q8f9hQqXcAAAAC/family-guy-peter.gif"
    ]

    await ctx.send(random.choice(peter_gifs))


# START BOT
if TOKEN is None:
    print("TOKEN IS NONE")
else:
    bot.run(TOKEN)
