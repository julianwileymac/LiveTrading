# Async Interactive Brokers class

import asyncio
import time
import ib_insync as ibi
import datetime

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
                for ticker in tickers:
                    print(ticker)
                    print(datetime.datetime.now(),ticker.close)

    def stop(self):
        self.ib.disconnect()


app = App()
try:
    asyncio.run(app.run())
except (KeyboardInterrupt, SystemExit):
    app.stop()