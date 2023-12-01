NUMBERS = ['zero','one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content


def getFirstDigit(text: str) -> str:
    for character in text:   
        if character.isnumeric():
            return character
        

def getLastDigit(text: str) -> str:
    value = ''
    for character in text:
        if character.isnumeric():
            value = character

    return value


def replaceTextNumberToDigits(text: str) -> str:
    first = 1000
    firstWord = ''

    for number in NUMBERS:
        valueFirst = text.find(number)

        if valueFirst == -1:
            continue

        if valueFirst < first:
            first = valueFirst
            firstWord = number

    if firstWord != '':
        text = text.replace(firstWord, str(NUMBERS.index(firstWord)))

    
    last = 0
    lastWord = ''

    for number in NUMBERS:
        valueLast = text.rfind(number)

        if valueLast == -1:
            continue

        if valueLast > last:
            last = valueLast
            lastWord = number
    
    if lastWord != '':
        text = text.replace(lastWord, str(NUMBERS.index(lastWord)))
    
    return text


def getNumber(text: str, numbersAsText: bool = True) -> int:
    if numbersAsText:
        textValue = replaceTextNumberToDigits(text)
    else:
        textValue = text

    first = getFirstDigit(textValue)
    last = getLastDigit(textValue)

    print(textValue + "   " + first + last)

    return int(first + last)     


def sumNumbers(textArray: [], numbersAsText: bool = True) -> int:
    sumValue = 0

    for text in textArray:
        number = getNumber(text, numbersAsText)
        sumValue += number
    
    return sumValue

testValuePart1 = [
    '1abc2',
    'pqr3stu8vwx',
    'a1b2c3d4e5f',
    'treb7uchet'
]

testValuePart2 = [
    'two1nine',
    'eightwothree',
    'abcone2threexyz',
    'xtwone3four',
    '4nineeightseven2',
    'zoneight234',
    '7pqrstsixteen'
]

def main():
    textArray = readLines()
    #print(sumNumbers(testValuePart2))

    #Part 1
    #print(sumNumbers(textArray, False))

    #Part 2
    print(sumNumbers(textArray))
    

main()
