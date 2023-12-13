def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

def formatToPatterns(lines: list) -> list:
    patterns = []
    pattern = []
    for line in lines:
        if line == '':
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    
    return patterns

def checkMirrorRows(pattern: list, smudge: bool) -> int:
    for i in range(1, len(pattern)):
        left = pattern[:i][::-1]
        right = pattern[i:]

        if smudge:
            if sum(sum(0 if a == b else 1 for a, b in zip(x, y)) for x, y in zip(left, right)) == 1:
                return i
        else:
            left = left[:len(right)]
            right = right[:len(left)]

            if left == right:
                return i
        
    return 0

def flipPattern(pattern: list):
    newPattern = []

    for column in range(len(pattern[0])):
        value = ''
        for row in range(len(pattern)):
            value += pattern[row][column]
        newPattern.append(value)

    return newPattern

def checkMirrorColumns(pattern: list, smudge: bool) -> int:
    newPattern = flipPattern(pattern)
    return checkMirrorRows(newPattern, smudge)

#Smudge set to true is solution for part II
def getSummarizeValue(lines: list, smudge: bool = True) -> int:
    patterns = formatToPatterns(lines)

    result = 0
    columns = 0
    rows = 0
    for pattern in patterns:
        column = checkMirrorColumns(pattern, smudge)
        row = checkMirrorRows(pattern, smudge)
        columns += column
        rows += row
        result += column
        result += row * 100

    return result

testArray = [
    '#.##..##.',
    '..#.##.#.',
    '##......#',
    '##......#',
    '..#.##.#.',
    '..##..##.',
    '#.#.##.#.',
    '',
    '#...##..#',
    '#....#..#',
    '..##..###',
    '#####.##.',
    '#####.##.',
    '..##..###',
    '#....#..#'
]

def main():
    lines = readLines()
    print(getSummarizeValue(lines, False))
    print(getSummarizeValue(lines))

main()
