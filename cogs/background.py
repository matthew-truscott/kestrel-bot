import datetime
import asyncio

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
        await asyncio.sleep(60)
