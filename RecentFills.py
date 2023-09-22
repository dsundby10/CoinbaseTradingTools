import cbpro
import Keys
import time
import datetime

# Initialize CB Pro References
auth_client = Keys.getAuthClient()

def getCurrentDate():
    currentDate = datetime.datetime.now()
    return currentDate.strftime("%m-%d-%Y %I:%M:%S")

# Calculate the Avg Price for Each Iteration
def calculateAvg(price, fee, size):
    #newPrice = float(price) + float(fee)
    #return newPrice * float(size)
    return float(price) * float(size)

def calculateFess(price, fee, size):
    return  float(fee)

# Updated to include available and hold
def checkBalancesRecentFills():
    # Get List of Balances With Balance > 0
    accounts = auth_client.get_accounts()
    balances = []
    balanceCount = 0
    for x in range(0, len(accounts)):
        checkBalance = float(accounts[x]['balance'])
        coin = accounts[x]['currency']

        if checkBalance >= 1:
            hold = float(accounts[x]['hold'])
            avail = checkBalance - hold
            #print("Coin: ", checkBalance, " ", coin, " Hold: ", accounts[x]['hold'], " Avail: ", avail)
        if coin == "YFI" and checkBalance != 0 or coin == "BTC" and checkBalance != 0:
            hold = float(accounts[x]['hold'])
            avail = checkBalance - hold
            #print("Coin: ", checkBalance, " ", coin, " Hold: ", accounts[x]['hold'], " Avail: ", avail)

        if float(accounts[x]['balance']) != 0:
            balances.insert(balanceCount, {
                "coin": accounts[x]['currency'],
                "balance": convertFloats(accounts[x]['balance']),
                "available": convertFloats(accounts[x]['available']),
                "hold": convertFloats(accounts[x]['hold'])
            })
            balanceCount+=1
    return balances

# Rough Draft -> Must check functionality / return values of API call
def getCoinCurrentPrice(coin):
    price = auth_client.get_product_ticker(coin)
    return price


def getTotalBalanceInUSD(balanceArr):
    totalUSD = 0

    for x in range(0, len(balanceArr)):
        coin = balanceArr[x][balanceArr['coin']]
        balance = int(balanceArr[x][balanceArr['balance']])
        price = 0
        if str(coin).__contains__("USD"):
            price = 1
            price = price * balance
        else:
            price = getCoinCurrentPrice(coin)
            price = price * balance

        totalUSD += price

    return totalUSD

def convertFloats(floatNumber):
    convertedNumber = 0
    if floatNumber != 0:
        convertedNumber = round(float(floatNumber), 2)
    else:
        convertedNumber = 0
    return convertedNumber



def getBalances(coin):
    balances = checkBalancesRecentFills()
    coinBalance = 0
    for x in range(0, len(balances)):
        if balances[x]['coin'].__str__().upper() == coin:
            #print("Coin: ", balances[x]['balance'])
            coinBalance = float(balances[x]['balance'])
    return coinBalance


def splitPair(pair):
    splitCoin = str(pair).split("-")


def generateAveragePositionOLD(pair):
    start_time = time.time()

    myFills = list(auth_client.get_fills(product_id=pair))
    splitCoin = str(pair).split("-")
    coin = splitCoin[0]
    balance = getBalances(coin)

    newBalance = 0
    avgPrice = 0
    totalFees = 0
    myAvg = 0
    # product_id / price / size / fee / side
    for x in range(0, len(myFills)):
        if myFills[x]['side'] == 'buy':
            if newBalance < balance:
                newBalance += float(myFills[x]['size'])

                totalFees += calculateFess(myFills[x]['price'], myFills[x]['fee'], myFills[x]['size'])

                avgPrice += calculateAvg(myFills[x]['price'], myFills[x]['fee'], myFills[x]['size'])
                #print("New Balance: ", newBalance, " /// Avg Price: ", avgPrice)
                myAvg = avgPrice / newBalance
                #print("Final AVG: ", avgPrice, '/', newBalance, " == $", myAvg)
                #print("Total Fees: ", totalFees)

    finalValuesObj = [{"AvgPrice": round(myAvg, 4), "TotalCoins": round(newBalance,3), "TotalFees": round(totalFees, 2)}]
    # print("---Function1 %s seconds ---" % (time.time() - start_time))
    # print(finalValuesObj)

    auth_client.session.close()
    return finalValuesObj

from itertools import islice

def generateAveragePosition(pair):
    #start_time = time.time()

    newFills = islice(auth_client.get_fills(pair), 4000) #Pulling last 4000 trades

    myFills = list(newFills)

    splitCoin = str(pair).split("-")
    coin = splitCoin[0]
    balance = getBalances(coin)

    newBalance = 0
    avgPrice = 0
    totalFees = 0
    myAvg = 0

    exceptor=0
    counter=0
    for x in range(0, 4000):

        try:
            if myFills[x]['side'] == 'buy':

                if newBalance < balance:
                    newBalance += float(myFills[x]['size'])

                    if newBalance <= balance:
                        totalFees += calculateFess(myFills[x]['price'], myFills[x]['fee'], myFills[x]['size'])
                        avgPrice += calculateAvg(myFills[x]['price'], myFills[x]['fee'], myFills[x]['size'])
                        #print(str(counter) + " || New Balance: ", newBalance, " || Avg Price: ", avgPrice)
                        myAvg = avgPrice / newBalance
                        counter += 1

                    else:

                        difference = newBalance - balance

                        # Update newbalance to = actual balance
                        newBalance = newBalance - difference

                        newSize = float(myFills[x]['size']) - difference
                        totalFees += calculateFess(myFills[x]['price'], myFills[x]['fee'], newSize) #Fee wont always be 100% spot on
                        avgPrice += calculateAvg(myFills[x]['price'], myFills[x]['fee'], newSize)
                        # print("Current Balance: " + str(balance) + "Iterated Balance:  " + str(newBalance) + " Differnce: " + str(newSize))
                        # print("Price: " + str(myFills[x]['price']) + " | Size: " + str(myFills[x]['size']) + " Created: " + myFills[x]['created_at'])
                        # print(str(counter) + " [Diff] || New Balance: ", newBalance, " || Avg Price: ", avgPrice)
                        myAvg = avgPrice / newBalance

                    # print("Final AVG: ", avgPrice, '/', newBalance, " == $", myAvg)
                    # print("Total Fees: ", totalFees)
        except:
            exceptor=1

    #print("--- Function2 %s seconds ---" % (time.time() - start_time))
    finalValuesObj = [{"AvgPrice": round(myAvg, 6), "TotalCoins": round(newBalance, 3), "TotalFees": round(totalFees, 2)}]
    #print(finalValuesObj)

    auth_client.session.close()
    return finalValuesObj



# Updated to include available and hold
def getBalancesForAvgCalculations():
    # Get List of Balances With Balance > 0
    accounts = auth_client.get_accounts()
    balances = []
    balanceCount = 0
    for x in range(0, len(accounts)):
        checkBalance = float(accounts[x]['balance'])
        coin = accounts[x]['currency']
        coinAmt = accounts[x]['balance']

        if checkBalance != 0:
            balances.insert(balanceCount, {
                "coin": accounts[x]['currency'],
                "balance": float(accounts[x]['balance']),
                "available": float(accounts[x]['available']),
                "hold": float(accounts[x]['hold'])
            })

            balanceCount+=1
    auth_client.session.close()
    return balances

def convertBalancesToUSDX(balancesArr):

    myData = []

    for x in range(len(balancesArr)):
        coin = balancesArr[x]['coin'] + "-USD"

        calculateTotalUSD = 0
        currentPrice = 0
        timestamp = ""
        # Account for the USD currencies
        if str(balancesArr[x]['coin']).__contains__("USD"):
            calculateTotalUSD = round(balancesArr[x]['balance'])
            currentPrice = 1
        else:
            productData = auth_client.get_product_ticker(coin)  # Can calculate market volume using this method
            currentPrice = productData['price']
            calculateTotalUSD = float(currentPrice) * float(balancesArr[x]['balance'])

        # Set a threshold for usd value to be bigger than x USD value to track
        if confirmBalanceBiggerThanThreshold(calculateTotalUSD, 1):
            obj = {"Coin" : balancesArr[x]['coin'],
                   "Balance" : balancesArr[x]['balance'],
                   "Price" : currentPrice,
                   "ValueUSD" : round(calculateTotalUSD, 2)}
            myData.insert(len(myData), obj)

    return myData

def confirmBalanceBiggerThanThreshold(usdValue, threshold):
    newValue = 0
    if usdValue > threshold:
        newValue = usdValue
    else:
        newValue = 0

    return newValue




def getAllAverages(convertArr):
    start_time = time.time()
    avgARR = []
    counter = 0
    for x in range(0, len(convertArr)):
        totalCoins = ""
        currency = ""
        pair = ""
        PL = 0
        currentBalanceToUSD = 0
        avgBalanceToUSD = 0
        currentPrice = convertArr[x]['Price']

        if str(convertArr[x]['Coin']).__contains__("USD"):
            currency = convertArr[x]['Coin']
            totalCoins = convertArr[x]['Balance']

            obj = [{"Coin": currency, "Balance": totalCoins, "Avg": "1", "CurrentPrice": currentPrice, "BalanceToUSD": totalCoins, "AvgBalanceToUSD": totalCoins, "PL": 0}]
            avgARR.insert(counter, obj)
            #print(obj)
            counter += 1
        else:
            pair = convertArr[x]['Coin'] + "-USD"
            avgObj = generateAveragePosition(pair)

            currentBalanceToUSD = float(currentPrice) * float(avgObj[0]["TotalCoins"])
            avgBalanceToUSD = float(avgObj[0]["AvgPrice"]) * float(avgObj[0]["TotalCoins"])
            calcPL = balanceToUSD - avgBalanceToUSD
            PL = round(balanceToUSD - avgBalanceToUSD, 2)

            obj = [{"Coin": pair, "Balance": avgObj[0]["TotalCoins"], "Avg": avgObj[0]["AvgPrice"], "CurrentPrice": currentPrice, "BalanceToUSD": round(currentBalanceToUSD, 2), "AvgBalanceToUSD": avgBalanceToUSD, "PL": PL}]
            #print(obj)
            avgARR.insert(counter, obj)
            counter+=1
    #print(avgARR)
    print("---AllAvgsExecutionTime %s seconds ---" % (time.time() - start_time))

    return avgARR




def getAllAveragesX(convertArr):
    start_time = time.time()
    avgARR = []
    counter = 0
    for x in range(0, len(convertArr)):
        totalCoins = ""
        currency = ""
        pair = ""
        PL = 0
        currentBalanceToUSD = 0
        avgBalanceToUSD = 0
        currentPrice = convertArr[x]['Price']

        if str(convertArr[x]['Coin']).__contains__("USD"):
            currency = convertArr[x]['Coin']
            totalCoins = convertArr[x]['Balance']

            obj = [{"Coin": currency, "Balance": round(totalCoins, 2), "Avg": "1", "CurrentPrice": currentPrice, "BalanceToUSD": round(totalCoins, 2), "AvgBalanceToUSD": round(totalCoins, 2), "PL": 0, "PercentChange": 0}]
            avgARR.insert(counter, obj)

            counter += 1
        else:
            pair = convertArr[x]['Coin'] + "-USD"
            avgObj = generateAveragePosition(pair)
            print(avgObj)

            currentBalanceToUSD = float(currentPrice) * float(avgObj[0]["TotalCoins"])
            avgBalanceToUSD = float(avgObj[0]["AvgPrice"]) * float(avgObj[0]["TotalCoins"])

            calcPL = currentBalanceToUSD - avgBalanceToUSD
            PL = round(currentBalanceToUSD - avgBalanceToUSD, 2)

            diffBalanceToUSD = currentBalanceToUSD - PL
            percentChange = calcPL / diffBalanceToUSD * 100

            obj = [{"Coin": pair, "Balance": avgObj[0]["TotalCoins"], "Avg": avgObj[0]["AvgPrice"], "CurrentPrice": currentPrice, "BalanceToUSD": round(currentBalanceToUSD, 2), "AvgBalanceToUSD": round(avgBalanceToUSD, 2), "PL": PL, "PercentChange": round(percentChange,2)}]

            avgARR.insert(counter, obj)
            counter+=1

    print("---AllAvgsExecutionTime %s seconds ---" % (time.time() - start_time))

    return avgARR


def calcTotalPLBtwnAllPositions(allAvgsArr):
    currentAvgObjPL = 0
    totalPL = 0
    totalUSDValue = 0
    avgUSDValue = 0
    for x in range(len(allAvgsArr)):
        # Have to pull the structure apart in reverse mode to access individual values per line
        currentAvgObj = allAvgsArr[x]
        currentAvgObjCoin = currentAvgObj[0]['Coin']
        currentAvgObjPL = float(currentAvgObj[0]['PL'])
        currentTotalBalanceToUSD = float(currentAvgObj[0]['BalanceToUSD'])
        currentAvgUSDValue = float(currentAvgObj[0]['AvgBalanceToUSD'])


        totalPL += currentAvgObjPL
        totalUSDValue += currentTotalBalanceToUSD
        avgUSDValue += avgUSDValue


    totalDifference = totalUSDValue - totalPL
    totalPercentChange = totalPL/totalDifference * 100

    dataObj = [{
        "Totals_totalUSDValue": round(totalUSDValue,2),
        "Totals_totalAvgValue": round(avgUSDValue,2),
        "Totals_totalPL": round(totalPL,2),
        "Totals_totalPerecntChange": round(totalPercentChange,2)
    }]

    print(dataObj)
    return dataObj




# balancesArr = getBalancesForAvgCalculations()
# convertArr = convertBalancesToUSDX(balancesArr)
# allAvgsArr = getAllAveragesX(convertArr)
# totalsArr = calcTotalPLBtwnAllPositions(allAvgsArr)


# allAvgsArr = [[{'Coin': 'ACH-USD', 'Balance': 3895045.9, 'Avg': 0.0581, 'CurrentPrice': '0.057544', 'BalanceToUSD': 224136.52, 'AvgBalanceToUSD': 226302.17, 'PL': -2165.65, 'PercentChange': -0.96}], [{'Coin': 'API3-USD', 'Balance': 11548.46, 'Avg': 4.4845, 'CurrentPrice': '4.55', 'BalanceToUSD': 52545.49, 'AvgBalanceToUSD': 51789.07, 'PL': 756.42, 'PercentChange': 1.46}], [{'Coin': 'BTRST-USD', 'Balance': 77030.75, 'Avg': 2.9372, 'CurrentPrice': '2.91', 'BalanceToUSD': 224159.48, 'AvgBalanceToUSD': 226254.72, 'PL': -2095.24, 'PercentChange': -0.93}], [{'Coin': 'COVAL-USD', 'Balance': 12492655.0, 'Avg': 0.1038, 'CurrentPrice': '0.09855', 'BalanceToUSD': 1231151.15, 'AvgBalanceToUSD': 1296737.59, 'PL': -65586.44, 'PercentChange': -5.06}], [{'Coin': 'DOGE-USD', 'Balance': 5255.0, 'Avg': 0, 'CurrentPrice': '0.1756', 'BalanceToUSD': 922.78, 'AvgBalanceToUSD': 0.0, 'PL': 922.78, 'PercentChange': -46138900.0}], [{'Coin': 'ENS-USD', 'Balance': 16333.72, 'Avg': 26.3642, 'CurrentPrice': '27.71', 'BalanceToUSD': 452607.38, 'AvgBalanceToUSD': 430625.46, 'PL': 21981.92, 'PercentChange': 5.1}], [{'Coin': 'LQTY-USD', 'Balance': 14348.45, 'Avg': 5.5143, 'CurrentPrice': '5.6', 'BalanceToUSD': 80351.32, 'AvgBalanceToUSD': 79121.66, 'PL': 1229.66, 'PercentChange': 1.55}], [{'Coin': 'LRC-USD', 'Balance': 294336.51, 'Avg': 1.3566, 'CurrentPrice': '1.3438', 'BalanceToUSD': 395529.4, 'AvgBalanceToUSD': 399296.91, 'PL': -3767.51, 'PercentChange': -0.94}], [{'Coin': 'PRO-USD', 'Balance': 95467.44, 'Avg': 2.7093, 'CurrentPrice': '2.58', 'BalanceToUSD': 246306.0, 'AvgBalanceToUSD': 258649.94, 'PL': -12343.94, 'PercentChange': -4.77}], [{'Coin': 'REQ-USD', 'Balance': 410164.0, 'Avg': 0.2904, 'CurrentPrice': '0.2884', 'BalanceToUSD': 118291.3, 'AvgBalanceToUSD': 119111.63, 'PL': -820.33, 'PercentChange': -0.69}], [{'Coin': 'USD', 'Balance': 2736713.3, 'Avg': '1', 'CurrentPrice': 1, 'BalanceToUSD': 2736713.3, 'AvgBalanceToUSD': 2736713.3, 'PL': 0, 'PercentChange': 0}], [{'Coin': 'USDT', 'Balance': 31731.64, 'Avg': '1', 'CurrentPrice': 1, 'BalanceToUSD': 31731.64, 'AvgBalanceToUSD': 31731.64, 'PL': 0, 'PercentChange': 0}], [{'Coin': 'XYO-USD', 'Balance': 61899942.7, 'Avg': 0.029, 'CurrentPrice': '0.02905', 'BalanceToUSD': 1798193.34, 'AvgBalanceToUSD': 1795098.34, 'PL': 3095.0, 'PercentChange': 0.17}]]
# totalsArr = [{'Totals_totalUSDValue': 7592639.1, 'Totals_totalAvgValue': 0, 'Totals_totalPL': -58793.33, 'Totals_totalPerecntChange': -0.77}]


def formatDataDisplayAllAvgs(allAvgsArr, totalsArr):
    formatAvgArr = []
    count=0
    finalFormattedAllAvgs_String = ""
    for x in range(len(allAvgsArr)):
        # Have to pull the structure apart in reverse mode to access individual values per line
        currentAvgObj = allAvgsArr[x]
        obj = [{
            "Coin": currentAvgObj[0]['Coin'],
            "Balance": currentAvgObj[0]['Balance'],
            "CurrentPrice": currentAvgObj[0]['CurrentPrice'],
            "BalanceToUSD": currentAvgObj[0]['BalanceToUSD'],
            "AvgBalanceToUSD": currentAvgObj[0]['AvgBalanceToUSD'],
            "PL": currentAvgObj[0]['PL'],
            "PercentChange": currentAvgObj[0]['PercentChange'],
        }]
        formatAvgArr.insert(len(formatAvgArr), obj)

        if x == len(allAvgsArr) - 1:
            formatAvgArr.insert(len(allAvgsArr)+1, totalsArr)


    return formatAvgArr


def formatDataDisplayAllAvgsToOneString(allAvgsArr, totalsArr):

    finalFormattedAllAvgs_String = ""
    for x in range(len(allAvgsArr)):

        # Have to pull the structure apart in reverse mode to access individual values per line
        currentAvgObj = allAvgsArr[x]

        Coin = currentAvgObj[0]['Coin']
        Balance = currentAvgObj[0]['Balance']
        CurrentPrice = currentAvgObj[0]['CurrentPrice']
        BalanceToUSD = currentAvgObj[0]['BalanceToUSD']
        AvgBalanceToUSD = float(currentAvgObj[0]['AvgBalanceToUSD']) * float(currentAvgObj[0]['CurrentPrice'])
        PL = currentAvgObj[0]['PL']
        PercentChange = currentAvgObj[0]['PercentChange']

        formatCoin = ""
        if str(Coin).__contains__("-USD"):
            formatCoin = str(Coin).split("-")
            Coin = formatCoin[0]

        formatStr = Coin + " |\t\t " + str(Balance) + " |\t\t " + str(CurrentPrice) + " |\t " + str(BalanceToUSD) + " |\t\t " + str(AvgBalanceToUSD) + " |\t\t " + str(PL) + " |\t\t " + str(PercentChange)
        finalFormattedAllAvgs_String +=  formatStr + "\n"


        if x == len(allAvgsArr) - 1:

            Totals_totalUSDValue = totalsArr[0]['Totals_totalUSDValue']
            Totals_totalAvgValue = totalsArr[0]['Totals_totalAvgValue']
            Totals_totalPL = totalsArr[0]['Totals_totalPL']
            Totals_totalPerecntChange = totalsArr[0]['Totals_totalPerecntChange']
            formatStr = "\nTotals |  Acc Balance $ " + str(Totals_totalUSDValue) + " | Acc Averages $" + str(Totals_totalAvgValue) + " |  P/L $" + str(Totals_totalPL) + " | Acc Percent Change % " + str(Totals_totalPerecntChange)
            finalFormattedAllAvgs_String += formatStr

    print(finalFormattedAllAvgs_String)
    return finalFormattedAllAvgs_String





# allAvgsArr = [[{'Coin': 'ACH-USD', 'Balance': 3895045.9, 'Avg': 0.0581, 'CurrentPrice': '0.057544', 'BalanceToUSD': 224136.52, 'AvgBalanceToUSD': 226302.17, 'PL': -2165.65, 'PercentChange': -0.96}], [{'Coin': 'API3-USD', 'Balance': 11548.46, 'Avg': 4.4845, 'CurrentPrice': '4.55', 'BalanceToUSD': 52545.49, 'AvgBalanceToUSD': 51789.07, 'PL': 756.42, 'PercentChange': 1.46}], [{'Coin': 'BTRST-USD', 'Balance': 77030.75, 'Avg': 2.9372, 'CurrentPrice': '2.91', 'BalanceToUSD': 224159.48, 'AvgBalanceToUSD': 226254.72, 'PL': -2095.24, 'PercentChange': -0.93}], [{'Coin': 'COVAL-USD', 'Balance': 12492655.0, 'Avg': 0.1038, 'CurrentPrice': '0.09855', 'BalanceToUSD': 1231151.15, 'AvgBalanceToUSD': 1296737.59, 'PL': -65586.44, 'PercentChange': -5.06}], [{'Coin': 'DOGE-USD', 'Balance': 5255.0, 'Avg': 0, 'CurrentPrice': '0.1756', 'BalanceToUSD': 922.78, 'AvgBalanceToUSD': 0.0, 'PL': 922.78, 'PercentChange': -46138900.0}], [{'Coin': 'ENS-USD', 'Balance': 16333.72, 'Avg': 26.3642, 'CurrentPrice': '27.71', 'BalanceToUSD': 452607.38, 'AvgBalanceToUSD': 430625.46, 'PL': 21981.92, 'PercentChange': 5.1}], [{'Coin': 'LQTY-USD', 'Balance': 14348.45, 'Avg': 5.5143, 'CurrentPrice': '5.6', 'BalanceToUSD': 80351.32, 'AvgBalanceToUSD': 79121.66, 'PL': 1229.66, 'PercentChange': 1.55}], [{'Coin': 'LRC-USD', 'Balance': 294336.51, 'Avg': 1.3566, 'CurrentPrice': '1.3438', 'BalanceToUSD': 395529.4, 'AvgBalanceToUSD': 399296.91, 'PL': -3767.51, 'PercentChange': -0.94}], [{'Coin': 'PRO-USD', 'Balance': 95467.44, 'Avg': 2.7093, 'CurrentPrice': '2.58', 'BalanceToUSD': 246306.0, 'AvgBalanceToUSD': 258649.94, 'PL': -12343.94, 'PercentChange': -4.77}], [{'Coin': 'REQ-USD', 'Balance': 410164.0, 'Avg': 0.2904, 'CurrentPrice': '0.2884', 'BalanceToUSD': 118291.3, 'AvgBalanceToUSD': 119111.63, 'PL': -820.33, 'PercentChange': -0.69}], [{'Coin': 'USD', 'Balance': 2736713.3, 'Avg': '1', 'CurrentPrice': 1, 'BalanceToUSD': 2736713.3, 'AvgBalanceToUSD': 2736713.3, 'PL': 0, 'PercentChange': 0}], [{'Coin': 'USDT', 'Balance': 31731.64, 'Avg': '1', 'CurrentPrice': 1, 'BalanceToUSD': 31731.64, 'AvgBalanceToUSD': 31731.64, 'PL': 0, 'PercentChange': 0}], [{'Coin': 'XYO-USD', 'Balance': 61899942.7, 'Avg': 0.029, 'CurrentPrice': '0.02905', 'BalanceToUSD': 1798193.34, 'AvgBalanceToUSD': 1795098.34, 'PL': 3095.0, 'PercentChange': 0.17}]]
# totalsArr = [{'Totals_totalUSDValue': 7592639.1, 'Totals_totalAvgValue': 0, 'Totals_totalPL': -58793.33, 'Totals_totalPerecntChange': -0.77}]


def formatDataDisplayAllAvgs2(allAvgsArr, totalsArr):
    formatAvgArr = []
    count=0
    finalFormattedAllAvgs_String = ""
    for x in range(len(allAvgsArr)):
        # Have to pull the structure apart in reverse mode to access individual values per line
        currentAvgObj = allAvgsArr[x]

        Coin = currentAvgObj[0]['Coin']
        Balance = currentAvgObj[0]['Balance']
        AvgPrice = currentAvgObj[0]['Avg']
        CurrentPrice = currentAvgObj[0]['CurrentPrice']
        BalanceToUSD = currentAvgObj[0]['BalanceToUSD']

        AvgBalanceToUSD = round(float(currentAvgObj[0]['Balance']) * float(currentAvgObj[0]['CurrentPrice']),2)
        PL = currentAvgObj[0]['PL']
        PercentChange = currentAvgObj[0]['PercentChange']

        formatCoin = ""
        if str(Coin).__contains__("-USD"):
            formatCoin = str(Coin).split("-")
            Coin = formatCoin[0]

        arr = [Coin, Balance, AvgPrice, AvgBalanceToUSD, CurrentPrice, BalanceToUSD, PL, PercentChange]
        formatAvgArr.insert(len(formatAvgArr), arr)

    return formatAvgArr





