from itertools import combinations
from math import sqrt

def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

GALAXY = '#'
EMPTY = '.'

def getEmptyLines(lines: list) -> list:
    emptyLines = []
    for y, line in enumerate(lines):

        emptyLine =  "".join(EMPTY for _ in range(len(line)))
        if emptyLine == line:
            emptyLines.append(y)
    
    return emptyLines

def getEmptyColumns(lines: list) -> list:
    emptyColumn = "".join(EMPTY for _ in range(len(lines)))
    emptyColumns = []
    for x in range(len(lines[0])):
        column = ""
        for y in range(len(lines)):
            column += lines[y][x]

        if column == emptyColumn:
            emptyColumns.append(x)

    return emptyColumns


def expandUniverse(lines: list) -> list:
    emptyLines = getEmptyLines(lines)
    emptyColumns = getEmptyColumns(lines)

    result = []
    for y, line in enumerate(lines):
        newLine = ""
        for x, character in enumerate(line):
            if x in emptyColumns:
                newLine += EMPTY + EMPTY
            else:
                newLine += character

        if y in emptyLines:
            result.append(newLine)
            result.append(newLine)
        else:
            result.append(newLine)

    return result

def getGalaxiesPairs(lines: list) -> list:
    orderNumber = 1
    galaxies = []
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == GALAXY:
                galaxies.append([x, y, orderNumber])
                orderNumber += 1

    return list(combinations(galaxies, 2))

def calculateDistanceBetween(galaxyA: list, galaxyB: list) -> int:
    #return sqrt(((galaxyB[0] - galaxyA[0])**2) + ((galaxyB[1] - galaxyA[1])**2))
    return abs(galaxyB[0] - galaxyA[0]) + abs(galaxyB[1] - galaxyA[1])

def getSumDistances(lines: list) -> int:
    universe = expandUniverse(lines)
    pairs = getGalaxiesPairs(universe)

    result = 0
    for pair in pairs:
        distance = calculateDistanceBetween(pair[0], pair[1])
        result += distance

    return result

def getSumDistancesNoArray(lines: list, scale = 1_000_000) -> int:
    pairs = getGalaxiesPairs(lines)
    emptyLines = getEmptyLines(lines)
    emptyColumns = getEmptyColumns(lines)

    result = 0
    for galaxyA, galaxyB in pairs:
        for line in range(min(galaxyA[1], galaxyB[1]), max(galaxyA[1], galaxyB[1])):
            result += scale if line in emptyLines else 1

        for column in range(min(galaxyA[0], galaxyB[0]), max(galaxyA[0], galaxyB[0])):
            result += scale if column in emptyColumns else 1
    
    return result

testArray = [
    '...#......',
    '.......#..',
    '#.........',
    '..........',
    '......#...',
    '.#........',
    '.........#',
    '..........',
    '.......#..',
    '#...#.....'
]

def main():
    lines = readLines()
    #print(getSumDistances(testArray))
    print(getSumDistancesNoArray(lines, 2))
    print(getSumDistancesNoArray(lines))

main()