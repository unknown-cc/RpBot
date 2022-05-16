
import asyncio
import discord
from discord.ext import commands
from core.defalut_cog import Cog_Extension
from permissions.roles import gov_roles, leader_roles, manager_roles, check_perms
job_emoji = ("👮", "🚑", "🚗", "📷")


class nick_channel(Cog_Extension):
    @commands.Cog.listener("on_message")
    async def rerole_channel_on_message(self, message):
        author = message.author
        author_roles = author.roles
        content = message.content
        channel = message.channel
        mentions = message.mentions

        # 確認是不是機器人
        if author.bot:
            return
        # 確認頻道ID
        nick_channel_id = 972012528139927552
        if not channel.id == nick_channel_id:
            return                       
        if ">>" in content:
            return          
        try:                    
            async def changeNick(channel , member , nick):
                full_nick = member.nick
                split_symbol = "➤"
                nick_data = full_nick.split(split_symbol)
                nick_prefix = nick_data[0]
                nick_name = nick_data[1].strip()
                if nick_name == nick:
                    raise Exception({
                        "message":"same nick"
                    })
                await member.edit(nick=f"{nick_prefix}➤ {nick}")
                await channel.send(content=f"<@{member.id}> 的暱稱已從 __**{nick_name}**__ 變更為 __**{nick}**__" , reference=message)
                check_emoji = "<a:check1:972097575836610631>"
                await message.add_reaction(check_emoji)
            # 檢查自己權限
            self_perms = check_perms(author)
            # 內容審查
            if "<#" in content:
                raise Exception({
                    "message": "mention error"
                })
            elif "\n" in content:
                raise Exception({
                    "message": "multiline"
                })
            elif "<@&" in content:
                raise Exception({
                    "message": "mention error"
                })
            else:
                if len(mentions) == 0:
                    if "<@" in content:
                         raise Exception({
                            "message": "mention error"
                        })
                    new_nick = content
                    target = author
                else:
                    if len(mentions) > 1:
                        raise Exception({
                            "message": "mention too more"
                        })
                    else:
                        if self_perms < 4 :
                            raise Exception({
                                "message" : "cant change other"
                            })
                        member = mentions[0]
                        other_perms = check_perms(member)
                        if author.id != 459033203861225484:
                            if not self_perms == 5:
                                if other_perms == 5:
                                    raise Exception({
                                        "message": "no permissions",
                                        "arg": member
                                    })
                                if self_perms <= other_perms:
                                    raise Exception({
                                        "message": "no permissions",
                                        "arg": member
                                    })
                        new_nick = content.replace(
                            f"<@{member.id}>", "").strip()
                        target = member
                # 檢查暱稱長度
                if len(new_nick) > 6 :
                    raise Exception({
                        "message":"nick too long"
                })
                else:
                    await changeNick(channel, target, new_nick)
            
        except discord.errors.Forbidden as e:
            if e.text == "Missing Permissions":
                await message.delete()
                return
        except Exception as e:
            async def response_error(message, text, emoji=None , delete = True):
                m = await message.channel.send(f"{text}", reference=message)
                if delete:                    
                    await message.add_reaction(emoji)
                    await asyncio.sleep(10)
                    await m.delete()
            delete_message = True
            error = e.args[0]
            if error["message"] == "nick too long":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"暱稱長度不可超過 6 個字元"
            elif error["message"] == "mention too more":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"只能標記一個成員"
            elif error["message"] == "mention error":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"無法辨識請求"
            elif error["message"] == "cant change other":
                error_emoji = "<a:warning:972097573869469727>"
                text = f"只有管理員可以變更他人的暱稱"
            elif error["message"] == "no permissions":
                error_emoji = "<a:warning:972097573869469727>"                
                member_id = error["arg"].id
                text = f"<@{author.id}> -> 您無法變更 <@{member_id}> 的暱稱"
                delete_message=False
            elif error["message"] == "same nick":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"新暱稱與舊暱稱相同"
            elif error["message"] == "finally error":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"無法解析請求"
            else:
                return
            await response_error(message, text, error_emoji , delete_message)
            if delete_message:
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(10)
            await message.delete()
def setup(client):
    client.add_cog(nick_channel(client))
