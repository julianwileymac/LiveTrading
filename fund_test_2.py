# Async Interactive Brokers class

import asyncio

import ib_insync as ibi

class App:

    async def run(self):
        self.ib = ibi.IB()
        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in ['AAPL', 'TSLA', 'AMD']]
            for contract in contracts:
                self.ib.reqMarketDataType(4)
                self.ib.reqMktData(contract, "258")

            async for tickers in self.ib.pendingTickersEvent:
                for ticker in tickers:
                    print(ticker)
                    # print(ticker.close)

    def stop(self):
        self.ib.disconnect()


app = App()
try:
    asyncio.run(app.run())
except (KeyboardInterrupt, SystemExit):
    app.stop()