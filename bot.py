import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
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


# ---------------- MAGIK (2 IMAGE BLEND) ----------------
@bot.command()
async def magik(ctx):
    if len(ctx.message.attachments) < 2:
        await ctx.send("Send 2 images with the command.")
        return

    img1_url = ctx.message.attachments[0].url
    img2_url = ctx.message.attachments[1].url

    img1 = Image.open(BytesIO(requests.get(img1_url).content)).convert("RGBA")
    img2 = Image.open(BytesIO(requests.get(img2_url).content)).convert("RGBA")

    img2 = img2.resize(img1.size)

    frames = []
    for i in range(11):
        alpha = i / 10
        frames.append(Image.blend(img1, img2, alpha))

    output = BytesIO()
    frames[-1].save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, "magik.png"))


# ---------------- PETER GRIFFIN GIF ----------------
@bot.command()
async def peter_griffin(ctx):
    gifs = [
        "https://media.tenor.com/8n3YhXy9Q7kAAAAC/peter-griffin-family-guy.gif",
        "https://media.tenor.com/3JQd7Qz7vVwAAAAC/peter-griffin-dance.gif",
        "https://media.tenor.com/l0Q8f9hQqXcAAAAC/family-guy-peter.gif"
    ]
    await ctx.send(random.choice(gifs))


# ---------------- MEME CAPTION (IMPACT STYLE) ----------------
@bot.command()
async def caption(ctx, *, text: str):
    if not ctx.message.attachments:
        await ctx.send("Send an image with the command.")
        return

    img_url = ctx.message.attachments[0].url
    img = Image.open(BytesIO(requests.get(img_url).content)).convert("RGB")

    # resize font dynamically
    font_size = max(20, img.width // 10)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    # caption box height
    box_height = font_size + 30

    # draw white bar
    draw.rectangle([(0, 0), (img.width, box_height)], fill="white")

    # center text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    text_x = (img.width - text_width) / 2
    text_y = 10

    draw.text((text_x, text_y), text, fill="black", font=font)

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, "caption.png"))


# ---------------- START BOT ----------------
if TOKEN is None:
    print("TOKEN IS NONE")
else:
    bot.run(TOKEN)
