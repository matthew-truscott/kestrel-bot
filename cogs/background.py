import datetime
import asyncio

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()

async def timeout_callback():
    await asyncio.sleep(0.1)
    print('pong!')

async def background_main(bot):
    await bot.wait_until_ready()
    print('background_main() is running')
    start_time = datetime.datetime.now()
    print(start_time)
    while not bot.is_closed:
        try:
            print('uptime: ', str(datetime.datetime.now() - start_time))
        except Exception as e:
            print(repr(e))
        await asyncio.sleep(5)

async def time(bot):
    timer = Timer(2, timeout_callback)
