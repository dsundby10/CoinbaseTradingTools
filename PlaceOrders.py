import cbpro
import time
from Variables import *
from Keys import getAuthClient


auth_client = getAuthClient()
public_client = cbpro.public_client
#auth_client.session.close()
def placeBuyOrder(price,size,order_type,productid):
    auth_client.buy(price=price,
                    size=size,
                    order_type=order_type,
                    #post_only = True,
                    product_id=productid)


def placeSellOrder(price,size,order_type,productid):
    auth_client.sell(price=price,
                     size=size,
                     order_type=order_type,
                     #post_only = True,
                     product_id=productid)


def placeMultipleOrders(coin, maxOrders, tradeType, order_type, orderSize, priceList):
    numOrders = 0
    for x in range(0,len(priceList)):

        if tradeType == "s" or tradeType == "Sell":
            placeSellOrder(priceList[x], orderSize, order_type, coin)
            numOrders += 1

        if tradeType == "b" or tradeType == "Buy":
            placeBuyOrder(priceList[x], orderSize, order_type, coin)
            numOrders += 1

        if numOrders == 15 or numOrders == 30 or numOrders == 45:
            print("Sleep -> NumOrders == ", numOrders)
            time.sleep(1)


    print("Total Executed ", tradeType.upper(), " Orders: ", numOrders)
    print("----Closing Authenticated Session Now----")
    auth_client.session.close()
    print("----Authenicated Session Closed-----")


#Bid / Ask
def getCurrentPrice(coin):
    # Checking for Slippage
    bid = 0
    ask = 0
    try:
        coinData = auth_client.get_product_ticker(coin)
    except:
        print("NONE")

    bid = coinData['bid']
    ask = coinData['ask']
    return [bid, ask]


def placeMultipleOrdersTEST(coin, maxOrders, tradeType, order_type, orderSize, priceList):
    numOrders = 0

    # Checking for Slippage
    try:

        coinData = auth_client.get_product_ticker(coin)

        checkPrice = float(coinData['price'])
        lowerPrice = float(priceList[0])
        upperPrice = float(priceList[len(priceList) - 1])

        checkLower = lowerPrice - checkPrice
        lowerDiff = checkLower / checkPrice * 100

        checkUpper = upperPrice - checkPrice
        upperDiff = checkUpper / checkPrice * 100

        print("Checking Price Before Executing Orders: ", coin, " Price: $", checkPrice)
        print("Trade Type: ", tradeType, " Lower Price: $", lowerPrice, " Upper Price: $", upperPrice)

        # Check For Slippage in Orders
        slippageWarning = 0
        if tradeType == "b" or tradeType == "Buy":

            if lowerDiff > 5 or upperDiff > 5:
                print("[BUY] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
                slippageWarning = 1

        if tradeType == "s" or tradeType == "Sell":

            if lowerDiff < 0:
                lowerDiff = lowerDiff * -1
            if upperDiff < 0:
                upperDiff = upperDiff * -1

            if lowerDiff > 100 or upperDiff > 100:
                print("[SELL] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
                slippageWarning = 1

        if slippageWarning == 0:
            for x in range(0, len(priceList)):

                if tradeType == "s" or tradeType == "Sell":
                    placeSellOrder(priceList[x], orderSize, order_type, coin)
                    numOrders += 1

                if tradeType == "b" or tradeType == "Buy":
                    placeBuyOrder(priceList[x], orderSize, order_type, coin)
                    numOrders += 1

                if numOrders == 15 or numOrders == 30 or numOrders == 45:
                    print("Sleep -> NumOrders == ", numOrders)
                    time.sleep(1)

    except:
        print("Failed To Place Order")


    print("Total Executed ", tradeType.upper(), " Orders: ", numOrders)
    print("----Closing Authenticated Session Now----")
    auth_client.session.close()
    print("----Authenicated Session Closed-----")

# def placeMultipleOrdersTEST(coin, maxOrders, tradeType, order_type, orderSize, priceList):
#     numOrders = 0
#
#     # Checking for Slippage
#     try:
#
#         coinData = auth_client.get_product_ticker(coin)
#
#         checkPrice = float(coinData['price'])
#         lowerPrice = float(priceList[0])
#         upperPice = float(priceList[len(priceList) - 1])
#
#         checkLower = lowerPrice - checkPrice
#         lowerDiff = checkLower / checkPrice * 100
#
#         checkUpper = upperPrice - checkPrice
#         upperDiff = checkUpper / checkPrice * 100
#
#         print("Checking Price Before Executing Orders: ", coin, " Price: $", checkPrice)
#         print("Trade Type: ", tradeType, " Lower Price: $", lowerPrice, " Upper Price: $", upperPrice)
#
#         # Check For Slippage in Orders
#         slippageWarning = 0
#         if tradeType == "b" or tradeType == "Buy":
#
#             if lowerDiff > 5 or upperDiff > 5:
#                 print("[BUY] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
#                 slippageWarning = 1
#
#         if tradeType == "s" or tradeType == "Sell":
#
#             if lowerDiff < 0:
#                 lowerDiff = lowerDiff * -1
#             if upperDiff < 0:
#                 upperDiff = upperDiff * -1
#
#             if lowerDiff > 35 or upperDiff > 35:
#                 print("[SELL] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
#                 slippageWarning = 1
#
#         if slippageWarning == 0:
#             for x in range(0, len(priceList)):
#
#                 if tradeType == "s" or tradeType == "Sell":
#                     placeSellOrder(priceList[x], orderSize, order_type, coin)
#                     numOrders += 1
#
#                 if tradeType == "b" or tradeType == "Buy":
#                     placeBuyOrder(priceList[x], orderSize, order_type, coin)
#                     numOrders += 1
#
#                 if numOrders == 15 or numOrders == 30 or numOrders == 45:
#                     print("Sleep -> NumOrders == ", numOrders)
#                     time.sleep(1)
#     except:
#         print("Failed To Place Order")
#
#
#     print("Total Executed ", tradeType.upper(), " Orders: ", numOrders)
#     print("----Closing Authenticated Session Now----")
#     auth_client.session.close()
#     print("----Authenicated Session Closed-----")


def placeMultipleOrdersTEST2(coin, maxOrders, tradeType, order_type, orderSize, priceList):
    numOrders = 0

    # Checking for Slippage
    #try:

    coinData = auth_client.get_product_ticker(coin)

    checkPrice = float(coinData['price'])
    lowerPrice = float(priceList[0])
    upperPrice = float(priceList[len(priceList) - 1])
    print("lower: ", lowerPrice, " upper: ", upperPrice)

    checkLower = lowerPrice - checkPrice
    lowerDiff = checkLower / checkPrice * 100

    checkUpper = upperPrice - checkPrice
    upperDiff = checkUpper / checkPrice * 100

    print("Checking Price Before Executing Orders: ", coin, " Price: $", checkPrice)
    print("Trade Type: ", tradeType, " Lower Price: $", lowerPrice, " Upper Price: $", upperPrice)

    # Check For Slippage in Orders
    slippageWarning = 0
    if tradeType == "b" or tradeType == "Buy":

        if lowerDiff > 5 or upperDiff > 5:
            print("[BUY] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
            slippageWarning = 1

    if tradeType == "s" or tradeType == "Sell":

        if lowerDiff < 0:
            lowerDiff = lowerDiff * -1
        if upperDiff < 0:
            upperDiff = upperDiff * -1

        if lowerDiff > 35 or upperDiff > 35:
            print("[SELL] Slippage Warning -> Lower % Diff: ", lowerDiff, " Upper % Diff: ", upperDiff)
            slippageWarning = 1

    # Final Calculations -> Execution Price/Size Happens Here
    if slippageWarning == 0:
        for x in range(0, len(priceList)):

            if tradeType == "s" or tradeType == "Sell":
                placeSellOrder(priceList[x], orderSize[x], order_type, coin)
                numOrders += 1

            if tradeType == "b" or tradeType == "Buy":
                placeBuyOrder(priceList[x], orderSize[x], order_type, coin)
                numOrders += 1

            if numOrders == 15 or numOrders == 30 or numOrders == 45:
                print("Sleep -> NumOrders == ", numOrders)
                time.sleep(1)
    #except:
        #print("Failed To Place Order")


    print("Total Executed ", tradeType.upper(), " Orders: ", numOrders)
    print("----Closing Authenticated Session Now----")
    auth_client.session.close()
    print("----Authenicated Session Closed-----")


def placeSingleOrder():
    tradeType = "s"
    order_type = "limit"
    coin = "BCH-USD"
    lowerPrice = 0
    upperPrice = 0
    maxCoins = 0
    maxOrders = 0
    quoteIncrement = getSpecificQuoteIncrement(coin)
    baseMinSize = getSpecificBaseMinSize(coin)

    priceList = generatePrices(coin, lowerPrice, upperPrice, quoteIncrement, maxOrders)
    orderSize = generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders)

    print("Coin:", coin, "Trade Type [", tradeType, "] Price Range: ", lowerPrice, " - ", upperPrice, " Max Coins: ",
          maxCoins, " Max Orders: ", maxOrders)
    print("Average Order Size: ", orderSize)

    displayOrderDataBeforePlacing(coin, tradeType, priceList, orderSize)
    tradeConfirmation = input("Execute Trade? (0 = YES, 1 = NO)")

    if tradeConfirmation == "0":
        placeMultipleOrders(coin, maxOrders, tradeType, order_type, orderSize, priceList)
    else:
        print("Trade Confirmation: NO - Exitting Process")



def getOpenOrders():
    myOrders = auth_client.get_orders()
    orderList = list(myOrders)
    print(orderList)
    print("----------Total Orders: ", len(orderList), "------------------------")
    for x in range(0,len(orderList)):
        print(orderList[x]['side'], " | ", orderList[x]['product_id'], " Price: ", orderList[x]['price'], " Qty: ", orderList[x]['size'])
    print("----------Total Orders: ", len(orderList), "------------------------")

    return orderList

def getSpecificOrders(coin, side, numOrders):
    orderList = getOpenOrders()
    specificList = []
    for x in range(0, len(orderList)):
        if orderList[x]['product_id'] == coin:
            print("Product Matched: ", coin)

            if orderList[x]['side'] == side:
                specificList.insert(x, orderList[x])

    return specificList

def cancelSpecificOrders(coin, side, numOrders):
    specificList = getSpecificOrders(coin, side, numOrders)
    counter = 0

    for x in range(0, len(specificList)):
        if counter == numOrders:
            break

        if side == 'buy':
            counter += 1
            auth_client.cancel_order(specificList[x]['id'])
            print("[Canceled Buy Order] Coin: ", coin, " Price: ", specificList[x]['price'])

        if side == 'sell':
            auth_client.cancel_order(specificList[x]['id'])
            counter += 1
            print("[Canceled Sell Order] Coin: ", coin, " Price: ", specificList[x]['price'])

    print("----Closing Authenticated Session Now----")
    auth_client.session.close()
    print("----Authenicated Session Closed-----")


def convertFloats(floatNumber):
    convertedNumber = 0
    if floatNumber != 0:
        convertedNumber = round(float(floatNumber), 2)
    else:
        convertedNumber = 0
    return convertedNumber

# Updated to include available and hold
def checkBalances(coin):
    # Get List of Balances With Balance > 0
    accounts = auth_client.get_accounts()
    balances = []
    balanceCount = 0

    splitCoin = str(coin).split("-")
    for x in range(0, len(accounts)):
        checkBalance = float(accounts[x]['balance'])
        checkCoin = accounts[x]['currency']

        if checkCoin == splitCoin[1]:
            balances.insert(balanceCount, {
                "coin": accounts[x]['currency'],
                "balance": convertFloats(accounts[x]['balance']),
                "available": convertFloats(accounts[x]['available']),
                "hold": convertFloats(accounts[x]['hold'])
            })

        if checkCoin == splitCoin[0]:
            balances.insert(balanceCount, {
                "coin": accounts[x]['currency'],
                "balance": convertFloats(accounts[x]['balance']),
                "available": convertFloats(accounts[x]['available']),
                "hold": convertFloats(accounts[x]['hold'])
            })
            balanceCount += 1


    return balances

