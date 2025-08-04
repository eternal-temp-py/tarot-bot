from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

import os
import random
from PIL import Image
from io import BytesIO

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def draw(ctx, number_of_cards: int = 1):
    try:
        folder = "tarot_images"
        files = os.listdir(folder)

        if number_of_cards < 1:
            await ctx.send("You need to draw at least one card.")
            return
        if number_of_cards > len(files):
            await ctx.send(f"I only have {len(files)} cards available.")
            return

        chosen_cards = random.sample(files, number_of_cards)

        images = []
        for card in chosen_cards:
            img_path = os.path.join(folder, card)
            img = Image.open(img_path).convert("RGBA")  # convert for consistency

            if random.choice([True, False]):
                img = img.rotate(180)

            images.append(img)

        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        combined = Image.new('RGBA', (total_width, max_height), (255, 255, 255, 0))

        x_offset = 0
        for im in images:
            combined.paste(im, (x_offset, 0), im)
            x_offset += im.width

        buf = BytesIO()
        combined.save(buf, format="PNG")
        buf.seek(0)

        await ctx.send(file=discord.File(fp=buf, filename="tarot_reading.png"))

    except Exception as e:
        await ctx.send("Oops! Something went wrong while drawing cards.")
        print(f"Error in draw command: {e}")


bot.run("DISCORD_TOKEN")