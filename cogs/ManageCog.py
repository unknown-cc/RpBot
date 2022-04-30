
import asyncio
from discord.ext import commands
from core.defalut_cog import Cog_Extension


async def deleteMessage(ctx, time=5):
    await asyncio.sleep(time)
    await ctx.message.delete()


class ManageCog(Cog_Extension):
    @commands.command(name="load", aliases=['載入'])
    @commands.is_owner()
    async def load(self, ctx, *, arg):
        extension = arg.title().replace(" ", "")
        self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} 已載入", delete_after=5)
        await deleteMessage(ctx, 5)

    @commands.command(name="unload", aliases=['卸載'])
    @commands.is_owner()
    async def unload(self, ctx, *, arg):
        extension = arg.title().replace(" ", "")
        self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} 已卸載", delete_after=5)
        await deleteMessage(ctx, 5)

    @commands.command(name="reload", aliases=['重載'])
    @commands.is_owner()
    async def reload(self, ctx, *, arg):
        extension = arg.title().replace(" ", "")
        self.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} 已重載", delete_after=5)
        await deleteMessage(ctx, 5)


def setup(client):
    client.add_cog(ManageCog(client))
