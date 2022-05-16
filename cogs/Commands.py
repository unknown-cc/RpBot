
import asyncio
from discord.utils import get as Get
from discord.ext import commands
from core.defalut_cog import Cog_Extension

class Commands(Cog_Extension):

    @commands.command()
    async def help(self, ctx):
        pass

    @commands.command(name='clear', aliases=['刪除訊息'])
    @commands.is_owner()
    async def clear(self, ctx, num=999):
        await ctx.channel.purge(limit=num+1)

    @commands.command(name="give_role", aliases=["修改身份組"])
    @commands.is_owner()
    async def give_role(self, ctx, act, *args):
        members = []
        roles = []
        if len(args) >= 3:
            if act in ("給", "新增", "add"):
                act = "add"
            elif act in ("移除", "remove"):
                act = "remove"
            for arg in args:
                if ("<@&") in arg:
                    guild_roles = await ctx.guild.fetch_roles()
                    role = Get(guild_roles, id=int(arg[3:-1]))
                    if not role == None:
                        roles.append(role)
                elif ("<@") in arg:
                    member = await ctx.guild.fetch_member(int(arg[2:-1]))
                    if not member == None:
                        members.append(member)

            # for member in members:
            #    print(member)
            for role in roles:
                print(role)
                for member in members:
                    if act == "add":
                        await member.add_roles(role)
                    elif act == "remove":
                        await member.remove_roles(role)

            print(args)

    @commands.command(name="react_message", aliases=["react", "反應"])
    @commands.is_owner()
    async def react_message(self, ctx, act , *emojis):
        message_id = ctx.message.reference.message_id
        message = await ctx.channel.fetch_message(message_id)
        if act == "all":
            server_emojis = ctx.guild.emojis
            for emoji in server_emojis:
                await message.add_reaction(emoji)
            return
        from discord import Emoji
        for emoji in emojis:
            print(type(emoji))
            if type(emoji) == str:
                print(emoji)
                if "$" in emoji:
                    from webhook.use import parseServerEmoji
                    e = await parseServerEmoji(self.bot , emoji)
            else:
                e = emoji
            if act in ("add"):
                await message.add_reaction(e)
        pass

    @commands.command(name="webhook_execute", aliases=["webhook.exe", "w.exe"])
    @commands.is_owner()
    async def webhook_execute(self, ctx , memberID , channelID , * , arg):
        from webhook.use import cloneWebhook
        await cloneWebhook(ctx , memberID , channelID , arg)
        pass
    
    @commands.command(name="make_rule", aliases=["rule.exe", "r.exe"])
    @commands.is_owner()
    async def make_rule (self , ctx , userData , * , arg):
        from webhook.use import sendWebhook , parseServerEmoji ,checkWebhook
        webhook = await checkWebhook(ctx.guild , f"<#{ctx.channel.id}>")
        data = userData.split(",")
        if userData == "0":
            username = ctx.author.nick
            if username == None:
                username = ctx.author.name
            avatar_url = ctx.author.avatar_url
        elif userData=="bot":
            username = "bot"
        else:
            username = data[0]
            avatar_url = data[1]
        text = await parseServerEmoji(self.bot , arg)
        if not text ==  None:
            if username == "bot":
                await ctx.send(text)
            else:
                await sendWebhook(webhook ,text ,username , avatar_url)        
        await ctx.message.delete()

    @commands.command(name="edit_rule",aliases=["erule.exe" , "er.exe"])
    @commands.is_owner()
    async def edit_rule(self , ctx , * , arg):
        from webhook.use import checkWebhook , parseServerEmoji
        messageID = ctx.message.reference.message_id
        if messageID == None :
            m = await ctx.send("❌ 未選定訊息")
            await asyncio.sleep(5)            
            await m.delete()
            return
        message = await ctx.channel.fetch_message(messageID)       
        content = message.content
        webhook = await checkWebhook(ctx.guild , f"<#{ctx.channel.id}>")
        text = await parseServerEmoji(self.bot , arg)
        print("everyone" , "@everyone" in content)
        
        if "@everyone" in content:
            text = "||@everyone||\n" + text
        if not (text == None and arg == ""):
            if webhook.id == message.author.id:
                await webhook.edit_message(messageID,content=text)
            elif self.bot.user.id == message.author.id:
                await message.edit(content=text)
        await ctx.message.delete()

    # 執行
    @commands.command(name="test")
    @commands.is_owner()
    async def test(self , ctx , * , arg):
        from webhook.use import parseServerEmoji
        emojis = await parseServerEmoji(self.bot , arg , "emoji")        
        if not emojis or not type(emojis) == list:
            return
        for emoji in emojis:
            emoji_data = emoji.split(":")
            emoji_name = emoji_data[1]
            emoji_id = emoji_data[2][:-1]
            await ctx.send(content=f"emoji: {emoji}\nname: {emoji_name}\nid: {emoji_id}")

def setup(bot):
    bot.add_cog(Commands(bot))
