
import os
from discord.ext import commands
import discord
# 宣告主體

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='>>' , help_command=None , intents=intents)


# 讀取 config
with open('./json/config.json' , 'r' , encoding='utf-8') as file:
    import json
    config = json.load(file)

# 載入 cog
for file in os.listdir("./cogs"):
    if file.endswith('.py') :
        bot.load_extension(f"cogs.{file[:-3]}")

if __name__ == "__main__":
    bot.run(config["auth"])
