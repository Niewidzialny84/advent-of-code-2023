def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

def flipPattern(lines: list) -> list:
    newPattern = []

    for column in range(len(lines[0])):
        value = ''
        for row in range(len(lines)):
            value += lines[row][column]
        newPattern.append(value)
    
    return newPattern

ROUND_ROCK = 'O'
CUBE_ROCK = '#'
EMPTY_SPACE = '.'

def tilt(lines: list) -> list:
    newPattern = []

    for line in lines:
        newLine = []

        for part in line.split(CUBE_ROCK):
            newPart = "".join(sorted(list(part), reverse=True))
            newLine.append(newPart)

        newLine = CUBE_ROCK.join(newLine)
        newPattern.append(newLine)

    return newPattern

def countWeight(lines: list) -> int:
    result = 0
    for i, line in enumerate(lines):
        part = line.count(ROUND_ROCK) * (len(line) - i)
        result += part
    return result

def cycle(lines: tuple) -> tuple:
    for _ in range(4):
        lines = tuple(map("".join, zip(*lines)))
        lines = tuple(CUBE_ROCK.join(["".join(sorted(tuple(group), reverse=True)) for group in row.split(CUBE_ROCK)]) for row in lines)
        lines = tuple(row[::-1] for row in lines)
    
    return lines


def processAndCount(lines: list) -> int:
    flip = flipPattern(lines)
    tiltValue = tilt(flip)
    flip = flipPattern(tiltValue)
    result = countWeight(flip)
    return result

def processAndCountCycle(lines: list, cycles: int = 1_000_000_000) -> int:
    t = tuple(lines)
    seen = {t}
    array = [t]

    counter = 0

    while True:
        counter += 1
        
        t = cycle(t)
        if t in seen:
            break

        seen.add(t)
        array.append(t)

    first = array.index(t)
    t = array[(cycles - first) % (counter - first) + first]
    result = countWeight(t)

    return result

testArray = [
    'O....#....',
    'O.OO#....#',
    '.....##...',
    'OO.#O....O',
    '.O.....O#.',
    'O.#..O.#.#',
    '..O..#O..O',
    '.......O..',
    '#....###..',
    '#OO..#....'
]

def main():
    lines = readLines()
    print(processAndCount(lines))
    print(processAndCountCycle(lines))
main()