import discord
import asyncio
import aiohttp

from redbot.core import commands

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = bot.loop.create_task(self.status_loop())

    async def status_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                api_url = "https://irpmta.ir/api/stats"
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url) as response:
                        data = await response.json()
                        if data["online"]:
                            players = data["players"]
                            activity = discord.Activity(name=f"{players} online", type=discord.ActivityType.watching)
                            await self.bot.change_presence(activity=activity, status=discord.Status.online)
                        else:
                            activity = discord.Activity(name="Berooz Resani...", type=discord.ActivityType.watching)
                            await self.bot.change_presence(activity=activity, status=discord.Status.idle)
            except Exception as e:
                print(f"Error updating status: {e}")
                activity = discord.Activity(name="Offline", type=discord.ActivityType.watching)
                await self.bot.change_presence(activity=activity, status=discord.Status.dnd)
            await asyncio.sleep(5)
            
    def cog_unload(self):
        self.task.cancel()