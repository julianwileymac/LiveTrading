import uuid
from datetime import datetime

from pydantic import BaseModel
from pydantic import confloat
from pydantic import StrictStr
from pydantic import validator

import faust
from faust import ChannelT, StreamT

# kafka models
class IbkrMarketDataProducerMessage(BaseModel):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = ""
    symbol: str
    exchange: str
    currency: str
    time: str
    bid: float
    bidSize: float
    ask: float
    askSize: float
    last: float
    lastSize: float
    prevBid: float
    prevBidSize: float
    prevAsk: float
    prevAskSize: float
    prevLast: float
    prevLastSize: float
    volume: float
    open: float
    high: float
    low: float
    close: float
    vwap: float
    # lat: confloat(gt=-90, lt=90)
    # lon: confloat(gt=-180, lt=180)

    @validator("message_id", pre=True, always=True)
    def set_id_from_name_uuid(cls, v, values):
        if "name" in values:
            return f"{values['name']}_{uuid.uuid4()}"
        else:
            raise ValueError("name not set")

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())


class ProducerResponse(BaseModel):
    name: StrictStr
    message_id: StrictStr
    topic: StrictStr
    timestamp: StrictStr = ""

    @validator("timestamp", pre=True, always=True)
    def set_datetime_utcnow(cls, v):
        return str(datetime.utcnow())

# Faust Models
class EquityDelayedData(faust.Record):
    name: StrictStr
    message_id: StrictStr = ""
    timestamp: StrictStr = ""
    symbol: str
    exchange: str
    currency: str
    time: datetime
    marketDataType: int
    minTick: float
    bid: float
    bidSize: float
    ask: float
    askSize: float
    last: float
    lastSize: float
    prevBid: float
    prevBidSize: float
    prevAsk: float
    prevAskSize: float
    prevLast: float
    prevLastSize: float
    volume: float
    open: float
    high: float
    low: float
    close: float