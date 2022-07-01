
import os
from discord.ext import commands
import discord
from boot.database_job_cooldown import load_job_change_cooldown_data
import globals
# 宣告主體

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='>>' , help_command=None , intents=intents)
bot.cnt = 20

# 讀取 config
with open('./json/config.json' , 'r' , encoding='utf-8') as file:
    import json
    config = json.load(file)

# 載入 cogs
for parent , dirs , files in os.walk("./cogs"):
    if "__" in parent:
        continue
    else:
        for file in files:
            if file.endswith(".py"):
                parent_fix = parent[2:].replace("\\",".").replace("/",".")
                print(f"{parent_fix}.{file[:-3]}")
                bot.load_extension(f"{parent_fix}.{file[:-3]}")

if __name__ == "__main__":
    
    bot.run(config["auth"].replace("$","M"))
