from collections import deque

def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

EMPTY = '.'
LEFT_MIRROR = '/'
RIGHT_MIRROR = '\\'
SPLITER_HORIZONTAL = '-'
SPLITER_VERTICAL = '|'
ENERGIZED = '#'

lines = []
energizedlines = []

def processBeam(entryX: int = 0, entryY: int = 0, directionX: int = 1, directionY: int = 0) -> int:
    global lines, energizedlines

    energizedlines[entryY][entryX] = ENERGIZED
    nextEntryX = entryX + directionX
    nextEntryY = entryY + directionY

    if (nextEntryX >= len(lines[0]) or nextEntryX < 0) or (nextEntryY >= len(lines) or nextEntryY < 0):
        return 0

    nextBlock = lines[nextEntryY][nextEntryX]

    if energizedlines[nextEntryY][nextEntryX] == ENERGIZED and not (nextBlock == LEFT_MIRROR or nextBlock == RIGHT_MIRROR or nextBlock == EMPTY):
        return 0

    if nextBlock == EMPTY or (nextBlock == SPLITER_HORIZONTAL and (directionX == 1 or directionX == -1)) or (nextBlock == SPLITER_VERTICAL and (directionY == 1 or directionY == -1)):
        return 1 + processBeam(nextEntryX, nextEntryY, directionX, directionY)
    elif (nextBlock == LEFT_MIRROR and directionX == 1) or (nextBlock == RIGHT_MIRROR and directionX == -1):
        return 1 + processBeam(nextEntryX, nextEntryY, 0, -1) #Up
    elif (nextBlock == LEFT_MIRROR and directionY == -1) or (nextBlock == RIGHT_MIRROR and directionY == 1):
        return 1 + processBeam(nextEntryX, nextEntryY, 1, 0) #Right
    elif (nextBlock == LEFT_MIRROR and directionX == -1) or (nextBlock == RIGHT_MIRROR and directionX == 1):
        return 1 + processBeam(nextEntryX, nextEntryY, 0, 1) #Down
    elif (nextBlock == LEFT_MIRROR and directionY == 1) or (nextBlock == RIGHT_MIRROR and directionY == -1):
        return 1 + processBeam(nextEntryX, nextEntryY, -1, 0) #Left
    elif nextBlock == SPLITER_HORIZONTAL and (directionY == 1 or directionY == -1):
        return 1 + processBeam(nextEntryX, nextEntryY, -1, 0) + processBeam(nextEntryX, nextEntryY, 1, 0) 
    elif nextBlock == SPLITER_VERTICAL and (directionX == 1 or directionX == -1):
        return 1 + processBeam(nextEntryX, nextEntryY, 0, -1) + processBeam(nextEntryX, nextEntryY, 0, 1) 
    
def calculateEnergized(fileLines: str) -> int:
    global lines, energizedlines

    lines = fileLines
    for line in lines:
        energizedlines.append(list(line))

    executions = processBeam()
    result = 0
    for line in energizedlines:
        print(line)
        for element in line:
            if element == ENERGIZED:
                result += 1
    
    return result
    
def processBeamIterative(lines: str, startX: int = -1, startY: int = 0, directionX: int = 1, directionY: int = 0) -> int:
    firstValue = [(startX, startY, directionX, directionY)]
    seen = set()
    queue = deque(firstValue)

    def addIfNotSeen(element: tuple):
        if element not in seen:
            seen.add(element)
            queue.append(element)

    while queue:
        x, y, currentDirectionX, currentDirectionY = queue.popleft()
        
        x += currentDirectionX
        y += currentDirectionY

        if x < 0 or x >= len(lines[0]) or y < 0 or y >= len(lines):
            continue

        currentBlock = lines[y][x]

        if currentBlock == EMPTY or (currentBlock == SPLITER_HORIZONTAL and currentDirectionX != 0) or (currentBlock == SPLITER_VERTICAL and currentDirectionY != 0):
            element = (x, y, currentDirectionX, currentDirectionY)
            addIfNotSeen(element)
        elif currentBlock == LEFT_MIRROR:
            currentDirectionX, currentDirectionY = -currentDirectionY, -currentDirectionX
            element = (x, y, currentDirectionX, currentDirectionY)
            addIfNotSeen(element)
        elif currentBlock == RIGHT_MIRROR:
            currentDirectionX, currentDirectionY = currentDirectionY, currentDirectionX
            element = (x, y, currentDirectionX, currentDirectionY)
            addIfNotSeen(element)
        else:
            for currentDirectionY, currentDirectionX in [(1, 0), (-1, 0)] if currentBlock == SPLITER_VERTICAL else [(0, 1), (0, -1)]:
                element = (x, y, currentDirectionX, currentDirectionY)
                addIfNotSeen(element)

    coordinates = {(x, y) for (x, y, _, _) in seen}

    return len(coordinates) 

def calculateEnergizedIterative(lines: str) -> int:
    return processBeamIterative(lines)

def calculateMaxEnergizedIterative(lines: str) -> int:
    maxValue = 0

    for x in range(len(lines[0])):
        maxValue = max(maxValue, processBeamIterative(lines, x, -1, 0, 1))
        maxValue = max(maxValue, processBeamIterative(lines, x, len(lines), 0, -1))


    for y in range(len(lines)):
        maxValue = max(maxValue, processBeamIterative(lines, -1, y, 1, 0))
        maxValue = max(maxValue, processBeamIterative(lines, len(lines[0]), y, 0, -1))

    return(maxValue)


testArray = [
    '.|...\....',
    '|.-.\.....',
    '.....|-...',
    '........|.',
    '..........',
    '.........\\',
    '..../.\\\\..',
    '.-.-/..|..',
    '.|....-|.\\',
    '..//.|....'
]

def main():
    fileLines = readLines()
    #print(calculateEnergized(testArray))
    print(processBeamIterative(fileLines))
    print(calculateMaxEnergizedIterative(fileLines))
    

main()
