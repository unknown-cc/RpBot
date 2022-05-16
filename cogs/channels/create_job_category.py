from typing import Tuple
from discord.utils import get
from discord.ext import commands
from core.defalut_cog import Cog_Extension


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


class create_job_category(Cog_Extension):
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


def setup(bot):
    bot.add_cog(create_job_category(bot))
