from Variables import *
import cbpro
import time
#from playsound import playsound
public_client = cbpro.PublicClient()



def convertVolumeToUSD(lowPrice, highPrice, volume):
    avgPrice = (lowPrice+highPrice) / 2
    return volume*avgPrice

def getTimeFramePercentDiff(lowPrice, highPrice):
    diff = highPrice - lowPrice
    avgPrice = (lowPrice + highPrice) / 2
    return (diff / avgPrice) * 100

def calculatePercentChange(coin, oldPrice, newPrice):
    # Percent change = new price - original price
    # difference / original number X 100

    change = float(newPrice) - float(oldPrice)
    percentChange = change / float(oldPrice) * 100

    return percentChange


#[ time, low, high, open, close, volume ]
def getCandleData(coinName, timeFrame, maxCandles):
    data = public_client.get_product_historic_rates(coinName, granularity=timeFrame)
    myArr = []
    obj = {}
    count = 0
    rdm=0
    totalUSDVolume = 0
    for x in range(maxCandles):
        try:
            convertTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[x][0]))

            change = calculatePercentChange(coinName, data[x][1], data[x][2])
            volumteToUSD = float(data[x][2]) * float(data[x][5])
            obj = {
                'coin': coinName,
                'time': convertTime,
                'low': data[x][1],
                'high': data[x][2],
                'open': data[x][3],
                'close': data[x][4],
                'volume': data[x][5],
                'volumeToUSD': round(volumteToUSD,2),
                'percentChange': round(change,2)
            }
            # print("Coin: ", coinName, " | Change: %", round(change, 3), "| High: $", round(data[x][2], 4), " | Low: $", round(data[x][1], 4))
            myArr.insert(x, obj)
        except:
            rdm=1
            #print("CoinName Failed to GET:", coinName, "X= ", x)
            #print("Total USD VOLUME - ", totalUSDVolume)
    return obj



def getAllCoinLastCandles(myCoinList):

    priceList = []
    counter = 0
    totalUSDVolume = 0
    for x in range(0, len(myCoinList)):
        coin = myCoinList[x]

        # Adjust Thresholds as needed (currently tracking 15 min candles)
        getPrice = getCandleData(coin, 900, 1) #15 min Candles (900)

        #getPrice = getCandleData(coin, 21600, 1) #6 Hr Candles (14400)
        #getPrice = getCandleData(coin, 86400, 1) #Daily Candles (86400)

        priceList.insert(x, getPrice)

        # Track usd volume
        #vol = getPrice['volumeToUSD']
        #totalUSDVolume += float(vol)

        # Limit = 15 API call per second
        if counter == 6:
            time.sleep(1)
            counter = 0

        counter+=1

    return priceList

# def generateTotalUSDPerTimeFrame(priceList):
#     totalusdvol = 0




def sortCoinDataListByVolume(coinDataList):
    newList = []
    totalvol = 0
    for x in range(len(coinDataList)):
        try:
            coin = coinDataList[x]['coin']
            timeFrame = coinDataList[x]['time']
            low = coinDataList[x]['low']
            high = coinDataList[x]['high']
            open = coinDataList[x]['open']
            close = coinDataList[x]['close']
            volume = coinDataList[x]['volume']
            voluemtoUSD = coinDataList[x]['volumeToUSD']
            percentChange = coinDataList[x]['percentChange']
            arr = [voluemtoUSD, coin, timeFrame, low, high, open, close, volume, percentChange]

            totalvol += float(voluemtoUSD)
            newList.insert(len(newList), arr)
        except:
            oops = 0

    print("Total USD Volume : ", totalvol )
    sortedList = sorted(newList)
    return sortedList


def sortCoinDataListByPercentChange(coinDataList):
    newList = []
    for x in range(len(coinDataList)):
        try:

            coin = coinDataList[x]['coin']
            timeFrame = coinDataList[x]['time']
            low = coinDataList[x]['low']
            high = coinDataList[x]['high']
            open = coinDataList[x]['open']
            close = coinDataList[x]['close']

            volume = coinDataList[x]['volume']
            voluemtoUSD = coinDataList[x]['volumeToUSD']

            percentChange = 0
            if float(open) > float(close):
                percentChange = float(coinDataList[x]['percentChange']) * -1
            else:
                percentChange = float(coinDataList[x]['percentChange'])

            # percentChange = coinDataList[x]['percentChange']
            arr = [percentChange, coin, timeFrame, low, high, open, close, volume, voluemtoUSD]
            newList.insert(len(newList), arr)
        except:
            oops = 0

    sortedList = sorted(newList)
    return sortedList



def displayResults(finalSortedList):
    print("-----------------------------Time: ", finalSortedList[0]['time'], "----------------------------------")
    count = 0
    for x in range(0, len(finalSortedList)):
        percentChange = 0
        if float(finalSortedList[x]['open']) > float(finalSortedList[x]['close']):
            percentChange = float(finalSortedList[x]['percentChange']) * -1
        else:
            percentChange = float(finalSortedList[x]['percentChange'])

        if float(finalSortedList[x]['percentChange'] >= 4):
            #playsound('C:\CoinbasePro\Alerts\holyshit.mp3')
            print(finalSortedList[x]['coin'], " | Change: %", round(percentChange, 3),
                  " | High: $", round(float(finalSortedList[x]['high']), 4), " | Low: $",
                  round(float(finalSortedList[x]['low']), 4), '| Open: $ ', round(float(finalSortedList[x]['open']), 4), ' | Close: $ ', round(float(finalSortedList[x]['close']), 4),'| Volume $', round(newVolume,2))
        elif float(finalSortedList[x]['percentChange'] >= 0.5):
            #playsound('C:\CoinbasePro\Alerts\holyshit.mp3')
            print(finalSortedList[x]['coin'], " | Change: %", round(percentChange, 3),
                  " | High: $", round(float(finalSortedList[x]['high']), 4), " | Low: $",
                  round(float(finalSortedList[x]['low']), 4), '| Open: $ ', round(float(finalSortedList[x]['open']), 4),
                  '| Close: $', round(float(finalSortedList[x]['close']), 4), '| Volume $', round(newVolume,2))


def displayData(sortedList, volumeOrPercent_0_1):
    percentThreshold = 1
    volumeThreshold = 50000
    for x in range(len(sortedList)):
        if x == 0 and volumeOrPercent_0_1 == 0:
            print("--------[Sort By Volume > " + str(volumeThreshold) + "-------- TimeFrame: " + str(sortedList[x][2]) + " --------[Sort By Volume > " + str(volumeThreshold) + "--------")

        if x == 0 and volumeOrPercent_0_1 == 1:
            print("--------[Sort By Percent > OR < " + str(percentThreshold) + "-------- TimeFrame: " + str(sortedList[x][2]) + "--------[Sort By Percent > OR < " + str(percentThreshold) + "--------")

        if volumeOrPercent_0_1 == 0:
            volumeToUSD = sortedList[x][0]
            if volumeToUSD > volumeThreshold:
                print(sortedList[x][1] + " | USD_Volume $" + str(sortedList[x][0]) + " | High $" + str(sortedList[x][4]) + " | Low $" + str(sortedList[x][3]), " | Open $" + str(sortedList[x][5]) + " | Close $" + str(sortedList[x][6]) + " | Change %" + str(sortedList[x][8]))
        else:
            percentChange = sortedList[x][0]
            if percentChange < -2 or percentChange > 2:
                print(sortedList[x][1] + " | % Change " + str(sortedList[x][0]) + " | High $" + str(sortedList[x][4]) + " | Low $" + str(sortedList[x][3]), " | Open $" + str(sortedList[x][5]) + " | Close $" + str(sortedList[x][6]) + " | USD_Volume $" + str(sortedList[x][8]))


# Used for Pump Detector
def generateProductListUSDonly():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""

    for x in range(0, len(products)):
        id = str(products[x]['id'])
        splitProduct = id.split("-")
        # Products to EXCLUDE
        if splitProduct[0] == "DDX" or splitProduct[0] == "OOKI" or splitProduct[0] == "PAX" or splitProduct[0] == "WBTC" or splitProduct[0] == "GYEN" or splitProduct[0] == "WLUNA" or splitProduct[0] == "UST" or splitProduct[0] == "REP" or splitProduct[0] == "KEEP" or splitProduct[0] == "BUSD" :
            k = 0
        elif splitProduct[1] == "USD":
            productList += id + ","

    productList = str(productList).split(",")

    return productList

keeploop = 0

coinDataList = [{'coin': 'SOL-USD', 'time': '2022-02-01 16:15:00', 'low': 110.87, 'high': 111.52, 'open': 110.9, 'close': 111.39, 'volume': 5240.048, 'volumeToUSD': 584370.15, 'percentChange': 0.59}, {'coin': 'TRIBE-USD', 'time': '2022-02-01 16:00:00', 'low': 0.6929, 'high': 0.6944, 'open': 0.6941, 'close': 0.6941, 'volume': 2166.6, 'volumeToUSD': 1504.49, 'percentChange': 0.22}, {'coin': 'MDT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.06218, 'high': 0.06255, 'open': 0.06219, 'close': 0.06229, 'volume': 310705, 'volumeToUSD': 19434.6, 'percentChange': 0.6}, {'coin': 'TRU-USD', 'time': '2022-02-01 16:00:00', 'low': 0.1922, 'high': 0.1933, 'open': 0.1931, 'close': 0.1923, 'volume': 741.9, 'volumeToUSD': 143.41, 'percentChange': 0.57}, {'coin': 'USDT-USD', 'time': '2022-02-01 16:15:00', 'low': 1.0005, 'high': 1.0006, 'open': 1.0005, 'close': 1.0006, 'volume': 120219.57, 'volumeToUSD': 120291.7, 'percentChange': 0.01}, {'coin': 'ATOM-USD', 'time': '2022-02-01 16:15:00', 'low': 28.95, 'high': 29.08, 'open': 28.95, 'close': 29.03, 'volume': 5375.92, 'volumeToUSD': 156331.75, 'percentChange': 0.45}, {'coin': 'ALCX-USD', 'time': '2022-02-01 16:00:00', 'low': 176.07, 'high': 176.82, 'open': 176.79, 'close': 176.22, 'volume': 10.5289, 'volumeToUSD': 1861.72, 'percentChange': 0.43}, {'coin': 'ARPA-USD', 'time': '2022-02-01 16:15:00', 'low': 0.0625, 'high': 0.0626, 'open': 0.0626, 'close': 0.0625, 'volume': 558.5, 'volumeToUSD': 34.96, 'percentChange': 0.16}, {'coin': 'FX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.5938, 'high': 0.5938, 'open': 0.5938, 'close': 0.5938, 'volume': 2.2, 'volumeToUSD': 1.31, 'percentChange': 0.0}, {'coin': 'LTC-USD', 'time': '2022-02-01 16:15:00', 'low': 114.78, 'high': 115.21, 'open': 114.79, 'close': 115.19, 'volume': 550.72677893, 'volumeToUSD': 63449.23, 'percentChange': 0.37}, {'coin': 'REN-USD', 'time': '2022-02-01 16:15:00', 'low': 0.3259, 'high': 0.3268, 'open': 0.3259, 'close': 0.3266, 'volume': 4845.618798, 'volumeToUSD': 1583.55, 'percentChange': 0.28}, {'coin': 'QNT-USD', 'time': '2022-02-01 16:15:00', 'low': 104.08, 'high': 104.63, 'open': 104.26, 'close': 104.22, 'volume': 99.924, 'volumeToUSD': 10455.05, 'percentChange': 0.53}, {'coin': 'REQ-USD', 'time': '2022-02-01 16:15:00', 'low': 0.23436, 'high': 0.2348, 'open': 0.2348, 'close': 0.23436, 'volume': 9504, 'volumeToUSD': 2231.54, 'percentChange': 0.19}, {'coin': 'TRB-USD', 'time': '2022-02-01 16:15:00', 'low': 20.83, 'high': 20.86, 'open': 20.85, 'close': 20.86, 'volume': 48.163, 'volumeToUSD': 1004.68, 'percentChange': 0.14}, {'coin': 'KRL-USD', 'time': '2022-02-01 16:15:00', 'low': 0.8377, 'high': 0.8427, 'open': 0.8427, 'close': 0.8377, 'volume': 2336.8, 'volumeToUSD': 1969.22, 'percentChange': 0.6}, {'coin': 'POLY-USD', 'time': '2022-02-01 16:15:00', 'low': 0.3845, 'high': 0.3853, 'open': 0.3851, 'close': 0.3853, 'volume': 5859, 'volumeToUSD': 2257.47, 'percentChange': 0.21}, {'coin': 'IMX-USD', 'time': '2022-02-01 16:15:00', 'low': 2.9, 'high': 2.92, 'open': 2.91, 'close': 2.92, 'volume': 405.29, 'volumeToUSD': 1183.45, 'percentChange': 0.69}, {'coin': 'IDEX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1193, 'high': 0.1226, 'open': 0.1193, 'close': 0.1226, 'volume': 191335.5, 'volumeToUSD': 23457.73, 'percentChange': 2.77}, {'coin': 'PAX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.99, 'high': 1, 'open': 1, 'close': 0.99, 'volume': 4.28, 'volumeToUSD': 4.28, 'percentChange': 1.01}, {'coin': 'ORN-USD', 'time': '2022-02-01 16:15:00', 'low': 4.26, 'high': 4.27, 'open': 4.27, 'close': 4.27, 'volume': 16.84, 'volumeToUSD': 71.91, 'percentChange': 0.23}, {'coin': 'BAND-USD', 'time': '2022-02-01 16:15:00', 'low': 3.49, 'high': 3.5, 'open': 3.5, 'close': 3.49, 'volume': 6, 'volumeToUSD': 21.0, 'percentChange': 0.29}, {'coin': 'XTZ-USD', 'time': '2022-02-01 16:15:00', 'low': 3.66, 'high': 3.68, 'open': 3.66, 'close': 3.66, 'volume': 19139.8, 'volumeToUSD': 70434.46, 'percentChange': 0.55}, {'coin': 'WCFG-USD', 'time': '2022-02-01 15:45:00', 'low': 0.63, 'high': 0.63, 'open': 0.63, 'close': 0.63, 'volume': 54.82, 'volumeToUSD': 34.54, 'percentChange': 0.0}, {'coin': 'MIR-USD', 'time': '2022-02-01 16:15:00', 'low': 1.171, 'high': 1.172, 'open': 1.172, 'close': 1.172, 'volume': 1183.02, 'volumeToUSD': 1386.5, 'percentChange': 0.09}, {'coin': 'SHIB-USD', 'time': '2022-02-01 16:15:00', 'low': 2.169e-05, 'high': 2.172e-05, 'open': 2.17e-05, 'close': 2.17e-05, 'volume': 6182191349, 'volumeToUSD': 134277.2, 'percentChange': 0.14}, {'coin': 'RLC-USD', 'time': '2022-02-01 16:15:00', 'low': 1.99, 'high': 1.99, 'open': 1.99, 'close': 1.99, 'volume': 40.63, 'volumeToUSD': 80.85, 'percentChange': 0.0}, {'coin': 'RARI-USD', 'time': '2022-02-01 16:15:00', 'low': 9.28, 'high': 9.38, 'open': 9.35, 'close': 9.37, 'volume': 407.387, 'volumeToUSD': 3821.29, 'percentChange': 1.08}, {'coin': 'GFI-USD', 'time': '2022-02-01 16:00:00', 'low': 4.54, 'high': 4.57, 'open': 4.54, 'close': 4.56, 'volume': 274.92, 'volumeToUSD': 1256.38, 'percentChange': 0.66}, {'coin': 'DOGE-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1422, 'high': 0.1425, 'open': 0.1422, 'close': 0.1424, 'volume': 423336.2, 'volumeToUSD': 60325.41, 'percentChange': 0.21}, {'coin': 'ZRX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.586069, 'high': 0.588281, 'open': 0.586069, 'close': 0.587092, 'volume': 8859.4728, 'volumeToUSD': 5211.86, 'percentChange': 0.38}, {'coin': 'UST-USD', 'time': '2022-02-01 16:15:00', 'low': 1, 'high': 1.001, 'open': 1.001, 'close': 1.001, 'volume': 6047.44, 'volumeToUSD': 6053.49, 'percentChange': 0.1}, {'coin': 'COMP-USD', 'time': '2022-02-01 16:15:00', 'low': 127.92, 'high': 128.24, 'open': 127.92, 'close': 128.18, 'volume': 83.292, 'volumeToUSD': 10681.37, 'percentChange': 0.25}, {'coin': 'STX-USD', 'time': '2022-02-01 16:15:00', 'low': 1.5, 'high': 1.5, 'open': 1.5, 'close': 1.5, 'volume': 276.46, 'volumeToUSD': 414.69, 'percentChange': 0.0}, {'coin': 'WLUNA-USD', 'time': '2022-02-01 16:15:00', 'low': 51.48, 'high': 51.79, 'open': 51.73, 'close': 51.7, 'volume': 5263.483, 'volumeToUSD': 272595.78, 'percentChange': 0.6}, {'coin': 'LPT-USD', 'time': '2022-02-01 16:15:00', 'low': 26.64, 'high': 26.68, 'open': 26.66, 'close': 26.68, 'volume': 31.783, 'volumeToUSD': 847.97, 'percentChange': 0.15}, {'coin': 'NU-USD', 'time': '2022-02-01 16:15:00', 'low': 0.4937, 'high': 0.494, 'open': 0.4938, 'close': 0.494, 'volume': 1023.845346, 'volumeToUSD': 505.78, 'percentChange': 0.06}, {'coin': 'ZEC-USD', 'time': '2022-02-01 16:15:00', 'low': 98.17, 'high': 98.32, 'open': 98.17, 'close': 98.25, 'volume': 187.91182466, 'volumeToUSD': 18475.49, 'percentChange': 0.15}, {'coin': 'VGX-USD', 'time': '2022-02-01 16:15:00', 'low': 1.89, 'high': 1.89, 'open': 1.89, 'close': 1.89, 'volume': 27.11, 'volumeToUSD': 51.24, 'percentChange': 0.0}, {'coin': 'BTC-USD', 'time': '2022-02-01 16:00:00', 'low': 38505.99, 'high': 38742.27, 'open': 38527.63, 'close': 38653.71, 'volume': 237.86896642, 'volumeToUSD': 9215583.72, 'percentChange': 0.61}, {'coin': 'XLM-USD', 'time': '2022-02-01 16:15:00', 'low': 0.204545, 'high': 0.204941, 'open': 0.204599, 'close': 0.204929, 'volume': 20650, 'volumeToUSD': 4232.03, 'percentChange': 0.19}, {'coin': 'BNT-USD', 'time': '2022-02-01 16:00:00', 'low': 2.51, 'high': 2.53, 'open': 2.52, 'close': 2.53, 'volume': 588.174689, 'volumeToUSD': 1488.08, 'percentChange': 0.8}, {'coin': 'MPL-USD', 'time': '2022-02-01 16:00:00', 'low': 15.04, 'high': 15.14, 'open': 15.11, 'close': 15.07, 'volume': 56.602, 'volumeToUSD': 856.95, 'percentChange': 0.66}, {'coin': 'COTI-USD', 'time': '2022-02-01 16:15:00', 'low': 0.3119, 'high': 0.3125, 'open': 0.3119, 'close': 0.3119, 'volume': 7071.2, 'volumeToUSD': 2209.75, 'percentChange': 0.19}, {'coin': 'YFI-USD', 'time': '2022-02-01 16:15:00', 'low': 25151.8, 'high': 25179.77, 'open': 25151.8, 'close': 25172.62, 'volume': 0.064734, 'volumeToUSD': 1629.99, 'percentChange': 0.11}, {'coin': 'AMP-USD', 'time': '2022-02-01 16:15:00', 'low': 0.03034, 'high': 0.0305, 'open': 0.03036, 'close': 0.0304, 'volume': 348763, 'volumeToUSD': 10637.27, 'percentChange': 0.53}, {'coin': 'FIL-USD', 'time': '2022-02-01 16:15:00', 'low': 20.8, 'high': 20.87, 'open': 20.8, 'close': 20.87, 'volume': 646.473, 'volumeToUSD': 13491.89, 'percentChange': 0.34}, {'coin': 'GODS-USD', 'time': '2022-02-01 16:15:00', 'low': 2.1, 'high': 2.11, 'open': 2.1, 'close': 2.1, 'volume': 100.67, 'volumeToUSD': 212.41, 'percentChange': 0.48}, {'coin': 'RLY-USD', 'time': '2022-02-01 16:15:00', 'low': 0.2273, 'high': 0.2277, 'open': 0.2277, 'close': 0.2276, 'volume': 109, 'volumeToUSD': 24.82, 'percentChange': 0.18}, {'coin': 'RAI-USD', 'time': '2022-02-01 16:00:00', 'low': 3.05, 'high': 3.05, 'open': 3.05, 'close': 3.05, 'volume': 30.57, 'volumeToUSD': 93.24, 'percentChange': 0.0}, {'coin': 'INV-USD', 'time': '2022-02-01 16:15:00', 'low': 591, 'high': 594.51, 'open': 593.91, 'close': 594, 'volume': 19.2357, 'volumeToUSD': 11435.82, 'percentChange': 0.59}, {'coin': 'BLZ-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1358, 'high': 0.1359, 'open': 0.1358, 'close': 0.1359, 'volume': 9823, 'volumeToUSD': 1334.95, 'percentChange': 0.07}, {'coin': 'COVAL-USD', 'time': '2022-02-01 16:15:00', 'low': 0.06143, 'high': 0.06224, 'open': 0.06166, 'close': 0.06173, 'volume': 328561, 'volumeToUSD': 20449.64, 'percentChange': 1.32}, {'coin': 'DOT-USD', 'time': '2022-02-01 16:15:00', 'low': 19.67, 'high': 19.71, 'open': 19.67, 'close': 19.71, 'volume': 526.875, 'volumeToUSD': 10384.71, 'percentChange': 0.2}, {'coin': 'AGLD-USD', 'time': '2022-02-01 16:15:00', 'low': 1.2, 'high': 1.23, 'open': 1.2, 'close': 1.22, 'volume': 46603.38, 'volumeToUSD': 57322.16, 'percentChange': 2.5}, {'coin': 'LCX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1177, 'high': 0.1184, 'open': 0.1181, 'close': 0.118, 'volume': 15130.2, 'volumeToUSD': 1791.42, 'percentChange': 0.59}, {'coin': 'ENJ-USD', 'time': '2022-02-01 16:15:00', 'low': 1.85, 'high': 1.86, 'open': 1.85, 'close': 1.86, 'volume': 1168.4, 'volumeToUSD': 2173.22, 'percentChange': 0.54}, {'coin': 'FIDA-USD', 'time': '2022-02-01 16:15:00', 'low': 2.47, 'high': 2.49, 'open': 2.49, 'close': 2.49, 'volume': 6925.34, 'volumeToUSD': 17244.1, 'percentChange': 0.81}, {'coin': 'SKL-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1162, 'high': 0.1162, 'open': 0.1162, 'close': 0.1162, 'volume': 1939.3, 'volumeToUSD': 225.35, 'percentChange': 0.0}, {'coin': 'POLS-USD', 'time': '2022-02-01 16:15:00', 'low': 1.58, 'high': 1.59, 'open': 1.58, 'close': 1.59, 'volume': 1486.25, 'volumeToUSD': 2363.14, 'percentChange': 0.63}, {'coin': 'FET-USD', 'time': '2022-02-01 16:15:00', 'low': 0.3215, 'high': 0.3226, 'open': 0.3215, 'close': 0.3218, 'volume': 2303.4, 'volumeToUSD': 743.08, 'percentChange': 0.34}, {'coin': 'MCO2-USD', 'time': '2022-02-01 16:15:00', 'low': 11.1, 'high': 11.21, 'open': 11.14, 'close': 11.21, 'volume': 381.95, 'volumeToUSD': 4281.66, 'percentChange': 0.99}, {'coin': 'SUSHI-USD', 'time': '2022-02-01 16:15:00', 'low': 4.41, 'high': 4.42, 'open': 4.41, 'close': 4.42, 'volume': 1607.81, 'volumeToUSD': 7106.52, 'percentChange': 0.23}, {'coin': 'SUKU-USD', 'time': '2022-02-01 16:15:00', 'low': 0.558, 'high': 0.5868, 'open': 0.5798, 'close': 0.5707, 'volume': 643186.9, 'volumeToUSD': 377422.07, 'percentChange': 5.16}, {'coin': 'LQTY-USD', 'time': '2022-02-01 16:15:00', 'low': 3.2, 'high': 3.2, 'open': 3.2, 'close': 3.2, 'volume': 542.91, 'volumeToUSD': 1737.31, 'percentChange': 0.0}, {'coin': 'DDX-USD', 'time': '2022-02-01 16:15:00', 'low': 2.87, 'high': 2.89, 'open': 2.87, 'close': 2.89, 'volume': 2919.51, 'volumeToUSD': 8437.38, 'percentChange': 0.7}, {'coin': 'DAI-USD', 'time': '2022-02-01 16:15:00', 'low': 0.9999, 'high': 0.999901, 'open': 0.9999, 'close': 0.999901, 'volume': 2495.02767, 'volumeToUSD': 2494.78, 'percentChange': 0.0}, {'coin': 'LINK-USD', 'time': '2022-02-01 16:15:00', 'low': 16.95, 'high': 17.03, 'open': 16.95, 'close': 17, 'volume': 5715.06, 'volumeToUSD': 97327.47, 'percentChange': 0.47}, {'coin': 'NKN-USD', 'time': '2022-02-01 16:15:00', 'low': 0.2227, 'high': 0.2233, 'open': 0.2228, 'close': 0.2227, 'volume': 3910.7, 'volumeToUSD': 873.26, 'percentChange': 0.27}, {'coin': 'MUSD-USD', 'time': '2022-02-01 16:00:00', 'low': 0.997, 'high': 0.997, 'open': 0.997, 'close': 0.997, 'volume': 603.36, 'volumeToUSD': 601.55, 'percentChange': 0.0}, {'coin': 'POWR-USD', 'time': '2022-02-01 16:00:00', 'low': 0.5509, 'high': 0.5517, 'open': 0.5515, 'close': 0.5513, 'volume': 11522.1, 'volumeToUSD': 6356.74, 'percentChange': 0.15}, {'coin': 'CTX-USD', 'time': '2022-02-01 16:15:00', 'low': 8.1, 'high': 8.1, 'open': 8.1, 'close': 8.1, 'volume': 2.895, 'volumeToUSD': 23.45, 'percentChange': 0.0}, {'coin': 'BAT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.843, 'high': 0.844, 'open': 0.843, 'close': 0.844, 'volume': 596.85, 'volumeToUSD': 503.74, 'percentChange': 0.12}, {'coin': 'CTSI-USD', 'time': '2022-02-01 16:15:00', 'low': 0.4741, 'high': 0.4748, 'open': 0.4748, 'close': 0.4741, 'volume': 733.6, 'volumeToUSD': 348.31, 'percentChange': 0.15}, {'coin': 'OXT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.2463, 'high': 0.2469, 'open': 0.2468, 'close': 0.2463, 'volume': 413, 'volumeToUSD': 101.97, 'percentChange': 0.24}, {'coin': 'CHZ-USD', 'time': '2022-02-01 16:15:00', 'low': 0.1874, 'high': 0.1881, 'open': 0.1874, 'close': 0.1877, 'volume': 23430.5, 'volumeToUSD': 4407.28, 'percentChange': 0.37}, {'coin': 'EOS-USD', 'time': '2022-02-01 16:15:00', 'low': 2.35, 'high': 2.36, 'open': 2.35, 'close': 2.35, 'volume': 3372.3, 'volumeToUSD': 7958.63, 'percentChange': 0.43}, {'coin': 'SPELL-USD', 'time': '2022-02-01 16:15:00', 'low': 0.00699, 'high': 0.00705, 'open': 0.007, 'close': 0.00701, 'volume': 2570448, 'volumeToUSD': 18121.66, 'percentChange': 0.86}, {'coin': 'ETH-USD', 'time': '2022-02-01 16:15:00', 'low': 2777.67, 'high': 2790, 'open': 2778.02, 'close': 2787.33, 'volume': 192.24022059, 'volumeToUSD': 536350.22, 'percentChange': 0.44}, {'coin': 'KNC-USD', 'time': '2022-02-01 16:15:00', 'low': 1.8668, 'high': 1.8696, 'open': 1.8686, 'close': 1.8668, 'volume': 707.8, 'volumeToUSD': 1323.3, 'percentChange': 0.15}, {'coin': 'PLU-USD', 'time': '2022-02-01 16:15:00', 'low': 15.22, 'high': 15.22, 'open': 15.22, 'close': 15.22, 'volume': 33.39, 'volumeToUSD': 508.2, 'percentChange': 0.0}, {'coin': 'RAD-USD', 'time': '2022-02-01 16:15:00', 'low': 5.57, 'high': 5.57, 'open': 5.57, 'close': 5.57, 'volume': 4.09, 'volumeToUSD': 22.78, 'percentChange': 0.0}, {'coin': 'ZEN-USD', 'time': '2022-02-01 16:00:00', 'low': 39.14, 'high': 39.17, 'open': 39.15, 'close': 39.15, 'volume': 21.147, 'volumeToUSD': 828.33, 'percentChange': 0.08}, {'coin': 'GRT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.4412, 'high': 0.4428, 'open': 0.4423, 'close': 0.4413, 'volume': 49949.42, 'volumeToUSD': 22117.6, 'percentChange': 0.36}, {'coin': 'GTC-USD', 'time': '2022-02-01 16:15:00', 'low': 8.14, 'high': 8.17, 'open': 8.16, 'close': 8.14, 'volume': 61.94, 'volumeToUSD': 506.05, 'percentChange': 0.37}, {'coin': 'FOX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.3658, 'high': 0.3729, 'open': 0.3684, 'close': 0.3703, 'volume': 21157.9, 'volumeToUSD': 7889.78, 'percentChange': 1.94}, {'coin': 'DESO-USD', 'time': '2022-02-01 16:15:00', 'low': 50.8, 'high': 51.21, 'open': 50.8, 'close': 51.21, 'volume': 105.183, 'volumeToUSD': 5386.42, 'percentChange': 0.81}, {'coin': 'UNI-USD', 'time': '2022-02-01 16:15:00', 'low': 11.15, 'high': 11.19, 'open': 11.15, 'close': 11.18, 'volume': 5955.238319, 'volumeToUSD': 66639.12, 'percentChange': 0.36}, {'coin': 'SNX-USD', 'time': '2022-02-01 16:15:00', 'low': 5.43, 'high': 5.46, 'open': 5.43, 'close': 5.46, 'volume': 275.759, 'volumeToUSD': 1505.64, 'percentChange': 0.55}, {'coin': 'AVAX-USD', 'time': '2022-02-01 16:15:00', 'low': 71.69, 'high': 71.91, 'open': 71.71, 'close': 71.7, 'volume': 2665.178, 'volumeToUSD': 191652.95, 'percentChange': 0.31}, {'coin': 'SHPING-USD', 'time': '2022-02-01 16:15:00', 'low': 0.035896, 'high': 0.0362, 'open': 0.03617, 'close': 0.036181, 'volume': 706927, 'volumeToUSD': 25590.76, 'percentChange': 0.85}, {'coin': 'FARM-USD', 'time': '2022-02-01 16:15:00', 'low': 109.63, 'high': 110.33, 'open': 109.85, 'close': 110.02, 'volume': 121.537, 'volumeToUSD': 13409.18, 'percentChange': 0.64}, {'coin': 'DNT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.0824, 'high': 0.0843, 'open': 0.0837, 'close': 0.0828, 'volume': 64352.6, 'volumeToUSD': 5424.92, 'percentChange': 2.31}, {'coin': 'ALGO-USD', 'time': '2022-02-01 16:15:00', 'low': 0.9624, 'high': 0.973, 'open': 0.971, 'close': 0.9631, 'volume': 266768.7, 'volumeToUSD': 259565.95, 'percentChange': 1.1}, {'coin': 'OMG-USD', 'time': '2022-02-01 16:15:00', 'low': 4.82, 'high': 4.82, 'open': 4.82, 'close': 4.82, 'volume': 150, 'volumeToUSD': 723.0, 'percentChange': 0.0}, {'coin': 'BCH-USD', 'time': '2022-02-01 16:15:00', 'low': 285.92, 'high': 286.74, 'open': 285.92, 'close': 286.57, 'volume': 28.64977928, 'volumeToUSD': 8215.04, 'percentChange': 0.29}, {'coin': 'BTRST-USD', 'time': '2022-02-01 16:15:00', 'low': 4.76, 'high': 4.8, 'open': 4.76, 'close': 4.77, 'volume': 403.53, 'volumeToUSD': 1936.94, 'percentChange': 0.84}, {'coin': 'ANKR-USD', 'time': '2022-02-01 16:15:00', 'low': 0.07808, 'high': 0.07832, 'open': 0.07823, 'close': 0.07808, 'volume': 64563, 'volumeToUSD': 5056.57, 'percentChange': 0.31}, {'coin': 'NCT-USD', 'time': '2022-02-01 16:15:00', 'low': 0.04787, 'high': 0.04814, 'open': 0.04811, 'close': 0.04799, 'volume': 147976, 'volumeToUSD': 7123.56, 'percentChange': 0.56}, {'coin': 'AXS-USD', 'time': '2022-02-01 16:15:00', 'low': 53.16, 'high': 53.43, 'open': 53.16, 'close': 53.26, 'volume': 832.075, 'volumeToUSD': 44457.77, 'percentChange': 0.51}, {'coin': 'LRC-USD', 'time': '2022-02-01 16:15:00', 'low': 0.9665, 'high': 0.9705, 'open': 0.9665, 'close': 0.9697, 'volume': 20429.654822, 'volumeToUSD': 19826.98, 'percentChange': 0.41}, {'coin': 'BAL-USD', 'time': '2022-02-01 16:15:00', 'low': 12.51, 'high': 12.53, 'open': 12.51, 'close': 12.51, 'volume': 15.67, 'volumeToUSD': 196.35, 'percentChange': 0.16}, {'coin': 'CRV-USD', 'time': '2022-02-01 16:15:00', 'low': 3.47, 'high': 3.49, 'open': 3.48, 'close': 3.47, 'volume': 3530.44, 'volumeToUSD': 12321.24, 'percentChange': 0.58}, {'coin': 'MASK-USD', 'time': '2022-02-01 16:00:00', 'low': 6.17, 'high': 6.23, 'open': 6.17, 'close': 6.21, 'volume': 1670.78, 'volumeToUSD': 10408.96, 'percentChange': 0.97}, {'coin': 'XYO-USD', 'time': '2022-02-01 16:15:00', 'low': 0.02108, 'high': 0.021118, 'open': 0.021094, 'close': 0.021118, 'volume': 97157.7, 'volumeToUSD': 2051.78, 'percentChange': 0.18}, {'coin': 'JASMY-USD', 'time': '2022-02-01 16:15:00', 'low': 0.04503, 'high': 0.04523, 'open': 0.04504, 'close': 0.04515, 'volume': 457800, 'volumeToUSD': 20706.29, 'percentChange': 0.44}, {'coin': 'RBN-USD', 'time': '2022-02-01 16:15:00', 'low': 1.8, 'high': 1.8, 'open': 1.8, 'close': 1.8, 'volume': 41.84, 'volumeToUSD': 75.31, 'percentChange': 0.0}, {'coin': 'BOND-USD', 'time': '2022-02-01 16:15:00', 'low': 9.78, 'high': 9.81, 'open': 9.81, 'close': 9.81, 'volume': 152.629, 'volumeToUSD': 1497.29, 'percentChange': 0.31}, {'coin': 'ICP-USD', 'time': '2022-02-01 16:15:00', 'low': 19.93, 'high': 19.98, 'open': 19.93, 'close': 19.94, 'volume': 1979.3624, 'volumeToUSD': 39547.66, 'percentChange': 0.25}, {'coin': 'GALA-USD', 'time': '2022-02-01 16:15:00', 'low': 0.20248, 'high': 0.20434, 'open': 0.20248, 'close': 0.20424, 'volume': 2147254, 'volumeToUSD': 438769.88, 'percentChange': 0.92}, {'coin': '1INCH-USD', 'time': '2022-02-01 16:15:00', 'low': 1.69, 'high': 1.7, 'open': 1.69, 'close': 1.69, 'volume': 3536.17, 'volumeToUSD': 6011.49, 'percentChange': 0.59}, {'coin': 'STORJ-USD', 'time': '2022-02-01 16:15:00', 'low': 1.16, 'high': 1.16, 'open': 1.16, 'close': 1.16, 'volume': 83.22, 'volumeToUSD': 96.54, 'percentChange': 0.0}, {'coin': 'MANA-USD', 'time': '2022-02-01 16:15:00', 'low': 2.687, 'high': 2.694, 'open': 2.687, 'close': 2.689, 'volume': 69229.1, 'volumeToUSD': 186503.2, 'percentChange': 0.26}, {'coin': 'ORCA-USD', 'time': '2022-02-01 16:15:00', 'low': 3.67, 'high': 3.71, 'open': 3.69, 'close': 3.68, 'volume': 3393.45, 'volumeToUSD': 12589.7, 'percentChange': 1.09}, {'coin': 'QUICK-USD', 'time': '2022-02-01 16:15:00', 'low': 198.54, 'high': 201.18, 'open': 198.54, 'close': 200.3, 'volume': 187.6363, 'volumeToUSD': 37748.67, 'percentChange': 1.33}, {'coin': 'REP-USD', 'time': '2022-02-01 16:00:00', 'low': 13, 'high': 13.05, 'open': 13, 'close': 13.05, 'volume': 100.382891, 'volumeToUSD': 1310.0, 'percentChange': 0.38}, {'coin': 'ASM-USD', 'time': '2022-02-01 16:15:00', 'low': 0.05893, 'high': 0.05939, 'open': 0.05939, 'close': 0.05893, 'volume': 183787, 'volumeToUSD': 10915.11, 'percentChange': 0.78}, {'coin': 'PERP-USD', 'time': '2022-02-01 16:00:00', 'low': 6.38, 'high': 6.41, 'open': 6.38, 'close': 6.41, 'volume': 557.121, 'volumeToUSD': 3571.15, 'percentChange': 0.47}, {'coin': 'DASH-USD', 'time': '2022-02-01 16:15:00', 'low': 96.5, 'high': 96.67, 'open': 96.5, 'close': 96.59, 'volume': 30.708, 'volumeToUSD': 2968.54, 'percentChange': 0.18}, {'coin': 'LOOM-USD', 'time': '2022-02-01 16:15:00', 'low': 0.0825, 'high': 0.0825, 'open': 0.0825, 'close': 0.0825, 'volume': 712.1, 'volumeToUSD': 58.75, 'percentChange': 0.0}, {'coin': 'NMR-USD', 'time': '2022-02-01 16:15:00', 'low': 25.21, 'high': 25.28, 'open': 25.21, 'close': 25.23, 'volume': 3.56, 'volumeToUSD': 90.0, 'percentChange': 0.28}, {'coin': 'BICO-USD', 'time': '2022-02-01 16:15:00', 'low': 2.07, 'high': 2.07, 'open': 2.07, 'close': 2.07, 'volume': 2179.68, 'volumeToUSD': 4511.94, 'percentChange': 0.0}, {'coin': 'CGLD-USD', 'time': '2022-02-01 16:15:00', 'low': 3.24, 'high': 3.26, 'open': 3.25, 'close': 3.25, 'volume': 2251.54, 'volumeToUSD': 7340.02, 'percentChange': 0.62}, {'coin': 'AUCTION-USD', 'time': '2022-02-01 16:15:00', 'low': 14.55, 'high': 14.61, 'open': 14.58, 'close': 14.61, 'volume': 162.755, 'volumeToUSD': 2377.85, 'percentChange': 0.41}, {'coin': 'KEEP-USD', 'time': '2022-02-01 16:15:00', 'low': 0.4526, 'high': 0.4535, 'open': 0.4532, 'close': 0.4526, 'volume': 1313.9, 'volumeToUSD': 595.85, 'percentChange': 0.2}, {'coin': 'DIA-USD', 'time': '2022-02-01 16:15:00', 'low': 0.95, 'high': 0.95, 'open': 0.95, 'close': 0.95, 'volume': 212.35, 'volumeToUSD': 201.73, 'percentChange': 0.0}, {'coin': 'ADA-USD', 'time': '2022-02-01 16:15:00', 'low': 1.0742, 'high': 1.0782, 'open': 1.0742, 'close': 1.0764, 'volume': 442222.07, 'volumeToUSD': 476803.84, 'percentChange': 0.37}, {'coin': 'PLA-USD', 'time': '2022-02-01 16:15:00', 'low': 0.9225, 'high': 0.9249, 'open': 0.9246, 'close': 0.9225, 'volume': 153, 'volumeToUSD': 141.51, 'percentChange': 0.26}, {'coin': 'CVC-USD', 'time': '2022-02-01 16:15:00', 'low': 0.2876, 'high': 0.288, 'open': 0.2879, 'close': 0.2876, 'volume': 2816.4, 'volumeToUSD': 811.12, 'percentChange': 0.14}, {'coin': 'CRO-USD', 'time': '2022-02-01 16:15:00', 'low': 0.4345, 'high': 0.4355, 'open': 0.4345, 'close': 0.4348, 'volume': 55394.6, 'volumeToUSD': 24124.35, 'percentChange': 0.23}, {'coin': 'YFII-USD', 'time': '2022-02-01 16:15:00', 'low': 2314.71, 'high': 2315.22, 'open': 2314.71, 'close': 2315.22, 'volume': 0.00058, 'volumeToUSD': 1.34, 'percentChange': 0.02}, {'coin': 'OGN-USD', 'time': '2022-02-01 16:15:00', 'low': 0.329, 'high': 0.33, 'open': 0.329, 'close': 0.33, 'volume': 54131.46, 'volumeToUSD': 17863.38, 'percentChange': 0.3}, {'coin': 'ACH-USD', 'time': '2022-02-01 16:15:00', 'low': 0.0389, 'high': 0.039082, 'open': 0.038996, 'close': 0.039046, 'volume': 190275.8, 'volumeToUSD': 7436.36, 'percentChange': 0.47}, {'coin': 'BADGER-USD', 'time': '2022-02-01 16:15:00', 'low': 11.23, 'high': 11.26, 'open': 11.23, 'close': 11.25, 'volume': 131.414, 'volumeToUSD': 1479.72, 'percentChange': 0.27}, {'coin': 'CLV-USD', 'time': '2022-02-01 16:15:00', 'low': 0.35, 'high': 0.36, 'open': 0.35, 'close': 0.36, 'volume': 114.13, 'volumeToUSD': 41.09, 'percentChange': 2.86}, {'coin': 'UNFI-USD', 'time': '2022-02-01 16:15:00', 'low': 5.36, 'high': 5.38, 'open': 5.38, 'close': 5.38, 'volume': 21.4, 'volumeToUSD': 115.13, 'percentChange': 0.37}, {'coin': 'MKR-USD', 'time': '2022-02-01 16:15:00', 'low': 2178.44, 'high': 2186.43, 'open': 2179.01, 'close': 2183.56, 'volume': 13.87157, 'volumeToUSD': 30329.22, 'percentChange': 0.37}, {'coin': 'MATIC-USD', 'time': '2022-02-01 16:15:00', 'low': 1.6484, 'high': 1.6544, 'open': 1.6484, 'close': 1.651, 'volume': 84855.1, 'volumeToUSD': 140384.28, 'percentChange': 0.36}, {'coin': 'FORTH-USD', 'time': '2022-02-01 16:00:00', 'low': 5.26, 'high': 5.26, 'open': 5.26, 'close': 5.26, 'volume': 13.256, 'volumeToUSD': 69.73, 'percentChange': 0.0}, {'coin': 'PRO-USD', 'time': '2022-02-01 16:15:00', 'low': 2.23, 'high': 2.25, 'open': 2.25, 'close': 2.24, 'volume': 1120.45, 'volumeToUSD': 2521.01, 'percentChange': 0.9}, {'coin': 'IOTX-USD', 'time': '2022-02-01 16:15:00', 'low': 0.0922, 'high': 0.09252, 'open': 0.09234, 'close': 0.09238, 'volume': 2926, 'volumeToUSD': 270.71, 'percentChange': 0.35}, {'coin': 'AAVE-USD', 'time': '2022-02-01 16:15:00', 'low': 164.41, 'high': 164.96, 'open': 164.6, 'close': 164.49, 'volume': 229.836, 'volumeToUSD': 37913.75, 'percentChange': 0.33}, {'coin': 'ENS-USD', 'time': '2022-02-01 16:15:00', 'low': 19.54, 'high': 19.6, 'open': 19.54, 'close': 19.55, 'volume': 140.997, 'volumeToUSD': 2763.54, 'percentChange': 0.31}, {'coin': 'MLN-USD', 'time': '2022-02-01 16:15:00', 'low': 56.45, 'high': 56.59, 'open': 56.55, 'close': 56.59, 'volume': 14.464, 'volumeToUSD': 818.52, 'percentChange': 0.25}, {'coin': 'SUPER-USD', 'time': '2022-02-01 16:15:00', 'low': 0.7, 'high': 0.71, 'open': 0.71, 'close': 0.71, 'volume': 420.47, 'volumeToUSD': 298.53, 'percentChange': 1.43}, {'coin': 'UMA-USD', 'time': '2022-02-01 16:15:00', 'low': 5.95, 'high': 5.98, 'open': 5.98, 'close': 5.97, 'volume': 631.79, 'volumeToUSD': 3778.1, 'percentChange': 0.5}, {'coin': 'TRAC-USD', 'time': '2022-02-01 16:15:00', 'low': 0.6605, 'high': 0.6741, 'open': 0.6616, 'close': 0.6724, 'volume': 12377.7, 'volumeToUSD': 8343.81, 'percentChange': 2.06}, {'coin': 'RGT-USD', 'time': '2022-02-01 16:15:00', 'low': 21.2, 'high': 21.22, 'open': 21.2, 'close': 21.22, 'volume': 9.041, 'volumeToUSD': 191.85, 'percentChange': 0.09}, {'coin': 'API3-USD', 'time': '2022-02-01 16:15:00', 'low': 3.45, 'high': 3.46, 'open': 3.45, 'close': 3.46, 'volume': 45.53, 'volumeToUSD': 157.53, 'percentChange': 0.29}, {'coin': 'ETC-USD', 'time': '2022-02-01 16:15:00', 'low': 26.7, 'high': 26.75, 'open': 26.7, 'close': 26.7, 'volume': 942.09428612, 'volumeToUSD': 25201.02, 'percentChange': 0.19}, {}]


# While Loop to Keep It Running
while keeploop == 0:


    try:

        coinList = generateProductListUSDonly()
        coinDataList = getAllCoinLastCandles(coinList)
        sortedListVolume = sortCoinDataListByVolume(coinDataList)
        sortedListPercent = sortCoinDataListByPercentChange(coinDataList)
        displayData(sortedListVolume,0)
        displayData(sortedListPercent,1)

    except:
        print("To many API calls")

    time.sleep(300) #60 second = 1 minute // default = 300 second = 5 minutes











