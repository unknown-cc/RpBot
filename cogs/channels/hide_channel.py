
import asyncio
from discord.ext import commands
from core.defalut_cog import Cog_Extension

previous_overwrites = {}

class hide_channel(Cog_Extension):
     # 暫時隱藏觀看
    @commands.command(name="hide_channel" , aliases=["view.exe"])
    @commands.is_owner()
    async def hide_channel(self , ctx , act , *args):
        async def switch(channels , act):
            global previous_overwrites
            for channel in channels:
                overwrites = channel.overwrites
                previous_overwrites[channel.id]  = channel.overwrites
                for role in overwrites:
                    if role.name == "@everyone":
                        continue
                    overwrite = overwrites[role]
                    if act == "open":
                        overwrite.update(view_channel = True)
                    elif act == "hide":
                        overwrite.update(view_channel = False)
                await channel.edit(overwrites = overwrites)
        
        channel = ctx.channel        
        if act in ("復原","recover" , "rec" , "end" , "back"):
            global previous_overwrites
            for channel_id in previous_overwrites:
                channel = await self.bot.fetch_channel(channel_id)
                await channel.edit(overwrites = previous_overwrites[channel_id])
            previous_overwrites = {}
            return
        channels = []
        if args[0] in ("this","0"):
            channels.append(ctx.channel)
            pass
        elif args[0] in ("category" , "分類"):
            category = ctx.channel.category
            if category:
                for channel in category.channels: channels.append(channel)
            pass
        else:
            for arg in args:
                if "<#" in arg:
                    channel = await self.bot.fetch_channel(int(arg[2:-1]))
                    if channel:channels.append(channel)
        print(channels)
        if not len(channels) > 0 : return
        if act in ("hide"):
            await switch(channels , "hide")
        elif act in ("open"):
            await switch(channels , "open")
            
            

                
def setup(bot):
    bot.add_cog(hide_channel(bot))
