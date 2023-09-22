import PySimpleGUI as sg
from Variables import *
from GUI_Variables import *
from PlaceOrders import placeMultipleOrders, cancelSpecificOrders, checkBalances, placeMultipleOrdersTEST, getCurrentPrice, placeMultipleOrdersTEST2
from RecentFills import generateAveragePosition
import datetime


def calculatePrices(lower, upper, qty, numOrders):
    avg = float(lower) * float(upper)

def getCurrentDate():
    currentDate = datetime.datetime.now()
    return currentDate.strftime("%m-%d-%Y %I:%M:%S")

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

    print(priceX)



    calcCurrentValueToUSD = (float(priceX[0]) * float(totalCoins)) + float(totalFees)
    calcAvgValuetoUSD = (float(currentAvg) * float(totalCoins)) + float(totalFees)

    print(" Current Value to USD: " + str(calcCurrentValueToUSD))
    print(" Current Avg Value to USD: " + str(calcAvgValuetoUSD))

    totalPL = 0

    if calcCurrentValueToUSD > calcAvgValuetoUSD:
       # totalPL = calcAvgValuetoUSD - calcCurrentValueToUSD
        totalPL = calcCurrentValueToUSD - calcAvgValuetoUSD
        print("Total PL (1) -> " + str(totalPL))
    else:
        totalPL = calcAvgValuetoUSD - calcCurrentValueToUSD
        #totalPL = calcCurrentValueToUSD - calcAvgValuetoUSD
        print("Total PL (2) -> " + str(totalPL))

    returnArr = [priceX[0], round(totalPL)]

    return returnArr






# 1 - Generate All Base Data for the GUI
coinData = generateProductList2()  # [{id,quote_increment,base_min_size}]
coinList = sortedProductList(coinData)  # Returns the Sorted Trading Pairs
typeList = generateTradeType()
tradeSettingType = ['normal', 'bottom', 'middle', 'top']

# Set Theme for GUI
sg.theme(getGUITheme())
windowNumber = "1"
GUI_Title = "Trading - 2x1 - " + windowNumber
GUI_Title_Balance = "Balance Info - 2x1 -" + windowNumber
GUI_Title_Avg = "Average Info - 2x1 -" + windowNumber
GUI_Title_Error = "Error Window - 2x1 - " + windowNumber

line1A = sg.Text('Coin', ), sg.Combo(coinList, size=(13, 13), enable_events=True, key='-Coin1-'), sg.Text("Type"), sg.Combo(typeList, default_value="Buy", key="-TradeType1-"), sg.Text("Trade:"), sg.Combo(tradeSettingType, default_value='normal', key='-TradeSettingType1-')
line1B = sg.Text(size=(7, 1)), sg.Text('Coin'), sg.Combo(coinList, size=(13, 13), key='-Coin2-'), sg.Text("Type"), sg.Combo(typeList, default_value="Sell", key="-TradeType2-"), sg.Text("Trade:"), sg.Combo(tradeSettingType, default_value='normal', key='-TradeSettingType2-' )
line2A = sg.Button('Lower $', key='-lower1-'), sg.InputText(key='-LowerPrice1-', size=(15, 15)), sg.Button('Upper $',key='-upper1-'), sg.InputText(key='-UpperPrice1-', size=(15, 15))
line2B = sg.Text(size=(9, 1)), sg.Button('Lower $', key='-lower2-'), sg.InputText(key='-LowerPrice2-',size=(15, 15)), sg.Button('Upper $',key='-upper2-'), sg.InputText(key='-UpperPrice2-', size=(15, 15))
line3A = sg.Text('Qty'), sg.InputText(key='-QTY1-', size=(15, 15)), sg.Text('# Orders'), sg.InputText(key='-MaxOrders1-', size=(15, 15)), sg.Button("$", key='-$1-'), sg.Text(size=(8, 1), key="-calcPrice1-")
line3B = sg.Text(" "), sg.Text('Qty'), sg.InputText(key='-QTY2-', size=(15, 15)), sg.Text('# Orders'), sg.InputText(key='-MaxOrders2-', size=(15, 15)), sg.Button("$", key='-$2-'), sg.Text(size=(8, 1), key="-calcPrice2-")
line4A = sg.Text(size=(5, 1)), sg.Button('5%', key='-5A-'), sg.Button('10%', key='-10A-'), sg.Button('25%', key='-25A-'), sg.Button('50%', key='-50A-'), sg.Button('75%', key='-75A-'), sg.Button('MAX', key='-MAXA-')
line4B = sg.Text(size=(22, 1)), sg.Button('5%', key='-5B-'), sg.Button('10%', key='-10B-'), sg.Button('25%', key='-25B-'), sg.Button('50%', key='-50B-'), sg.Button('75%', key='-75B-'), sg.Button('MAX', key='-MAXB-')
line7A = sg.Text(size=(2, 1)), sg.Button('  Place Orders  ', key='-placeOrders1-'), sg.Button(' Get Balance ',key='-getBalance1-'), sg.Button(' Get Avg ', key='-getAvg1-')
line7B = sg.Text(size=(20, 1)), sg.Button('  Place Orders  ', key='-placeOrders2-'), sg.Button(' Get Balance ',key='-getBalance2-'), sg.Button(' Get Avg ', key='-getAvg2-')
line8A = sg.Text('Cancel # Orders'), sg.InputText(key='-NumCancelOrders1-', default_text="50", size=(20, 20)), sg.Combo(typeList, default_value="Buy", key="-CancelType1-"), sg.Button('Cancel', key='-cancelOrders1-')
line8B = sg.Text("\t"), sg.Text('Cancel # Orders'), sg.InputText(key='-NumCancelOrders2-', default_text="50", size=(20, 20)), sg.Combo(typeList, default_value="Sell", key="-CancelType2-"), sg.Button('Cancel', key='-cancelOrders2-')


def tradingWindow():
    layout = [[line1A + line1B],
              [line2A + line2B],
              [line3A + line3B],
              [line4A + line4B],
              [line7A + line7B],
              [line8A + line8B]]
    return sg.Window(GUI_Title, layout, location=(800, 600), finalize=True)


# Should put this into GUI
def displayErrorWindow():
    layout = [[sg.Text("Error Triggered - Could be CB API - OR - Your Entry -- !")],
              [sg.Text("Double Check Entry and *Make sure what you attempted didn't actually execute*!")],
              [sg.Button('Exit', size=(15, 1))]]
    return sg.Window(GUI_Title_Error, layout, finalize=True)



def displayBalanceWindow(total, avail, hold, coin):
    displayTotal = "Total: " + str(total) + " " + coin
    displayAvail = "Available: " + str(avail) + " " + coin
    displayHold = "Coins in Orders: " + str(hold) + " " + coin
    layout2 = [[sg.Text(displayTotal)],
               [sg.Text(displayAvail)],
               [sg.Text(displayHold)],
               [sg.Button('Exit', size=(15, 1))]]

    return sg.Window(GUI_Title_Balance, layout2, finalize=True)

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
    return sg.Window(GUI_Title_Avg, layout, finalize=True)



# Convert lazy typing into actual readable / acceptable api formation for combo box Ex: btcusd -> BTC-USD // ex: btc-usd -> BTC-USD // wont work for a few cases but doesnt effect me
def checkCoin(coinList, coin):
    newCoin = coin

    if str(coin).islower():
        print("Lower Case Found!")
        newCoin = str(coin).upper()
        print("Old Coin: ", coin, " New Coin: ", newCoin)

    if str(coin).__contains__("-") == False:
        print("Minus NOT FOUND!")
        splitValue = "USD"
        if str(coin.upper()).__contains__("USDT"):
            splitValue = "USDT"

        splitter = coin.upper().split(splitValue)
        splitter2 = coin.upper().split(splitter[0])

        newCoin = splitter[0] + "-" + splitter2[1]
        print(newCoin)


    return newCoin


tradeWindow, universalWindow = tradingWindow(), None  # start off with 1 window open


# 3 - the read
while True:  # The Event Loop
    window, event, values = sg.read_all_windows()

    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()

        if window == universalWindow:  # if closing win 2, mark as closed
            print("Window has swapped")
            universalWindow = None

        elif window == tradeWindow:  # if closing win 1, exit program
            break


    try:

            # Calculate USD value
            if event == "-$1-":
                lower = values['-LowerPrice1-']
                qty = values['-QTY1-']
                updateTotalPrice = float(lower) * float(qty)
                window.Element('-calcPrice1-').Update(round(updateTotalPrice, 2))

                # Update Base Max Size
                coin = values['-Coin1-']
                baseMaxSize = getBaseMaxSize(coin, coinData)
                # window.Element('-baseMax1-').Update(baseMaxSize, visible=True)

                # Auto Fill Price with Lower
            if event == "-lower1-":
                coin = values['-Coin1-']
                coin = checkCoin(coinList, coin)
                window.Element('-Coin1-').Update(coin)

                currentPrice = getCurrentPrice(coin)
                window.Element('-LowerPrice1-').Update(currentPrice[0])
                window.Element('-UpperPrice1-').Update(currentPrice[0])

                # Auto Fill Price with Upper
            if event == "-upper1-":
                coin = values['-Coin1-']
                coin = checkCoin(coinList, coin) # Fixes lazy typing format to readable format
                window.Element('-Coin1-').Update(coin)

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

                tradeSettingTypez = values['-TradeSettingType1-']

                # Updated to Meet New Implementation
                quoteIncrement = getSpecificQuoteIncrement2(coin, coinData)
                baseMinSize = getSpecificBaseMinSize2(coin, coinData)

                priceList = generatePrices(coin, lowerPrice, upperPrice, quoteIncrement, maxOrders)
                orderSize = generateOrderSizesTest(coin, baseMinSize, maxCoins, maxOrders, tradeSettingTypez)

                #previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize)

                if tradeSettingTypez == "normal":
                    orderSize1 = generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders)

                    #previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize1)
                    print("OrderSize: ", orderSize1, " // " , priceList)
                    placeMultipleOrdersTEST(coin, maxOrders, tradeType, order_type, orderSize1, priceList)
                else:
                    previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize)
                    placeMultipleOrdersTEST2(coin, maxOrders, tradeType, order_type, orderSize, priceList)

                print("-----------Executing Trades----------")


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
                totalPL_updateAvg1 = generatePositionPL(avgCoin1_updateAvg1, totalCoins_updateAvg1,
                                                        totalFees_updateAvg1,
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

            if event == "-$2-":
                lower = values['-LowerPrice2-']
                qty = values['-QTY2-']
                updateTotalPrice = float(lower) * float(qty)
                window.Element('-calcPrice2-').Update(round(updateTotalPrice, 2))

                # Update Base Max Size
                coin = values['-Coin2-']
                baseMaxSize = getBaseMaxSize(coin, coinData)
                # window.Element('-baseMax2-').Update(baseMaxSize, visible=True)

            if event == "-lower2-":
                coin = values['-Coin2-']
                coin = checkCoin(coinList, coin)
                window.Element('-Coin2-').Update(coin)

                currentPrice = getCurrentPrice(coin)
                window.Element('-LowerPrice2-').Update(currentPrice[0])
                window.Element('-UpperPrice2-').Update(currentPrice[0])

                # Auto Fill Price with Upper
            if event == "-upper2-":
                coin = values['-Coin2-']
                coin = checkCoin(coinList, coin) # Fixes lazy typing format to readable format
                window.Element('-Coin2-').Update(coin)

                currentPrice = getCurrentPrice(coin)
                window.Element('-LowerPrice2-').Update(currentPrice[1])
                window.Element('-UpperPrice2-').Update(currentPrice[1])


            if event == '-5B-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                priceUpper = values['-UpperPrice2-']
                window.Element('-QTY2-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .05))

            if event == '-10B-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                priceUpper = values['-UpperPrice2-']
                window.Element('-QTY2-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .10))

            if event == '-25B-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                priceUpper = values['-UpperPrice2-']
                window.Element('-QTY2-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .25))

            if event == '-50B-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                priceUpper = values['-UpperPrice2-']
                window.Element('-QTY2-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .50))

            if event == '-75B-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                priceUpper = values['-UpperPrice2-']
                window.Element('-QTY2-').Update(generatePercentForTrades(coin, tradeType, priceUpper, .75))

            if event == '-MAXB-':
                tradeType = values['-TradeType2-']
                coin = values['-Coin2-']
                balances = checkBalances(coin)
                splitCoin = str(coin).split("-")

                # Buys = Get USD Balance
                if tradeType == 'Buy':
                    available = balances[1]['available']
                    price = values['-UpperPrice2-']
                    maxValue = float(available) / float(price)
                    window.Element('-QTY2-').Update(maxValue)

                # Sells = Get Coin Balance
                if tradeType == 'Sell':
                    available = balances[0]['available']
                    window.Element('-QTY2-').Update(available)

            if event == '-placeOrders2-':
                coin = values['-Coin2-']
                tradeType = values['-TradeType2-']
                order_type = "limit"
                lowerPrice = float(values['-LowerPrice2-'])
                upperPrice = float(values['-UpperPrice2-'])
                maxCoins = float(values['-QTY2-'])
                maxOrders = int(values['-MaxOrders2-'])

                tradeSettingTypez = values['-TradeSettingType2-']
                # Updated to Meet New CB API Implementation
                quoteIncrement = getSpecificQuoteIncrement2(coin, coinData)
                baseMinSize = getSpecificBaseMinSize2(coin, coinData)

                priceList = generatePrices(coin, lowerPrice, upperPrice, quoteIncrement, maxOrders)
                orderSize = generateOrderSizesTest(coin, baseMinSize, maxCoins, maxOrders, tradeSettingTypez)

                #previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize)

                if tradeSettingTypez == "normal":
                    orderSize1 = generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders)

                    # previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize1)
                    print("OrderSize: ", orderSize1, " // ", priceList)
                    placeMultipleOrdersTEST(coin, maxOrders, tradeType, order_type, orderSize1, priceList)
                else:
                    previewList = displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize)
                    placeMultipleOrdersTEST2(coin, maxOrders, tradeType, order_type, orderSize, priceList)
                print("-----------Executing Trades----------")


            if event == '-cancelOrders2-':
                coin = values['-Coin2-']
                cancelType = str(values['-CancelType2-']).lower()
                numCancelOrders = int(values['-NumCancelOrders2-'])
                cancelSpecificOrders(coin, cancelType, numCancelOrders)

            if event == '-getBalance2-':
                coin = values['-Coin2-']
                balances = checkBalances(coin)
                total = balances[0]['balance']
                available = balances[0]['available']
                hold = balances[0]['hold']

                displayTotal = "Total: " + str(total) + " " + coin
                displayAvail = "Available: " + str(available) + " " + coin
                displayHold = "Coins in Orders: " + str(hold) + " " + coin
                layout2 = [[sg.Text(displayTotal, key='-displayTotal2-')],
                           [sg.Text(displayAvail, key='-displayAvail2-')],
                           [sg.Text(displayHold, key='-displayHold2-')],
                           [sg.Button("Update", key='-updateBalance2-'), sg.Button('Exit', size=(15, 1))]]

                balanceTitle = "Balance Tracker -> " + coin
                balanceWindow2 = sg.Window("GUI_Title_Balance", layout2, finalize=True, size=(600, 150))

            if event == '-updateBalance2-':
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

                balanceWindow2.Element('-displayTotal2-').Update(formatTotal)
                balanceWindow2.Element('-displayAvail2-').Update(formatAvail)
                balanceWindow2.Element('-displayHold2-').Update(formatHold)


            if event == '-getAvg2-':
                avgCoin2_updateAvg2 = values['-Coin2-']
                averages_updateAvg2 = generateAveragePosition(avgCoin2_updateAvg2)
                avgPrice_updateAvg2 = averages_updateAvg2[0]["AvgPrice"]
                totalFees_updateAvg2 = averages_updateAvg2[0]["TotalFees"]
                totalCoins_updateAvg2 = averages_updateAvg2[0]["TotalCoins"]

                # Track P/L
                totalPL_updateAvg2 = generatePositionPL(avgCoin2_updateAvg2, totalCoins_updateAvg2,
                                                        totalFees_updateAvg2, avgPrice_updateAvg2)

                displayPrice_updateAvg2 = "Price: " + str(totalPL_updateAvg2[0])
                displayAvg_updateAvg2 = "Avg $ " + str(avgPrice_updateAvg2)
                displayFee_updateAvg2 = "Fees $ " + str(totalFees_updateAvg2)
                displayCoins_updateAvg2 = "Coins " + str(totalCoins_updateAvg2) + " " + avgCoin2_updateAvg2
                displayPL_updateAvg2 = "Total P/L $ " + str(totalPL_updateAvg2[1]) + " || " + getCurrentDate()

                USDtotal_updateAvg2 = round(float(totalPL_updateAvg2[0]) * float(totalCoins_updateAvg2), 2)
                displayTotalPositionUSD_updateAvg2 = "Total USD: $" + str(USDtotal_updateAvg2)

                displayString_updateAvg2 = displayAvg_updateAvg2 + " || " + displayPrice_updateAvg2 + "\n" + displayTotalPositionUSD_updateAvg2 + " || " + displayFee_updateAvg2 + "\n" + displayCoins_updateAvg2 + "\n" + displayPL_updateAvg2

                avgLine2A = sg.Text(displayString_updateAvg2, key='-displayAvgInfo2-',
                                    size=(getAvgPositionTracker_TextSize())), sg.Text("")
                avgLine2B = sg.Text(displayString_updateAvg2, key='-displayAvgOldInfo2-',
                                    size=(getAvgPositionTracker_TextSize())), sg.Text("")
                avgLine2E = sg.Button('Update Avg', key='-updateAvg2-', size=(15, 1)), sg.Text("")
                avgLine2F = sg.Button('Exit', size=(15, 1)), sg.Text("")

                customAvgFrame2A = [[sg.Frame('', [avgLine2A])],
                                    [sg.Frame('', [avgLine2E])]]

                customAvgFrame2B = [[sg.Frame('', [avgLine2B])],
                                    [sg.Frame('', [avgLine2F])]]

                avgTitle2_updateAvg2 = "Average Position Tracker -> " + avgCoin2_updateAvg2

                Frame1_UpdateAvg2 = "Current || " + avgCoin2_updateAvg2
                Frame2_UpdateAvg2 = "Previous || " + avgCoin2_updateAvg2
                frames1_updatedAvg2 = [[sg.Frame(Frame1_UpdateAvg2, layout=customAvgFrame2A)]]
                frames2_updatedAvg2 = [[sg.Frame(Frame2_UpdateAvg2, layout=customAvgFrame2B)]]

                avgLayout2 = [[sg.Column(frames1_updatedAvg2), sg.Column(frames2_updatedAvg2)]]
                avgWindow2 = sg.Window(avgTitle2_updateAvg2, avgLayout2, finalize=True)

            if event == '-updateAvg2-':
                newAverages_updateAvg2 = generateAveragePosition(avgCoin2_updateAvg2)
                newAvg_updateAvg2 = newAverages_updateAvg2[0]["AvgPrice"]
                newFees_updateAvg2 = newAverages_updateAvg2[0]["TotalFees"]
                newCoins_updateAvg2 = newAverages_updateAvg2[0]["TotalCoins"]

                # Track P/L
                newTotalPL_updateAvg2 = generatePositionPL(avgCoin2_updateAvg2, newCoins_updateAvg2, newFees_updateAvg2,
                                                           newAvg_updateAvg2)

                formatPrice_updateAvg2 = "Current Price $ " + newTotalPL_updateAvg2[0]
                formatAvgTotal_updateAvg2 = "Avg $ " + str(newAvg_updateAvg2)
                formatFees_updateAvg2 = "Fees $ " + str(newFees_updateAvg2)
                formatCoins_updateAvg2 = "Coins: " + str(newCoins_updateAvg2) + " " + avgCoin2_updateAvg2
                formatPL_updateAvg2 = "Total P/L $ " + str(newTotalPL_updateAvg2[1]) + " || " + getCurrentDate()
                newUSDtotal_updateAvg2 = round(float(newTotalPL_updateAvg2[0]) * float(newCoins_updateAvg2), 2)
                formatTotalUSDPositionUSD_updateAvg2 = "Size in USD: $" + str(newUSDtotal_updateAvg2)

                formattedFinalString_updateAvg2 = formatAvgTotal_updateAvg2 + " || " + formatPrice_updateAvg2 + "\n" + formatTotalUSDPositionUSD_updateAvg2 + " || " + formatFees_updateAvg2 + "\n" + formatCoins_updateAvg2 + "\n" + formatPL_updateAvg2

                # Get the Original Average Info -> Push to the Previous Average Info Tab
                previousAvgInfo_updateAvg2 = avgWindow2.Element('-displayAvgInfo2-').Get()

                avgWindow2.Element('-displayAvgInfo2-').update(formattedFinalString_updateAvg2)
                avgWindow2.Element('-displayAvgOldInfo2-').Update(previousAvgInfo_updateAvg2)
    except:
        universalWindow = displayErrorWindow()

        print("FAILED -- Dont close the window..... Retry")











# 4 - the close
window.close()

# # finally show the input value in a popup window
# sg.popup('You entered', float(values['-LowerPrice-']) * float(values['-UpperPrice-']))