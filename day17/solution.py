from heapq import heappush, heappop

#Create function for reading file and splitting lines, returning lines, taking as parameter file defaulted to 'input.txt'
def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()


def parseToList(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line)) for line in lines]


def findShortestLowestCostPath(grid: list[list[int]], maxContinousSteps: int, minimumSteps: int) -> int:
    seen = set()
    heapQueue = [(0, 0, 0, 0, 0, 0)]

    while heapQueue:
        heatLoss, y, x, directionY, directionX, continousSteps = heappop(heapQueue)
    
        if y == len(grid) - 1 and x == len(grid[0]) - 1 and continousSteps >= minimumSteps:
            return heatLoss

        if (y, x, directionY, directionX, continousSteps) in seen:
            continue

        seen.add((y, x, directionY, directionX, continousSteps))
        
        if continousSteps < maxContinousSteps and (directionY, directionX) != (0, 0):
            nextY = y + directionY
            nextX = x + directionX
            if 0 <= nextY < len(grid) and 0 <= nextX < len(grid[0]):
                heappush(heapQueue, (heatLoss + grid[nextY][nextX], nextY, nextX, directionY, directionX, continousSteps + 1))

        if continousSteps >= minimumSteps or (directionY, directionX) == (0, 0):
            for nextdirectionY, nextdirectionX in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if (nextdirectionY, nextdirectionX) != (directionY, directionX) and (nextdirectionY, nextdirectionX) != (-directionY, -directionX):
                    nextY = y + nextdirectionY
                    nextX = x + nextdirectionX
                    if 0 <= nextY < len(grid) and 0 <= nextX < len(grid[0]):
                        heappush(heapQueue, (heatLoss + grid[nextY][nextX], nextY, nextX, nextdirectionY, nextdirectionX, 1))

    return 0

def getShortestPathValue(grid: list[str], maxContinousSteps: int = 10, minimumSteps: int = 4) -> int:
    grid = parseToList(grid)
    return findShortestLowestCostPath(grid, maxContinousSteps, minimumSteps)

testArray = [
    '2413432311323',
    '3215453535623',
    '3255245654254',
    '3446585845452',
    '4546657867536',
    '1438598798454',
    '4457876987766',
    '3637877979653',
    '4654967986887',
    '4564679986453',
    '1224686865563',
    '2546548887735',
    '4322674655533'
]

def main():
    lines = read_file()
    print(getShortestPathValue(lines, 3, 0))
    print(getShortestPathValue(lines))

main()
