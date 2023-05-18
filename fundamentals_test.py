from ibapi.wrapper import *
from ibapi.client import *
import time

class Test(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)

    # def contractDetails(self, reqId, contractDetails):
    #     print(f'longName {contractDetails.longName}')

    def reqFundamentalData(self, reqId: TickerId, contract: Contract,
                           reportType: str, fundamentalDataOptions: TagValueList):
        print(fundamentalDataOptions)
        # super().fundamentalData(reqId, data)
        # print("FundamentalData Returned. ReqId: {}, Symbol: {},  XML Data: {}".format(
        #     reqId, contr.symbol, data))

    def fundamentalData(self, reqId, data):
        print(data)

    def contractDetailsEnd(self, reqId):
        print('end connection')
        self.disconnect()


def main():
    app = Test()

    app.connect(host='127.0.0.1', port=7497, clientId=1000)

    mycontract = Contract()  # create contract object
    mycontract.symbol = 'AAPL'
    mycontract.secType = 'STK'
    mycontract.exchange = 'SMART'  # smart routing
    mycontract.currency = 'USD'
    mycontract.primaryExchange = 'ISLAND'

    time.sleep(3)

    app.reqFundamentalData(1, mycontract, 'RESC', [])  # RESC is analyst reports
    # https://interactivebrokers.github.io/tws-api/classIBApi_1_1EClient.html#ac7862d96b6d5f045eaf4bf74ea2eda6f

    app.run()


if __name__ == '__main__':
    main()