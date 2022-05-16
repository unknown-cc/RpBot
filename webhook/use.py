

# 確認有無指定的 webhook 沒有就創一個
async def checkWebhook(guild, channelID):
    webhook_name = "rpBot"
    channels = await guild.fetch_channels()
    from discord.utils import get
    channel = get(channels, id=int(channelID[2:-1]))
    webhooks = await channel.webhooks()
    webhook = None
    for w in webhooks:
        if w.name == webhook_name:
            webhook = w
    if webhook == None:
        webhook = await channel.create_webhook(name=webhook_name, avatar=None)

    return webhook


async def sendWebhook(arg, text, username, avatar_url):
    import discord

    async def send(webhook):
        if not webhook == None:
            wm = await webhook.send(content=text, wait=True, username=username, avatar_url=avatar_url)
            return wm
    if type(arg) == discord.Webhook:
        webhook = arg
        return await send(webhook)
    elif ("http" in arg):
        from aiohttp import ClientSession
        async with ClientSession() as session:
            webhook = discord.Webhook.from_url(
                arg, adapter=discord.AsyncWebhookAdapter(session))
            return await send(webhook)


async def cloneWebhook(ctx, bot, channelID, args, time=-1):
    if ("<@") in bot:
        user = await ctx.guild.fetch_member(int(bot[2:-1]))
        avatar_url = user.avatar_url
        username = user.nick
        if username == None:
            username = user
    elif "," in bot:
        data = bot.split(",")
        username = data[0]
        avatar_url = data[1]
    else:
        username = None
    if username == None:
        return
    if channelID == "0":
        webhook = await checkWebhook(ctx.guild, f"<#{ctx.channel.id}>")
    else:
        webhook = await checkWebhook(ctx.guild, channelID)
    if not webhook == None:
        wm = await sendWebhook(webhook, args, username, avatar_url)
        if time > 0:
            import asyncio
            await asyncio.sleep(3)
            await wm.delete()
    pass


async def parseServerEmoji(bot, content, back="text"):
    if not ("$") in content:
        return content
    import re
    emojiRegex = re.compile(r"\$.+?\$")
    emoji_strs = re.findall(emojiRegex, content)
    if len(emoji_strs) == 0:
        return content
    emojis = []
    found_emoji = False
    text = content
    for emoji_str in emoji_strs:
        is_matched = False
        for guild in bot.guilds:
            server_emojis = guild.emojis
            for server_emoji in server_emojis:
                if (server_emoji.name) == emoji_str[1:-1]:
                    if (server_emoji.animated):
                        emoji = f"<a:{server_emoji.name}:{server_emoji.id}>"
                        text = text.replace(emoji_str, emoji)
                        emojis.append(emoji)
                    else:
                        emoji = f"<:{server_emoji.name}:{server_emoji.id}>"
                        text = text.replace(emoji_str, emoji)
                        emojis.append(emoji)
                    found_emoji, is_matched = True , True
            if is_matched:
                break
        if is_matched:
            continue    
    if found_emoji:
        if back == "text":
            return text
        elif back == "emoji":
            return emojis
    else:
        return