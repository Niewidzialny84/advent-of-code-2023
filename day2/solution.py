
def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

RED = 'red'
BLUE = 'blue'
GREEN = 'green'
COLORS = [RED, BLUE, GREEN]
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

def getAmountColor(text: str) -> [int,str]:
    for color in COLORS:
        if text.find(color) != -1:
            t = text.replace(color, '')
            return [int(t), color]

def splitDraws(text: str) -> []:
    colon = text.find(':') + 1
    return text[colon:len(text)].split(';')

def splitColors(text: str) -> []:
    return text.split(',')

def checkForMaximum(amount: int, color: str) -> bool:
    if color == RED and amount > MAX_RED:
        return True
    
    if color == BLUE and amount > MAX_BLUE:
        return True
    
    if color == GREEN and amount > MAX_GREEN:
        return True
    
    return False

def checkGame(text: str) -> bool:
    draws = splitDraws(text)

    for draw in draws:
        colors = splitColors(draw)
        for color in colors:
            amount, value = getAmountColor(color)
            if checkForMaximum(amount, value):
                return False
    return True

def checkGames(textArray: []) -> int:
    iterator = 1
    value = 0
    for text in textArray:
        if checkGame(text):
            value += iterator
        iterator += 1

    return value

def getFewer(text: str) -> [int, int, int]:
    draws = splitDraws(text)

    red = 0
    green = 0
    blue = 0

    for draw in draws:
        colors = splitColors(draw)
        for color in colors:
            amount, value = getAmountColor(color)
            if value == RED and amount > red:
                red = amount

            if value == BLUE and amount > blue:
                blue = amount

            if value == GREEN and amount > green:
                green = amount
    
    return [red, green, blue]

def sumFewerGames(textArray: []) -> int:
    value = 0
    for text in textArray:
        red, green, blue = getFewer(text)
        multiplication = red * blue * green
        value += multiplication

    return value
        
testGames = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
]

def main():
    lines = readLines()
    # print(checkGames(testGames))
    # print(checkGames(lines))
    print(sumFewerGames(lines))
        
main()