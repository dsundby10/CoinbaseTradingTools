from tradingview_ta import TA_Handler, Interval, Exchange
import cbpro
import json
import time
from Config_Center import *

# Generate Coinbase Product List
def generateProductList():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""
    for x in range(0, len(products)):
        id = str(products[x]['id'])
        statusMessage = products[x]['status_message'] # Testing

        splitID = str(id).split("-")

        if splitID[1] == "USD": # Only Want USD trading pairs (Not USDT/BTC/ETH/USDC Pairs)
            productList += id + ","

    productList = str(productList).split(",")

    return productList

# Use the Coinbase default symbols -> This will convert to this APIs expected symbol
def convertSymbol(symbol):
    splitSymbol = str(symbol).split("-")

    return splitSymbol[0] + splitSymbol[1]

# Use the Coinbase default interval -> This will convert to this APIs expected intervals
def convertInterval(interval):
    if interval == 60:
        convertedInterval = Interval.INTERVAL_1_MINUTE
    if interval == 300:
        convertedInterval = Interval.INTERVAL_5_MINUTES
    if interval == 900:
        convertedInterval = Interval.INTERVAL_15_MINUTES
    if interval == 3600:
        convertedInterval = Interval.INTERVAL_1_HOUR
    if interval == 14400:
        convertedInterval = Interval.INTERVAL_4_HOURS
    if interval == 86400:
        convertedInterval = Interval.INTERVAL_1_DAY

    return convertedInterval

def generateTA_Handler(symbol, screener, exchange, interval):
    adjustInterval = convertInterval(interval)
    dataArr = TA_Handler(
        symbol=convertSymbol(symbol),
        screener="crypto",
        exchange="COINBASE",
        interval=adjustInterval
    )

    return dataArr


def getTA(symbol, screener, exchange, interval):
    adjustInterval = convertInterval(interval)
    dataTA = TA_Handler(
        symbol=convertSymbol(symbol),
        screener="crypto",
        exchange="COINBASE",
        interval=adjustInterval
    )
    #dataTA = generateTA_Handler(symbol, screener, exchange, interval)
    #print("Current Interval: " + str(interval) + " /// Adjusted Interval: " + str(adjustInterval) + " // Converted Interval: " + str(convertTimeFrame(interval)))
    try:
        # Get Analysis
        analysis = dataTA.get_analysis()

        indicators = analysis.indicators
        print(symbol, indicators)
        indicatorObj = indicatorValues(symbol, adjustInterval, indicators)

    except:
        print("None")
        indicatorObj = indicatorValuesFailed(symbol, adjustInterval, "Failed")

    return indicatorObj

# Gather A lot of Data from the Trading-view-api - Not going to use it all - but good to have later down the road
def indicatorValues(symbol, interval, indicators):

    volumeToUsd = float(indicators['volume']) * float(indicators['close'])
    # Create an Object of Selected Indicators to Use

    arr = [symbol, interval, indicators['close'], indicators['open'], indicators['volume'],volumeToUsd, indicators['change'],
           indicators['SMA5'], indicators['SMA10'], indicators['SMA20'], indicators['SMA30'], indicators['SMA50'], indicators['SMA100'], indicators['SMA200'],
           indicators['EMA5'], indicators['EMA10'], indicators['EMA20'], indicators['EMA30'], indicators['EMA50'], indicators['EMA100'], indicators['EMA200'],
           indicators['MACD.macd'], indicators["MACD.signal"], indicators['BB.lower'], indicators['BB.upper'],
           indicators['Pivot.M.Fibonacci.S1'], indicators['Pivot.M.Fibonacci.S2'], indicators['Pivot.M.Fibonacci.S3'],
           indicators['Pivot.M.Fibonacci.Middle'], indicators['Pivot.M.Fibonacci.R1'],
           indicators['Pivot.M.Fibonacci.R2'], indicators['Pivot.M.Fibonacci.R3'],
           indicators['VWMA'], indicators['RSI']
           ]
    print(arr)
    indicatorsObj = {
        "coin": symbol,     #0
        "timeFrame": interval,
        "price": indicators['close'],
        "open": indicators['open'],
        "volume": indicators['volume'],
        "volumeToUSD": volumeToUsd,     #5
        "change": indicators['change'], #6

        "SMA5": indicators['SMA5'], #7
        "SMA10": indicators['SMA10'],
        "SMA20": indicators['SMA20'],
        "SMA30": indicators['SMA30'],
        "SMA50": indicators['SMA50'],
        "SMA100": indicators['SMA100'],
        "SMA200": indicators['SMA200'], #13


        "EMA5": indicators['EMA5'], #14
        "EMA10": indicators['EMA10'],
        "EMA20": indicators['EMA20'],
        "EMA30": indicators['EMA30'],
        "EMA50": indicators['EMA50'],
        "EMA100": indicators['EMA100'],
        "EMA200": indicators['EMA200'], #20

        "MACD.macd": indicators['MACD.macd'],
        "MACD.signal": indicators["MACD.signal"], #22

        "BB.lower": indicators['BB.lower'],
        "BB.upper": indicators['BB.upper'], # 24

        "FIB_S1": indicators['Pivot.M.Fibonacci.S1'],
        "FIB_S2": indicators['Pivot.M.Fibonacci.S2'],
        "FIB_S3": indicators['Pivot.M.Fibonacci.S3'],
        "FIB_M": indicators['Pivot.M.Fibonacci.Middle'],
        "FIB_R1": indicators['Pivot.M.Fibonacci.R1'],
        "FIB_R2": indicators['Pivot.M.Fibonacci.R2'],
        "FIB_R3": indicators['Pivot.M.Fibonacci.R3'],

        "VWMA": indicators['VWMA'],
        "RSI": indicators['RSI']
    }

   # print(indicatorsObj)
    return arr

# Set a Default Value for Coins that "fail" - would fail if they were just recenently
# addded to the exchange and they havent been active long enough to meet that specific time frame threshold
def indicatorValuesFailed(symbol, interval, indicators):
    # Create an Object of Selected Indicators to Use

    arr = [symbol, interval, 0,0,0,0,0,
           0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,
           0,0,0,0,
           0,0,0,0,0,0,0,0,0]
    indicatorsObj = {
        "coin": symbol,
        "timeFrame": interval,
        "price": 0,
        "open": 0,
        "volume": 0,
        "volumeToUSD": 0,  # 5
        "change": 0,

        "SMA5": 0,
        "SMA10": 0,
        "SMA20": 0,
        "SMA30": 0,
        "SMA50": 0,
        "SMA100": 0,
        "SMA200": 0,

        "EMA5": 0,
        "EMA10": 0,
        "EMA20": 0,
        "EMA30": 0,
        "EMA50": 0,
        "EMA100": 0,
        "EMA200": 0,


        "MACD.macd": 0,
        "MACD.signal": 0,

        "BB.lower": 0,
        "BB.upper": 0,

        "FIB_S1": 0,
        "FIB_S2": 0,
        "FIB_S3": 0,
        "FIB_M": 0,
        "FIB_R1": 0,
        "FIB_R2": 0,
        "FIB_R3": 0,
        "VWMA": 0,
        "RSI": 0

    }

    return arr


# 1 min , 5 min , 15 min , 1hr, 4hr, 1day
def generateTimeFrames():
    myArr = [60, 300, 900, 3600, 14400, 86400]
    return myArr

# Convert Time Frame to Meet API - Standards for Calls
def convertTimeFrame(interval):
    timeFrame = ""
    if interval == 60:
        timeFrame = "1 Min"
    if interval == 300:
        timeFrame = "5 Min"
    if interval == 900:
        timeFrame = "15 Min"
    if interval == 3600:
        timeFrame = "1 Hour"
    if interval == 14400:
        timeFrame = "4 Hour"
    if interval == 86400:
        timeFrame = "Daily"

# Load Data to Json File
def writeJsonData(fileName, data):
    with open(fileName, 'w') as outfile:
        json_string = json.dumps(data)
        outfile.write(json_string)

filename = 'indicators.json'


def updateIndicatorsJSON():
    newData = {'Indicators': []}


def updateIndicatorValuesInJson():
    symbols = generateProductList()
    timeFrames = generateTimeFrames()
    jsonArr = []
    newData = {'Indicators': []}
    count = 0

    start_time = time.time()
    for x in range(len(symbols) - 1):

        for y in range(len(timeFrames) - 1):
            newInterval = timeFrames[y]
            values = getTA(symbols[x], "crypto", "COINBASE", newInterval)
            # jsonArr.insert(len(jsonArr), values)
            newData['Indicators'].insert(count, values)
            count += 1

    writeJsonData(filename, newData)
    print("--- %s seconds ---" % (time.time() - start_time))


def updateIndividualIndicator(symbol):
    timeFrames = generateTimeFrames()
    jsonArr = []
    newData = {'Indicators': []}
    count = 0
    start_time = time.time()

    for y in range(len(timeFrames) - 1):
        newInterval = timeFrames[y]
        values = getTA(symbol, "crypto", "COINBASE", newInterval)
        # jsonArr.insert(len(jsonArr), values)
        newData['Indicators'].insert(count, values)
        count += 1

    writeJsonData('indicators.json', newData)
    print("--- %s seconds ---" % (time.time() - start_time))


def readTechnicalAnalysisValues(fileName, symbol):
    newData = readJsonData(fileName)
    base = newData['Indicators']

    newArr = []

    for x in range(len(base)):
        b = base[x]
        # Timeframe, Open, Volume, Change, MA5/
        arr = [b[1], b[3], round(b[5],2), round(b[6],2), b[7], b[8],b[9],b[10],b[11],b[12],b[13], b[23], b[24]]
        newArr.insert(len(newArr), arr)

    return newArr

#updateIndividualIndicator("SUKU-USD")





