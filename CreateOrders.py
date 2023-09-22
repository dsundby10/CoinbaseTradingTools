import cbpro
import time
from Keys import getAuthClient

auth_client = getAuthClient()

# Format Order Display for Console Output
def formatOrderDisplay(order):
    formatStr = ""
    try:
        formatStr =  str(order['product_id']) + " | Price $" + str(order['price']) + " | Qty: " + str(order['size'])
    except:
        print("FormatOrderDisplay -> Failed")
        #formatStr = "[FAILED-FORMAT ORDER DISPLAY]"
    return formatStr
# Quote Increment (returns an int used for rounding)
def getSpecificQuoteIncrementX(coin, coinData):
    quoteIncrement = 0
    for x in range(0, len(coinData)):
        if coin == coinData[x]['id']:
            quoteIncrement = coinData[x]['quote_increment']
    return quoteIncrement

# Base Min Size (returns an int used for rounding)
def getSpecificBaseMinSizeX(coin, coinData):
    baseMinSize = 0
    for x in range(0, len(coinData)):
        if coin == coinData[x]['id']:
            baseMinSize = coinData[x]['base_min_size']
    return baseMinSize

# Calc Quote Inc. (order price)
def calculateQuoteIncrementals(quoteIncrement):
    count = 0
    size = 0
    for x in quoteIncrement:
        if x == "1":
            size = count-1
        count += 1
    return size

# Calc BaseMin Inc. (order size)
def calculateBaseMinSizeIncrementals(baseMinSize):
    count = 0
    size = 0
    for x in baseMinSize:
        if x == "1":
            size = count - 1
        count += 1
    return size


# Get the Data Needed to Successfully Size your Orders (based off size/price to comply with Coinbase standards)
def getCoinPreReqs(pair, coinData, price, size):
    quoteIncrement = getSpecificQuoteIncrementX(pair, coinData)
    baseMinSize = getSpecificBaseMinSizeX(pair, coinData)

    convertQuoteIncrement = calculateQuoteIncrementals(quoteIncrement)
    convertBaseMinSize = calculateBaseMinSizeIncrementals(baseMinSize)

    floatPrice = float(price)
    floatSize = float(size)

    convertPrice = round(floatPrice, convertQuoteIncrement)
    convertSize = round(floatSize, convertBaseMinSize)


    return [convertPrice, convertSize]

# Used for Individual Buy/Sell Order Function (for accuracy)
def calcQuotePrice(pair, price, coinData):
    quoteIncrement = getSpecificQuoteIncrementX(pair, coinData)
    convertQuoteIncrement = calculateQuoteIncrementals(quoteIncrement)
    incrementalPrice = round(price, convertQuoteIncrement)

    return incrementalPrice



# Place Buy Order -> used in Multiple Order Function
def placeBuyOrder(price,size,order_type,productid):
    currentOrder = auth_client.buy(price=price,
                    size=size,
                    order_type=order_type,
                    #post_only = True,
                    product_id=productid)
    print("Buy Order Placed -> ", formatOrderDisplay(currentOrder))
    return currentOrder

# Place Sell Order -> used in Multiple Order Function
def placeSellOrder(price,size,order_type,productid):
    currentOrder = auth_client.sell(price=price,
                     size=size,
                     order_type=order_type,
                     #post_only = True,
                     product_id=productid)

    print("Sell Order Placed -> ", formatOrderDisplay(currentOrder))
    return currentOrder

# Place Individual Buy Order -> Used after a Sell order is Filled
def placeIndividualBuyOrder(price,size,order_type, productid, coinData):
    fixedPriceAndSize = getCoinPreReqs(productid, coinData, price, size)  # Returns [Price, Size]

    success = 0
    try:
        currentOrder = auth_client.buy(price=price,
                                       size=size,
                                       order_type=order_type,
                                       post_only=True,
                                       product_id=productid)
    except:
        currentOrder = [{"id": 'FAILED'}]
        print("Failed To Place Buy Order")
    return currentOrder

# Place Individual Sell Order -> Used after a Buy order is Filled
def placeIndividualSellOrder(price, size,order_type, productid, coinData):
    fixedPriceAndSize = getCoinPreReqs(productid,coinData, price, size) # Returns [Price, Size]

    try:
        currentOrder = auth_client.sell(price=fixedPriceAndSize[0],
                                        size=fixedPriceAndSize[1],
                                        order_type=order_type,
                                        post_only=True,
                                        product_id=productid)
    except:
        currentOrder = [{"id": 'FAILED'}]
        print("Failed To Place Sell Order")
    return currentOrder




def generateProductList():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""
    productsObj = []
    proudctsCount = 0
    for x in range(0, len(products)):
        myObj = []
        id = str(products[x]['id'])
        quote = str(products[x]['quote_increment'])
        #baseminsize = str(products[x]['base_min_size'])
        #basemaxsize = str(products[x]['base_max_size'])
        baseminsize = str(0)
        combined = id, ",", quote, ",", baseminsize

        if id.__contains__("USD"):
            myObj = {
                'id' : id,
                'quote_increment' : quote,
                'base_min_size' : baseminsize,
                #'base_max_size' : basemaxsize
            }
            #print("Count: ", proudctsCount, myObj)
            productsObj.insert(proudctsCount, myObj)
            proudctsCount += 1

    return productsObj
