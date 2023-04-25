import asyncio
import json

from aiokafka import AIOKafkaProducer
from core.config import KAFKA_INSTANCE
from core.config import PROJECT_NAME
from core.models.model import IbkrMarketDataProducerMessage
from core.models.model import ProducerResponse
from fastapi import FastAPI
from loguru import logger
import ib_insync as ibi
import uuid
import datetime
from threading import Thread
import uvicorn

class IbStreamer:

    def __init__(self, client='127.0.0.1',port=7497,clientId=11, logger=None):
        self.client = client
        self.port = port
        self.clientId = clientId
        self.logger = logger
        self.ib = ibi.IB().connect()
    async def streamMarketData(self, aioproducer, symbols = ['AAPL', 'TSLA', 'AMD']):
        self.ib = ibi.IB()
        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in symbols]
            for contract in contracts:
                self.ib.reqMarketDataType(3)
                self.ib.reqMktData(contract)

            async for tickers in self.ib.pendingTickersEvent:
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
                            'prevBid': ticker.prevBid,
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
                    print(datetime.datetime.now(), ticker.close)
                    msg_data = json.dumps(data).encode("ascii")
                    await aioproducer.send(topicname='mktDataStream', msg_data=msg_data)
                    # response = ProducerResponse(
                    #     name=msg.name, message_id=msg.message_id, topic=topicname
                    # )
                    # logger.info(response)

    def stop(self):
        self.ib.disconnect()

app = FastAPI(title=PROJECT_NAME)

loop = asyncio.get_event_loop()
aioproducer = AIOKafkaProducer(
    loop=loop, client_id=PROJECT_NAME, bootstrap_servers=KAFKA_INSTANCE
)

# IBApi
ibs = IbStreamer()

@app.on_event("startup")
async def startup_event():
    await aioproducer.start()
    ibs.streamMarketData(aioproducer)

@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()


@app.post("/producer/{topicname}")
async def kafka_produce(msg: IbkrMarketDataProducerMessage, topicname: str):
    """
    Produce a message into <topicname>
    This will produce a message into a Apache Kafka topic
    And this path operation will:
    * return ProducerResponse
    """

    await aioproducer.send(topicname, json.dumps(msg.dict()).encode("ascii"))
    response = ProducerResponse(
        name=msg.name, message_id=msg.message_id, topic=topicname
    )
    logger.info(response)
    return response


@app.get("/ping")
def ping():
    return {"ping": "pong!"}