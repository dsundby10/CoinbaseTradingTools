import cbpro
import Keys
import time
import datetime
from Time import *

# Initialize CB Pro References
auth_client = Keys.getAuthClient()

def getCurrentDate():
    currentDate = datetime.datetime.now()
    return currentDate.strftime("%m-%d-%Y %I:%M:%S")


def formatOrderStructureX(order):
    orderObj = [{
        'coin': order['product_id'],
        'price': order['price'],
        'size': order['size'],
        'side': order['side'],
        'created_at': order['created_at'],
        'fill_fees': order['fill_fees'],
        'filled_size': order['filled_size'],
    }]
    return orderObj


# Format the data all open orders
# This is the baseData in the structure (Used in getAllOpenOrders)
def formatOrderStructure(order):
    orderId = order['id']
    coin = order['product_id']
    side = order['side']
    price = order['price']
    size = order['size']
    filled_size = order['filled_size']
    created_at = order['created_at']


    orderObj2 = [orderId, coin, side,  price, size, filled_size, created_at]
    return orderObj2

# Get ALL open Orders
def getAllOpenOrders():
    myOrders = auth_client.get_orders()
    orderList = list(myOrders)

    orderStructure = []
    for x in range(len(orderList)):
        obj = formatOrderStructure(orderList[x])
        orderStructure.insert(len(orderStructure), obj)

    return orderStructure

# Get Orders by Specific Coin
def getOrdersBySpecificPair(comboListProduct):
    orderStructure = []
    if comboListProduct == "ALL":
        orderStructure = getAllOpenOrders()
    else:
        myOrders = auth_client.get_orders(product_id=comboListProduct)
        orderList = list(myOrders)

        orderStructure = []
        for x in range(len(orderList)):
            obj = formatOrderStructure(orderList[x])
            orderStructure.insert(len(orderStructure), obj)

    return orderStructure


def formatOrdersForTableDisplay(formattedOrders):
    tableOrderStructure = []
    for x in range(len(formattedOrders)):
        product = formattedOrders[x][1]
        side = formattedOrders[x][2]
        price = formattedOrders[x][3]
        size = formattedOrders[x][4]
        filled_size = formattedOrders[x][5]
        created_at = strip8601Time(formattedOrders[x][6])

        orderArr = [product,side,price,size, filled_size, created_at]

        tableOrderStructure.insert(x, orderArr)

    return tableOrderStructure



# Cancel the orders from the selected values on the table
# getSelectedRows is needed for this function
def cancelSelectedOrders(selectedRow, baseData):
    success = 0
    for x in range(len(selectedRow)):

        rowNumber = int(selectedRow[x])
        orderIDtoCancel = baseData[rowNumber]
        auth_client.cancel_order(orderIDtoCancel[0])
        success = 1

    return success


# Get all Uniq products from orders and return a sorted list
def getAllUniqueProducts(baseData):
    uniqProduct = []
    productStr = ""
    count = 0
    for x in range(len(baseData)):
        orderData = baseData[x]
        if x == 0:
            uniqProduct.insert(count, orderData[1])
            productStr += orderData[1]
            count+=1

        elif productStr.__contains__(orderData[1]):
            holder=0
        else:
            uniqProduct.insert(count, orderData[1])
            productStr += orderData[1]
            count += 1

    uniqProduct.sort()

    finalUniqProduct = ["ALL"]
    for i in range(len(uniqProduct)):
        finalUniqProduct.insert(i+1,uniqProduct[i])

    return finalUniqProduct




