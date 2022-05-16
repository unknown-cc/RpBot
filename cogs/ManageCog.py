
import asyncio
import re
import os
from discord.ext import commands
from core.defalut_cog import Cog_Extension


async def deleteMessage(ctx, time=5):
    await asyncio.sleep(time)
    await ctx.message.delete()


async def manage_cog(bot, ctx, act, extension):
    files = []
    for parent, dirname, filename in os.walk("./cogs"):
        if parent.endswith(extension):
            for file in filename:
                parent_fix = parent[2:].replace("\\", ".")
                files.append(f"{parent_fix}.{file[:-3]}")
        elif f"{extension}.py" in filename:
            parent_fix = parent[2:].replace("\\", ".")
            files.append(f"{parent_fix}.{extension}")
    for file in files:
        if act == "load":
            bot.load_extension(file)
            await ctx.send(f"{file} 已載入", delete_after=5)
        elif act == "reload":
            bot.reload_extension(file)
            await ctx.send(f"{file} 已重載", delete_after=5)            
        elif act == "unload":
            bot.unload_extension(file)
            await ctx.send(f"{file} 已卸載", delete_after=5)



class ManageCog(Cog_Extension):
    @commands.command(name="load", aliases=['載入'])
    @commands.is_owner()
    async def load(self, ctx, *, arg):
        await manage_cog(self.bot, ctx, "load", arg)

    @commands.command(name="unload", aliases=['卸載'])
    @commands.is_owner()
    async def unload(self, ctx, *, arg):
        await manage_cog(self.bot, ctx, "unload", arg)

    @commands.command(name="reload", aliases=['重載'])
    @commands.is_owner()
    async def reload(self, ctx, *, arg):
        await manage_cog(self.bot, ctx, "reload", arg)


def setup(client):
    client.add_cog(ManageCog(client))
