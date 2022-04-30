from PIL import Image, ImageDraw

def draw_ellipse(image, bounds, width=1, outline='white', antialias=4):

    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    offset, fill = (width/-2.0, 'white')
    #print(offset , fill)
    left, top = [(value + offset) * antialias for value in bounds[:2]]
    right, bottom = [(value - offset) * antialias for value in bounds[2:]]
    #print(left,top,right,bottom)
    draw.ellipse([left, top, right, bottom], fill=fill)
    # downsample the mask using PIL.Image.LANCZOS 
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    #mask.show()
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)