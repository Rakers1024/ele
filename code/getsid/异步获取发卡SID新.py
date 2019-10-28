import asyncio
import requests
import FaKa
import time
import aiohttp


async def requests_meantime_dont_wait(number):
    url = 'http://www.bxfaka.com/orderquery2?st=contact&kw=' + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            print("{url} 得到响应".format(url=url))


async def fast_requsts(numbers):
    start = time.time()
    await asyncio.wait([requests_meantime_dont_wait(number) for number in numbers])
    end = time.time()
    print("Complete in {} seconds".format(end - start))


loop = asyncio.get_event_loop()
loop.run_until_complete(fast_requsts(FaKa.getNumbers('../../data/card/te.txt')))