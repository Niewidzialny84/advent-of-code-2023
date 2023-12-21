from collections import deque

def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()
    
START = 'S'
GARDEN = '.'
ROCK = '#'
STEP = 'O'

def parseLines(lines: list[str]) -> list[list[str]]:
    result = []

    for line in lines:
        newLine = []
        for character in line:
            newLine.append(character)
        
        result.append(newLine)
    
    return result

def findStart(plot: list[list[str]]) -> tuple[int, int]:
    for y, line in enumerate(plot):
        for x, character in enumerate(line):
            if character == START:
                return y, x

    return -1, -1    

def processStep(plot: list[list[str]]) -> list[list[str]]:
    copy = []
    for line in plot:
        newLine = []
        for character in line:
            if character == STEP:
                newLine.append(GARDEN)
            else:
                newLine.append(character)
        copy.append(newLine)
    
    for y, line in enumerate(plot):
        for x, character in enumerate(line):
            if character != STEP:
                continue
            
            for i, j in [(0, 1), (0, -1), (1, 0), (-1 ,0)]:
                if y + i < 0 or y + i >= len(plot) or x + j < 0 or x + j >= len(plot[0]):
                    continue

                if plot[y + i][x + j] != GARDEN:
                    continue

                copy[y + i][x + j] = STEP
    
    return copy

def processSteps(plot: list[list[str]], steps: int) -> list[list[str]]:
    y, x = findStart(plot)
    plot[y][x] = STEP
    
    for _ in range(steps):
        plot = processStep(plot)

    return plot

def fill(plot: list[list[str]], startY: int, startX: int, size: int) -> int:
    result = set()
    seen = {(startY, startX)}
    queue = deque([(startY, startX, size)])

    while queue:
        y, x, s = queue.popleft()

        if s % 2 == 0:
            result.add((y, x))

        if s == 0:
            continue

        for newY, newX in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
            if newY < 0 or newY >= len(plot) or newX < 0 or newX >= len(plot) or plot[newY][newX] == ROCK or (newY, newX) in seen:
                continue
            seen.add((newY, newX))
            queue.append((newY, newX, s - 1))
        
    return len(result)

def countInfinitePlot(lines: list[str], steps: int = 26501365) -> int:
    plot = parseLines(lines)
    
    startY, startX = findStart(plot)

    size = len(plot)
    
    plotWidth = steps // size - 1 

    odd = (plotWidth // 2 * 2 + 1) ** 2
    even = ((plotWidth + 1) // 2 * 2) ** 2

    oddPoints = fill(plot, startY, startX, size * 2 + 1)
    evenPoints = fill(plot, startY, startX, size * 2)

    cornerTop = fill(plot, size - 1, startX, size - 1)
    cornerRight = fill(plot, startY, 0, size - 1)
    cornerBottom = fill(plot, 0, startX, size - 1)
    cornerLeft = fill(plot, startY, size - 1, size - 1)

    smallTopRight = fill(plot, size - 1, 0, size // 2 - 1)
    smallTopLeft = fill(plot, size - 1, size - 1, size // 2 - 1)
    smallBottomRight = fill(plot, 0, 0, size // 2 - 1)
    smallBottomLeft = fill(plot, 0, size - 1, size // 2 - 1)

    largeTopRight = fill(plot, size - 1, 0, size * 3 // 2 - 1)
    largeTopLeft = fill(plot, size - 1, size - 1, size * 3 // 2 - 1)
    largeBottomRight = fill(plot, 0, 0, size * 3 // 2 - 1)
    largeBottomLeft = fill(plot, 0, size - 1, size * 3 // 2 - 1)

    result = odd * oddPoints
    result += even * evenPoints
    result += cornerTop + cornerRight + cornerBottom + cornerLeft
    result += (plotWidth + 1) * (smallTopRight + smallTopLeft + smallBottomRight + smallBottomLeft)
    result += plotWidth * (largeTopRight + largeTopLeft + largeBottomRight + largeBottomLeft)
    
    return result

def countReachablePlotsInSteps(lines: list[str], steps: int = 6, infinite: bool = True) -> int:
    plot = parseLines(lines)

    plot = processSteps(plot, steps)
    result = 0
    for line in plot:
        for character in line:
            if character == STEP:
                result += 1

    return result

testArray = [
    '...........',
    '.....###.#.',
    '.###.##..#.',
    '..#.#...#..',
    '....#.#....',
    '.##..S####.',
    '.##..#...#.',
    '.......##..',
    '.##.#.####.',
    '.##..##.##.',
    '...........'
]

def main():
    lines = read_file()
    print(countReachablePlotsInSteps(lines, 64))
    print(countInfinitePlot(lines))

main()