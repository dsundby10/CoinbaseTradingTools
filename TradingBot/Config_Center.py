import json

# Testing Vars
fileName = 'json_data.json'
botConfig_filename = 'bot_config.json'

def writeJsonData(fileName, data):
    with open(fileName, 'w') as outfile:
        json_string = json.dumps(data)
        outfile.write(json_string)

def readJsonData(fileName):
    with open(fileName) as json_file:
        data = json.load(json_file)
    return data

def displayJsonData(fileName, coinToFind):
    newData = readJsonData(fileName)
    base = newData['TradingPairs']
    allValues = []
    for x in range(len(base)):
        if base[x]['Coin'] == coinToFind:
            allValues.insert(0, base[x])
    return allValues

# Update Data in Json File
def updateJsonData(fileName, data, coinToFind, allValues):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']
    for x in range(len(base)):

        if str(base[x]['Coin']) == str(coinToFind):

            updatedObj = {'Coin': coinToFind,
                       'BuyThreshold1': allValues[0],
                       'SellThreshold1':allValues[1],
                       'BuyThreshold2': allValues[2],
                       'SellThreshold2': allValues[3],
                       'BuyThreshold3': allValues[4],
                       'SellThreshold3': allValues[5],
                       'StopPlacingBuysPrice': allValues[6],
                       'StopPlacingSellsPrice': allValues[7]}
            newData['TradingPairs'].insert(x, updatedObj)
        else:
            newData['TradingPairs'].insert(x, base[x])

    writeJsonData(fileName, newData)

def calculateTradeHistory(currentValues, newValues, tradeType):
    buyVolume = float(currentValues['BuyVolume']) + float(newValues[0])
    sellVolume = float(currentValues['SellVolume']) + float(newValues[1])
    coinsBought = float(currentValues['CoinsBought']) + float(newValues[2])
    coinsSold = float(currentValues['CoinsSold']) + float(newValues[3])
    numBuyOrders = float(currentValues['NumBuyOrders']) + float(newValues[4])
    numSellOrders = float(currentValues['NumSellOrders']) + float(newValues[5])
    fees = float(currentValues['Fees']) + float(newValues[6])

    getDiff = sellVolume - buyVolume

    if tradeType == 'sell':
        PL = float(currentValues['PL']) + getDiff
        buyVolume = float(currentValues['BuyVolume']) + 0
    else:
        PL = currentValues['PL']
        sellVolume = float(currentValues['SellVolume'])

    return [buyVolume, sellVolume, coinsBought, coinsSold, numBuyOrders, numSellOrders, fees, PL]


def updateTradeHistoryData(fileName, data, coinToFind, newValues, tradeType):
    configData = readJsonData(fileName)
    newData = {'TradeHistory': []}
    base = configData['TradeHistory']

    valuesToReturn = []
    for x in range(len(base)):
        if str(base[x]['Coin']) == str(coinToFind):
            currentValues = []
            #print("Before: ", base[x])
            allValues = calculateTradeHistory(base[x], newValues, tradeType)
            updatedObj = {'Coin': coinToFind,
                          'BuyVolume': allValues[0],
                          'SellVolume': allValues[1],
                          'CoinsBought': allValues[2],
                          'CoinsSold': allValues[3],
                          'NumBuyOrders': allValues[4],
                          'NumSellOrders': allValues[5],
                          'Fees': allValues[6],
                          'PL': allValues[7],
                          #'EstimatedPL': allValues[8]
                          }
            #print("Updated: ", updatedObj)
            newData['TradeHistory'].insert(x, updatedObj)
        else:
            newData['TradeHistory'].insert(x, base[x])

    writeJsonData(fileName, newData)
    return allValues


def restructureCoinList(coinList):
    newCoinList = []
    for x in range(len(coinList)):
        if x == 0:
            newCoinList.insert(len(newCoinList), "ALL")
        else:
            if x == len(coinList)-1:
                newCoinList.insert(len(newCoinList), coinList[x])
            else:
                newCoinList.insert(len(newCoinList), coinList[x-1])
    return newCoinList

# Base Data Creation for New Users
def createBaseJsonData(coinList, filePathToCreate):
    newData = {'TradingPairs': []}
    for x in range(len(newCoinList)):
        dataObj = {'Coin': newCoinList[x],
                   'BuyThreshold1': .01,
                   'SellThreshold1': .01,
                   'BuyThreshold2': .015,
                   'SellThreshold2': .015,
                   'BuyThreshold3': .02,
                   'SellThreshold3': .02,
                   'StopPlacingBuysPrice': 2500,
                   'StopPlacingSellsPrice': 2600}
        newData['TradingPairs'].insert(x, dataObj)
    writeJsonData(filePathToCreate, newData)

# Base Data Creation for New Users
def createBaseBotConfigData(coinList, filePathToCreate):
    newData = {'TradingPairs': []}
    for x in range(len(newCoinList)):
        dataObj = [{'Coin': newCoinList[x],
                    'Enabled': False,
                   'BuyThreshold1': .05,
                   'SellThreshold1': .01,
                   }]
        newData['TradingPairs'].insert(x, dataObj)
    writeJsonData(filePathToCreate, newData)


def updateBotConfigSpecialThresholds(fileName, coinToFind, updatedValues):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    # [{data data data}, {datata}], [{datadatadat}, {data adad}]
    for x in range(len(base)):

        #print(base[x][0]['Coin'])
        if str(base[x][0]['Coin']) == str(coinToFind):
            #print("Yes" + str(len(base[x])))
            newArr = []
            for y in range(len(base[x])):
                newArr.insert(len(newArr), base[x][y])
                print("Y: " + str(y) + " // ", newArr)
                if y == len(base[x])-1:
                    newArr.insert(len(newArr), updatedValues)
                    print("Y: " + str(y) + " // ", newArr)
                    newData['TradingPairs'].insert(x, newArr)
        else:
            newData['TradingPairs'].insert(x, base[x])

    writeJsonData(fileName, newData)


def removeBotConfigSpecialThresholds(fileName, coinToFind, valuesToRemove):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']


    for x in range(len(base)):

        # print(base[x][0]['Coin'])
        if str(base[x][0]['Coin']) == str(coinToFind):
            print(base[x])
            # print("Yes" + str(len(base[x])))
            newArr = []
            for y in range(len(base[x])):
                if valuesToRemove == base[x][y]:
                    print("Removing -> Y: " + str(y) + " // ")
                else:
                    newArr.insert(len(newArr), base[x][y])
                if y == len(base[x]) - 1:

                    newData['TradingPairs'].insert(x, newArr)
        else:

            newData['TradingPairs'].insert(x, base[x])

    writeJsonData(fileName, newData)

objToAdd1 = {'SellThreshold1': .05,
            'Price1': .49,
            'Price2': .495}
objToAdd2 = {'SellThreshold1': .03,
            'Price1': .48,
            'Price2': .489}
objToAdd3 = {'SellThreshold1': .09,
            'Price1': .47,
            'Price2': .48}

objToAdd4 = {'BuyThreshold1': .08,
            'Price1': .52,
            'Price2': .53}

objToAdd5 = {'BuyThreshold1': .025,
            'Price1': .5,
            'Price2': .51}

objToAdd6 = {'BuyThreshold1': .04,
            'Price1': .515,
            'Price2': .52}



def checkThresholdAgainstFilledPrice(fileName, coin, tradeType, filledPrice):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    currentThreshold = 0
    buyThreshold = 0
    sellThreshold = 0
    for x in range(len(base)):

        if str(base[x][0]['Coin']) == str(coin):
            if base[x][0]['Enabled'] == True:
                print("Custom Thresholds ARE ENABLED -- CHECKING THRESHOLDS")
                if tradeType == "buy":
                    buyThreshold = base[x][0]['BuyThreshold1']
                    sellThreshold = base[x][0]['SellThreshold1']

                    for y in range(len(base[x])):
                        try:
                            threshold = base[x][y]['SellThreshold1']

                            if filledPrice >= float(base[x][y]["Price1"]) and filledPrice < float(base[x][y]["Price2"]):
                                #print("Price1" + str(base[x][y]["Price1"]) + " // " + str(base[x][y]["Price2"]))
                                print("Custom Sell Threshold Found for Filled Buys Btwn " + str(base[x][y]["Price1"]) + " // " + str(base[x][y]["Price2"]) + " Setting Sell Threshold to " + str(threshold))
                                sellThreshold = base[x][y]['SellThreshold1']
                        except:
                            k=0
                            #print("N/a")

                else:
                    buyThreshold = base[x][0]['BuyThreshold1']
                    sellThreshold = base[x][0]['SellThreshold1']


                    for y in range(len(base[x])):
                        try:
                            threshold = base[x][y]['BuyThreshold1']
                            #print(threshold)
                            if filledPrice >= float(base[x][y]["Price1"]) and filledPrice < float(base[x][y]["Price2"]):
                                print("Custom Buy Threshold Found for Filled Sells Btwn " + str(
                                    base[x][y]["Price1"]) + " // " + str(
                                    base[x][y]["Price2"]) + " Setting Buy Threshold to " + str(threshold))


                                buyThreshold = base[x][y]['BuyThreshold1']
                        except:
                            k=0
            else:
                buyThreshold = base[x][0]['BuyThreshold1']
                sellThreshold = base[x][0]['SellThreshold1']
                print("Custom Threshold Not Enabled ---- Returning Default Values: " + str(buyThreshold) + " // " + str(sellThreshold))

    #print("Retrurned: " + str(buyThreshold) + " || " + str(sellThreshold))
    return [buyThreshold, sellThreshold]


def createBaseTradeHistoryData(coinList, filePathToCreate):
    newData = {'TradeHistory': []}
    for x in range(len(newCoinList)):
        dataObj = {'Coin': newCoinList[x],
                   'BuyVolume': 0,
                   'SellVolume': 0,
                   'CoinsBought': 0,
                   'CoinsSold': 0,
                   'NumBuyOrders': 0,
                   'NumSellOrders': 0,
                   'Fees': 0,
                   'PL': 0,
                   'EstimatedPL': 0
                   }
        newData['TradeHistory'].insert(x, dataObj)
    writeJsonData(filePathToCreate, newData)




def createActiveOpenOrdersData():
    newData = {'OpenOrders': []}


def createTradeLog(fileName):
    newData = {'TradeLog': []}
    writeJsonData(fileName, newData)
    return newData
#createTradeLog('indicators.json')


def updateTradeLog(fileName, dataToAdd):
    newData = readJsonData(fileName)
    base = newData['TradeLog']
    newLog = {'TradeLog': base}
    newLog['TradeLog'].insert(len(base), dataToAdd)
    writeJsonData(fileName, newLog)

#filledArr = [coin, price, size, round(sellVolume,2), buyThreshold, sellThreshold, convertPrice, filledSize, buyVolume, getCurrentDate()]
def updateTradeLogForTableDisplay(fileName, dataToAdd):
    newData = readJsonData(fileName)
    base = newData['TradeLog']
    newLog = {'TradeLog': base}
    dataObj = {
        'coin': dataToAdd[0],
        'side': dataToAdd[1],
        'price1': dataToAdd[2],
        'size1': dataToAdd[3],
        'volume1': dataToAdd[4],
        'fee': dataToAdd[5],
        'buyThreshold': dataToAdd[6],
        'sellThreshold': dataToAdd[7],
        'price2': dataToAdd[8],
        'size2': dataToAdd[9],
        'volume2': dataToAdd[10],
        'timestamp': dataToAdd[11]
    }
    newLog['TradeLog'].insert(len(base), dataObj)
    writeJsonData(fileName, newLog)



def updateTechnicalAnalysisValues(symbol):
    newData = readJsonData(fileName)
    base = newData['Indicators']
    newLog = {'Indicators': base}

# Used for Threshold Data MA Values
def roundMA(num):
    num1 = float(num)
    roundedNum = 0
    if num > 1:
        roundedNum = round(num1,2)
    elif num > .01:
        roundedNum = round(num1, 4)
    else:
        roundedNum = num1
    return roundedNum

# Used for Threshold Table Data MA Values
def readTechnicalAnalysisValues(fileName, symbol):
    newData = readJsonData(fileName)
    base = newData['Indicators']

    newArr = []

    for x in range(len(base)):
        b = base[x]
        # Timeframe, Open, Volume, Change, MA5/
        #arr = [b[1], b[3], round(b[5],2), round(b[6],2), b[7], b[8],b[9],b[10],b[11],b[12],b[13]]
        arr = [b[1], roundMA(b[3]), roundMA(b[5]), round(b[6],2), roundMA(b[7]), roundMA(b[8]), roundMA(b[9]), roundMA(b[10]), roundMA(b[11]), roundMA(b[12]), roundMA(b[13])]

        newArr.insert(len(newArr), arr)

    return newArr

#-- Testing Area --- #
#readTechnicalAnalysisValues("SUKU-USD")
#createTradeLog('tradeLog_1.json')
#createTradeLog('tra')