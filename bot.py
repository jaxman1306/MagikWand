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


# ---------------- BASIC COMMANDS ----------------
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


# ---------------- MAGIK (SINGLE IMAGE BLUR EFFECT) ----------------
@bot.command()
async def magik(ctx):
    if not ctx.message.attachments:
        await ctx.send("Send 1 image with the command.")
        return

    img_data = requests.get(ctx.message.attachments[0].url).content
    img = Image.open(BytesIO(img_data)).convert("RGB")

    # simple transformation effect
    img = img.resize((img.width // 2, img.height // 2))
    img = img.filter(Image.BLUR)

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, "magik.png"))


# ---------------- PETER GRIFFIN (RAW TENOR LINK ONLY) ----------------
@bot.command()
async def peter_griffin(ctx):
    api_key = "LIVDSRZULELA"

    res = requests.get(
        "https://tenor.googleapis.com/v2/search",
        params={
            "q": "peter griffin family guy",
            "key": api_key,
            "limit": 20,
            "media_filter": "gif"
        }
    )

    data = res.json()

    if "results" not in data or not data["results"]:
        await ctx.send("No GIF found.")
        return

    gif_url = random.choice(data["results"])["media_formats"]["gif"]["url"]

    # RAW LINK ONLY (NO EMBED FORMATTING)
    await ctx.send(gif_url)


# ---------------- MEME CAPTION (TOP BAR TEXT) ----------------
@bot.command()
async def caption(ctx, *, text: str):
    if not ctx.message.attachments:
        await ctx.send("Send 1 image with the command.")
        return

    img = Image.open(BytesIO(requests.get(ctx.message.attachments[0].url).content)).convert("RGB")

    font_size = max(20, img.width // 10)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(img)

    bar_height = font_size + 30
    draw.rectangle([(0, 0), (img.width, bar_height)], fill="white")

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]

    x = (img.width - text_width) / 2
    y = 10

    draw.text((x, y), text, fill="black", font=font)

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    await ctx.send(file=discord.File(output, "caption.png"))


# ---------------- START BOT (NO DUPLICATION POSSIBLE HERE) ----------------
if __name__ == "__main__":
    if TOKEN is None:
        print("TOKEN IS NONE")
    else:
        bot.run(TOKEN)
