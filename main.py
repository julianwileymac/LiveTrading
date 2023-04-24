# Async Interactive Brokers class

import asyncio
import time
import ib_insync as ibi
import datetime
import json
import uuid
class App:

    async def run(self):
        self.ib = ibi.IB()
        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in ['AAPL', 'TSLA', 'AMD']]
            for contract in contracts:
                self.ib.reqMarketDataType(3)
                self.ib.reqMktData(contract)

            async for tickers in self.ib.pendingTickersEvent:
                print(ibi.util.df(tickers))
                for ticker in tickers:
                    # data = json.dumps(ticker.dict())
                    stock_dict = ticker.contract.dict()

                    data = {'name': ticker.contract.symbol,
                            'message_id': str(uuid.uuid4()),
                            'timestamp': str(datetime.datetime.utcnow()),
                        'symbol': ticker.contract.symbol,
                            'exchange': ticker.contract.exchange,
                            'currency': ticker.contract.currency,
                     # 'time': datetime.datetime(2023, 4, 24, 23, 0, 32, 864429, tzinfo=datetime.timezone.utc),
                            'time': str(ticker.time),
                            'bid': ticker.bid,
                            'bidSize': ticker.bidSize,
                            'ask': ticker.ask,
                            'askSize': ticker.askSize,
                            'last': ticker.last,
                            'lastSize': ticker.lastSize,
                            'prevBid':  ticker.prevBid,
                            'prevBidSize': ticker.prevBidSize,
                            'prevAsk': ticker.prevAsk,
                            'prevAskSize': ticker.prevAskSize,
                            'prevLast': ticker.prevLast,
                            'prevLastSize': ticker.prevLastSize,
                            'volume': ticker.volume,
                            'open': ticker.open,
                            'high': ticker.high,
                            'low': ticker.low,
                            'close': ticker.close,
                            'vwap': ticker.vwap,
                            }


                    # print(ticker.dict())
                    print(json.dumps(data))
                    print(stock_dict)
                    print(datetime.datetime.now(),ticker.close)

                    await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
                    response = ProducerResponse(
                        name=msg.name, message_id=msg.message_id, topic=topicname
                    )
                    logger.info(response)

    def stop(self):
        self.ib.disconnect()


app = App()
try:
    asyncio.run(app.run())
except (KeyboardInterrupt, SystemExit):
    app.stop()