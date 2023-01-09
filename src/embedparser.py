"""
A discord.py embed parser.
Made to work with https://rival.rocks/embed
This could've definitely been written better but it works.

Example :: await ctx.reply(**await to_object(embedcode))
"""

import discord, yarl, pytz
from datetime import datetime
from . import DL as http


def get_parts(code: str):
    """
    :param code : Embed code using custom format
    :returns  : A list of parts
    """
    
    params = params.replace('{embed}', '')
    return [p[1:][:-1] for p in params.split('$v')]


async def to_object(code: str):
    """
    :param code : Embed code using custom format
    :returns  : A dict meant to be used with `ctx.send` and/or `ctx.reply`
    """
    
    embed = {}
    fields = []
    content = None
    timestamp = None
    files = []
    delete=None
    view = discord.ui.View()

    for part in get_parts(params):

        if part.startswith('content:'):
            content = part[len('content:'):]

        if part.startswith('url:'):
            embed['url'] = part[len('url:'):]

        if part.startswith('title:'):
            embed['title'] = part[len('title:'):]

        if part.startswith('delete:'):
            if part[len('delete:'):].strip().isdigit():
                delete=int(part[len('delete:'):].strip())

        if part.startswith('description:'):
            embed['description'] = part[len('description:'):]

        if part.startswith('footer:'):
            embed['footer'] = part[len('footer:'):]

        if part.startswith('color:'):
            try:
                embed['color'] = int(part[len('color:'):].strip().strip('#'), 16)
            except:
                embed['color'] = 0x2f3136

        if part.startswith('image:'):
            embed['image'] = {'url': part[len('description:'):]}

        if part.startswith("thumbnail:"):
            embed['thumbnail'] = {'url': part[len('thumbnail:'):]}

        if part.startswith('attach:'):
            files.append(
                discord.File(
                    BytesIO(await http.read(part[len('attach:'):].replace(' ', ''))), yarl.URL(part[len('attach:') :].replace(' ', '')).name)
            )

        if part.startswith('author:'):
            z = part[len('author:'):].split(' && ')
            icon_url = None
            url = None
            for p in z[1:]:
                if p.startswith('icon:'):
                    p = p[len('icon:') :]
                    icon_url = p.replace(' ', '')
                elif p.startswith('url:'):
                    p = p[len('url:'):]
                    url = p.replace(' ', '')
            try:
                name = z[0] if z[0] else None
            except:
                name = None

            x['author'] = {'name': name}
            if icon_url:
                embed['author']['icon_url'] = icon_url
            if url:
                embed['author']['url'] = url

        if part.startswith('field:'):
            z = part[len('field:'):].split(' && ')
            value = None
            inline='true'
            for p in z[1:]:
                if p.startswith('value:'):
                    p = p[len('value:'):]
                    value = p
                elif p.startswith('inline:'):
                    p = p[len('inline:'):]
                    inline = p.replace(' ', '')
            try:
                name = z[0] if z[0] else None
            except:
                name = None
            
            if isinstance(inline, str):
                if inline == 'true':
                    inline = True

                elif inline == 'false':
                    inline = False

            fields.append({'name': name, 'value': value, 'inline': inline})

        if part.startswith('footer:'):
            z = part[len('footer:'):].split(' && ')
            text = None
            icon_url = None
            for p in z[1:]:
                if p.startswith('icon:'):
                    p = p[len('icon:'):]
                    icon_url = p.replace(' ', '')
            try:
                text = z[0] if z[0] else None
            except:
                pass
                
            x['footer'] = {'text': text}
            if icon_url:
                embed['footer']['icon_url'] = icon_url

        if part.startswith('label:'):
            z = part[len('label:'):].split(' && ')
            label = 'no label'
            url = None
            for p in z[1:]:
                if p.startswith('link:'):
                    p = p[len('link:'):]
                    url = p.replace(' ', '')
                    
            try:
                label = z[0] if z[0] else None
            except:
                pass
                

            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.link, 
                    label=label, 
                    url=url
                )
            )
            
        if part.startswith('image:'):
            z = part[len('image:'):]
            embed['image'] = {'url': z}
            
        if part.startswith('timestamp:'):
            z = part[len('timestamp:'):].replace(' ', '')
            if z == 'true':
                timestamp = True
                
    if not embed:
        embed = None
    else:
        embed['fields'] = fields
        embed = discord.Embed.from_dict(embed)

    if not params.count('{') and not params.count('}'):
        content = params
        
    if timestamp:
        embed.timestamp = datetime.now(pytz.timezone('America/New_York'))

    return {'content': content, 'embed': embed, 'files': files, 'view': view, 'delete_after': delete}
