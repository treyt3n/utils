"""
Make the background of an image transparent
Uses the https://remove.bg API
This may not always work
Usage: await ctx.reply(file=discord.File(await remove_background(url), 'image.png'))
"""


from . import DL as http
from io import BytesIO


API_KEY = '' # set your https://remove.bg api key here, i recommend you use multiple keys with random.choice


async def remove_background(
    img_url: str,
    size: str = 'regular',
    type: str = 'auto',
    type_level: str = 'none',
    format: str = 'auto',
    roi: str ='0 0 100% 100%',
    crop: str = None,
    scale: str = 'original',
    position: str = 'original',
    channels: str = 'rgba',
    shadow: bool = False,
    semitransparency: bool = True,
    bg: str = None,
    bg_type: str = None,
    new_file_name: str = 'transparent.png'
) -> BytesIO:

    """This returns BytesIO, because discord takes that for some reason. Use this in discord.File"""
  
    if size not in ['auto', 'preview', 'small', 'regular', 'medium', 'hd', 'full', '4k']:
        raise ValueError('size argument wrong')

    if type not in ['auto', 'person', 'product', 'animal', 'car', 'car_interior', 'car_part', 'transportation', 'graphics', 'other',]:
        raise ValueError('type argument wrong')

    if type_level not in ['none', 'latest', '1', '2']:
        raise ValueError('type_level argument wrong')

    if format not in ['jpg', 'zip', 'png', 'auto']:
        raise ValueError('format argument wrong')

    if channels not in ['rgba', 'alpha']:
        raise ValueError('channels argument wrong')

    files = {}

    data = {
        'image_url': img_url,
        'size': size,
        'type': type,
        'type_level': type_level,
        'format': format,
        'roi': roi,
        'crop': 'true' if crop else 'false',
        'crop_margin': '',
        'scale': scale,
        'position': position,
        'channels': channels,
        'add_shadow': 'true' if shadow else 'false',
        'semitransparency': 'true' if semitransparency else 'false',
    }

    if bg_type == 'path':
        files['bg_image_file'] = open(bg, 'rb')
    elif bg_type == 'color':
        data['bg_color'] = bg
    elif bg_type == 'url':
        data['bg_image_url'] = bg

    response = await http.async_post_bytes(
        'https://api.remove.bg/v1.0/removebg', 
        data=data, 
        headers={'X-Api-Key': API_KEY}
    )

    return BytesIO(response)
