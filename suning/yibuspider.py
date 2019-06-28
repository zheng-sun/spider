import asyncio
import uuid
import aiohttp

user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

def parse_page(url, res):
    #print(url)
    print('{} 解析结果 {}'.format(url, len(res)))

async def get_page(url, callback=parse_page):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    if response.reason == 'OK':
        result = await response.read()
    callback(url, result)
    await session.close()


if __name__ == '__main__':
    tasks = [
        get_page('http://www.gov.cn'),
        get_page('https://www.douyu.com')
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
