from itertools import product
import random

filename = "input.txt"

poolSize = 20

legalValues = []
parameterPositions = []
parameterValues = []
parameterNames = []
allPairsDisplay = []
unusedPairs = []
unusedPairsSearch = []

# read file and populate into list
with open(filename, "r") as rfile:
    for linenum, line in enumerate(rfile):
        parameterName, values = line.split(":")
        values = values.split(",")
        parameterName = parameterName.strip()
        values = map(lambda x: x.strip(),values)
        legal = []
        for value in values:
            num = len(parameterValues)
            parameterValues.append(value)
            legal.append(num)
            parameterPositions.append(linenum)
        parameterNames.append(parameterName)
        legalValues.append(legal)

# generate all all pairs
for listnum, list1 in enumerate(legalValues):
    for list2num in range(listnum+1, len(legalValues)):
        list2 = legalValues[list2num]
        for x,y in product(list1, list2):
            allPairsDisplay.append((x,y))

allPairsDisplay.sort()
unusedPairs = allPairsDisplay

parameterValuesNum = len(parameterValues)
parameterNum = len(parameterNames)

# generate unused pair search

unusedCounts = [0 for i in range(parameterValuesNum)]
for i in range(parameterValuesNum):
    l = []
    for j in range(parameterValuesNum):
        if parameterPositions[i] < parameterPositions[j]:
            l.append(1)
            unusedCounts[i] += 1
            unusedCounts[j] += 1
        else:
            l.append(0)

    unusedPairsSearch.append(l)

# generate test sets

testSets = []

while len(unusedPairs) > 0:
    canidateSets = []
    for canidate in range(poolSize):

        testSet = [0] * parameterNum
        
        # find best pair
        bestWeight = 0;
        bestPair = (0,0);
        for pair in unusedPairs:
            x, y = pair
            weight = unusedCounts[x] + unusedCounts[y]
            if weight > bestWeight or weight == bestWeight and random.randint(0,1):
                bestWeight = weight
                bestPair = pair

        # group of best pair
        x, y = bestPair
        firstPos = parameterPositions[x]
        secondPos = parameterPositions[y]

        ordering = [i for i in range(parameterNum)]
        ordering.remove(firstPos)
        ordering.remove(secondPos)
        random.shuffle(ordering)

        testSet[firstPos] = x
        testSet[secondPos] = y

        ordering = [firstPos, secondPos] + ordering

        for i, currPos in enumerate(ordering):
            if i < 2:
                continue
            possiblieValues = legalValues[currPos]
            currentCount = 0
            highestCount = 0
            bestJ = 0
            for j in range(len(possiblieValues)):
                currentCount = 0
                for p in range(i):
                    candidatePair = [possiblieValues[j], testSet[ordering[p]]]
                    if unusedPairsSearch[candidatePair[0]][candidatePair[1]] or unusedPairsSearch[candidatePair[1]][candidatePair[0]]:
                        currentCount += 1
                if currentCount > highestCount or currentCount == highestCount and random.randint(0,1):
                    highestCount = currentCount
                    bestJ = j
            testSet[currPos] = possiblieValues[bestJ]
        canidateSets.append(testSet)

    # find best test among canidate
    mostPairsCaptured = -1
    mostPairsCapturedTest = []
    for canidateSet in canidateSets:
        # calculate pairs captured bt test
        pairsCaptured = 0
        for i in range(len(canidateSet)-1):
            for j in range(i+1,len(canidateSet)):
                if unusedPairsSearch[i][j]:
                    pairsCaptured += 1

        if pairsCaptured > mostPairsCaptured or pairsCaptured == mostPairsCaptured and random.randint(0,1):
            mostPairsCaptured = pairsCaptured
            mostPairsCapturedTest = canidateSet

    for i in mostPairsCapturedTest:
        unusedCounts[i] -= 1
        for j in mostPairsCapturedTest:
            try:
                unusedPairs.remove((i,j))
            except ValueError:
                pass
            unusedPairsSearch[i][j] = 0

    testSets.append(mostPairsCapturedTest)

# print result
print len(testSets), "tests"
for test in testSets:
    l = [parameterValues[x] for x in test]
    print l

