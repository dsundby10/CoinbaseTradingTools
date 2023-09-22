import cbpro
import time
import datetime
import json
from itertools import islice
from Keys import getAuthClient
from Config_Center import *
from CreateOrders import *
from OrderManagement import *
from Indicators import *
import PySimpleGUI as sg
auth_client = getAuthClient()



# Sort Open Orders By Product ID
def generateAllOpenOrdersSortedProductList(allOpenOrders):
    openOrderProductList = []
    for x in range(len(allOpenOrders)):
        openOrderProductList.insert(len(openOrderProductList), allOpenOrders[x]['product_id'])
    return sorted(openOrderProductList)


# Categorize Sorted Product List by Uniq Pairs
def generateUniqPairs(sortedProductList):
    uniqPairs = []
    count=0
    if len(sortedProductList) != 0:
        uniqPairs.insert(0, sortedProductList[0])
        for x in range(len(sortedProductList)):
            currentCoin = sortedProductList[x]

            if uniqPairs[count] != currentCoin:
                count+=1
                uniqPairs.insert(count, currentCoin)
    return uniqPairs

# Updates Threshold Data in the JSON file
def updateThresholdData(fileName, coinToFind, allValues):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    for x in range(len(base)):

        if str(base[x][0]['Coin']) == str(coinToFind):
            newArr = []
            for y in range(len(base[x])):
                if y == 0:
                    updatedObj = {'Coin': coinToFind,
                                  'Enabled': base[x][0]['Enabled'],
                                  'BuyThreshold1': allValues[0],
                                  'SellThreshold1': allValues[1],
                                  }
                    newArr.insert(len(newArr), updatedObj)
                    #newData['TradingPairs'].insert(x, updatedObj)
                else:
                    newArr.insert(len(newArr), base[x][y])

                # End
                if y == len(base[x]) - 1:
                    newData['TradingPairs'].insert(x, newArr)
        else:
            newData['TradingPairs'].insert(x, base[x])

    writeJsonData(fileName, newData)


# Get Balances based off the Unique Generated Product List
def getBalances(uniqProductList):
    # Get List of Balances With Balance > 0
    accounts = auth_client.get_accounts()
    balances = []
    balanceCount = 0
    for x in range(0, len(accounts)):
        checkBalance = float(accounts[x]['balance'])
        coin = accounts[x]['currency']
        coinAmt = accounts[x]['balance']

        for y in range(len(uniqProductList)):
            checker = str(uniqProductList[y]).split("-")
            if str(coin) == checker[0]:
                total = accounts[x]['balance']
                available = accounts[x]['available']
                hold = accounts[x]['hold']
                holderArr = [uniqProductList[y], total, available, hold]
                balances.insert(len(balances), holderArr)

    auth_client.session.close()
    return balances

def calculateUSDValue(price, size):
    newPrice = float(price) * float(size)
    return newPrice

# Generating Low / High Prices of Open orders for both BUYS & SELLS
def generateHighsAndLows(uniqProductList, allOpenOrders):

    allDataArr = []

    #Genereate Balances Based off Uniq Product List
    balances = getBalances(uniqProductList)

    for x in range(len(uniqProductList)):
        currentCoin = uniqProductList[x]
        ticker = auth_client.get_product_ticker(currentCoin)
        currentPrice = float(ticker['price'])
        currentAvailable = float(balances[x][2])
        #print(currentAvailable)
        highPrice = 0
        lowPrice = 0
        count = 1
        buyCount = 1
        sellCount = 1

        totalBuysCoins = 0
        totalSellCoins = 0

        totalUSDValueBuys = 0
        totalUSDValueSells = 0


        highestBuyPrice = 0
        lowestBuyPrice = 0

        highestSellPrice = 0
        lowestSellPrice = 0


        holderArr = []


        for y in range(len(allOpenOrders)):
            if allOpenOrders[y]['product_id'] == uniqProductList[x]:
                size = float(allOpenOrders[y]['size'])
                price = float(allOpenOrders[y]['price'])
                side = allOpenOrders[y]['side']
                if count == 1:
                    highPrice = float(allOpenOrders[y]['price'])
                    lowPrice = float(allOpenOrders[y]['price'])
                    count = 2

                    if side == 'sell':
                        highestSellPrice = float(allOpenOrders[y]['price'])
                        lowestSellPrice = float(allOpenOrders[y]['price'])
                    else:
                        highestBuyPrice = float(allOpenOrders[y]['price'])
                        lowestBuyPrice = float(allOpenOrders[y]['price'])
                else:

                    if side == 'sell':
                        #print("Current Price " + str(price) + " || Highest Sell Price: " + str(highestSellPrice) + " Lowest Sell Price: " + str(lowestSellPrice))
                        if highestSellPrice == 0:
                            highestSellPrice = float(allOpenOrders[y]['price'])
                            lowestSellPrice = float(allOpenOrders[y]['price'])

                        if price > highestSellPrice:
                            highestSellPrice = float(allOpenOrders[y]['price'])

                        if price < lowestSellPrice:
                            lowestSellPrice = float(allOpenOrders[y]['price'])

                    if side == 'buy':
                        if highestBuyPrice == 0:
                            highestBuyPrice = float(allOpenOrders[y]['price'])
                            lowestBuyPrice = float(allOpenOrders[y]['price'])
                        if price > highestBuyPrice:
                            highestBuyPrice = float(allOpenOrders[y]['price'])
                        if price < lowestBuyPrice:
                            lowestBuyPrice = float(allOpenOrders[y]['price'])

                    count += 1

                if side == 'sell':
                    sellCount += 1
                    totalSellCoins += size
                    totalUSDValueSells += calculateUSDValue(price, size)
                else:
                    buyCount += 1
                    totalBuysCoins += size
                    totalUSDValueBuys += calculateUSDValue(price, size)

            if y == len(allOpenOrders) - 1:
                if highestSellPrice == 0:
                    sellCount = 0
                if highestBuyPrice == 0:
                    buyCount = 0
                #print(currentCoin + " Highest Buy Price: " + str(highestBuyPrice) + " Lowest Buy Price: " + str(lowestBuyPrice) + " // Highest Sell PRice: " + str(highestSellPrice) + " Lowest Sell Price: " + str(lowestSellPrice))
                holderArr = [currentCoin, lowestBuyPrice, highestBuyPrice, currentPrice, lowestSellPrice, highestSellPrice, round(totalBuysCoins,4), totalSellCoins, round(totalUSDValueBuys,2), round(totalUSDValueSells,2), round(currentAvailable,2), buyCount, sellCount]
                print(holderArr)
                allDataArr.insert(len(allDataArr), holderArr)

    return allDataArr

# Generate Table data based off of data in NewBotConfig.json & current active open orders
def generateTableData(fileName, orderBreakdownArr):
    thresholdData = readJsonData(fileName)
    baseData = thresholdData['TradingPairs']

    newData = []
    #Check data in newbotconfig arr -> against open orders
    for x in range(len(baseData)):
        for y in range(len(orderBreakdownArr)):
            if baseData[x][0]['Coin'] == orderBreakdownArr[y][0]:
                product = baseData[x][0]['Coin']
                enabled = formatEnabled(baseData[x][0]['Enabled'])
                buyThreshold = baseData[x][0]['BuyThreshold1']
                sellThreshold = baseData[x][0]['SellThreshold1']
                lowestBuy = orderBreakdownArr[y][1]
                highestBuy = orderBreakdownArr[y][2]
                currentPrice = orderBreakdownArr[y][3]
                lowestSell = orderBreakdownArr[y][4]
                highestSell = orderBreakdownArr[y][5]
                totalBuyCoins = orderBreakdownArr[y][6]
                totalSellCoins = orderBreakdownArr[y][7]
                totalBuysUSD = orderBreakdownArr[y][8]
                totalSellsUSD = orderBreakdownArr[y][9]
                currentAvailable = orderBreakdownArr[y][10]
                totalBuyOrders = orderBreakdownArr[y][11]
                totalSellOrders = orderBreakdownArr[y][12]

                currentUSDValue = float(currentPrice) * float(totalSellCoins)
                getUSDChange = float(totalSellsUSD) - currentUSDValue
                #dataArr = [product, buyThreshold, sellThreshold, lowestBuy, highestBuy,currentPrice, lowestSell, highestSell, totalBuyCoins, totalBuysUSD,  totalSellCoins, totalSellsUSD, currentAvailable, totalBuyOrders, totalSellOrders]
                dataArr = [product, enabled, buyThreshold, sellThreshold, lowestBuy, highestBuy,currentPrice, lowestSell, highestSell, round(totalBuyCoins,2), round(totalSellCoins,2), round(totalBuysUSD,2),  round(totalSellsUSD,2), round(getUSDChange,2), currentAvailable, totalBuyOrders, totalSellOrders]

                newData.insert(len(newData), dataArr)
    return newData

def formatEnabled(enabled):
    strx = ""
    if enabled == True:
        strx = "Y"
    else:
        strx = "N"
    return strx

def calculateTotalBuySellUSD(orderBreakDownArr):
    totalUSDSells = 0
    totalUSDBuys = 0
    totalChange = 0

    currentUSDValue = 0
    getUSDChange = 0
    for x in range(len(orderBreakDownArr)):
        totalUSDBuys += float(orderBreakDownArr[x][8])
        totalUSDSells += float(orderBreakDownArr[x][9])
        totalChange += float(orderBreakDownArr[x][10])
    return [round(totalUSDBuys,2), round(totalUSDSells,2)]


# Gather All Necessary Data Before Launching GUI ---
sg.theme("Dark")
botconfigFileName = 'NewBotConfig1.json'
openOrders = auth_client.get_orders()
allOpenOrders = list(openOrders)
sortedProductList = generateAllOpenOrdersSortedProductList(allOpenOrders)
uniqProductList = generateUniqPairs(sortedProductList)
orderBreakdownArr = generateHighsAndLows(uniqProductList, allOpenOrders)

tableData = generateTableData(botconfigFileName, orderBreakdownArr)
totalSumsUSD = calculateTotalBuySellUSD(orderBreakdownArr)

headings = ['Product', 'Enabled', 'Buy Threshold', 'Sell Threshold', "Lowest Buy", "Highest Buy", "Current Price", "Lowest Sell", "Highest Sell", "Coins to Buy", "Coins to Sell", "Buys in USD", "Sells in USD", "USD Change", "Available", "Open Buy Orders", "Open Sell Orders" ]

numRows = len(tableData)

# Create Buttons / Add functions to onClick (key)
btn1 = sg.Button('Update Orders', key='-updateOrders-')
btn2 = sg.Button('Cancel Buy Orders', key='-cancelBuys-')
btn3 = sg.Button('Cancel Sell Orders', key='-cancelSells-')
# ------ Window Layout ------
layout = [[sg.Table(values=tableData, headings=headings, max_col_width=10,
                    auto_size_columns=False,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=25,
                    enable_events=True,
                    key='-TABLE-',
                    row_height=20)],

          [sg.Text('Product'), sg.InputText(key='-Coin-', enable_events=True),sg.Text('Buy Threshold'), sg.InputText(key='-BuyThreshold-', enable_events=True), sg.Text("Sell Threshold"), sg.InputText(key='-SellThreshold-', enable_events=True)],
          [sg.Text('Total USD Value [Buys] - $'), sg.Text(totalSumsUSD[0], key='-totalBuysUSD-'), sg.Text('Total USD Value [Sells] - $'), sg.Text(totalSumsUSD[1], key='-totalSellsUSD-'), sg.Text()],
          [sg.Button('Update Threshold', key='-updateThreshold-'), sg.Button('Active Thresholds', key='-activeThresholds-'), sg.Button('Refresh Product List', key='-refresh-'), sg.Button('Adjust Buy Orders', key='-adjustBuys-'), sg.Button('Adjust Sell Orders', key='-adjustSells-')],

          [sg.Text('TimeStamp: ' + getCurrentDate(), key="-timestamp-")]
          ]

def createTradeWindow():
    event, values = sg.Window('Confirmation', [
        [sg.Text('Are you sure you want to delete current trade history?')],
        [sg.Button("No"), sg.Button("Yes")]]).read(close=True)

    if event == 'No':
        print("No")
    else:
        print("Yes -> Deleting Now")
        #clearTradeLog(tradeLogFilePath, historicalTradeLogFilePath)

# ------ Create Window ------
window = sg.Window('Bot Manager', layout) #no_titlebar=True

from Config_Functions import createThresholdWindow

newBotConfig_FileName = 'NewBotConfig1.json'
# ------ Event Loop ------
while True:
    event, values = window.read()
    print("Event ", event)
    print("Values ", values)
    if event == sg.WIN_CLOSED:
        break
    try:
        if event == '-activeThresholds-':
            data = tableData[selectedRows[0]]
            coin = data[0]
            print(coin)
            location = window.current_location()

            # Launch Threshold Window
            createThresholdWindow(newBotConfig_FileName, coin, uniqProductList, location)
        if event == '-adjustBuys-':
            data = tableData[selectedRows[0]]
            coin = data[0]
            lowestBuy = data[4]
            highestBuy = data[5]
            lowestSell = data[7]
            highestSell = data[8]
            coinstobuy = data[9]
            coinstosell = data[10]
            numBuys = data[15]
            numSells = data[16]
            location = window.current_location()
            print(data)
            print("Updating Orders for Coin: ")
            createTradingWindow2(coin, "Buy", lowestBuy, highestBuy, coinstobuy, numBuys, location)

        if event == '-adjustSells-':
            data = tableData[selectedRows[0]]
            coin = data[0]
            lowestSell = data[7]
            highestSell = data[8]
            coinstosell = data[10]
            numSells = data[16]
            location = window.current_location()
            createTradingWindow2(coin, "Sell", lowestSell, highestSell, coinstosell, numSells, location)

        if event == '-TABLE-':
            # tableValues = values['-TABLE-']
            data_selected = [tableData[row] for row in values[event]]
            selectedRows = values['-TABLE-']

            data = tableData[selectedRows[0]]
            print(data)
            coin = data[0]
            buyThreshold = data[2]
            sellThreshold = data[3]

            window.Element('-Coin-').Update(coin)
            window.Element('-BuyThreshold-').Update(buyThreshold)
            window.Element('-SellThreshold-').Update(sellThreshold)

        if event == '-updateThreshold-':
            coin_X = values['-Coin-']
            buyThreshold_X = values['-BuyThreshold-']
            sellThreshold_X = values['-SellThreshold-']
            allValuesToUpdate = [buyThreshold_X, sellThreshold_X]

            updateThresholdData(botconfigFileName, coin_X, allValuesToUpdate)
            tableData = generateTableData(botconfigFileName, orderBreakdownArr)
            window.Element('-TABLE-').Update(values=tableData)

        if event == '-refresh-':
            openOrders = auth_client.get_orders()
            allOpenOrders = list(openOrders)
            sortedProductList = generateAllOpenOrdersSortedProductList(allOpenOrders)
            uniqProductList = generateUniqPairs(sortedProductList)
            orderBreakdownArr = generateHighsAndLows(uniqProductList, allOpenOrders)

            # updateThresholdData(botconfigFileName, coin_X, allValuesToUpdate)
            tableData = generateTableData(botconfigFileName, orderBreakdownArr)
            totalSumsUSD = calculateTotalBuySellUSD(orderBreakdownArr)
            window.Element('-TABLE-').Update(values=tableData)
            window.Element('-totalBuysUSD-').Update(totalSumsUSD[0])
            window.Element('-totalSellsUSD-').Update(totalSumsUSD[1])
            window.Element('-timestamp-').Update(getCurrentDate())

    except:
        print("Failed --- API --- Retry")

