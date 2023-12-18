#Create function for reading file and splitting lines, returning lines, taking as parameter file defaulted to 'input.txt'
def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()

def parseInput(lines: list[str]) -> list[list[str]]:
    instructions = []

    for line in lines:
        split = line.split(' ')
        instructions.append([split[0], int(split[1]), split[2][2: -1]])

    return instructions

RIGHT = 'R'
LEFT = 'L'
DOWN = 'D'
UP = 'U'
EMPTY = '.'
FILLED = '#'

def findPossibleXMax(values: list[list[str]]) -> int:
    result = 0
    for direction, value, _ in values:
        if direction == RIGHT:
            result += value

    return result

def findPossibleYMax(values: list[list[str]]) -> int:
    result = 0
    for direction, value, _ in values:
        if direction == DOWN:
            result += value

    return result

def createEmptyField(x: int, y: int) -> list[list[str]]:
    result = []

    for _ in range(y):
        line = []
        for _ in range(x):
            line.append(EMPTY)
        result.append(line)
    
    return result

def createLoop(lines: str) -> list[list[str]]:
    parsedInput = parseInput(lines)
    xMax = findPossibleXMax(parsedInput) + 1
    yMax = findPossibleYMax(parsedInput) + 1
    field = createEmptyField(xMax, yMax)

    currentX = 0
    currentY = 0
    field[currentY][currentX] = FILLED

    for direction, value, color in parsedInput:

        if direction == RIGHT:
            for x in range(value):
                field[currentY][currentX + x] = FILLED
            currentX += value
            continue

        if direction == LEFT:
            for x in range(value):
                field[currentY][currentX - x] = FILLED
            currentX -= value
            continue
        
        if direction == DOWN:
            for y in range(value):
                field[currentY + y][currentX] = FILLED
            currentY += value
            continue

        if direction == UP:
            for y in range(value):
                field[currentY - y][currentX] = FILLED
            currentY -= value
            continue

    return field

def fillLoop(field: list[list[str]]) -> list[list[str]]:
    for y in range(len(field)):

        shouldFill = 0
        line = "".join([x for x in field[y]])
        first = line.find(FILLED)
        last = line.rfind(FILLED)
        for x in range(first, last):
            field[y][x] = FILLED
    
    return field

#Sadly only works on positive input, but normal one starts with left thus rendering this solution useless
#More of a meme solution
def caulculateFilledArea(lines: list[str]) -> int:
    loop = createLoop(lines)
    loop = fillLoop(loop)

    result = 0

    for line in loop:
        result += line.count(FILLED)

    return result

#Shoelace solution
def calculateFilledAreaShoelace(lines: list[str], colorIsDistance: bool = True) -> int:
    parsedInput = parseInput(lines)

    if colorIsDistance:
        parsedInput = convertColorToDistance(parsedInput)

    b = 0
    points = [(0, 0)]

    for direction, value, _ in parsedInput:

        if direction == UP:
            directionY, directionX = (-1, 0)
        elif direction == DOWN:
            directionY, directionX = (1, 0)
        elif direction == RIGHT:
            directionY, directionX = (0, 1)
        elif direction == LEFT:
            directionY, directionX = (0, -1)
        
        b += value

        y, x = points[-1]

        points.append((y + directionY * value, x + directionX * value))
    

    partialSum = 0

    for i in range(len(points)):
        partialSum += points[i][0] * (points[i - 1][1] - points[(i + 1) % len(points)][1])

    A = abs(partialSum) // 2

    inner = A - b // 2 + 1

    return (inner + b)

def convertColorToDistance(parsedInput: list[list[str]]) -> list[list[str]]:
    result = []

    for _, _, color in parsedInput:
        distance = int(color[:5], 16)
        direction = int(color[5:6])
        
        if direction == 0:
            direction = RIGHT
        elif direction == 1:
            direction = DOWN
        elif direction == 2:
            direction = LEFT
        elif direction == 3:
            direction = UP

        result.append([direction, distance, color])

    return result

testArray = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)'
]

def main():
    lines = read_file()
    print(calculateFilledAreaShoelace(lines, False))
    print(calculateFilledAreaShoelace(lines))
main()