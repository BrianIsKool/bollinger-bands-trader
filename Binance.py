import asyncio
from binance import AsyncClient, BinanceSocketManager

class Binance:
    def __init__(self, queue, event):
        self.queue = queue
        self.event = event

    async def sub(self, streams):
        client = await AsyncClient.create()
        bm = BinanceSocketManager(client)
        ms = bm.multiplex_socket(streams)
        async with ms as tscm:
            while True:
                res = await tscm.recv()
                await self.on_message(res)

    async def on_message(self, msg):
        # print(msg)
        if "kline" in msg['stream']:
            close = float(msg['data']['k']['c'])
            kline_status = bool(msg['data']['k']['x'])
            stream = str(msg['stream'])
            name = stream.split('@')[0] + '_' + stream.split('@')[1].split('_')[1]
            # print([close, kline_status, name, "kline"])
            await self.queue.put([close, kline_status, name, "kline"])
            self.event.set()
        elif "trade" in msg['stream']:
            close = float(msg['data']['p'])
            stream = str(msg['stream'])
            name = stream.split('@')[0]
            await self.queue.put([close, name, "book"])
            self.event.set()

# async def run():
#     queue = asyncio.Queue()
#     event = asyncio.Event()
#     bina = Binance(queue=queue, event=event)
#     task = asyncio.create_task(bina.sub(streams=['btctusd@kline_1m', "btctusd@trade"]))
#     await asyncio.gather(task)
# asyncio.run(run())