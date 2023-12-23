def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()

def parseLines(lines: list[str]) -> list[list[str]]:
    result = []

    for line in lines:
        newLine = []
        for character in line:
            newLine.append(character)
        
        result.append(newLine)
    
    return result

PATH = '.'
FOREST = '#'
UP_SLOPE = '^'
DOWN_SLOPE = 'v'
RIGHT_SLOPE = '>'
LEFT_SLOPE = '<'
SLOPES = [UP_SLOPE, DOWN_SLOPE, RIGHT_SLOPE, LEFT_SLOPE]
DIRECTIONS = {
    UP_SLOPE: [(-1, 0)], 
    DOWN_SLOPE: [(1, 0)], 
    RIGHT_SLOPE: [(0, 1)], 
    LEFT_SLOPE: [(0, -1)],
    PATH: [(-1, 0), (1, 0), (0, -1), (0, 1)]
}


def getStartAndEnd(plot: list[list[str]]) -> tuple[tuple[int, int], tuple[int,int]]:
    start = (0, plot[0].index(PATH))
    end = (len(plot) - 1, plot[-1].index(PATH))
    
    return start, end

def findNeighbourPoints(plot: list[list[str]]) -> list[tuple[int, int]]:
    start, end = getStartAndEnd(plot)
    points = [start, end]

    for y, line in enumerate(plot):
        for x, character in enumerate(line):
            if character == FOREST:
                continue

            neighbour = 0
            for nextY, nextX in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
                if 0 <= nextY < len(plot) and 0 <= nextX < len(plot[0]) and plot[nextY][nextX] != FOREST:
                    neighbour += 1
                if neighbour >= 3:
                    points.append((y, x))
    
    return points

def createPathGraph(plot: list[list[str]], points: list[tuple[int, int]], ignoreSlopes: bool) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    graph = {point: {} for point in points}

    for startY, startX in points:
        stack = [(0, startY, startX)]
        seen = {(startY, startX)}

        while stack:
            n, y, x = stack.pop()

            if n != 0 and (y, x) in points:
                graph[(startY, startX)][(y, x)] = n
                continue

            directions = DIRECTIONS[plot[y][x]]
            if ignoreSlopes:
                directions = DIRECTIONS[PATH]

            for directionY, directionX in directions:
                nextY = y + directionY
                nextX = x + directionX

                if 0 <= nextY < len(plot) and 0 <= nextX < len(plot[0]) and plot[nextY][nextX] != FOREST and (nextY, nextX) not in seen:
                    stack.append((n + 1, nextY, nextX))
                    seen.add((nextY, nextX))

    return graph 

class DFS():
    def __init__(self, graph: dict[tuple[int, int], dict[tuple[int, int], int]]) -> None:
        self.graph = graph 

    def prerformSearch(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        self.seen = set()
        self.end = end
        
        return self.depthFirstSearch(start)


    def depthFirstSearch(self, start: tuple[int, int]) -> int:
        if start == self.end:
            return 0
        
        m = -float('inf')

        self.seen.add(start)
        for node in self.graph[start]:
            if node not in self.seen:
                m = max(m, self.depthFirstSearch(node) + self.graph[start][node])
        self.seen.remove(start)

        return m

#Ignore slopes is Part II
def findLongestPath(lines: list[str], ignoreSlopes: bool = True) -> int:
    plot = parseLines(lines)
    start, end = getStartAndEnd(plot)
    points = findNeighbourPoints(plot)
    graph = createPathGraph(plot, points, ignoreSlopes)
    dfs = DFS(graph)
    result = dfs.prerformSearch(start, end)

    return result


testArray = [
    '#.#####################',
    '#.......#########...###',
    '#######.#########.#.###',
    '###.....#.>.>.###.#.###',
    '###v#####.#v#.###.#.###',
    '###.>...#.#.#.....#...#',
    '###v###.#.#.#########.#',
    '###...#.#.#.......#...#',
    '#####.#.#.#######.#.###',
    '#.....#.#.#.......#...#',
    '#.#####.#.#.#########v#',
    '#.#...#...#...###...>.#',
    '#.#.#v#######v###.###v#',
    '#...#.>.#...>.>.#.###.#',
    '#####v#.#.###v#.#.###.#',
    '#.....#...#...#.#.#...#',
    '#.#########.###.#.#.###',
    '#...###...#...#...#.###',
    '###.###.#.###v#####v###',
    '#...#...#.#.>.>.#.>.###',
    '#.###.###.#.###.#.#v###',
    '#.....###...###...#...#',
    '#####################.#'
]

def main():
    lines = read_file()
    print(findLongestPath(lines, False))
    print(findLongestPath(lines))

main()
