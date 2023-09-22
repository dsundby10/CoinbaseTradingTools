import cbpro

# Not Neeeded
def getCoinList():
    coinList = [{'id': 'LQTY-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'QNT-USD', 'quote_increment': '0.01', 'base_min_size': '0.003'}, {'id': 'AGLD-USD', 'quote_increment': '0.01', 'base_min_size': '0.36'}, {'id': 'TRB-USD', 'quote_increment': '0.01', 'base_min_size': '0.016'}, {'id': 'GFI-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'FX-USD', 'quote_increment': '0.0001', 'base_min_size': '0.8'}, {'id': 'KEEP-USD', 'quote_increment': '0.0001', 'base_min_size': '1.3'}, {'id': 'LRC-USD', 'quote_increment': '0.0001', 'base_min_size': '0.45'}, {'id': 'AUCTION-USDT', 'quote_increment': '0.01', 'base_min_size': '0.027'}, {'id': 'DESO-USDT', 'quote_increment': '0.01', 'base_min_size': '0.01'}, {'id': 'UST-USD', 'quote_increment': '0.001', 'base_min_size': '0.99'}, {'id': 'POLS-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'CVC-USDC', 'quote_increment': '0.000001', 'base_min_size': '2'}, {'id': 'RGT-USD', 'quote_increment': '0.01', 'base_min_size': '0.025'}, {'id': 'TRIBE-USD', 'quote_increment': '0.0001', 'base_min_size': '0.9'}, {'id': 'BNT-USD', 'quote_increment': '0.01', 'base_min_size': '0.22'}, {'id': 'CRO-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'IDEX-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'ALCX-USD', 'quote_increment': '0.01', 'base_min_size': '0.0024'}, {'id': 'ENS-USD', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'ZEN-USD', 'quote_increment': '0.01', 'base_min_size': '0.01'}, {'id': 'MANA-USD', 'quote_increment': '0.001', 'base_min_size': '0.32'}, {'id': 'BTRST-USD', 'quote_increment': '0.01', 'base_min_size': '0.17'}, {'id': 'TRAC-USD', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'INV-USD', 'quote_increment': '0.01', 'base_min_size': '0.001'}, {'id': 'POWR-USDT', 'quote_increment': '0.0001', 'base_min_size': '1.6'}, {'id': 'AVAX-USDT', 'quote_increment': '0.01', 'base_min_size': '0.011'}, {'id': 'POLY-USDT', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'KNC-USD', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'GALA-USD', 'quote_increment': '0.00001', 'base_min_size': '3'}, {'id': 'TRU-USDT', 'quote_increment': '0.0001', 'base_min_size': '1.7'}, {'id': 'USDT-USDC', 'quote_increment': '0.0001', 'base_min_size': '0.99'}, {'id': 'MATIC-USD', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'ASM-USD', 'quote_increment': '0.00001', 'base_min_size': '6'}, {'id': 'SPELL-USDT', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'VGX-USDT', 'quote_increment': '0.01', 'base_min_size': '0.23'}, {'id': 'MCO2-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'POWR-USD', 'quote_increment': '0.0001', 'base_min_size': '0.6'}, {'id': 'COVAL-USDT', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'ZEN-USDT', 'quote_increment': '0.01', 'base_min_size': '0.01'}, {'id': 'USDT-EUR', 'quote_increment': '0.0001', 'base_min_size': '0.97'}, {'id': 'MASK-USD', 'quote_increment': '0.01', 'base_min_size': '0.07'}, {'id': 'ETC-USD', 'quote_increment': '0.01', 'base_min_size': '0.018'}, {'id': 'FARM-USDT', 'quote_increment': '0.01', 'base_min_size': '0.002'}, {'id': 'SUPER-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'BAND-USD', 'quote_increment': '0.01', 'base_min_size': '0.11'}, {'id': 'CLV-USDT', 'quote_increment': '0.01', 'base_min_size': '0.79'}, {'id': 'ALGO-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'ACH-USD', 'quote_increment': '0.000001', 'base_min_size': '11'}, {'id': 'IMX-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'MANA-USDC', 'quote_increment': '0.000001', 'base_min_size': '1'}, {'id': 'IOTX-USD', 'quote_increment': '0.00001', 'base_min_size': '4'}, {'id': 'ALCX-USDT', 'quote_increment': '0.01', 'base_min_size': '0.0025'}, {'id': 'ASM-USDT', 'quote_increment': '0.00001', 'base_min_size': '6'}, {'id': 'ORN-USDT', 'quote_increment': '0.01', 'base_min_size': '0.12'}, {'id': 'AVAX-USD', 'quote_increment': '0.01', 'base_min_size': '0.011'}, {'id': 'ARPA-USDT', 'quote_increment': '0.0001', 'base_min_size': '5.3'}, {'id': 'CHZ-USDT', 'quote_increment': '0.0001', 'base_min_size': '2'}, {'id': 'QUICK-USD', 'quote_increment': '0.01', 'base_min_size': '0.0025'}, {'id': 'RARI-USD', 'quote_increment': '0.01', 'base_min_size': '0.048'}, {'id': 'GRT-USD', 'quote_increment': '0.0001', 'base_min_size': '0.96'}, {'id': 'ZEC-USD', 'quote_increment': '0.01', 'base_min_size': '0.0056'}, {'id': 'REN-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'BTC-USDC', 'quote_increment': '0.01', 'base_min_size': '0.000016'}, {'id': 'SOL-USDT', 'quote_increment': '0.01', 'base_min_size': '0.004'}, {'id': 'REQ-USD', 'quote_increment': '0.00001', 'base_min_size': '4'}, {'id': 'PAX-USD', 'quote_increment': '0.01', 'base_min_size': '0.99'}, {'id': 'EOS-USD', 'quote_increment': '0.01', 'base_min_size': '0.2'}, {'id': 'DOGE-USDT', 'quote_increment': '0.0001', 'base_min_size': '3.8'}, {'id': 'BOND-USD', 'quote_increment': '0.01', 'base_min_size': '0.032'}, {'id': 'PERP-USDT', 'quote_increment': '0.01', 'base_min_size': '0.06'}, {'id': 'SUSHI-USD', 'quote_increment': '0.01', 'base_min_size': '0.09'}, {'id': 'WLUNA-USD', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'BICO-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'ENJ-USD', 'quote_increment': '0.01', 'base_min_size': '0.32'}, {'id': 'API3-USDT', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'COVAL-USD', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'DASH-USD', 'quote_increment': '0.01', 'base_min_size': '0.004'}, {'id': 'GODS-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'BAT-USD', 'quote_increment': '0.001', 'base_min_size': '0.92'}, {'id': 'DNT-USD', 'quote_increment': '0.0001', 'base_min_size': '3'}, {'id': 'DESO-USD', 'quote_increment': '0.01', 'base_min_size': '0.01'}, {'id': 'RAD-USD', 'quote_increment': '0.01', 'base_min_size': '0.08'}, {'id': 'LPT-USD', 'quote_increment': '0.01', 'base_min_size': '0.02'}, {'id': 'LOOM-USDC', 'quote_increment': '0.000001', 'base_min_size': '6'}, {'id': 'PAX-USDT', 'quote_increment': '0.01', 'base_min_size': '1'}, {'id': 'SPELL-USD', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'OGN-USD', 'quote_increment': '0.001', 'base_min_size': '0.93'}, {'id': 'WCFG-USD', 'quote_increment': '0.01', 'base_min_size': '0.57'}, {'id': 'WBTC-USD', 'quote_increment': '0.01', 'base_min_size': '0.000016'}, {'id': 'ENS-USDT', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'KRL-USD', 'quote_increment': '0.0001', 'base_min_size': '0.3'}, {'id': 'USDT-USD', 'quote_increment': '0.0001', 'base_min_size': '0.99'}, {'id': 'DAI-USDC', 'quote_increment': '0.000001', 'base_min_size': '0.99'}, {'id': 'COTI-USD', 'quote_increment': '0.0001', 'base_min_size': '1.9'}, {'id': 'LTC-USD', 'quote_increment': '0.01', 'base_min_size': '0.0043'}, {'id': 'SOL-USD', 'quote_increment': '0.01', 'base_min_size': '0.004'}, {'id': 'DDX-USD', 'quote_increment': '0.01', 'base_min_size': '0.17'}, {'id': 'GNT-USDC', 'quote_increment': '0.000001', 'base_min_size': '1'}, {'id': 'ICP-USDT', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'MDT-USD', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'BTC-USDT', 'quote_increment': '0.01', 'base_min_size': '0.000016'}, {'id': 'CGLD-USD', 'quote_increment': '0.01', 'base_min_size': '0.16'}, {'id': 'POLS-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': '1INCH-USD', 'quote_increment': '0.01', 'base_min_size': '0.23'}, {'id': 'RLY-USDT', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'AXS-USD', 'quote_increment': '0.01', 'base_min_size': '0.007'}, {'id': 'FOX-USDT', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'MIR-USD', 'quote_increment': '0.001', 'base_min_size': '0.31'}, {'id': 'BTC-USD', 'quote_increment': '0.01', 'base_min_size': '0.000016'}, {'id': 'RBN-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'DNT-USDC', 'quote_increment': '0.000001', 'base_min_size': '5'}, {'id': 'AGLD-USDT', 'quote_increment': '0.01', 'base_min_size': '0.36'}, {'id': 'RLY-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'IOTX-USDT', 'quote_increment': '0.00001', 'base_min_size': '3'}, {'id': 'UST-USDT', 'quote_increment': '0.001', 'base_min_size': '0.99'}, {'id': 'PLA-USD', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'ICP-USD', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'FARM-USD', 'quote_increment': '0.01', 'base_min_size': '0.006'}, {'id': 'ADA-USD', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'USDT-GBP', 'quote_increment': '0.0001', 'base_min_size': '0.97'}, {'id': 'BICO-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'FET-USD', 'quote_increment': '0.0001', 'base_min_size': '1.1'}, {'id': 'NCT-USDT', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'OXT-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'ETH-USD', 'quote_increment': '0.01', 'base_min_size': '0.00022'}, {'id': 'FET-USDT', 'quote_increment': '0.0001', 'base_min_size': '1.1'}, {'id': 'AMP-USD', 'quote_increment': '0.00001', 'base_min_size': '17'}, {'id': 'RLC-USD', 'quote_increment': '0.01', 'base_min_size': '0.22'}, {'id': 'DDX-USDT', 'quote_increment': '0.01', 'base_min_size': '0.17'}, {'id': 'PERP-USD', 'quote_increment': '0.01', 'base_min_size': '0.06'}, {'id': 'ZRX-USD', 'quote_increment': '0.000001', 'base_min_size': '0.82'}, {'id': 'COMP-USD', 'quote_increment': '0.01', 'base_min_size': '0.002'}, {'id': 'NKN-USD', 'quote_increment': '0.0001', 'base_min_size': '1.7'}, {'id': 'ORN-USD', 'quote_increment': '0.01', 'base_min_size': '0.12'}, {'id': 'WCFG-USDT', 'quote_increment': '0.01', 'base_min_size': '0.57'}, {'id': 'TRU-USD', 'quote_increment': '0.0001', 'base_min_size': '1.7'}, {'id': 'GYEN-USD', 'quote_increment': '0.000001', 'base_min_size': '47'}, {'id': 'AAVE-USD', 'quote_increment': '0.01', 'base_min_size': '0.003'}, {'id': 'NMR-USD', 'quote_increment': '0.01', 'base_min_size': '0.023'}, {'id': 'WLUNA-USDT', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'BTRST-USDT', 'quote_increment': '0.01', 'base_min_size': '0.17'}, {'id': 'USDC-EUR', 'quote_increment': '0.001', 'base_min_size': '0.97'}, {'id': 'SUPER-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'SUKU-USDT', 'quote_increment': '0.0001', 'base_min_size': '0.9'}, {'id': 'VGX-USD', 'quote_increment': '0.01', 'base_min_size': '0.23'}, {'id': 'OMG-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'REP-USD', 'quote_increment': '0.01', 'base_min_size': '0.04'}, {'id': 'LINK-USD', 'quote_increment': '0.01', 'base_min_size': '0.03'}, {'id': 'IMX-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'RAD-USDT', 'quote_increment': '0.01', 'base_min_size': '0.08'}, {'id': 'MASK-USDT', 'quote_increment': '0.01', 'base_min_size': '0.07'}, {'id': 'YFII-USD', 'quote_increment': '0.01', 'base_min_size': '0.00025'}, {'id': 'ETH-USDC', 'quote_increment': '0.01', 'base_min_size': '0.00022'}, {'id': 'SUKU-USD', 'quote_increment': '0.0001', 'base_min_size': '0.9'}, {'id': 'DOT-USDT', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'TRAC-USDT', 'quote_increment': '0.0001', 'base_min_size': '0.5'}, {'id': 'XTZ-USD', 'quote_increment': '0.01', 'base_min_size': '0.16'}, {'id': 'CLV-USD', 'quote_increment': '0.01', 'base_min_size': '0.78'}, {'id': 'FIL-USD', 'quote_increment': '0.01', 'base_min_size': '0.016'}, {'id': 'DAI-USD', 'quote_increment': '0.000001', 'base_min_size': '0.99'}, {'id': 'BADGER-USDT', 'quote_increment': '0.01', 'base_min_size': '0.032'}, {'id': 'SNX-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'MUSD-USD', 'quote_increment': '0.001', 'base_min_size': '0.99'}, {'id': 'BAL-USD', 'quote_increment': '0.01', 'base_min_size': '0.04'}, {'id': 'ADA-USDC', 'quote_increment': '0.001', 'base_min_size': '0.5'}, {'id': 'IDEX-USDT', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'API3-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'STORJ-USD', 'quote_increment': '0.01', 'base_min_size': '0.57'}, {'id': 'DOGE-USD', 'quote_increment': '0.0001', 'base_min_size': '3.8'}, {'id': 'SKL-USD', 'quote_increment': '0.0001', 'base_min_size': '2.7'}, {'id': 'ANKR-USD', 'quote_increment': '0.00001', 'base_min_size': '7'}, {'id': 'MLN-USD', 'quote_increment': '0.01', 'base_min_size': '0.007'}, {'id': 'PRO-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'KRL-USDT', 'quote_increment': '0.0001', 'base_min_size': '0.3'}, {'id': 'BAT-USDC', 'quote_increment': '0.000001', 'base_min_size': '1'}, {'id': 'LCX-USDT', 'quote_increment': '0.0001', 'base_min_size': '2.8'}, {'id': 'ZEC-USDC', 'quote_increment': '0.01', 'base_min_size': '0.0056'}, {'id': 'BLZ-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'ATOM-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'RAI-USD', 'quote_increment': '0.01', 'base_min_size': '0.32'}, {'id': 'FOX-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'LCX-USD', 'quote_increment': '0.0001', 'base_min_size': '2.8'}, {'id': 'GTC-USD', 'quote_increment': '0.01', 'base_min_size': '0.11'}, {'id': 'CVC-USD', 'quote_increment': '0.0001', 'base_min_size': '1.8'}, {'id': 'NU-USD', 'quote_increment': '0.0001', 'base_min_size': '1.1'}, {'id': 'UMA-USD', 'quote_increment': '0.01', 'base_min_size': '0.064'}, {'id': 'USDC-GBP', 'quote_increment': '0.001', 'base_min_size': '0.98'}, {'id': 'YFI-USD', 'quote_increment': '0.01', 'base_min_size': '0.000029'}, {'id': 'ARPA-USD', 'quote_increment': '0.0001', 'base_min_size': '5.3'}, {'id': 'LOOM-USD', 'quote_increment': '0.0001', 'base_min_size': '0.7'}, {'id': 'MDT-USDT', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'JASMY-USD', 'quote_increment': '0.00001', 'base_min_size': '5'}, {'id': 'BCH-USD', 'quote_increment': '0.01', 'base_min_size': '0.0016'}, {'id': 'GALA-USDT', 'quote_increment': '0.00001', 'base_min_size': '3'}, {'id': 'SHIB-USD', 'quote_increment': '0.0000001', 'base_min_size': '18000'}, {'id': 'MCO2-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'NCT-USD', 'quote_increment': '0.00001', 'base_min_size': '10'}, {'id': 'BADGER-USD', 'quote_increment': '0.01', 'base_min_size': '0.032'}, {'id': 'MKR-USD', 'quote_increment': '0.01', 'base_min_size': '0.00033'}, {'id': 'CRV-USD', 'quote_increment': '0.01', 'base_min_size': '0.23'}, {'id': 'POLY-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'UNI-USD', 'quote_increment': '0.01', 'base_min_size': '0.041'}, {'id': 'CRO-USDT', 'quote_increment': '0.0001', 'base_min_size': '2.3'}, {'id': 'REQ-USDT', 'quote_increment': '0.00001', 'base_min_size': '4'}, {'id': 'CTSI-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}, {'id': 'FORTH-USD', 'quote_increment': '0.01', 'base_min_size': '0.063'}, {'id': 'AUCTION-USD', 'quote_increment': '0.01', 'base_min_size': '0.027'}, {'id': 'XYO-USD', 'quote_increment': '0.000001', 'base_min_size': '17'}, {'id': 'ETH-USDT', 'quote_increment': '0.01', 'base_min_size': '0.00022'}, {'id': 'DOT-USD', 'quote_increment': '0.01', 'base_min_size': '0.021'}, {'id': 'LQTY-USD', 'quote_increment': '0.01', 'base_min_size': '0.1'}, {'id': 'SHIB-USDT', 'quote_increment': '0.0000001', 'base_min_size': '18000'}, {'id': 'CHZ-USD', 'quote_increment': '0.0001', 'base_min_size': '2'}, {'id': 'AXS-USDT', 'quote_increment': '0.01', 'base_min_size': '0.007'}, {'id': 'XLM-USD', 'quote_increment': '0.000001', 'base_min_size': '2'}, {'id': 'XYO-USDT', 'quote_increment': '0.000001', 'base_min_size': '17'}, {'id': 'XRP-USD', 'quote_increment': '0.0001', 'base_min_size': '1'}]
    return coinList

def getPopupMessage():
    message = "Dont be like Dan.......\nTry Again (Make sure what you executed actually Failed)"
    return message

# Used for Pump Detector
def generateProductList2():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""
    myList = []
    counter=0
    for x in range(0, len(products)):
        id = str(products[x]['id'])
        if id.__contains__("USD"):
            obj = {'id': products[x][id]}
            myList.insert(counter, obj)

    productList = str(productList).split(",")

    return myList

# Used for Pump Detector
def generateProductList():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""

    for x in range(0, len(products)):
        id = str(products[x]['id'])
        if id.__contains__("USD"):
            productList += id + ","

    productList = str(productList).split(",")

    return productList


# Used for Pump Detector
def generateProductListForMonthly():
    public_client = cbpro.PublicClient()
    products = public_client.get_products()
    productList = ""
    throwAway = ""
    for x in range(0, len(products)):
        id = str(products[x]['id'])

        if id.__contains__("USDT") or id.__contains__("USDC"):
            throwAway += id + ","

        else:
            if id.__contains__("USD"):
                productList += id + ","

    productList = str(productList).split(",")

    return productList



# Updated for GUI 12/11/2021 -> Core Component for GUI
# coinData returns -> [{id, quote_increment, base_min_size, base_max_size}]
def generateProductList2():
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
        baseminsize = str("0")
        basemaxsize = str("0")
        #basemaxsize = str(products[x]['base_max_size'])
        combined = id, ",", quote, ",", baseminsize

        if id.__contains__("USD"):
            myObj = {
                'id' : id,
                'quote_increment' : quote,
                'base_min_size' : baseminsize,
                'base_max_size' : basemaxsize
            }
            #print("Count: ", proudctsCount, myObj)
            productsObj.insert(proudctsCount, myObj)
            proudctsCount += 1

    return productsObj



# Base Max Size to Display on GUI
def getBaseMaxSize(coin, coinData):
    basemaxsize = "0"

    for x in range(len(coinData)):
        if coinData[x]['id'] == coin:
            basemaxsize = coinData[x]['base_max_size']

    return basemaxsize





# Updated for GUI 12/11/2021 -> Returns Sorted Product List for Trading Pair
def sortedProductList(productsObj):

    sortedList = []
    for x in range(0, len(productsObj)):
        coin = productsObj[x]['id']
        sortedList.insert(x, coin)
    # Sort The List
    sortedList.sort()

    return sortedList


# Trade Type List for GUI
def generateTradeType():
    typeList = []
    typeList.insert(0, "Buy")
    typeList.insert(1, "Sell")
    return typeList



# Updated for GUI 12/11/2021
def getSpecificQuoteIncrement2(coin, coinData):
    quoteIncrement = 0
    for x in range(0, len(coinData)):

        if coin == coinData[x]['id']:
            quoteIncrement = coinData[x]['quote_increment']
            #print(coinData[x], " -> ", quoteIncrement)
    return quoteIncrement

# Updated for GUI 12/11/2021
def getSpecificBaseMinSize2(coin, coinData):
    baseMinSize = 0
    for x in range(0, len(coinData)):

        if coin == coinData[x]['id']:
            baseMinSize = coinData[x]['base_min_size']
            #print(coinData[x], " -> ", baseMinSize)
    return baseMinSize

# Generate Order Prices using Lower-Upper prices
def generatePrices(coin, lowerPrice, uppperPrice, quoteIncrement, maxOrders):

    priceDiff = uppperPrice - lowerPrice

    convertQuoteIncrement = calculateQuoteIncrementals(quoteIncrement)

    incrementalPrice = round(priceDiff/maxOrders, convertQuoteIncrement)
    #print("Incrementing price by: ", incrementalPrice)
    priceList = []

    for x in range(0, maxOrders):
        price = 0
        if x == 0:
            price = round(lowerPrice + incrementalPrice, convertQuoteIncrement)
            #print("Order # ",x, ": ", price)
        else:
            price = round(priceList[x-1] + incrementalPrice, convertQuoteIncrement)
            #print("Order # ", x, ": ", price)
        priceList.insert(x, price)

    return priceList


def generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders):
    print("Base Min Size: ", baseMinSize)
    convertBaseMinSize = calculateBaseMinSizeIncrementals(baseMinSize)
    sizePerOrder = round(maxCoins / maxOrders, convertBaseMinSize)

    # Fixed Round Issue
    if sizePerOrder == 0:
        sizePerOrder = round(maxCoins / maxOrders, 3)

    print("Convert base min size: ", convertBaseMinSize, " Size Per Order: ", sizePerOrder)

    return sizePerOrder



def generateOrderSizesTest(coin, baseMinSize, maxCoins, maxOrders, tradeSetting):
    print("Generate Order Size Test: ", tradeSetting)
    convertBaseMinSize = calculateBaseMinSizeIncrementals(baseMinSize)

    divisor = maxCoins/maxOrders
    bottom=0
    top=0
    leftoverOrders = maxOrders-1
    incremental = 0

    sizePerOrderArr = []

    if tradeSetting == 'bottom':
        bottom = divisor/2
        top = bottom+divisor
        incremental = divisor/leftoverOrders
        calcSize = 0
        print("Bottom: ", bottom, " || Top: ", top, " || Incremental: ", incremental)

        for x in range(0, maxOrders):
            if x == 0:
                calcSize = round(bottom, convertBaseMinSize)
                sizePerOrderArr.insert(x, bottom)
                print("Order [", x, "] - Size: ", bottom)
            else:
                calcSize = round(sizePerOrderArr[x-1] + incremental, convertBaseMinSize)
                sizePerOrderArr.insert(x, calcSize)
                print("Order [", x, "] - Size: ", calcSize)


    if tradeSetting == 'top':
        bottom = divisor/2
        top = bottom+divisor
        incremental = divisor / leftoverOrders
        print("Bottom: ", bottom, " || Top: ", top, " || Incremental: ", incremental)

        for x in range(0, maxOrders):
            if x == 0:
                calcSize = round(top, convertBaseMinSize)
                sizePerOrderArr.insert(x, calcSize)
                print("Order [", x, "] - Size: ", top)
            else:
                calcSize = round(sizePerOrderArr[x - 1] - incremental, convertBaseMinSize)
                sizePerOrderArr.insert(x, calcSize)
                print("Order [", x, "] - Size: ", calcSize)

    return sizePerOrderArr




maxCoins = 500
maxOrders = 20
tradeSetting = 'top'
#generateOrderSizesTest('none', 'none', maxCoins, maxOrders, tradeSetting)


def calculateBaseMinSizeIncrementals(baseMinSize):
    count = 0
    size = 0

    for x in baseMinSize:
        if x == "1":
            size = count - 1
        count += 1

    #print("BaseMin Incremental Size: ", size)
    return size


def calculateQuoteIncrementals(quoteIncrement):
    count = 0
    size = 0
    for x in quoteIncrement:
        if x == "1":
            size = count-1
        count += 1

    #print("Incremental Size: ", size)
    return size


def displayOrderDataBeforePlacing(coin, tradeType, priceList, orderSize):
    convertTrade = ""
    if tradeType == "s":
        convertTrade = "Sell"
    if tradeType == "b":
        convertTrade = "Buy"

    print("Displaying Orders for ", coin)
    for x in range(0, len(priceList)):
        print("Order # [", x+1, "] Coin: ", coin, " Type: ", convertTrade, " Price: ", priceList[x], " Qty: ", orderSize)


def displayOrderDataBeforePlacingGUI(coin, tradeType, priceList, orderSize):
    previewList = []
    print("Displaying Orders for ", coin)
    for x in range(0, len(priceList)):
        text = "Order # [", x+1, "] Coin: ", coin, " Type: ", tradeType, " Price: ", priceList[x], " Qty: ", orderSize
        previewList.insert(x, text)
        print("Order # [", x+1, "] Coin: ", coin, " Type: ", tradeType, " Price: ", priceList[x], " Qty: ", orderSize)
    return previewList

def displayOrderDataBeforePlacingGUITEST(coin, tradeType, priceList, orderSize):
    previewList = []
    print("Displaying Orders for ", coin)
    for x in range(0, len(priceList)):
        text = "Order # [", x+1, "] Coin: ", coin, " Type: ", tradeType, " Price: ", priceList[x], " Qty: ", orderSize[x]
        previewList.insert(x, text)
        print("Order # [", x+1, "] Coin: ", coin, " Type: ", tradeType, " Price: ", priceList[x], " Qty: ", orderSize[x])
    return previewList



# Not Needed
def generateListofCoins():
    myCoinList = getCoinList()

    sortedList = []
    for x in range(0, len(myCoinList)):
        coin = myCoinList[x]['id']
        sortedList.insert(x, coin)
    # Sort The List
    sortedList.sort()

    return sortedList

# Not Needed
def generateListofCoins2():

    myCoinList = getCoinList()
    sortedList = []
    for x in range(0, len(myCoinList)):
        coin = myCoinList[x]['id']
        sortedList.insert(x, coin)
    # Sort The List
    sortedList.sort()

    return sortedList

# Not Needed
def getSpecificQuoteIncrement(pair):
    myCoinList = getCoinList()
    quoteIncrement = 0
    for x in range(0, len(myCoinList)):

        if pair == myCoinList[x]['id']:
            quoteIncrement = myCoinList[x]['quote_increment']

    return quoteIncrement
# Not Needed
def getSpecificBaseMinSize(pair):
    myCoinList = getCoinList()
    baseMinSize = 0
    for x in range(0, len(myCoinList)):

        if pair == myCoinList[x]['id']:
            baseMinSize = myCoinList[x]['base_min_size']

    return baseMinSize







def generatePercentForTrade(coin, tradeType, percent):

    balances = checkBalances(coin)
    print(balances[0])
    print(balances[1])

    splitCoin = str(coin).split("-")

    newAmt = 0
    # Buys = Get USD Balance
    if tradeType == 'Buy':
        available = balances[1]['available']
        print(available)
        print("Type: ", tradeType, " Max Balance: ", available, " ", coin)

        price = values['-UpperPrice-']
        maxValue = (percent * float(available)) / float(price)
        print(maxValue)
        window.Element('-QTY-').Update(maxValue)

    # Sells = Get Coin Balance
    if tradeType == 'Sell':
        available = balances[0]['available']
        print(available)
        print("Type: ", tradeType, " Max Balance: ", available, " ", coin)
        newAmt = float(available) * percent
        window.Element('-QTY-').Update(newAmt)

    return newAmt


# tradeType = "b"
# order_type = "limit"
# coin = "ETH-USD"
# lowerPrice = 1275
# upperPrice = 1295
# maxCoins = 15
# maxOrders = 7
# quoteIncrement = getSpecificQuoteIncrement(coin)
# baseMinSize = getSpecificBaseMinSize(coin)
#
# priceList = generatePrices(coin, lowerPrice, upperPrice, quoteIncrement, maxOrders)
# orderSize = generateOrderSizes(coin, baseMinSize, maxCoins, maxOrders)
#
# print("Coin:", coin, "Trade Type [", tradeType, "] Price Range: ", lowerPrice, " - ", upperPrice, " Max Coins: ", maxCoins, " Max Orders: ", maxOrders)
# print("Average Order Size: ", orderSize)
#
# displayOrderDataBeforePlacing(coin, tradeType, priceList, orderSize)
# tradeConfirmation = input("Execute Trade? (0 = YES, 1 = NO)")
#
# if tradeConfirmation == "0":
#     placeMultipleOrders(coin, maxOrders, tradeType, order_type, orderSize, priceList)
# else:
#     print("Trade Confirmation: NO - Exitting Process")

#{'id': 'SUPER-USD', 'base_currency': 'SUPER', 'quote_currency': 'USD', 'base_min_size': '0.1', 'base_max_size': '170000', 'quote_increment': '0.01', 'base_increment': '0.01', 'display_name': 'SUPER/USD', 'min_market_funds': '1', 'max_market_funds': '100000', 'margin_enabled': False, 'fx_stablecoin': False, 'max_slippage_percentage': '0.03000000', 'post_only': False, 'limit_only': False, 'cancel_only': True, 'trading_disabled': False, 'status': 'online', 'status_message': 'We are now accepting deposits. Trading will begin shortly.', 'auction_mode': False}
