# MAIN FILE

# 4/12/2021
# Christian Dad Bot for Discord
# Jacob Sung Pd 3

import discord
import os
import random
import utilmodule
from dotenv import load_dotenv
from discord.ext import commands # for managing commands

def main():
    # signal a command using this character
    client = commands.Bot(command_prefix = '!') 

    # protect delicate discord bot info
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    # extension loading and unloading
    @client.command()
    async def load(ctx, extension):
        client.load_extension(f'cogs.{extension}')

    @client.command()
    async def unload(ctx, extension):
        client.unload_extension(f'cogs.{extension}')

    @client.event
    async def on_ready():
        print("ONLINE")

    # LOADS THE EXTERNAL CLASSES
    for cog_name in utilmodule.format_cogs():
        client.load_extension(cog_name)

    client.run(TOKEN)
    
if __name__ == "__main__":
    main()