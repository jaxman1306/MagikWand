import os
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import requests
from io import BytesIO
import random
import sys

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=",m ", intents=intents)

# ---------------- DOUBLE INSTANCE GUARD ----------------
# prevents silent duplicate logic inside same process
if hasattr(sys, "_bot_running"):
    print("Bot already running in this process. Exiting duplicate.")
    sys.exit()
sys._bot_running = True


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# ---------------- SAFE MESSAGE HANDLER ----------------
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


# ---------------- BASIC ----------------
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


# ---------------- MAGIK (1 IMAGE) ----------------
@bot.command()
async def magik(ctx):
    if not ctx.message.attachments:
        await ctx.send("Send 1 image with the command.")
        return

    try:
        img_data = requests.get(ctx.message.attachments[0].url).content
        img = Image.open(BytesIO(img_data)).convert("RGB")

        img = img.resize((img.width // 2, img.height // 2))
        img = img.filter(ImageFilter.BLUR)
        img = ImageEnhance.Contrast(img).enhance(1.8)

        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)

        await ctx.send(file=discord.File(output, "magik.png"))

    except Exception as e:
        print(e)
        await ctx.send("Magik failed.")


# ---------------- PETER (FIXED LINK ONLY) ----------------
@bot.command(name="peter")
async def peter(ctx):
    await ctx.send("https://tenor.com/view/peter-gif-6441173819862827223")


# ---------------- CAPTION (AUTO FIT TEXT) ----------------
@bot.command()
async def caption(ctx, *, text: str):
    if not ctx.message.attachments:
        await ctx.send("Send 1 image with the command.")
        return

    try:
        img_data = requests.get(ctx.message.attachments[0].url).content
        img = Image.open(BytesIO(img_data)).convert("RGB")

        draw = ImageDraw.Draw(img)

        font_size = int(img.width * 0.14)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bar_height = font_size + 40

        # shrink text until fits
        while True:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= img.width - 40 or font_size <= 15:
                break

            font_size -= 2
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

        draw.rectangle([(0, 0), (img.width, bar_height)], fill="white")

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (img.width - text_width) / 2
        y = (bar_height - text_height) / 2

        draw.text((x, y), text, fill="black", font=font)

        output = BytesIO()
        img.save(output, format="PNG")
        output.seek(0)

        await ctx.send(file=discord.File(output, "caption.png"))

    except Exception as e:
        print(e)
        await ctx.send("Caption failed.")


# ---------------- START ----------------
if __name__ == "__main__":
    if TOKEN is None:
        print("TOKEN IS NONE")
    else:
        bot.run(TOKEN)
