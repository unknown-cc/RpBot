from discord.ext import commands, tasks

class LoopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_loop.change_interval(minutes = self.bot.cnt)

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        self.test_loop.start()

    @tasks.loop(hours=24)
    async def test_loop(self):
        import datetime
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] 喚醒了機器人")
        pass

def setup(bot):
    bot.add_cog(LoopCog(bot))