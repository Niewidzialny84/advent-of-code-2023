def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

def createArray(inputArray: [] = readLines()) -> []:
    array = []
    for iterator, line in enumerate(inputArray):
        array.append([])
        for character in line:
            if character == '\n':
                continue

            array[iterator].append(character)

    return array

DOT = '.'
SYMBOLS = ['*', '#', '+', '-', '$', '/', '@', '=', '&', '%']

def scanForNumber(line: str, number: int) -> int:
    starting = line[number]
    right = []
    left = []
    rightIterator = number + 1
    leftIterator = number - 1
    rightEnd = False
    leftEnd = False
    rightCharacter = ''
    leftCharacter = ''
    for i in range(0, len(line) - 1):
        if rightIterator <= (len(line) - 1):
            rightCharacter = line[rightIterator]
        else:
            rightEnd = True

        if leftIterator >= 0:
            leftCharacter = line[leftIterator]
        else:
            leftEnd = True

        for symbol in SYMBOLS:
            if rightCharacter == DOT or rightCharacter == symbol:
                rightEnd = True

            if leftCharacter == DOT or leftCharacter == symbol:
                leftEnd = True

        if not rightEnd:
            right.append(rightCharacter)

        if not leftEnd:
            left.append(leftCharacter)
        
        rightIterator += 1
        leftIterator -= 1

    result = ''
    left.reverse()
    for char in left:
        result += char
    
    result += starting

    for char in right:
        result += char

    return int(result)

def getSurroundingNumbers(y: int, x: int, array: [[]], gearOnly: bool) -> int:
    numbers = []
    lines = []
    for i in range(-1, 2):
        if (y + i < 0) or (y + i > len(array)):
            continue
        
        isRepeat = False
        for j in range(-1, 2):
            if(x + j < 0) or (x + j > len(array[0])):
                continue

            if str(array[y + i][x + j]).isnumeric():
                number = scanForNumber(array[y + i], x + j)
                if not isRepeat:
                    numbers.append(number)
                isRepeat = True
            else:
                isRepeat = False
        
        lines.append(array[y + i])

    if len(numbers) != 2 and gearOnly:
        return 0
    
    if gearOnly:
        return numbers[0] * numbers[1]

    result = 0
    for number in numbers:
        result += number
    
    return result

#gearOnly -> second part
def scanForSymbol(array: [[]], gearOnly: bool = True) -> int:
    result = 0

    if gearOnly:
        symbols = ['*']
    else:
        symbols = SYMBOLS

    for y in range(len((array)) - 1):

        for x in range(len(array[y]) - 1):
            for symbol in symbols:
                if array[y][x] == symbol:
                    result += getSurroundingNumbers(y, x, array, gearOnly)
    
    return result


testArray = [
    '467..114..',
    '...*......',
    '..35..633.',
    '......#...',
    '617*......',
    '.....+.58.',
    '..592.....',
    '......755.',
    '...$.*....',
    '.664.598..'
]

def main():
    test = createArray(testArray)
    real = createArray()
    #print(scanForSymbol(test, False))

    print(scanForSymbol(real))

main()