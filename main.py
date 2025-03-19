import asyncio
import asyncpg
from Binance import Binance
from trade import Trade
import statistics

ip=''
passwd = ""

tables = [''] # you need database with btctusd_1m
streams = ['btctusd@kline_1m']
window = 24 # 
db = {}
bends = {'1m': {}}

trade = Trade()

async def main(queue, event):
    conn = await asyncpg.connect(database="",
                        host=ip,
                        user="",
                        password=passwd,
                        )
    
    for i in tables: # п
        data = await conn.fetch(f'SELECT * FROM {i} ORDER BY "id" asc OFFSET (SELECT COUNT(*) FROM {i}) - {window-1}')
        db[i] = []
        # print(i)
        for s in data:
            db[i].append(s[5])


    while True:
        await event.wait()
        item = await queue.get()

        for pair in db:
            if item[-1] == 'kline':
                if item[1] == True:
                    if len(db[item[2]]) == window:
                        del db[item[2]][0]
                        db[item[2]].append(item[0])
                        await bbends(db[item[2]], tf=item[2])

            if len(db[pair]) < window:
                print(pair)
                db[pair].append(item[0])
            elif len(db[pair]) == window:
                db[pair][-1] = item[0]
                await bbends(db[pair], tf=pair)
                
        event.clear()

        async def bbends(lst, tf):
            mid = statistics.mean(lst)
            sma = round(statistics.stdev(lst), 7)

            upper_band = mid + 2 * sma
            lower_band = mid - 2 * sma
            pair = str(tf).split('_')[0]

            if tf == "btctusd_1m":
                bends['1m'][pair] = {'up':upper_band, 'down':lower_band, 'mid': mid}

            price = lst[-1]
            if pair in bends['1m']:
                if price < bends['1m'][pair]['down']:
                    await trade.buy(pair=pair)
                    print(pair, 'buy')
                if price > bends['1m'][pair]['up']:
                    await trade.sell(pair=pair)
                    print(pair, price, 'sell')      

async def run():
    queue = asyncio.Queue()
    event = asyncio.Event()

    binance = Binance(queue, event)
    task = asyncio.create_task(trade.sub())
    task2 = asyncio.create_task(trade.price())
    main_task = asyncio.create_task(main(queue, event))
    sub_task = asyncio.create_task(binance.sub(streams))
    task4 = asyncio.create_task(trade.timer())
    # price = asyncio.create_task(trade.sub())
    await asyncio.gather(main_task, sub_task, task, task2, task4)

    ### мб kline медленные ###
asyncio.run(run())
