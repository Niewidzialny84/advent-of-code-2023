from collections import deque

def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

VERTICAL = '|'
HORIZONTAL = '-'
DOWN_RIGHT = 'L'
DOWN_LEFT = 'J'
UP_LEFT = '7'
UP_RIGHT = 'F'
GROUND = '.'
START = 'S'

DOWN_NEXT = VERTICAL + UP_LEFT + UP_RIGHT
UP_NEXT = VERTICAL + DOWN_LEFT + DOWN_RIGHT
LEFT_NEXT = HORIZONTAL + DOWN_RIGHT + UP_RIGHT
RIGHT_NEXT = HORIZONTAL + DOWN_LEFT + UP_LEFT
    
DOWN = START + UP_NEXT
UP = START + DOWN_NEXT
LEFT = START + RIGHT_NEXT
RIGHT = START + LEFT_NEXT

def findStart(lines: list) -> list:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == 'S':
                return [x, y]

def findLoop(lines: list) -> list:
    startX, startY = findStart(lines)

    loop = {(startX, startY)}
    queue = deque([(startX, startY)])
    S = {VERTICAL, HORIZONTAL, DOWN_LEFT, DOWN_RIGHT, UP_LEFT, UP_RIGHT}

    def append(x: str, y: str, character: str, value: set, current: set) -> set:
            loop.add((x, y))
            queue.append((x, y))
            if character == START:
                current &= value
            return current

    while queue:
        x, y = queue.popleft()
        character = lines[y][x]

        if y > 0 and character in DOWN and lines[y - 1][x] in DOWN_NEXT and (x, y - 1) not in loop:
            S = append(x, y - 1, character, {VERTICAL, DOWN_LEFT, DOWN_RIGHT}, S)

        if y < len(lines) - 1 and character in UP and lines[y + 1][x] in UP_NEXT and (x, y + 1) not in loop:
            S = append(x, y + 1, character, {VERTICAL, UP_LEFT, UP_RIGHT}, S)

        if x > 0 and character in LEFT and lines[y][x - 1] in LEFT_NEXT and (x - 1, y) not in loop:
            S = append(x - 1, y, character, {HORIZONTAL, DOWN_LEFT, UP_LEFT}, S)

        if x < len(lines[y]) - 1 and character in RIGHT and lines[y][x + 1] in RIGHT_NEXT and (x + 1, y) not in loop:
            S = append(x + 1, y, character, {HORIZONTAL, DOWN_RIGHT, UP_RIGHT}, S)
        
    return loop, S

def findFurthestDistance(lines: list) -> int:
    loop, S = findLoop(lines)
    
    return len(loop) // 2

def findTiles(lines: list) -> int:
    loop, S = findLoop(lines)

    (replace,) = S

    lines = [row.replace(START, replace) for row in lines]
    lines = ["".join(character if (x, y) in loop else GROUND for x, character in enumerate(line)) for y, line in enumerate(lines)]

    outside = set()

    for y, line in enumerate(lines):
        within = False
        up = None
        for x, character in enumerate(line):
            if character == VERTICAL:
                within = not within
            elif character in [DOWN_RIGHT, UP_RIGHT]:
                up = character == DOWN_RIGHT
            elif character in [DOWN_LEFT, UP_LEFT]:
                if character != (DOWN_LEFT if up else UP_LEFT):
                    within = not within
                up = None
            elif character == GROUND:
                pass

            if not within:
                outside.add((x,y))
            
    return (len(lines) * len(lines[0])) - len(outside | loop)

testArray1 = [
    '.....',
    '.S-7.',
    '.|.|.',
    '.L-J.',
    '.....'
]

testArray2 = [
    'FF7FSF7F7F7F7F7F---7',
    'L|LJ||||||||||||F--J',
    'FL-7LJLJ||||||LJL-77',
    'F--JF--7||LJLJ7F7FJ-',
    'L---JF-JLJ.||-FJLJJ7',
    '|F|F-JF---7F7-L7L|7|',
    '|FFJF7L7F-JF7|JL---7',
    '7-L-JL7||F7|L7F-7F7|',
    'L.L7LFJ|||||FJL7||LJ',
    'L7JLJL-JLJLJL--JLJ.L'
]

def main():
    lines = readLines()
    print(findFurthestDistance(lines))
    print(findTiles(lines))

main()

