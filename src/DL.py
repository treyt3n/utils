import aiohttp, json


async def async_post_json(url, data=None, json=None, headers=None, params=None, ssl=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data, json=json, params=params, ssl=ssl) as response:
            return await response.json()


async def async_post_text(url, data=None, headers=None, params=None, ssl=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data, params=params, ssl=ssl) as response:
            res=await response.read()
            return res.decode('utf-8')


async def async_post_bytes(url, data=None, headers=None, params=None, ssl=None):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=data, params=params, ssl=ssl) as response:
            return await response.read()


async def async_dl(url, headers=None, params=None, ssl=None):
    total_size=0
    data=b''
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params, ssl=ssl) as response:
            assert response.status == 200
            while True:
                chunk=await response.content.read(4*1024)
                data += chunk
                total_size += len(chunk)
                if not chunk:
                    break
                if total_size > 500000000:
                    return None
    return data


async def async_text(url, headers=None, params=None, ssl=None):
    data=await async_dl(url, headers, params, ssl)
    if data:
        return data.decode('utf-8')
    return data


async def async_json(url, headers=None, params=None, ssl=None):
    data=await async_dl(url, headers, params, ssl)
    if data:
        return json.loads(data.decode('utf-8'))
    return data


async def async_read(url, headers=None, params=None, ssl=None):
    return await async_dl(url, headers, params, ssl)


get = async_json
text = async_text
read = async_read
post = async_post_json
