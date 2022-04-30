
from discord.ext import commands
from core.defalut_cog import Cog_Extension
from discord_components import DiscordComponents

class Events(Cog_Extension):

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        DiscordComponents(self.bot)
        print('目前登入 ---->', self.bot.user)
        print('ID:', self.bot.user.id)
        
        

    @commands.Cog.listener("on_message")
    async def on_message(self , message):
        if not message.author.bot:
            #內容
            content = message.content
            print(f"[{message.guild}] - [{message.channel}]")
            name = message.author.nick
            if name == None:
                print(f"{message.author} \n{message.content}")
            else:print(f"{name} : {content}")
                    
    
    @commands.Cog.listener("on_command_error")
    async def on_command_error(self , ctx, error):
        try:
            if isinstance(error , commands.CommandNotFound):
                print(f"[ 指令 ] {ctx.message.content[1:]}" , f"是不存在的指令")
                await ctx.message.delete()
            if isinstance(error , commands.CommandInvokeError):
                print(f"[ 指令 ] {ctx.message.content[1:]}" , f"在使用時發生錯誤: \n{error.args[0]}")
                await ctx.message.delete()
            if isinstance(error , commands.CommandError):
                print(f"[ 指令 ] {ctx.message.content[1:]}" , f"在使用時發生錯誤: \n{error.args[0]}")
                await ctx.message.delete()
        except:
            pass



def setup(client):
    client.add_cog(Events(client))

