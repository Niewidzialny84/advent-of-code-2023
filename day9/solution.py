def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content


def differences(numbers: list) -> list:
    array = []

    for i, number in enumerate(numbers):
        if i >= len(numbers) - 1:
            break
        array.append((number - numbers[i + 1]) * -1)
    
    zeroes = array.count(0)

    if array == []:
        return [0]

    if zeroes == len(array):
        return [array[len(array) - 1]]
    else:
        recur = differences(array)
        return recur + [array[len(array) - 1] + recur[len(recur) - 1]]


def processLine(line: str) -> list:
    
    coreNumbers = []
    for number in line.split():
        if number == '' or number == '\n' or number == ' ':
            continue

        coreNumbers.append(int(number))

    arr = differences(coreNumbers)
    last = arr[len(arr) - 1]
    if len(coreNumbers) == 0:
        print(line)
    coreLast = coreNumbers[-1]
    arr.append(last + coreLast)
    
    return arr

def sumLine(line: str) -> int:
    array = processLine(line)
    result = 0

    for number in array:
        result += number

    return result

def sumLines(lines: list) -> int:
    result = 0
    for line in lines:
        result += processLine(line)[-1]

    return result

testArray = [
    '0 3 6 9 12 15',
    '1 3 6 10 15 21',
    '10 13 16 21 30 45'
]

def main():
    lines = readLines()
    print(sumLines(lines))

main()