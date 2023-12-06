def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

def createTimeDistancePairs(lines: str) -> []:
    pairs = []
    time = lines[0].split(':')[1].split()
    distance = lines[1].split(':')[1].split()
    
    for iterator, t in enumerate(time):
        pair = [int(t), int(distance[iterator])]
        pairs.append(pair)
    
    return pairs

def getPossibleWays(pairs: []) -> []:
    result = []

    for time, distance in pairs:
        pair = []
        for hold in range(1, time):
            travelTime = time - hold
            travelDistance = travelTime * hold

            if travelDistance > distance:
                pair.append([travelTime, travelDistance])
        
        result.append(pair)

    return result

def formLargeRace(pairs: []) -> []:
    sumTime = ''
    sumDistance = ''
    for time, distance in pairs:
        sumTime += str(time)
        sumDistance += str(distance)

    return [[int(sumTime), int(sumDistance)]]

#Long race is part 2 
def multiplyWays(lines: str, longRace: bool = True) -> int:
    result = 1

    pairs = createTimeDistancePairs(lines)
    if longRace:
        pairs = formLargeRace(pairs)

    possibleWays = getPossibleWays(pairs)

    for ways in possibleWays:
        result *= len(ways)

    return result

testData = [
    'Time:      7  15   30',
    'Distance:  9  40  200'
]

def main():
    lines = readLines()
    #print(multiplyWays(testData))
    print(multiplyWays(lines))

main()