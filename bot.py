import os
import discord
from discord.ext import commands
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO

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


@bot.command()
async def magik(ctx):
    if not ctx.message.attachments:
        await ctx.send("Send an image with the command.")
        return

    url = ctx.message.attachments[0].url
    response = requests.get(url)

    img = Image.open(BytesIO(response.content)).convert("RGB")

    img = img.resize((img.width // 2, img.height // 2))
    img = img.filter(ImageFilter.BLUR)
    img = ImageEnhance.Contrast(img).enhance(2)

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, "magik.png"))


if TOKEN is None:
    print("TOKEN IS NONE")
else:
    bot.run(TOKEN)
