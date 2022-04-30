from io import BytesIO
import discord
from PIL import Image, ImageFont, ImageDraw
import requests
from pil.Antialias import draw_ellipse
from discord.utils import get as Get



async def serverInOutImage(member, arg, channelID , eventMessage="--未設定訊息--"):
    background_path = "./images/wp2455904-los-santos.jpg"
    image_font_style_path = "./ttf/Graffiti.ttf"
    join_message = f"歡迎\n{member}\n降落至寶島RolePlay\n"
    leave_message = f"注意\n{member}\n潛逃至國外了"
    # 載入背景層
    FloorBackGround = Image.open(background_path).convert('RGBA')
    FloorBackGround.resize((800, 600))
    FloorImageBackGroundSize = FloorBackGround.size
    # 新建陰影層
    FloorTextShadow = Image.new(
        'RGBA', FloorImageBackGroundSize, (255, 255, 255, 0))
    # 字型
    font = ImageFont.truetype(image_font_style_path, 100)
    if (arg == "join"):
        text = join_message
    elif (arg == "leave"):
        text = leave_message
    else:
        return

    # 陰影顏色
    shadowcolor = (0, 0, 0, 150)
    # 文字填滿顏色
    fillcolor = "white"

    # 宣告陰影的畫筆
    drawShadow = ImageDraw.Draw(FloorTextShadow)

    textHight = 200

    h, pad = textHight, font.size + 20
   # 在陰影層畫出陰影

    for line in text.split("\n"):
        # 抓取文字大小
        textSize = font.getsize(line)
        x = int((FloorImageBackGroundSize[0] - textSize[0]) / 2)
        y = int((FloorImageBackGroundSize[1] - textSize[1]) / 2) + h

        for i in range(3):
            drawShadow.text((x-i, y), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x+i, y), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x, y+i), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x, y-i), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x+i, y+i), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x+i, y-i), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x-i, y+i), line, font=font,
                            fill=shadowcolor, align="center")
            drawShadow.text((x+i, y+i), line, font=font,
                            fill=shadowcolor, align="center")
        h += pad
    # 將陰影層和背景層合成
    from PIL import ImageFilter
    FloorTextShadow = FloorTextShadow.filter(ImageFilter.GaussianBlur(10))
    FloorBackGround = Image.alpha_composite(
        FloorBackGround, FloorTextShadow)
    h = textHight
    # 宣告背景層的畫筆
    drawBackGroud = ImageDraw.Draw(FloorBackGround)
    for line in text.split("\n"):
        textSize = font.getsize(line)
        x = int((FloorImageBackGroundSize[0] - textSize[0]) / 2)
        y = int((FloorImageBackGroundSize[1] - textSize[1]) / 2) + h
        # 畫出文字黑邊
        drawBackGroud.text((x-1, y-1), line, font=font,
                           fill=(0, 0, 0), align="center")
        drawBackGroud.text((x+1, y-1), line, font=font,
                           fill=(0, 0, 0), align="center")
        drawBackGroud.text((x-1, y+1), line, font=font,
                           fill=(0, 0, 0), align="center")
        drawBackGroud.text((x+1, y+1), line, font=font,
                           fill=(0, 0, 0), align="center")

        # 畫出文字
        drawBackGroud.text((x, y), line, font=font,
                           fill=fillcolor, align="center")
        h += pad

    # 頭像

    avatar_url = member.avatar_url
    avatar_size = (500, 500)
    avatar_hight = 200
    with requests.get(avatar_url) as r:
        imageData = r.content
    FloorAvatar = Image.open(BytesIO(imageData)).convert("RGBA")
    FloorAvatar = FloorAvatar.resize(avatar_size)
    mask_offset = 5
    mask_size = (avatar_size[0], avatar_size[1])

    # 頭像遮罩

    mask_box = [mask_offset, mask_offset, mask_size[0] -
                mask_offset, mask_size[1] - mask_offset]
    MaskAvatar = Image.new('RGBA', mask_size, color=(0, 0, 0, 0))

    draw_ellipse(MaskAvatar, mask_box, 1, "white", antialias=8)

    # 頭像圓形外框
    circleBorder = 30
    circleSize = (FloorAvatar.size[0] + circleBorder,
                  FloorAvatar.size[1] + circleBorder)

    # 頭向外框置中
    x = int(FloorImageBackGroundSize[0] / 2) - int(circleSize[0]/2)
    y = int(FloorImageBackGroundSize[1] / 2) - \
        int(circleSize[1]/2) - avatar_hight
    circleBox = [x, y, x+circleSize[0], y + circleSize[1]]

    # 頭像陰影
    shadow_offset = 20
    shadow_box = [x-shadow_offset, y-shadow_offset,
                  circleBox[2] + shadow_offset, circleBox[3]+shadow_offset]
    shadowAvatar = Image.new(
        'RGBA', FloorImageBackGroundSize, color=(255, 255, 255, 0))
    draw_ellipse(shadowAvatar, shadow_box,
                 outline=(0, 0, 0, 150), antialias=8)
    shadowAvatar = shadowAvatar.filter(ImageFilter.GaussianBlur(20))
    FloorBackGround = Image.alpha_composite(FloorBackGround, shadowAvatar)

    # 繪製頭像外框
    draw_ellipse(FloorBackGround, circleBox, 1, "white", antialias=4)

    bg = Image.new('RGBA', FloorBackGround.size, (255, 255, 255, 0))

    # 頭像置中
    x = int(FloorImageBackGroundSize[0] / 2) - int(mask_size[0]/2)
    y = int(FloorImageBackGroundSize[1] / 2) - \
        int(mask_size[1]/2) - avatar_hight

    bg.paste(FloorBackGround, (0, 0))
    bg.paste(FloorAvatar, (x, y), mask=MaskAvatar)
    # bg.show()
    guild = member.guild
    channels = await guild.fetch_channels()
    channel = Get(channels, id=int(channelID))

    with BytesIO() as image_binary:
        bg.save(image_binary, 'PNG')
        image_binary.seek(0)
        await channel.send(content=eventMessage,file=discord.File(fp=image_binary, filename='image.png'))
