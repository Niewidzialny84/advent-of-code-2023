from collections import deque

def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()
    
class Vertex():
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return 'X: ' + str(self.x) + ' Y: ' + str(self.y) + ' Z: ' + str(self.z)
    
class Cube():
    def __init__(self, cornerA: Vertex, cornerB: Vertex) -> None:
        self.cornerA = cornerA
        self.cornerB = cornerB

    def __repr__(self) -> str:
        return 'cornerA: {' + str(self.cornerA) + '} cornerB: {' + str(self.cornerB) + '}'

def parseLines(lines: list[str]) -> list[Cube]:
    result = []
    for line in lines:
        splits = line.split('~')
        cornerA = splits[0].split(',')
        cornerB = splits[1].split(',')
        cube = Cube(Vertex(int(cornerA[0]), int(cornerA[1]), int(cornerA[2])), Vertex(int(cornerB[0]), int(cornerB[1]), int(cornerB[2])))
        result.append(cube)
    
    return result

def overlaps(a: Cube, b: Cube) -> bool:
        return max(a.cornerA.x, b.cornerA.x) <= min(a.cornerB.x, b.cornerB.x) and max(a.cornerA.y, b.cornerA.y) <= min(a.cornerB.y, b.cornerB.y)

def processDrop(cubes: list[Cube]) -> list[Cube]:
    for index, cube in enumerate(cubes):
        maxZ = 1
        for check in cubes[:index]:
            if overlaps(cube, check):
                maxZ = max(maxZ, check.cornerB.z + 1)

        cube.cornerB.z -= cube.cornerA.z - maxZ
        cube.cornerA.z = maxZ
    
    return cubes

def sortCubes(cubes: list[Cube]) -> list[Cube]:
    cubes.sort(key=lambda cube: cube.cornerA.z)
    return cubes

def findSupports(cubes: list[Cube]) -> tuple[dict[set[int]], dict[set[int]]]:
    kvSupport = {i: set() for i in range(len(cubes))}
    vkSupport = {i: set() for i in range(len(cubes))}

    for j, upper in enumerate(cubes):
        for i, lower in enumerate(cubes[:j]):
            if overlaps(lower, upper) and upper.cornerA.z == lower.cornerB.z + 1:
                kvSupport[i].add(j)
                vkSupport[j].add(i)

    return kvSupport, vkSupport

def processLines(lines: list[str]) -> list[Cube]:
    cubes = parseLines(lines)
    cubes = sortCubes(cubes)
    cubes = processDrop(cubes)
    cubes = sortCubes(cubes)
    return cubes

#Part I
def countRemovable(lines: list[str]) -> int:
    cubes = processLines(lines)
    kvSupport, vkSupport = findSupports(cubes)

    total = 0

    for i in range(len(cubes)):
        if all(len(vkSupport[j]) >= 2 for j in kvSupport[i]):
            total += 1

    return total

#Part II
def sumCubesFallWhenRemoved(lines: list[str]) -> int:
    cubes = processLines(lines)
    kvSupport, vkSupport = findSupports(cubes)

    total = 0

    for i in range(len(cubes)):
        queue = deque(j for j in kvSupport[i] if len(vkSupport[j]) == 1)
        falling = set(queue)
        falling.add(i)

        while queue:
            j = queue.popleft()
            for k in kvSupport[j] - falling:
                if vkSupport[k] <= falling:
                    queue.append(k)
                    falling.add(k)

        total += len(falling) -1

    return total


testArray = [
    '1,0,1~1,2,1',
    '0,0,2~2,0,2',
    '0,2,3~2,2,3',
    '0,0,4~0,2,4',
    '2,0,5~2,2,5',
    '0,1,6~2,1,6',
    '1,1,8~1,1,9'
]

def main():
    lines = read_file()
    print(countRemovable(lines))
    print(sumCubesFallWhenRemoved(lines))

main()