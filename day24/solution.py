import sympy

def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()

class Vertex():
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return "{X=" + str(self.x) + " Y=" + str(self.y) + " Z=" + str(self.z) + "}"
    
class Hailstone():
    def __init__(self, position: Vertex, velocity: Vertex) -> None:
        self.position = position
        self.velocity = velocity

        self.a = self.velocity.y
        self.b = -self.velocity.x
        self.c = self.velocity.y * self.position.x - self.velocity.x * self.position.y

    def __repr__(self) -> str:
        return "Hailstone{" + f"a={self.a}, b={self.b}, c={self.c}, position={self.position}, velocity={self.velocity}" + "}"

def parseLines(lines: list[str]) -> list[Hailstone]:
    result = []

    for line in lines:
        pos, vel = line.split('@')
        pos = pos.split(',')
        vel = vel.split(',')
        position = Vertex(int(pos[0]), int(pos[1]), int(pos[2]))
        velocity = Vertex(int(vel[0]), int(vel[1]), int(vel[2]))

        hailstone = Hailstone(position, velocity)

        result.append(hailstone)

    return result

def checkIntersection(hailstoneA: Hailstone, hailstoneB: Hailstone, regionBegin: int = 200000000000000, regionEnd: int = 400000000000000) -> bool:
    if hailstoneA.a * hailstoneB.b == hailstoneA.b * hailstoneB.a:
        return False
    
    x = (hailstoneA.c * hailstoneB.b - hailstoneB.c * hailstoneA.b) / (hailstoneA.a * hailstoneB.b - hailstoneB.a * hailstoneA.b)
    y = (hailstoneB.c * hailstoneA.a - hailstoneA.c * hailstoneB.a) / (hailstoneA.a * hailstoneB.b - hailstoneB.a * hailstoneA.b)

    if regionBegin <= x <= regionEnd and regionBegin <= y <= regionEnd:
        if all((x - hailstone.position.x) * hailstone.velocity.x >= 0 and (y - hailstone.position.y) * hailstone.velocity.y >= 0 for hailstone in (hailstoneA, hailstoneB)):
            return True
        
    return False

#Part I
def countIntersections(lines: list[str]) -> int:
    hailstones = parseLines(lines)
    
    result = 0

    for index, hailstoneA in enumerate(hailstones):
        for hailstoneB in hailstones[:index]:
            if checkIntersection(hailstoneA, hailstoneB):
                result += 1

    return result

#Part II
def findRockPositions(lines: list[str]) -> int:
    hailstones = parseLines(lines)

    x, y, z, vx, vy, vz = sympy.symbols("x, y, z, vx, vy, vz")

    equations = []

    for index, hailstone in enumerate(hailstones):
        equations.append((x - hailstone.position.x) * (hailstone.velocity.y - vy) - (y - hailstone.position.y) * (hailstone.velocity.x - vx))
        equations.append((y - hailstone.position.y) * (hailstone.velocity.z - vz) - (z - hailstone.position.z) * (hailstone.velocity.y - vy))

        if index < 2:
            continue

        answers = [solution for solution in sympy.solve(equations) if all(x % 1 == 0 for x in solution.values())]
        if len(answers) == 1:
            break

    answer = answers[0]

    return answer[x] + answer[y] + answer[z]

testArray = [
    '19, 13, 30 @ -2,  1, -2',
    '18, 19, 22 @ -1, -1, -2',
    '20, 25, 34 @ -2, -2, -4',
    '12, 31, 28 @ -1, -2, -1',
    '20, 19, 15 @  1, -5, -3',
]

def main():
    lines = read_file()
    print(countIntersections(lines))
    print(findRockPositions(lines))

main()
