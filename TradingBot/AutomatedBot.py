import cbpro
import time
import datetime
from itertools import islice
from Keys import getAuthClient
from Config_Center import *
import json
from CreateOrders import *

auth_client = getAuthClient()
public_client = cbpro.public_client
botConfig_filename = 'bot_config.json'
botConfig_filename_custom = 'NewBotConfig1.json'
bot1_OpenOrders = 'openOrders_1.json'

tradeLogFileName = 'tradeLog_1.json'
tradeLogFileName2 = 'tradeLog_2.json'
profitFromFilledSellOrders = 0


def getCurrentDate():
    currentDate = datetime.datetime.now()
    return currentDate.strftime("%m-%d-%Y %I:%M:%S")

# Read from the JSON config to gather current Thresholds PER Coin // NOT USED ANYMORE
def getCurrentCoinThresholds(coin):
    configValues = displayJsonData(botConfig_filename, coin)
    try:
        if coin == configValues[0]['Coin']:
            return configValues
    except:
        configValues = displayJsonData(botConfig_filename, "ALL")
        return configValues


def createOrderJSON(fileName):
    orderList = getOpenOrders()
    orderStructure = {'OpenOrders': []}

    for x in range(len(orderList)):
        orderObj = {'id': orderList[x]['id'],
                    'product_id': orderList[x]['product_id'],
                    'price': orderList[x]['price'],
                    'size': orderList[x]['size'],
                    'side': orderList[x]['side']
                    }

        orderStructure['OpenOrders'].insert(x, orderObj)

    writeJsonData(fileName, orderStructure)


def getOpenOrders():
    myOrders = auth_client.get_orders()
    myOrderList = list(myOrders)

    return myOrderList



def trackOpenOrders(fileName):
    activeOrders = getOpenOrders()
    # print("[trackOpenOrders] -> New Open Order List Length -> ", len(activeOrders))

    orderStructureFromJSON = readJsonData(fileName)
    ordersFromJSON = orderStructureFromJSON['OpenOrders']

    desc = "[Track Open Orders] - "
    #print(desc + " ordersFromJSON Length: " + str(len(ordersFromJSON)))
    #print(desc, ordersFromJSON)

    tracker = 0
    trigger = 0
    filledOrMissingOrders = []

    # Need to add a conditional to account for NO orders being active
    if len(activeOrders) == 0:
        trigger = 1
        print("=======---------- NO ACTIVE OPEN ORDERS -----======== " + str(getCurrentDate()))
        for x in range(len(ordersFromJSON)):
            filledOrMissingOrders.insert(x, ordersFromJSON[x])

    else:
        for x in range(len(ordersFromJSON)):
            orderID1 = ordersFromJSON[x]['id']

            for y in range(len(activeOrders)):

                orderID2 = activeOrders[y]['id']

                if orderID1 == orderID2:
                    tracker = 1

                if y == len(activeOrders) - 1:
                    if tracker == 0:
                        # print("ORDER from JSON is missing from Active Orders -> " + orderID1)
                        # print("This means it must've been canceled / filled... ")
                        trigger = 1
                        # print(ordersFromJSON[x])
                        # print("INSERTED ------------------: ")
                        filledOrMissingOrders.insert(len(filledOrMissingOrders), ordersFromJSON[x])
                    else:
                        # print("Setting Tracker Var Back to 0")
                        tracker = 0

    trackOpenOrderData = [trigger, filledOrMissingOrders, ordersFromJSON, activeOrders]
    return trackOpenOrderData



def trackManuallyCreatedOpenOrders(fileName):
    # ordersFromJSON = trackOpenOrderData[2]

    activeOrders = getOpenOrders()

    orderStructureFromJSON = readJsonData(fileName)
    ordersFromJSON = orderStructureFromJSON['OpenOrders']

    tracker = 0
    trigger = 0

    newJSONOrders = []
    activeListButNotInJSON = []

    for x in range(len(activeOrders)):
        orderID1 = activeOrders[x]['id']
        for y in range(len(ordersFromJSON)):
            orderID2 = ordersFromJSON[y]['id']

            if orderID1 == orderID2:
                tracker = 1

        if len(ordersFromJSON) == 0:
            trigger = 1
            activeListButNotInJSON.insert(len(activeListButNotInJSON), x)
            #print("Adding new order to JSON DATA -> ", activeOrders[x])

        elif y == len(ordersFromJSON) - 1:
            if tracker == 0:
                trigger = 1
                activeListButNotInJSON.insert(len(activeListButNotInJSON), x)
                #print("Adding new order to JSON DATA -> ", activeOrders[x])
            else:
                tracker = 0

    if trigger == 1:
        #print(activeListButNotInJSON)
        for x in range(len(activeListButNotInJSON)):
            orderFromJSONLength = len(ordersFromJSON) - 1
            activeOrdersValueInt = int(activeListButNotInJSON[x])
            ordersFromJSON.insert(orderFromJSONLength, activeOrders[activeOrdersValueInt])
            #print("[TrackManuallyCreatedOrders] - Added - " + str(activeOrders[activeOrdersValueInt]['id']) + " // Price: " + str(activeOrders[activeOrdersValueInt]['price']) + " || OrdersFromJSON new length = " + str(len(ordersFromJSON)))
            #print("ordersFromJSON new length -> ", len(ordersFromJSON))

    trackerManualCreatedOrders = [trigger, ordersFromJSON]
    return trackerManualCreatedOrders


coinData = generateProductList()  # [{id,quote_increment,base_min_size}]


def checkOrderStatus(trackOpenOrderData, coinData, profitFromFilledSellOrders, startTime):
    trigger = trackOpenOrderData[0]
    filledOrMissingOrders = trackOpenOrderData[1]
    ordersFromJSON = trackOpenOrderData[2]
    #print("CHECKING ORDERS STATUS --------> ORDERS FROM JSON LENGTH: ", len(ordersFromJSON))

    ordersToRemoveFromJSON = []
    newOrdersCreated = []
    orderWasCreated = 0

    buyVolume = 0
    sellVolume = 0
    buyOrderCount = 0
    sellOrderCount = 0
    orderWasPlaced = 0
    buySize = 0
    sellSize = 0

    newArr = []
    desc = "[Check Order Status] - "
    if trigger == 1:

        for y in range(len(ordersFromJSON)):
            orderID1 = ordersFromJSON[y]['id']
            newArr.insert(len(newArr), ordersFromJSON[y])
            #print("Iteration [" + str(y) + "] - newArr -> ", newArr)
            checkOrder = []

            for x in range(len(filledOrMissingOrders)):
                if orderID1 == filledOrMissingOrders[x]['id']:
                    try:
                        checkOrder = auth_client.get_order(filledOrMissingOrders[x]['id'])
                        #print("Iteration [Y/X] [" + str(y) + ", " + str(x) + "] ", checkOrder)
                    except:
                        idk=0
                        #print("Check Order Failed")
                    try:

                        if checkOrder['message'] == 'NotFound':
                            #print("Order Must've Been Canceled -> No Longer Track This Order ID " + filledOrMissingOrders[x]['id'])

                            # Remove order info from the array to stop tracking it
                            if len(newArr) == 1:
                                #print("[Cancel/Missing] Popping NewArr -> ", newArr)
                                newArr.pop(0)
                            else:
                                #print("[Cancel/ Missing] Popping NewArr -> ", newArr[len(newArr) - 1])
                                newArr.pop(len(newArr) - 1)


                    except:

                        filledPrice = checkOrder['price']
                        filledFee = float(checkOrder['fill_fees'])
                        filledSize = float(checkOrder['filled_size']) # changed from size to filled_size /// looking potentially ['executed_value'] as well

                        if str(checkOrder['settled']) == "True" and filledSize != 0:
                            # print("Need to Create an Opposing Order for this ORDER")
                            coin = filledOrMissingOrders[x]['product_id']
                            tradeType = filledOrMissingOrders[x]['side']
                            size = float(filledOrMissingOrders[x]['size'])
                            price = float(filledOrMissingOrders[x]['price'])
                            fee = float(checkOrder['size'])

                            # uniqThresholds = getCurrentCoinThresholds(coin)
                            # buyThreshold = float(uniqThresholds[0]['BuyThreshold1'])
                            # sellThreshold = float(uniqThresholds[0]['SellThreshold1'])


                            if tradeType == 'buy':
                                # Check for Customized Thresholds --
                                thresholds = checkThresholdAgainstFilledPrice(botConfig_filename_custom, coin, "buy", float(filledPrice))
                                buyThreshold = float(thresholds[0])
                                sellThreshold = float(thresholds[1])

                                calcNewPrice = price * sellThreshold
                                incrementNewPrice = price + calcNewPrice
                                convertPrice = calcQuotePrice(coin, incrementNewPrice, coinData)


                                createSellOrder = placeIndividualSellOrder(convertPrice, filledSize, "limit", coin, coinData)

                                newOrdersCreated.insert(len(newOrdersCreated), createSellOrder)

                                buyVolume = (float(filledPrice) * float(filledSize)) + filledFee

                                sellVolume = (float(convertPrice) * float(filledSize)) + filledFee
                                potentialProfit = (float(convertPrice) * filledSize  + fee) - buyVolume

                                pp = sellVolume - buyVolume

                                filledStr = "[Buy Order Filled] - [" + coin + "] - Price: $" + str(filledPrice) + " | Size: " + str(filledSize ) + " | Total With Fees: $ " + str(round(buyVolume,2)) + " [" + getCurrentDate() + "]"
                                #Disabled --- NEED TO FIX ---- 3/19/2022
                                #updateTradeLog(tradeLogFileName, filledStr)
                                filledArr = [coin, tradeType, price, size,  round(buyVolume, 2), round(filledFee,2), buyThreshold, sellThreshold, convertPrice, filledSize, sellVolume, getCurrentDate()]
                                # Disabled --- NEED TO FIX ---- 3/19/2022
                                #updateTradeLog(tradeLogFileName, filledStr)
                                # Disabled --- NEED TO FIX ---- 3/19/2022
                                #updateTradeLogForTableDisplay(tradeLogFileName2, filledArr)
                                print("[Buy Order Filled] - [" + coin + "] - Price: $" + str(filledPrice) + " | Size: " + str(filledSize ) + " | Total With Fees: $ " + str(round(buyVolume,2)))
                                print("[Sell Order Created] - [" + coin + "] - Price $" + str(convertPrice) + " | Size: " + str(
                                    filledSize) + " | Est Profit if Filled Based on Buy Threshold [" + str(buyThreshold) + "]  $" + str(
                                    round(pp, 2)))
                                print("-------------------------------------------------------------------------")


                                # Remove Current Order from Array -> and Push the newly created order info in the Arr
                                if len(newArr) == 1:
                                    #print("[Buy Filled] Popping NewArr -> ", newArr)
                                    newArr.pop(0)
                                    newArr.insert(len(newArr), createSellOrder)
                                else:
                                    #print("[Buy Filled] Popping NewArr -> ", newArr[len(newArr) - 1])
                                    newArr.pop(len(newArr) - 1)
                                    newArr.insert(len(newArr), createSellOrder)
                                orderWasCreated = 1

                            elif tradeType == 'sell':
                                # Check for Customized Thresholds --
                                thresholds = checkThresholdAgainstFilledPrice(botConfig_filename_custom, coin, "sell", float(filledPrice))
                                buyThreshold = float(thresholds[0])
                                sellThreshold = float(thresholds[1])

                                calcNewPrice = price * buyThreshold
                                incrementNewPrice = price - calcNewPrice
                                convertPrice = calcQuotePrice(coin, incrementNewPrice, coinData)
                                createBuyOrder = placeIndividualBuyOrder(convertPrice, filledSize , "limit", coin, coinData)
                                newOrdersCreated.insert(len(newOrdersCreated), createBuyOrder)

                                #potentialProfit = convertPrice * sellThreshold + fee
                                sellVolume = (float(filledPrice) * float(filledSize)) + filledFee

                                buyVolume = (float(convertPrice) * filledSize + filledFee)
                                #print("SellVol: " + str(sellVolume) + " // precalc " + str(holder))


                                pp = sellVolume - buyVolume
                                # print("ConverPrice: " + str(convertPrice) + " BuyVol: " + str(buyVolume) + " Sell Vol: " + str(sellVolume) + " PP : " + str(pp))

                                filledStr = "[Sell Order Filled] - [" + coin + "] - Price: $" + str(filledPrice) + " | Size: " + str(filledSize) + " | Total With Fees: $ " + str(round(sellVolume,2)) +" [" + getCurrentDate() + "]"
                                filledArr = [coin, tradeType, price, size,  round(sellVolume, 2), round(filledFee,2), buyThreshold, sellThreshold, convertPrice, filledSize, buyVolume, getCurrentDate()]
                                #DISABLED NEED TO FIX----- 3/19/2022
                                #updateTradeLog(tradeLogFileName, filledStr)
                                #updateTradeLogForTableDisplay(tradeLogFileName2, filledArr)

                                print("[Sell Order Filled] - [" + coin + "] - Price: $" + str(filledPrice) + " | Size: " + str(filledSize) + " | Total With Fees: $ " + str(round(sellVolume,2)) + " Estimated Profit: $ " + str(round(pp,2)))
                                print("[Buy Order Created] - [" + coin + "] - Price $" + str(convertPrice) + " | Size: " + str(
                                    filledSize) + " | Potenital Profit Using Buy Threshold [" + str(buyThreshold) + "] $" + str(
                                    round(pp, 2)))

                                profitFromFilledSellOrders += pp
                                print("----------------(.)---(.)---------------(.)---(.)--------(.)---(.)-------------")

                                #print("-------StartTime [" + str(startTime) + "]-------------------Total Profits From Sells $" + str(round(profitFromFilledSellOrders,2))+ "-------- Current Time [" + str(getCurrentDate()) + "]--------------------------------------")

                                # Remove Current Order from Array -> and Push the newly created order info in the Arr
                                if len(newArr) == 1:
                                    #print("[Sell Filled] Popping NewArr -> ", newArr)
                                    newArr.pop(0)
                                    newArr.insert(len(newArr), createBuyOrder)
                                else:
                                    #print("[Sell Filled] Popping NewArr -> ", newArr[len(newArr) - 1])
                                    newArr.pop(len(newArr) - 1)
                                    newArr.insert(len(newArr), createBuyOrder)
                                orderWasCreated = 1
                            else:
                                #print("Trade Type Not Found -> Doing Nothing")
                                idk = 0
                        else:
                            #print("STATUS = FALSE -> DO NOTHING")
                            idk = 0
    else:
        idk=0
        #print("No Orders Btwn the JSON & Active List were Triggered")


    #print(newArr)
    newOrderTracker = [orderWasCreated, newOrdersCreated, newArr, profitFromFilledSellOrders]  # changed newarr from orderjson
    return newOrderTracker


def combineOrders(fileName, trackOpenOrderData, newOrdersTracker):
    trigger = trackOpenOrderData[0]
    orderWasCreated = newOrdersTracker[0]

    filledOrMissingOrders = trackOpenOrderData[1]
    newOrdersCreated = newOrdersTracker[1]

    ordersFromJSON = newOrdersTracker[2]

    #print("[combineOrders] - ORDERSFROMJSON -> ", len(ordersFromJSON))

    desc = "[Combine Orders] - "
    arr1 = []
    arr2 = []

    if trigger == 1:
        #print("Trigger -> 1 -> Changes have been made btwn the 2 lists")

        if orderWasCreated == 1:
            #print("Trigger = 1 && OrderWasCreated = 1 -> New Orders Were Created -> Restructure List")
            # print("Removing Orderrs from the JSON LIST -> Returning a new list")
            # arr1 = removeOrdersFromJSON(ordersFromJSON, ordersToRemove)
            #print("Adding new Orders to that returned list")
            arr2 = addNewOrdersToJSON(ordersFromJSON, newOrdersCreated)
            #print("NEW LIST LENGTH -> ", len(arr2))

            return arr2

        else:
            idk=0
            #print("Trigger = 1 && OrderWasCreated = 0 -> Missing Orders ONLY -> ")
            return ordersFromJSON

    else:
       # print("Trigger = 0 -> No Changes Made -> Identical JSON data with Active Orders")
        return ordersFromJSON


def addNewOrdersToJSON(ordersFromJSON, newOrdersCreated):
    newStructure = []
    for x in range(len(newOrdersCreated)):
        orderFromJSONLength = len(ordersFromJSON) - 1
        ordersFromJSON.insert(orderFromJSONLength, newOrdersCreated[x])
    return ordersFromJSON


def updateOpenOrdersJSON(fileName, ordersFromJSON):
    newOrders = {'OpenOrders': []}

    for x in range(len(ordersFromJSON)):
        try:
            orderObj = {'id': ordersFromJSON[x]['id'],
                        'product_id': ordersFromJSON[x]['product_id'],
                        'price': ordersFromJSON[x]['price'],
                        'size': ordersFromJSON[x]['size'],
                        'side': ordersFromJSON[x]['side']
                        }
            newOrders['OpenOrders'].insert(x, orderObj)
        except:
            idk=0
            #print("failed to update an order [", x, "]")

    writeJsonData(fileName, newOrders)


createOrderJSON(bot1_OpenOrders)
time.sleep(1)
running = 0

profitFromFilledSellOrders = 0
profits = 0

startTime = getCurrentDate()

while running == 0:
    ordersFromJson = []
    filledOrMissingOrders = []
    activeOrders = []
    trackerData1 = []


    try:
        # print("OrdersFromJson Top Loop -> ", len(ordersFromJson))
        # Checks JSON -> if orders were executed from the List
        trackerOpenOrderData1 = trackOpenOrders(bot1_OpenOrders)

        # Checks Active Open Orders -> If missing from JSON list (manually created orders)
        # Returns a Combined List of any Active Open Orders + All the Orders from the JSON
        # trackerManualCreatedOrders = trackManuallyCreatedOpenOrders(trackerOpenOrderData1)

        ordersFromJson = trackerOpenOrderData1[2]
        filledOrMissingOrders = trackerOpenOrderData1[1]
        activeOrders = trackerOpenOrderData1[3]

        trackerData1 = [trackerOpenOrderData1[0], filledOrMissingOrders, ordersFromJson, activeOrders]
        if trackerOpenOrderData1[0] == 1:

            newOrdersCreated = checkOrderStatus(trackerData1, coinData, profitFromFilledSellOrders, startTime)

            # newOrdersForJSON = combineOrders(bot1_OpenOrders, trackerData1, newOrdersCreated)

            profitFromFilledSellOrders = float(newOrdersCreated[3])
            # updateOpenOrdersJSON(bot1_OpenOrders, newOrdersForJSON)
            updateOpenOrdersJSON(bot1_OpenOrders, newOrdersCreated[2])



        else:
            trackerManualCreatedOrders = trackManuallyCreatedOpenOrders(bot1_OpenOrders)
            if trackerManualCreatedOrders[0] == 1:
                updateOpenOrdersJSON(bot1_OpenOrders, trackerManualCreatedOrders[1])

        time.sleep(5)

    except:
         print("Failed--- API ---- Sleep 3 Sec --- ")
         time.sleep(5)








