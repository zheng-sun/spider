import asyncio
import uuid

user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

def parse_page(host, res):
    print('%s 解析结果 %s ' % (host, len(res)))

async def get_page(host, port=80, url='/', callback=parse_page, ssl = False, encode_set='utf-8'):
    print('下载 http://%s:%s%s' % (host, port, url))
    if ssl:
        port = 443
    # 发起tcp链接，IO阻塞操作
    recv,send = await asyncio.open_connection(host=host, port=port,ssl=ssl)

    #封装http协议的报头，因为asyncio模块只能封装并发送tcp包
    request_headers = """GET {} HTTP/1.0\r\nHost: {}\r\nUser-agent: %s\r\n\r\n""".format(url, host, user_agent)
    request_headers = request_headers.encode(encode_set)

    send.write(request_headers)
    await send.drain()

    #接收响应头 IO阻塞操作
    while True:
        line = await recv.readline()
        if line == b'\r\n':
            break
        print('%s Response headers: %s' %(host, line))
    #接收响应体 IO阻塞操作
    text = await recv.read()

    callback(host, text)

    send.close()

if __name__ == '__main__':
    tasks = [
        get_page('www.gov.cn', url='/', ssl=False),
        get_page('www.douyu.com', url='/', ssl=True)
    ]

    loop=asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
