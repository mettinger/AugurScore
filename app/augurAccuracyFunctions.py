import numpy as np

with open('./node/finalizedPrices.txt','r') as fp:
    finalizedMarkets = eval(fp.read())
    
categoricalMarkets = [i for i in finalizedMarkets if i[0]['numOutcomes'] > 2]
binaryMarkets = [i for i in finalizedMarkets if i[0]['marketType'] == 'yesNo']

def gaussianKernel(x, y, sigma):
    return np.exp(-(x-y)**2/(2 * (sigma**2)))/(np.sqrt(2*np.pi) * sigma)

def uniformKernel(x, y, halfWidth):
    if abs(x - y) <= halfWidth:
        return 1.
    else:
        return 0.

def logScore(probVector, outcomeIndex):
    return np.log(probVector[outcomeIndex])

def brierScore(probVector, outcomeIndex):
    if outcomeIndex == 0:
        return (1 - probVector[0]**2) + (0 - probVector[1]**2)
    else:
        return (0 - probVector[0]**2) + (1 - probVector[1]**2)
    
def sphericalScore(probVector, outcomeIndex):
    return probVector[outcomeIndex]/np.norm(probVector)


def scoreMarketsBinary(admittedMarkets, 
                       secondsAhead, 
                       kernelFunction, 
                       kernelWidth, 
                       scoreFunction, 
                       minTrades = 1, 
                       minWeight = 0.):
    
    weightVector = np.array([0])
    scoreVector = np.array([0])
    for thisMarket in admittedMarkets:
        marketData = thisMarket[0]
        if len(list(thisMarket[1].keys())) < minTrades:
            continue
        else:
            pricedOutcome = list(thisMarket[1].keys())[0]
        priceData = thisMarket[1][pricedOutcome]
        marketId = marketData['id']
        endTime = marketData['endTime']
        consensusIndex = np.argmax(marketData['consensus']['payout'])
        centerTime = endTime - secondsAhead
        flipFlag = (int(pricedOutcome) != consensusIndex)
        for i,thisTrade in enumerate(priceData):
            
            # if the price of the designated outcome doesn't occur, flip the probability
            if not flipFlag:
                price = float(thisTrade['price'])
            else:
                price = 1. - float(thisTrade['price'])
                
            amount = float(thisTrade['amount'])
            tradeTime = thisTrade['timestamp']
            
            timeWeight = kernelFunction(centerTime, tradeTime, kernelWidth)
            weight = timeWeight * amount
            if weight >= minWeight:
                weightVector = np.append(weightVector, weight)
                if consensusIndex == 0:
                    scoreVector = np.append(scoreVector,[scoreFunction([price, 1-price], 0)],0)
                else:
                    scoreVector = np.append(scoreVector,[scoreFunction([1-price, price],1)],0)
            
    return np.average(scoreVector[1:],axis = 0,weights=weightVector[1:])

















