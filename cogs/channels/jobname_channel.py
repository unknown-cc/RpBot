
import asyncio
from tkinter import E
import discord
from discord.ext import commands
from core.defalut_cog import Cog_Extension
from discord_components import Button, ButtonStyle, Interaction

from permissions.roles import gov_roles, leader_roles, manager_roles, check_perms


class jobname_channel(Cog_Extension):
    @commands.Cog.listener("on_message")
    async def rerole_channel_on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        mentions = message.mentions
        # 確認是不是機器人
        if author.bot:
            return
        # 確認頻道ID
        jobname_channel_id = 972012415204085790
        if not channel.id == jobname_channel_id:
            return
        if ">>" in content:
            return
        try:
            # 修改暱稱
            async def changeNick(channel, member, prefix, perms: int = 0):
                full_nick = member.nick
                split_symbol = "➤"
                nick_data = full_nick.split(split_symbol)
                nick_prefix = nick_data[0].strip()
                nick_name = nick_data[1].strip()
                if nick_prefix == prefix:
                    raise Exception({
                        "message": "same prefix"
                    })

                await member.edit(nick=f"{prefix} ➤ {nick_name}")
                check_emoji = "<a:check1:972097575836610631>"
                await channel.send(f"<@{member.id}> 的職位已從~~**{nick_prefix[1:].strip()}**~~變更為__**{prefix[1:].strip()}**__。", reference=message)
                await message.add_reaction(check_emoji)
            # 修改暱稱↑

            # 檢查自己權限
            self_perms = check_perms(author)
            if self_perms < 2:
                raise Exception({
                    "message": "self no perms"
                })

            job_emoji = author.nick[:1]

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
                job_emoji = author.nick[:1]
                if len(mentions) == 0:
                    if "<@" in content:
                         raise Exception({
                            "message": "mention error"
                        })
                    prefix = content
                    target = author
                else:
                    if len(mentions) > 1:
                        raise Exception({
                            "message": "mention too more"
                        })
                    else:
                        member = mentions[0]
                        other_perms = check_perms(member)
                        if not author.guild_permissions.administrator:
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
                            if other_perms == 0:
                                raise Exception({
                                    "message": "employed"
                                })
                        if self_perms >= 4:
                            job_emoji = member.nick[:1]
                        prefix = content.replace(
                            f"<@{member.id}>", "").strip()
                        target = member
                # 檢查暱稱長度
                if len(prefix) > 10:
                    raise Exception({
                        "message": "prefix too long"
                    })
                elif len(prefix) <= 1:
                    raise Exception({
                        "message": "prefix too short"
                    })
                else:
                    await changeNick(channel, target, f"{job_emoji} {prefix}", self_perms)

        except discord.errors.Forbidden as e:
            if e.text == "Missing Permissions":
                await message.delete()
                return
        except Exception as e:
            async def response_error(message, text, emoji=None, delete=True):
                m = await message.channel.send(f"{text}", reference=message)
                if delete:
                    await message.add_reaction(emoji)
                    await asyncio.sleep(10)
                    await m.delete()
            delete_message = True
            error = e.args[0]
            if error["message"] == "prefix too long":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"職位長度不可超過 10 個字元"
            elif error["message"] == "prefix too short":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"職位長度需要超過 1 個字元"
            elif error["message"] == "mention too more":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"只能標記一個成員"
            elif error["message"] == "no permissions":
                error_emoji = "<a:no1:972097574175645749>"
                member_id = error["arg"].id
                text = f"<@{author.id}> -> 您無權變更 <@{member_id}> 的職位"
                delete_message = False
            elif error["message"] == "same prefix":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"新職位與舊職位相同"
            elif error["message"] == "self no perms":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"<@{author.id}> -> 您無權使用此頻道的功能"
            elif error["message"] == "employed":
                error_emoji = "<a:no1:972097574175645749>"
                text = f"<@{author.id}> -> 請先至 <#972013196628070400> 為市民新增身分組"
            elif error["message"] == "mention error":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"無法識別請求"
            elif error["message"] == "multiline":
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"偵測到多行內容"
            else:
                error_emoji = "<a:confuse:972499920277872640>"
                text = f"無法完成請求"
            await response_error(message, text, error_emoji, delete_message)
            if delete_message:
                await asyncio.sleep(1)
            else:
                await asyncio.sleep(10)
            await message.delete()


def setup(client):
    client.add_cog(jobname_channel(client))
