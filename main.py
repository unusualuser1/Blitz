import os
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

class Blitz(commands.Bot):

    def __init__(self):
        super().__init__(intents=discord.Intents.all(),command_prefix=commands.when_mentioned_or("!"))
        
    async def on_ready(self):
        for file in os.listdir('cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')        
                    print(f'loaded {file[:-3]}')
                except Exception as e:
                    print(e = f"{type(e).__name__}: {e}")

        print(f'Logged on as  {self.user.name}{self.user.id}')
        synced = await self.tree.sync()
        print(f'synced commands: {len(synced)}')

        

bot = Blitz()
bot.run(token=token)
