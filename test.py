import asyncio
import threading
import time 

class AsyncThread(threading.Thread):
    def __init__(self, loop, *args, **kwargs):
        self.loop = loop
        self.future = asyncio.run_coroutine_threadsafe(app(), self.loop)
        super().__init__(*args, **kwargs)

    def run(self):
        self.loop.run_forever()

    def stop(self):
        self.loop.call_soon_threadsafe(self.loop.stop)

async def app():
    while True:
        print('app running')
        await asyncio.sleep(1)

def main():
    new_loop = asyncio.new_event_loop()
    async_thread = AsyncThread(new_loop)
    async_thread.start()

    while True:
        print('main is Doing something else')
        time.sleep(0.5)

main()