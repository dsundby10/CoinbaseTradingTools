

# Variables
# Trading GUI THEME
tradingGUITheme = "Dark"
allAvergaesGUITheme = "Dark"

# Average Layout Window Sizes (To be Used to Trading GUI)
avgLayoutWindow_Width = 325
avgLayoutWindow_Height = 200
avgLayoutWindow_TextWidth = 30
avgLayoutWindow_TextHeight = 6

# Balance Layout Window Sizes (To be Used to Trading GUI)
balanceLayoutWindow_Width = 325
balanceLayoutWindow_Height = 200
balanceLayoutWindow_TextWidth = 30
balanceLayoutWindow_TextHeight = 6

# **ALL Averages** Layout Window Sizes
allAvgsLayoutWindow_Width = 600
allAvgsLayoutWindow_Height = 400
allAvgsWindow_TextWidth = 200
allAvgsWindow_TextHeight = 20


# Trading GUI Theme Setter
def getGUITheme():
    return tradingGUITheme

def getAllAveragesGUITheme():
    return allAvergaesGUITheme


# [Getters] -> Average Layout Window Sizes (To be Used to Trading GUI)
def getAvgPositionTracker_TextSize():
    return avgLayoutWindow_TextWidth, avgLayoutWindow_TextHeight

def getAvgPositionTracker_WindowSize():
    return  avgLayoutWindow_Width,avgLayoutWindow_Height

# [Getters] ->  Balance Layout Window Sizes
def getBalancePositionTracker_TextSize():
    return balanceLayoutWindow_TextWidth, balanceLayoutWindow_TextHeight

def getBalancePositionTracker_WindowSize():
    return  balanceLayoutWindow_Width, balanceLayoutWindow_Height

# [Getters] -> **All Averages** Layout Window Sizes
def getAllAvgPositionsTrackerTextSize():
    return allAvgsWindow_TextWidth, allAvgsWindow_TextHeight

def getAllAvgPositionsTrackerWindowSize():
    return allAvgsLayoutWindow_Width, allAvgsLayoutWindow_Height

def getKeys():
    return ""