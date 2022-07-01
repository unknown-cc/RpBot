
import asyncio
from discord.ext import commands
from core.defalut_cog import Cog_Extension
from discord_components import Button, ButtonStyle , Interaction
from permissions.roles import gov_roles, leader_roles, manager_roles , check_perms

#job_emoji = ("👮", "🚑", "🚗", "📷")

class role_channel(Cog_Extension):
    @commands.Cog.listener("on_message")
    async def rerole_channel_on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        guild = message.guild
        try:
            # 確認是不是機器人
            if author.bot:
                return
            # 確認頻道ID
            rerole_channel_id = 972013196628070400
            if not (channel.id == rerole_channel_id or channel.id == 965941281366868028):
                return
            if ">>" in content:
                return
            # 解析自己的權限
            self_perms = check_perms(author)
            if self_perms < 2 :
                raise Exception({
                    "message" : "no permissions"
                })
            # 解析訊息
            content_data = content.replace("  ", " ").strip().split(" ")
            # 定義動作關鍵字
            add_acts = ["add", "新增", "give", "給", "+"]
            remove_acts = ["remove", "del", "刪除", "移除", "拔除", "-"]
            act = None
            # 解析動作關鍵字
            if content_data[0] in add_acts:
                act = "add"
            elif content_data[0] in remove_acts:
                act = "remove"
            if act != None:
                content_data.pop(0)
            else:
                raise Exception({
                    "message": "no act"
                })

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
                    role = get(roles, id=role_id)
                    if not author.id == 459033203861225484:
                        if self_perms < 5:
                            if role.id in gov_roles:
                                raise Exception({
                                    "message": "error role",
                                    "arg": role
                                })
                        if self_perms < 4:
                            if role.id in leader_roles+gov_roles:
                                raise Exception({
                                    "message": "error role",
                                    "arg": role
                                })
                    if role != None:
                        target_roles.append(role)
                elif "<@" in data:
                    member_id = data[2:-1]
                    # 導向成員
                    member = await guild.fetch_member(member_id)
                    other_perms = check_perms(member)
                    if self_perms < 5 :
                        if not author.id == 459033203861225484:
                            if self_perms <= other_perms:
                                raise Exception({
                                    "message": "error member",
                                    "arg": member
                                })
                    if member != None:
                        target_members.append(member)
            # 確認清單有成員
            if not target_members:
                raise Exception({
                    "message": "no members"
                })
            # 確認清單有身分組
            if not target_roles:
                raise Exception({
                    "message": "no roles"
                })
            # 完成表情
            check_emoji = "<a:check3:972097575274553464>"
            text_member = f"成員："      
            # 開始修改身分組
            for member in target_members:
                text_member = text_member + f"<@{member.id}> "
                for role in target_roles:
                    if act == "add":
                        await member.add_roles(role, atomic=True)
                    elif act == "remove":
                        
                        await member.remove_roles(role, atomic=True)
            # 身分組完成訊息
            text_role = f"身分組："
            for role in target_roles:
                text_role = text_role + f"<@&{role.id}> "
            if act == "add":
                text = text_member + "已新增" + text_role
            elif act == "remove":
                text = text_member + "已移除" + text_role

            components =[]
            # 變更身分組表情
            if self_perms >= 4:
                # 按鈕
                game_admin = Button(label="遊戲管理員",style=ButtonStyle.grey,custom_id="game_admin")
                plan_admin = Button(label="活動管理員",style=ButtonStyle.grey,custom_id="plan_admin")
                dc_admin = Button(label="滴管",style=ButtonStyle.grey,custom_id="dc_admin")
                goverment = Button(label="市政府",style=ButtonStyle.grey,custom_id="goverment")
                employed = Button(label="市民",style=ButtonStyle.grey,custom_id="employed")
                police = Button(label="警察局",style=ButtonStyle.grey,custom_id="police")
                ambulance = Button(label="醫護局",style=ButtonStyle.grey,custom_id="ambulance")
                mechanic = Button(label="車業",style=ButtonStyle.grey,custom_id="mechanic")
                newser = Button(label="新聞局",style=ButtonStyle.grey,custom_id="newser")
                black1 = Button(label="竹聯幫",style=ButtonStyle.grey,custom_id="black1")
                black2 = Button(label="罪惡堂",style=ButtonStyle.grey,custom_id="black2")
                black3 = Button(label="Joker",style=ButtonStyle.grey,custom_id="black3")
                black4 = Button(label="黑幫4",style=ButtonStyle.grey,custom_id="black4")
                components = [[game_admin,plan_admin,dc_admin,goverment],[employed,police,ambulance,mechanic,newser],[black1,black2,black3,black4]]
            else:
                job_emoji = author.nick[:1]
                for target in target_members:
                    member = await guild.fetch_member(target.id)
                    member_perms = check_perms(member)
                    full_nick = member.nick
                    split_symbol = "➤"
                    nick_data = full_nick.split(split_symbol)
                    nick_prefix = nick_data[0].strip()[1:]
                    nick_name = nick_data[1].strip()
                    if member_perms == 0:
                        await member.edit(nick=f"🌏 市民 {split_symbol} {nick_name}")
                    elif member_perms <= 3 :
                        await member.edit(nick=f"{job_emoji} {nick_prefix} {split_symbol} {nick_name}")
                
            wm = await channel.send(text, reference=message,components=components)
            await message.add_reaction(check_emoji)
            await asyncio.sleep(30)
            await wm.edit(components=[])
        except Exception as e:
            async def response_error(message, text, emoji=None , delete = True):
                m = await message.channel.send(f"{text}", reference=message)
                if delete:                    
                    await message.add_reaction(emoji)
                    await asyncio.sleep(10)
                    await m.delete()
            delete_message = True
            error = e.args[0]
            if error["message"] == "no act":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"未偵測到動作關鍵字"
            elif error["message"] == "error member":
                error_emoji = "<a:warning:972097573869469727>"
                arg = error["arg"]                
                text = f"<@{author.id}> -> 您無法變動 <@{arg.id}> 的身分組。"
                delete_message = False
            elif error["message"] == "error role":
                error_emoji = "<a:warning:972097573869469727>"
                arg = error["arg"]
                text = f"<@{author.id}> -> <@&{arg.id}> 不是您可以變動的身分組。"
                delete_message = False
            elif error["message"] == "no members":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"未指定成員"
            elif error["message"] == "no roles":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"未指定身分組"
            elif error["message"] == "no permissions":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"您無權使用此功能。"
            await response_error(message, text, error_emoji , delete_message)
            if delete_message:
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(10)
            await message.delete()

    @commands.Cog.listener("on_button_click")
    async def on_button_click(self , interaction:Interaction):
        if interaction.channel_id != 972013196628070400:
            return
        await interaction.defer(edit_origin=True)
        
        channel = await self.bot.fetch_channel(interaction.channel_id)
        ref_message_id = interaction.message.reference.message_id        
        ref_message = await channel.fetch_message(ref_message_id)
        if ref_message.author.id != interaction.user.id:
            return
        job = interaction.custom_id
        job_emoji = None
        if job == "game_admin":
            job_emoji = "🎲"
        elif job == "plan_admin":
            job_emoji = "🎠"
        elif job == "dc_admin":
            job_emoji = "🔖"
        elif job == "goverment":
            job_emoji = "⭐"
        elif job == "employed":
            job_emoji = "🌏"
        elif job == "police":
            job_emoji = "👮"
        elif job == "ambulance":
            job_emoji = "🚑"    
        elif job == "mechanic":
            job_emoji = "🚗"
        elif job == "newser":
            job_emoji = "📷"
        elif job == "black1":
            job_emoji = "🎋"
        elif job == "black2":
            job_emoji = "👺"
        elif job == "black3":
            job_emoji = "🤡"
        elif job == "black4":
            job_emoji = "❓"
        if job_emoji:
            mentions = ref_message.mentions
            for member in mentions:
                nick = member.nick
                if not nick[:1] == job_emoji:
                    await member.edit(nick=f"{job_emoji}{nick[1:]}")

        
            
def setup(client):
    client.add_cog(role_channel(client))
