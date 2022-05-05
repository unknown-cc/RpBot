import asyncio
import re
from sys import prefix
from typing import Tuple
from unicodedata import category
from discord.utils import get
from discord.ext import commands
from core.defalut_cog import Cog_Extension

from permissions import overwrites
from discord import PermissionOverwrite


# def jobOverwrites(ctx):
#     overwrite = {
#         ctx.guild.default_role: overwrites.AdminRole()
#     }
#     return overwrite

# 裝飾器工廠 創建分類
def create_category(ctx, name):
    def decorator(func):
        async def wrapper():
            category = await ctx.guild.create_category(name=name, overwrites=None)
            await ctx.message.delete()
            return await func(category)
        return wrapper
    return decorator

# 分類創建頻道


async def createChannelInCategory(category, channel_names: Tuple, type="text"):
    for name in channel_names:
        if type == "text":
            await category.create_text_channel(name)
        if type == "voice":
            await category.create_voice_channel(name)

# 設置頻道權限


async def setChannelsPerms(channels, specialRoles, perm):
    for channel in channels:
        for sp in specialRoles:
            await channel.set_permissions(sp, overwrite=perm)


class ManageChannel(Cog_Extension):
    # 創建公職分類 + 頻道
    @commands.command(name='cjc', aliases=['創建公職'])
    @commands.is_owner()
    async def createJobCategory(self, ctx, act, *args):
        if len(args) > 0:
            category_name = " ".join(args)

            if act in ("對外", "公開", "外部"):
                @create_category(ctx, category_name)
                async def jobPublicCategory(category):
                    text_channel_names = (
                        "公告",
                        "人員名單",
                        "黑名單",
                        "投訴區",
                    )
                    await createChannelInCategory(category, text_channel_names, "text")
                    voice_channel_names = (
                        "會客室",
                        "面試區",
                    )
                    await createChannelInCategory(category, voice_channel_names, "voice")
                await jobPublicCategory()
            if act in ("對內", "內部", "非公開"):
                @create_category(ctx, category_name)
                async def jobPrivateCategory(category):
                    text_channel_names = (
                        "內部公告",
                        "薪資紀錄",
                        "倉庫紀錄",
                        "打卡紀錄",
                        "開單紀錄",
                        "請假區",
                        "聊天室",
                    )
                    await createChannelInCategory(category, text_channel_names, "text")
                    voice_channel_names = (
                        "無線電 1",
                        "無線電 2",
                        "無線電 3",
                        "高層會議室",
                    )
                    await createChannelInCategory(category, voice_channel_names, "voice")
                await jobPrivateCategory()

    # 刪掉一個頻道 或 一個分類與其中的所有頻道
    @commands.command(name='delchannel', aliases=['軍機'])
    @commands.is_owner()
    async def deleteChannel(self, ctx, *args):
        await ctx.message.delete()
        if len(args) == 1 and args[0] in (">>小男孩",):
            # await ctx.send(f"✈ 寶島軍機飛過並投下了一顆 **小男孩**")
            # await asyncio.sleep(10)
            await ctx.channel.delete()
        # 炸掉整個
        elif len(args) == 1 and args[0] in (">>胖子",):
            category = ctx.channel.category
            # for channel in category.channels:
            #     if f"{channel.type}" == "text":
            #         await channel.send(f"✈ 寶島軍機飛過並投下了一顆 **胖子**")
            # await asyncio.sleep(20)
            for channel in category.channels:
                await channel.delete()
            await category.delete()
        elif len(args) > 1 and args[0] in (">>小男孩",):
            IDs = args[1:]
            channels = []
            for id in IDs:
                channelID = re.sub("\<|\#|\>", "", id)
                channel = await self.bot.fetch_channel(channelID)
                # await channel.send(f"✈ 寶島軍機飛過並投下了一顆 **小男孩**")
                channels.append(channel)
            for channel in channels:
                await channel.delete()
        else:
            await ctx.send(f"✈ 寶島軍機飛過而已，大家別緊張", delete_after=10)

    # 刪除所有頻道的身分組
    @commands.command(name="delRole", aliases=["蹦蹦頻道身分組"])
    @commands.is_owner()
    async def deleteAllRole(self, ctx):
        channels = ctx.guild.channels
        for channel in channels:
            overwrites = channel.overwrites
            for member in dict.keys(overwrites):
                await channel.set_permissions(member, overwrite=None)

    # 分類裡 統一編輯所有頻道的名字
    @commands.command(name="edit_category_and_channel_name", aliases=["裝潢", "修改分頻名稱", "修改名稱"])
    @commands.has_permissions(manage_channels=True)
    async def editCategoryAndChannelName(self, ctx, act, *args):
        print(args , f"[{len(args)}]")
        if len(args) > 0:
            category = ctx.channel.category
            channels = category.channels
            if act in ("prefix", "加綴"):
                for channel in channels:
                    print(channel)
                    format = ' '.join(args)
                    format = format.replace("{name}", f"{channel.name}")
                    
                    await channel.edit(name=f"{format}")
            if act in ("replace", "取代"):
                old = args[0]
                new = ""
                if len(args) == 2:
                    new = args[1]
                for channel in channels:
                    await channel.edit(name=f"{channel.name.replace( old , new)}")

        await ctx.message.delete()

    # 修改分頻權限
    # >> members|roles perm
    @commands.command(name="set_channels_role_in_category", aliases=["修改分頻權限", "修改權限"])
    @commands.is_owner()
    async def setChannelsRoleInCategory(self, ctx, *args):
        from permissions import overwrites
        # 宣告權限
        roles = {
            "僅限觀看": overwrites.ReadOnlyRole(),
            "限制閱覽": overwrites.limitReadRole(),
            "正常權限": overwrites.NormalRole(),
            "管理員權限": overwrites.AdminRole(),
            "無": None
        }
        args = list(args)
        # 獲取權限
        perm = args.pop(-1)
        # 無效權限名稱
        if not perm in roles:
            from discord import Embed, Colour
            await ctx.send(embed=Embed(
                title="❌ 無效的權限名稱",
                colour=Colour(0xff0000)
            )
                .add_field(name="有效權限列表", value="\n".join(dict.keys(roles)), inline=False), delete_after=10)
            return
        else:
            perm = roles[perm]

        guild = ctx.guild
        specialRoles = []
        channels = []
        # 封裝 target
        for target in args:
            if '@&' in target:
                # 身分組
                sp = get(await guild.fetch_roles(), id=int(target[3:-1]))
                if not sp == None:
                    specialRoles.append(sp)

            elif not ('@&' in target) and '@' in target:
                # 成員
                sp = await guild.fetch_member(int(target[2:-1]))
                if not sp == None:
                    specialRoles.append(sp)
            elif '#' in target:
                channel = await self.bot.fetch_channel(target[2:-1])
                if not channel == None:
                    channels.append(channel)
            elif target in ("分類頻道", "分類"):
                channels = channels + list(ctx.channel.category.channels)
            elif target in ("伺服器", "所有頻道"):
                channels = channels + list(ctx.guild.channels)

        # 檢查 channels 是否存在 channel
        if len(channels) == 0:
            await ctx.send("```❌ 未指定頻道```", delete_after=10)
            return

        await setChannelsPerms(channels, specialRoles, perm)

    # 修改公職分類權限
    # 公職權限初始化 首長/長官 高層 基層
    @commands.command(name="set_job_category_perm", aliases=["公職頻道權限初始化", "公職權限初始化"])
    @commands.is_owner()
    async def setJobCategoryPerm(self, ctx, leaderID, advanceID, memberID):
        category = ctx.channel.category
        channels = category.channels
        roles = await ctx.guild.fetch_roles()
        if "<@&" in leaderID:
            leaderRole = get(roles, id=int(leaderID[3:-1]))
        if "<@&" in advanceID:
            advanceRole = get(roles, id=int(advanceID[3:-1]))
        if "<@&" in memberID:
            memberRole = get(roles, id=int(memberID[3:-1]))

        # memberRole 僅限觀看的身分組
        ReadOnlyTextChannel = (
            "公告",
            "人員名單",
            "內部公告"
        )
        ReadOnlyVoiceChannel = (
            "高層會議室"
        )

        for channel in channels:
            if str(channel.type) == "text":
                await channel.set_permissions(leaderRole, overwrite=overwrites.LeaderRole())
                await channel.set_permissions(advanceRole, overwrite=overwrites.AdvanceRole())
                if channel.name in ReadOnlyTextChannel:
                    await channel.set_permissions(memberRole, overwrite=overwrites.ReadOnlyRole())
                else:
                    await channel.set_permissions(memberRole, overwrite=overwrites.NormalRole())
            elif str(channel.type) == "voice":
                await channel.set_permissions(leaderRole, overwrite=overwrites.LeaderRole())
                await channel.set_permissions(advanceRole, overwrite=overwrites.AdvanceRole())
                if channel.name in ReadOnlyVoiceChannel:
                    await channel.set_permissions(memberRole, overwrite=overwrites.ReadOnlyVoiceRole())
                else:
                    await channel.set_permissions(memberRole, overwrite=overwrites.NormalVoiceRole())


    @commands.command(name="copy_something", aliases=["copy.exe"])
    @commands.is_owner()
    async def copyExE(self, ctx, *args):
        args = list(args)
        target = args.pop(0)
        if target in ("頻道", "channel"):
            if len(args) > 0:
                for channelID in args:
                    channel = await self.bot.fetch_channel(int(channelID[2:-1]))
                    c = await channel.clone()
                    await c.move(before=channel)
                    await channel.delete()
                pass
            else:
                c = await ctx.channel.clone()
                await c.move(before=ctx.channel)
                await ctx.channel.delete()
        if target in ("分類", "所有頻道"):
            category = ctx.channel.category
            channels = category.channels
            for channel in channels:
                c = await channel.clone()
                await c.move(before=channel)
                await channel.delete()

    

def setup(bot):
    bot.add_cog(ManageChannel(bot))
