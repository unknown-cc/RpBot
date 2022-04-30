import asyncio
from discord.ext import commands
from core.defalut_cog import Cog_Extension

agree_member = []
class Rules(Cog_Extension):
    
    # 成員加入事件
    @commands.Cog.listener("on_member_join")
    async def on_member_join(self , member):
        if member.bot:
            return
        from pil.Image import serverInOutImage
        defalut_role_id = 849960343765778448
        roles = await member.guild.fetch_roles()
        from discord.utils import get
        default_role = get(roles , id=defalut_role_id)
        await member.add_roles(default_role , atomic=True)
        await member.edit(nick=f"🛬 觀光客 ➤ " + member.name)
        EventMessage = f"🎊 歡迎 <@{member.id}> 加入寶島 RolePlay 🎊"
        await serverInOutImage(member , "join" , 966335022497939486,EventMessage)        

    # 成員離開事件
    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self , member):
        if member.bot:
            return
        from pil.Image import serverInOutImage
        EventMessage = f"我們懷念他 <@{member.id}>"
        await serverInOutImage(member , "leave" , 966335558051840011,EventMessage)

    # 消息反應增加事件
    @commands.Cog.listener("on_raw_reaction_add")
    async def on_reaction_add(self, payload):
        # 規則反應
        if payload.member.bot:
            return
        # 訊息ID
        if not payload.message_id==969182477857996830:
            return
        # 表情ID
        if payload.member.id in agree_member:
            return
        # 按了對應的反應
        if payload.emoji.id == 870974929443647508:
            roles = await payload.member.guild.fetch_roles()
            from discord.utils import get
            # 調整身分組
            default_role = get(roles , id=849960343765778449)            
            remove_role = get(roles , id=849960343765778448)
            await payload.member.add_roles(default_role , atomic=True)            
            await payload.member.remove_roles(remove_role)
            # 調整暱稱
            await payload.member.edit(nick=f"🌏 市民 ➤ " + payload.member.name)
            # 防刷
            agree_member.append(payload.member.id)
            await asyncio.sleep(10)
            await agree_member.remove(payload.member.id)
            


def setup(client):
    client.add_cog(Rules(client))
