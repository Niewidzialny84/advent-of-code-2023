def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

def splitCard(line: str) -> ([], []):
    winningNumbers = []
    allNumbers = []

    text = line.split(' | ')
    winningText = text[0]
    allText = text[1]

    colon = winningText.find(':') + 2
    winningText = winningText[colon:]
    winningText = winningText.split(' ')

    for win in winningText:
        if win == '':
            continue

        winningNumbers.append(int(win))

    allText = allText.split(' ')
    for number in allText:
        if number == '':
            continue

        allNumbers.append(int(number))

    return winningNumbers, allNumbers

def checkCardWinnings(line: str) -> int:
    winningNumbers, numbersToCheck = splitCard(line)

    result = -1
    for win in winningNumbers:
        for number in numbersToCheck:
            if win == number:
                result += 1

    return result

#Part 1
def sumCardWinnings(lines: []) -> int:
    result = 0
    for line in lines:
        partial = checkCardWinnings(line)
        if partial == -1:
            partial = 0
        else: 
            partial = 2 ** partial

        result += partial

    return result

#Part 2
def sumCardsCopies(lines: []) -> int:
    copies = [1 for i in range(len(lines))]
    
    for iterator, line in enumerate(lines):
        partial = checkCardWinnings(line) + 1

        if partial == 0:
            continue

        for c in range(copies[iterator]):
            for i in range(1, partial + 1):
                nextIterator = iterator + i

                if nextIterator > len(lines):
                    continue
                copies[nextIterator] += 1
    
    result = 0
    for c in copies:
        result += c

    return result

testArray = [
    'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
]

def main():
    lines = readLines()
    # print(sumCardWinnings(lines))
    print(sumCardsCopies(lines))

main()