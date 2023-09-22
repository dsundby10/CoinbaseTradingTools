import PySimpleGUI as sg
from Config_Center import *
from Indicators import *
newBotConfig_FileName = 'NewBotConfig1.json'

def getThresholdData(coin, fileName):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    newArr = []
    for x in range(len(base)):
        if str(base[x][0]['Coin']) == str(coin):
            for y in range(len(base[x])):
                newArr.insert(len(newArr), base[x][y])
                #print( base[x][y])

    return newArr

def removeBotConfigSpecialThresholds(fileName, coinToFind, index):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    if index == 0 or index == 1:
        print("CANT REMOVE!")
    else:
        for x in range(len(base)):

            # print(base[x][0]['Coin'])
            if str(base[x][0]['Coin']) == str(coinToFind):
                print(base[x])
                # print("Yes" + str(len(base[x])))
                newArr = []
                for y in range(len(base[x])):
                    if y == index - 1:
                        print("Removing -> Y: " + str(y) + " // ")
                    else:
                        newArr.insert(len(newArr), base[x][y])
                    if y == len(base[x]) - 1:
                        newData['TradingPairs'].insert(x, newArr)
            else:

                newData['TradingPairs'].insert(x, base[x])

        #print(newData)
        writeJsonData(fileName, newData)

# Add new Custom Thresholds to The Current Coins List
def addNewBotConfigSpecialThresholds(fileName, coinToFind, updatedValues):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    # [{data data data}, {datata}], [{datadatadat}, {data adad}]
    for x in range(len(base)):

        # print(base[x][0]['Coin'])
        if str(base[x][0]['Coin']) == str(coinToFind):

            newArr = []
            for y in range(len(base[x])):
                newArr.insert(len(newArr), base[x][y])

                if y == len(base[x]) - 1:
                    newArr.insert(len(newArr), updatedValues)
                    print("Y: " + str(y) + " // ", newArr)
                    newData['TradingPairs'].insert(x, newArr)
        else:
            newData['TradingPairs'].insert(x, base[x])

    writeJsonData(fileName, newData)

# Update an existing Custom Thresholds to The Current Coins List
def updateBotConfigSpecialThresholds(fileName, coinToFind, index, updatedValues):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    for x in range(len(base)):

        if str(base[x][0]['Coin']) == str(coinToFind):
            newArr = []
            for y in range(len(base[x])):

                if y == 0 and index == 0 or y == 0 and index == 1:
                    if updatedValues[0] == "Buy":
                        print("updatedvalues[0] == buy")
                        obj = {"Coin": base[x][y]['Coin'],
                               "Enabled": base[x][y]['Enabled'],
                               "BuyThreshold1": updatedValues[1],
                               "SellThreshold1": base[x][y]['SellThreshold1']}
                        #print(obj)
                        newArr.insert(len(newArr), obj)
                    else:
                        obj = {"Coin": base[x][y]['Coin'],
                           "Enabled": base[x][y]['Enabled'],
                           "BuyThreshold1": base[x][y]['BuyThreshold1'],
                           "SellThreshold1": updatedValues[1]}
                        #print(obj)
                        newArr.insert(len(newArr), obj)

                elif y == index - 1:
                    newArr.insert(len(newArr), updatedValues)
                else:
                    newArr.insert(len(newArr), base[x][y])
                # End
                if y == len(base[x]) - 1:
                    newData['TradingPairs'].insert(x, newArr)

        else:
            newData['TradingPairs'].insert(x, base[x])
    print(newData)
    writeJsonData(fileName, newData)


def updateEnableThresholdValue(fileName, coinToFind, updatedValue):
    configData = readJsonData(fileName)
    newData = {'TradingPairs': []}
    base = configData['TradingPairs']

    # [{data data data}, {datata}], [{datadatadat}, {data adad}]
    for x in range(len(base)):

        if str(base[x][0]['Coin']) == str(coinToFind):

            newArr = []
            for y in range(len(base[x])):

                if y == 0:
                    obj = {'Coin': base[x][y]['Coin'], 'Enabled': updatedValue, 'BuyThreshold1': base[x][y]['BuyThreshold1'], 'SellThreshold1': base[x][y]['SellThreshold1']}
                    newArr.insert(len(newArr), obj)

                else:
                    newArr.insert(len(newArr), base[x][y])

                # End
                if y == len(base[x]) - 1:
                    newData['TradingPairs'].insert(x, newArr)

        else:
            newData['TradingPairs'].insert(x, base[x])
    print(newData)
    writeJsonData(fileName, newData)


#Format values to match the strcutre in json file
def formatValues(valueArr):

    valueObj = []
    if valueArr[0] == 'Buy':

        valueObj = {'BuyThreshold1': valueArr[1],
                    'Price1': valueArr[2],
                    'Price2': valueArr[3]
        }
    else:
        valueObj = {'SellThreshold1': valueArr[1],
                    'Price1': valueArr[2],
                    'Price2': valueArr[3]
                    }
    return valueObj



# Get the data ready to be displayed for the Table
def formatThresholdDataForTable(thresholdData):

    arr = []

    finalArr = []
    for x in range(len(thresholdData)):
        if x == 0:
            arr = ['Buy', thresholdData[x]['BuyThreshold1'], 'N/A', 'N/A']
            arr2 = ['Sell', thresholdData[x]['SellThreshold1'], 'N/A', 'N/A']
            finalArr.insert(len(finalArr), arr)
            finalArr.insert(len(finalArr), arr2)
        else:
            try:
                arr = ['Buy', thresholdData[x]['BuyThreshold1'], thresholdData[x]['Price1'],thresholdData[x]['Price2']]
                finalArr.insert(len(finalArr), arr)
            except:
                arr = ['Sell', thresholdData[x]['SellThreshold1'], thresholdData[x]['Price1'],thresholdData[x]['Price2']]
                finalArr.insert(len(finalArr), arr)

    return finalArr

# Check if custom thresholds are enabled /disbaled
def getEnabledValue(thresholdData):
    isEnabled = False
    for x in range(len(thresholdData)):
        if x == 0:
            return thresholdData[x]['Enabled']

#============================Trading GUI Functions=============== #
import datetime
from Variables import *
from GUI_Variables import *
from PlaceOrders import placeMultipleOrders, cancelSpecificOrders, checkBalances, placeMultipleOrdersTEST, getCurrentPrice
from RecentFills import generateAveragePosition

def calculatePrices(lower, upper, qty, numOrders):
    avg = float(lower) * float(upper)


def generatePercentForTrades(coin, tradeType, price, percent):
    balances = checkBalances(coin)
    print(balances[0])
    print(balances[1])

    splitCoin = str(coin).split("-")

    returnValue = 0
    # Buys = Get USD Balance
    if tradeType == 'Buy':
        available = balances[1]['available']
        maxValue = (percent * float(available)) / float(price)
        returnValue = maxValue

    # Sells = Get Coin Balance
    if tradeType == 'Sell':
        available = balances[0]['available']
        newAmt = float(available) * percent
        returnValue = newAmt

    return returnValue

def generatePositionPL(coin, totalCoins, totalFees, currentAvg):
    priceX = getCurrentPrice(coin) # returns array [bid,ask]

    calcCurrentValueToUSD = (float(priceX[0]) * float(totalCoins)) + float(totalFees)
    calcAvgValuetoUSD = (float(currentAvg) * float(totalCoins)) + float(totalFees)

    print(" Current Value to USD: " + str(calcCurrentValueToUSD))
    print(" Current Avg Value to USD: " + str(calcAvgValuetoUSD))

    totalPL = 0

    if calcCurrentValueToUSD > calcAvgValuetoUSD:
        totalPL = calcCurrentValueToUSD - calcAvgValuetoUSD
        print("Total PL (1) -> " + str(totalPL))
    else:
        totalPL = calcCurrentValueToUSD - calcAvgValuetoUSD
        print("Total PL (2) -> " + str(totalPL))

    returnArr = [priceX[0], round(totalPL)]

    return returnArr

def getCurrentDate():
    currentDate = datetime.datetime.now()
    return currentDate.strftime("%m-%d-%Y %I:%M:%S")

# Pre Functions -------

# 1 - Generate All Base Data for the GUI
coinData = generateProductList2()  # [{id,quote_increment,base_min_size}]
coinList = sortedProductList(coinData)  # Returns the Sorted Trading Pairs
typeList = generateTradeType()


#-------------------------------------------------------------------End Trading Window Fucntions --------------------

def createThresholdWindow(fileName, currentCoin, activeCoinList, location):
    print("entered")
    thresholdData = getThresholdData(currentCoin, fileName)
    tableData = formatThresholdDataForTable(thresholdData)
    comboListData = ['Buy', 'Sell']
    headings = ['Type', 'Threshold', 'Price1', 'Price2']
    analysisHeadings = ['TFrame', 'Open', 'VolumeUSD', '% Change', 'MA5', 'MA10', 'MA20', 'MA30', 'MA50', 'MA100', 'MA200']

    updateIndividualIndicator(currentCoin)
    analysisData = readTechnicalAnalysisValues('indicators.json', currentCoin)

    # Main Table
    col1 = [
        [sg.Table(values=tableData, headings=headings, max_col_width=20,
                  display_row_numbers=True,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=30,
                  enable_events=True,
                  key='-TABLE-')]
    ]

    col2_header = [[sg.Text(currentCoin, key='-title-', justification='c')]]

    col2_row1 = [
        [ sg.Table(values=analysisData, headings=analysisHeadings, max_col_width=10,
                  #display_row_numbers=True,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=6,
                  enable_events=True,
                  key='-TABLE1-')]
    ]

    col2_row2 = [
        [sg.Checkbox('Enabled', default=getEnabledValue(thresholdData), key='-enableCheckbox-', enable_events=True)],
        [sg.Combo(activeCoinList, key="-comboList-", size=(15, 10), enable_events=True, default_value=currentCoin), sg.Button("Refresh MAs", key='-refreshMA-')]
    ]

    sizeX = 7
    col2_row3 = [
        [sg.Text('Threshold %'), sg.InputText(key='-Threshold-', enable_events=True, size=(sizeX, 1)),
         sg.Text("Lower Price"),
         sg.InputText(key='-lowerPrice-', enable_events=True, size=(sizeX, 1)), sg.Text("Upper Price"),
         sg.InputText(key='-upperPrice-', enable_events=True, size=(sizeX, 1)),
         sg.Button('Update Threshold', key='-updateThreshold-'),
         sg.Button('Remove Threshold', key='-removeThreshold-')],

        [sg.Text('Add New Threshold'), sg.Combo(comboListData, key='-thresholdType-', default_value='Buy'),
         sg.Text('Threshold %'), sg.InputText(key='-Threshold2-', enable_events=True, size=(sizeX, 1)),
         sg.Text("Lower Price"),
         sg.InputText(key='-lowerPrice2-', enable_events=True, size=(sizeX, 1)), sg.Text("Upper Price"),
         sg.InputText(key='-upperPrice2-', enable_events=True, size=(sizeX, 1)),
         sg.Button('Add Threshold', key='-addThreshold-')],
    ]

    # Trading GUI Window
    col2_row4A = [[sg.Text("", size=(10,1))]]
    col2_row4 = [

        [sg.Text('Coin', ), sg.Combo(coinList, size=(13, 13), key='-Coin1-', default_value=currentCoin), sg.Text("Type"),
         sg.Combo(typeList, key="-TradeType1-", default_value="Buy"), sg.Text("Max:"),
         sg.Text(size=(8, 1), key="-baseMax1-")],
        [sg.Button('Lower $', key='-lower1-'), sg.InputText(key='-LowerPrice1-', size=(15, 15), default_text=0),
         sg.Button('Upper $', key='-upper1-'), sg.InputText(key='-UpperPrice1-', size=(15, 15), default_text=0)],
        [sg.Text('Qty'), sg.InputText(key='-QTY1-', size=(15, 15), default_text=0), sg.Text('# Orders'),
         sg.InputText(key='-MaxOrders1-', size=(15, 15), default_text=0), sg.Button("$", key='-$1-'),
         sg.Text(size=(8, 1), key="-calcPrice1-")],
        [sg.Text(size=(5, 1)), sg.Button('5%', key='-5A-'), sg.Button('10%', key='-10A-'),
         sg.Button('25%', key='-25A-'), sg.Button('50%', key='-50A-'), sg.Button('75%', key='-75A-'),
         sg.Button('MAX', key='-MAXA-')],
        [sg.Text(size=(2, 1)), sg.Button('  Place Orders  ', key='-placeOrders1-'),
         sg.Button(' Get Balance ', key='-getBalance1-'), sg.Button(' Get Avg ', key='-getAvg1-')],
        [sg.Text('Cancel # Orders'), sg.InputText(key='-NumCancelOrders1-', size=(20, 20), default_text=0),
         sg.Combo(typeList, key="-CancelType1-", default_value="Buy"), sg.Button('Cancel', key='-cancelOrders1-')]

    ]



    col2 = [
        [sg.Frame(layout=[[sg.Column(col2_row2, vertical_alignment='c'), sg.Column(col2_row3, vertical_alignment='c')]],vertical_alignment='c', title='')],
        [sg.HorizontalSeparator()],
        [sg.Frame(layout=[[sg.Column(col2_row1, vertical_alignment='c')]], vertical_alignment='c', title='')],
        [sg.HorizontalSeparator()],
        [sg.Frame(layout=[[sg.Column(col2_row4A, vertical_alignment='c'), sg.Column(col2_row4, vertical_alignment='c')]],vertical_alignment='c', title='')]]


    layout = [[sg.Column(col1), sg.Column(col2)]]

    window = sg.Window('******Custom Threshold Data******', layout, location=location)

    # 3 - the read
    while True:  # The Event Loop
        event, values = window.read()
        #print("Event ", event) # Help with debugging issues
        #print("Values ", values) # Help with debugging issues

        if event in (None, 'EXIT'):  # quit if exit button or X
            break

        if event == '-refreshMA-':
            coinname = values['-comboList-']
            # Update TA values
            updateIndividualIndicator(coinname)
            analysisData = readTechnicalAnalysisValues('indicators.json', coinname)
            window['-TABLE1-'].update(values=analysisData)

        if event == '-comboList-':
            coinname = values['-comboList-']
            thresholdData = getThresholdData(coinname, newBotConfig_FileName)
            tableData = formatThresholdDataForTable(thresholdData)

            # Update CheckBox Data
            enabled = thresholdData[0]['Enabled']
            window.Element('-enableCheckbox-').Update(enabled)

            # Update TA values
            updateIndividualIndicator(coinname)
            analysisData = readTechnicalAnalysisValues('indicators.json', coinname)
            window['-TABLE1-'].update(values=analysisData)

            # Update Title
            sg.Element('-title-').update(coinname)
            # Update Threshold Table
            window['-TABLE-'].update(values=tableData)

        if event == '-enableCheckbox-':
            coinname = values['-comboList-']
            checkboxValue = values['-enableCheckbox-']
            updateEnableThresholdValue(newBotConfig_FileName, coinname, checkboxValue)
            print(str(checkboxValue))

        if event == '-TABLE-':
            coinname = values['-comboList-']
            data_selected = [tableData[row] for row in values[event]]
            print(data_selected)
            selectedRows = values['-TABLE-']
            print(selectedRows)  # prints the row number

            data = tableData[selectedRows[0]]
            print(data)

            window.Element('-Threshold-').Update(data[1])
            window.Element('-lowerPrice-').Update(data[2])
            window.Element('-upperPrice-').Update(data[3])

        if event == '-updateThreshold-':
            coinname = values['-comboList-']
            threshold = values['-Threshold-']
            lowerPrice = values['-lowerPrice-']
            upperPrice = values['-upperPrice-']
            print("SelectedRow: ", selectedRows[0])

            if selectedRows[0] == 0 or selectedRows[0] == 1:
                valArr = [data[0], threshold]
                #print("val arr->", valArr)
                updateBotConfigSpecialThresholds(newBotConfig_FileName, coinname, selectedRows[0], valArr)
            else:
                valArr = [data[0], threshold, lowerPrice, upperPrice]
                formatValArr = formatValues(valArr)
                updateBotConfigSpecialThresholds(newBotConfig_FileName, coinname, selectedRows[0], formatValArr)

            thresholdData = getThresholdData(coinname, newBotConfig_FileName)
            tableData = formatThresholdDataForTable(thresholdData)
            window.Element('-TABLE-').Update(values=tableData)

        if event == '-removeThreshold-':
            coinname = values['-comboList-']
            removeBotConfigSpecialThresholds(newBotConfig_FileName, coinname, selectedRows[0])
            thresholdData = getThresholdData(coinname, newBotConfig_FileName)
            tableData = formatThresholdDataForTable(thresholdData)
            window.Element('-TABLE-').Update(values=tableData)

        if event == '-addThreshold-':  # this is really to update
            coinname = values['-comboList-']
            thresholdType = values['-thresholdType-']
            threshold2 = values['-Threshold2-']
            lowerPrice2 = values['-lowerPrice2-']
            upperPrice2 = values['-upperPrice2-']

            valArr2 = [thresholdType, threshold2, lowerPrice2, upperPrice2]
            updateValues2 = formatValues(valArr2)

            addNewBotConfigSpecialThresholds(newBotConfig_FileName, coinname, updateValues2)
            thresholdData = getThresholdData(coinname, newBotConfig_FileName)
            tableData = formatThresholdDataForTable(thresholdData)
            window.Element('-TABLE-').Update(values=tableData)

            # Trading GUI Window Events
        if event == "-$1-":
            lower = values['-LowerPrice1-']
            qty = values['-QTY1-']
            updateTotalPrice = float(lower) * float(qty)
            window.Element('-calcPrice1-').Update(round(updateTotalPrice, 2))

            # Update Base Max Size
            coin = values['-Coin1-']
            baseMaxSize = getBaseMaxSize(coin, coinData)
            window.Element('-baseMax1-').Update(baseMaxSize, visible=True)

            # Auto Fill Price with Lower
        if event == "-lower1-":
            coin = values['-Coin1-']
            currentPrice = getCurrentPrice(coin)
            window.Element('-LowerPrice1-').Update(currentPrice[0])
            window.Element('-UpperPrice1-').Update(currentPrice[0])

            # Auto Fill Price with Upper
        if event == "-upper1-":
            coin = values['-Coin1-']
            currentPrice = getCurrentPrice(coin)
            window.Element('-LowerPrice1-').Update(currentPrice[1])
            window.Element('-UpperPrice1-').Update(currentPrice[1])

        if event == '-5A-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            priceUpper = values['-UpperPrice1-']
            window.Element('-QTY1-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .05))

        if event == '-10A-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            priceUpper = values['-UpperPrice1-']
            window.Element('-QTY1-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .10))

        if event == '-25A-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            priceUpper = values['-UpperPrice1-']
            window.Element('-QTY1-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .25))

        if event == '-50A-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            priceUpper = values['-UpperPrice1-']
            window.Element('-QTY1-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .50))

        if event == '-75A-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            priceUpper = values['-UpperPrice1-']
            window.Element('-QTY1-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .75))

        if event == '-MAXA-':
            tradeType = values['-TradeType1-']
            coin = values['-Coin1-']
            balances = checkBalances(coin)
            splitCoin = str(coin).split("-")

            # Buys = Get USD Balance
            if tradeType == 'Buy':
                available = balances[1]['available']
                price = values['-UpperPrice1-']
                maxValue = float(available) / float(price)
                window.Element('-QTY1-').Update(maxValue)

            # Sells = Get Coin Balance
            if tradeType == 'Sell':
                available = balances[0]['available']
                window.Element('-QTY1-').Update(available)

        if event == '-placeOrders1-':
            coin = values['-Coin1-']
            tradeType = values['-TradeType1-']
            order_type = "limit"
            lowerPrice = float(values['-LowerPrice1-'])
            upperPrice = float(values['-UpperPrice1-'])
            maxCoins = float(values['-QTY1-'])
            maxOrders = int(values['-MaxOrders1-'])

            # Updated to Meet New Implementation
            quoteIncrement = getSpecificQuoteIncrement2(coin, coinData)
            baseMinSize = getSpecificBaseMinSize2(coin, coinData)

            priceList = generatePrices(coin, lowerPrice, upperPrice, quoteIncrement, maxOrders)
            orderSize = generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders)

            previewList = displayOrderDataBeforePlacingGUI(coin, tradeType, priceList, orderSize)
            print("-----------Executing Trades----------")
            placeMultipleOrdersTEST(coin, maxOrders, tradeType, order_type, orderSize, priceList)

        if event == '-cancelOrders1-':
            coin = values['-Coin1-']
            cancelType = str(values['-CancelType1-']).lower()
            numCancelOrders = int(values['-NumCancelOrders1-'])
            cancelSpecificOrders(coin, cancelType, numCancelOrders)

        if event == '-getBalance1-':
            coin = values['-Coin1-']
            balances = checkBalances(coin)
            total = balances[0]['balance']
            available = balances[0]['available']
            hold = balances[0]['hold']

            displayTotal = "Total: " + str(total) + " " + coin
            displayAvail = "Available: " + str(available) + " " + coin
            displayHold = "Coins in Orders: " + str(hold) + " " + coin
            layout1 = [[sg.Text(displayTotal, key='-displayTotal1-')],
                       [sg.Text(displayAvail, key='-displayAvail1-')],
                       [sg.Text(displayHold, key='-displayHold1-')],
                       [sg.Button("Update", key='-updateBalance1-'), sg.Button('Exit', size=(15, 1))]]

            balanceTitle = "Balance Tracker -> " + coin
            balanceWindow2 = sg.Window(balanceTitle, layout1, finalize=True, size=(600, 150))

        if event == '-updateBalance1-':
            balances = checkBalances(coin)
            newTotal = balances[0]['balance']
            newAvail = balances[0]['available']
            newHold = balances[0]['hold']
            print(newTotal, newAvail, newHold)

            oldTotal = total
            oldAvail = available
            oldHold = hold
            oldCoin = coin
            formatTotal = "New Total: " + str(newTotal) + " || " + " Old Total: " + str(oldTotal)
            formatAvail = "New Avail: " + str(newAvail) + " || " + " Old Avail:" + str(oldAvail)
            formatHold = "New Hold: " + str(newHold) + " || " + " Old Hold: " + str(oldHold)

            balanceWindow2.Element('-displayTotal1-').Update(formatTotal)
            balanceWindow2.Element('-displayAvail1-').Update(formatAvail)
            balanceWindow2.Element('-displayHold1-').Update(formatHold)

        if event == '-getAvg1-':
            avgCoin1_updateAvg1 = values['-Coin1-']
            averages_updateAvg1 = generateAveragePosition(avgCoin1_updateAvg1)
            avgPrice_updateAvg1 = averages_updateAvg1[0]["AvgPrice"]
            totalFees_updateAvg1 = averages_updateAvg1[0]["TotalFees"]
            totalCoins_updateAvg1 = averages_updateAvg1[0]["TotalCoins"]

            # Track P/L
            totalPL_updateAvg1 = generatePositionPL(avgCoin1_updateAvg1, totalCoins_updateAvg1, totalFees_updateAvg1,
                                                    avgPrice_updateAvg1)

            displayPrice_updateAvg1 = "Price: " + str(totalPL_updateAvg1[0])
            displayAvg_updateAvg1 = "Avg $ " + str(avgPrice_updateAvg1)
            displayFee_updateAvg1 = "Fees $ " + str(totalFees_updateAvg1)
            displayCoins_updateAvg1 = "Coins " + str(totalCoins_updateAvg1) + " " + avgCoin1_updateAvg1
            displayPL_updateAvg1 = "Total P/L $ " + str(totalPL_updateAvg1[1]) + " || " + getCurrentDate()

            USDtotal_updateAvg1 = round(float(totalPL_updateAvg1[0]) * float(totalCoins_updateAvg1), 2)
            displayTotalPositionUSD_updateAvg1 = "Total USD: $" + str(USDtotal_updateAvg1)

            displayString_updateAvg1 = displayAvg_updateAvg1 + " || " + displayPrice_updateAvg1 + "\n" + displayTotalPositionUSD_updateAvg1 + " || " + displayFee_updateAvg1 + "\n" + displayCoins_updateAvg1 + "\n" + displayPL_updateAvg1

            avgLine1A = sg.Text(displayString_updateAvg1, key='-displayAvgInfo1-',
                                size=(getAvgPositionTracker_TextSize())), sg.Text("")
            avgLine1B = sg.Text(displayString_updateAvg1, key='-displayAvgOldInfo1-',
                                size=(getAvgPositionTracker_TextSize())), sg.Text("")
            avgLine1E = sg.Button('Update Avg', key='-updateAvg1-', size=(15, 1)), sg.Text("")
            avgLine1F = sg.Button('Exit', size=(15, 1)), sg.Text("")

            customAvgFrame1A = [[sg.Frame('', [avgLine1A])],
                                [sg.Frame('', [avgLine1E])]]

            customAvgFrame1B = [[sg.Frame('', [avgLine1B])],
                                [sg.Frame('', [avgLine1F])]]

            avgTitle_updateAvg1 = "Average Position Tracker -> " + avgCoin1_updateAvg1

            Frame1_UpdateAvg1 = "Current || " + avgCoin1_updateAvg1
            Frame2_UpdateAvg1 = "Previous || " + avgCoin1_updateAvg1
            frames1_updatedAvg1 = [[sg.Frame(Frame1_UpdateAvg1, layout=customAvgFrame1A)]]
            frames2_updatedAvg1 = [[sg.Frame(Frame2_UpdateAvg1, layout=customAvgFrame1B)]]

            avgLayout1 = [[sg.Column(frames1_updatedAvg1), sg.Column(frames2_updatedAvg1)]]
            avgWindow1 = sg.Window(avgTitle_updateAvg1, avgLayout1, finalize=True)

        if event == '-updateAvg1-':
            newAverages_updateAvg1 = generateAveragePosition(avgCoin1_updateAvg1)
            newAvg_updateAvg1 = newAverages_updateAvg1[0]["AvgPrice"]
            newFees_updateAvg1 = newAverages_updateAvg1[0]["TotalFees"]
            newCoins_updateAvg1 = newAverages_updateAvg1[0]["TotalCoins"]

            # Track P/L
            newTotalPL_updateAvg1 = generatePositionPL(avgCoin1_updateAvg1, newCoins_updateAvg1, newFees_updateAvg1,
                                                       newAvg_updateAvg1)

            formatPrice_updateAvg1 = "Current Price $ " + newTotalPL_updateAvg1[0]
            formatAvgTotal_updateAvg1 = "Avg $ " + str(newAvg_updateAvg1)
            formatFees_updateAvg1 = "Fees $ " + str(newFees_updateAvg1)
            formatCoins_updateAvg1 = "Coins: " + str(newCoins_updateAvg1) + " " + avgCoin1_updateAvg1
            formatPL_updateAvg1 = "Total P/L $ " + str(newTotalPL_updateAvg1[1]) + " || " + getCurrentDate()
            newUSDtotal_updateAvg1 = round(float(newTotalPL_updateAvg1[0]) * float(newCoins_updateAvg1), 2)
            formatTotalUSDPositionUSD_updateAvg1 = "Size in USD: $" + str(newUSDtotal_updateAvg1)

            formattedFinalString_updateAvg1 = formatAvgTotal_updateAvg1 + " || " + formatPrice_updateAvg1 + "\n" + formatTotalUSDPositionUSD_updateAvg1 + " || " + formatFees_updateAvg1 + "\n" + formatCoins_updateAvg1 + "\n" + formatPL_updateAvg1

            # Get the Original Average Info -> Push to the Previous Average Info Tab
            previousAvgInfo_updateAvg1 = avgWindow1.Element('-displayAvgInfo1-').Get()

            avgWindow1.Element('-displayAvgInfo1-').update(formattedFinalString_updateAvg1)
            avgWindow1.Element('-displayAvgOldInfo1-').Update(previousAvgInfo_updateAvg1)


# Error Window Triggers a lot of the time because of Coinbase API being limited when running multiple checks in background --- but will trigger if you fail to provide correct data in the GUIS
def displayErrorWindow():
    layout = [[sg.Text("Error Triggered - Might be you - or API - Double Check What Your Attempting to do Then Try Again.")],
              [sg.Text("Try again (Make sure what you attempted didn't actually execute)...")],
              [sg.Button('Exit', size=(15, 1))]]
    return sg.Window("Error", layout, finalize=True)



def displayBalanceWindow(total, avail, hold, coin):
    displayTotal = "Total: " + str(total) + " " + coin
    displayAvail = "Available: " + str(avail) + " " + coin
    displayHold = "Coins in Orders: " + str(hold) + " " + coin
    layout2 = [[sg.Text(displayTotal)],
               [sg.Text(displayAvail)],
               [sg.Text(displayHold)],
               [sg.Button('Exit', size=(15, 1))]]

    return sg.Window("Balance", layout2, finalize=True)


def displayAveragesWindow(coin):
    print("Getting Average Now .... ")
    averages = generateAveragePosition(coin)
    avgPrice = averages[0]["AvgPrice"]
    totalFees = averages[0]["TotalFees"]
    totalCoins = averages[0]["TotalCoins"]

    displayAvg = "Average Price $" + str(avgPrice)
    displayFee = "Total Fees $" + str(totalFees)
    displayCoins = "Total Coins Calculated: " + str(totalCoins) + " " + coin
    layout = [[sg.Text(displayAvg)],
              [sg.Text(displayFee)],
              [sg.Text(displayCoins)],
              [sg.Button('Exit', size=(15, 1))]]
    return sg.Window("Average", layout, finalize=True)

