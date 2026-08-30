import discord
from discord import app_commands
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True

class DiscordBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = DiscordBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def handle_order_flow(channel, author):
    await channel.send("How many members do you want in your server?")

    def check(m):
        return m.author == author and m.channel == channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)

        if msg.content.isdigit():
            await channel.send("Our members are usually offline just for info.\nPlease DM jsstudios12")
        else:
            await channel.send("Please enter a valid number. Try again by sending 'hi' or using `/order`.")

    except asyncio.TimeoutError:
        await channel.send("Request timed out.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.strip().lower() == "hi":
        await handle_order_flow(message.channel, message.author)

    await bot.process_commands(message)

@bot.tree.command(name="order", description="Start the member request prompt")
async def order(interaction: discord.Interaction):
    await interaction.response.send_message("How many members do you want in your server?")

    def check(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)

        if msg.content.isdigit():
            await interaction.followup.send("Our members are usually offline just for info.\nPlease DM jsstudios12")
        else:
            await interaction.followup.send("Please enter a valid number.")

    except asyncio.TimeoutError:
        await interaction.followup.send("Request timed out.")


# --- PUT YOUR TOKEN ON THE LINE BELOW THIS ---
bot.run("")