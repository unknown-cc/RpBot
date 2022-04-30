
import asyncio
from discord.ext import commands
from core.defalut_cog import Cog_Extension

class ReroleChannel(Cog_Extension):
    @commands.Cog.listener("on_message")
    async def rerole_channel_on_message(self , message):
        allow_role_words=[
            
        ]

        author = message.author
        if author.bot:
            return        
        content = message.content
        channel = message.channel
        # 確認頻道ID
        rerole_channel_id = 965941281366868028
        if not channel.id == rerole_channel_id:
           return

        # 解析訊息
        content_data = content.replace("  "," ").strip().split(" ")
        # 定義動作關鍵字
        add_acts = ["add","新增","增加","給","給予"]
        remove_acts = ["remove","del","delete","刪除","移除","拔除"]
        act = None
        # 解析動作關鍵字      
        if content_data[0] in add_acts:
            act = "add"            
        elif content_data[0] in remove_acts:
            act = "remove"
        if act != None:
            content_data.pop(0)
        else:
            print("找不到動作關鍵字")
            return
        # 解析成員ID與身分組ID
        target_members = []
        target_roles = []
        guild = message.guild
        roles = await guild.fetch_roles()
        from discord.utils import get
        for data in content_data:
            if "<@&" in data:
                role_id = int(data[3:-1])
                # 導向身分組
                role = get(roles , id=role_id)
                if role != None:
                    target_roles.append(role)
            elif "<@" in data:
                member_id = data[2:-1]
                #導向成員
                member = await guild.fetch_member(member_id)
                if member != None:
                    target_members.append(member)
        for member in target_members:
            for role in target_roles:                
                if act == "add":
                    await member.add_roles(role,atomic=True)
                elif act == "remove":
                    await member.remove_roles(role,atomic=True)
        

def setup(client):
    client.add_cog(ReroleChannel(client))