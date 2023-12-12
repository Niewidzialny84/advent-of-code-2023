def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content

def splitRecords(lines: list) -> list:
    records = []
    numbers = []

    for line in lines:
        record, numberSplit = line.split(' ')
        numberArray = tuple(map(int, numberSplit.split(',')))
        records.append(record)
        numbers.append(numberArray)
    
    return records, numbers

OPERATIONAL = '.'
BROKEN = '#'
UNKNOWN = '?'

cache = {}

def findArrangmentOfLine(records: list, numbers: list) -> int:
    if records == '':
        return 1 if numbers == () else 0 

    if numbers == (): 
        return 0 if BROKEN in records else 1
    
    key = (records, numbers)
    if key in cache:
        return cache[key]

    result = 0

    if records[0] in [OPERATIONAL, UNKNOWN]:
        result += findArrangmentOfLine(records[1:], numbers)

    if records[0] in [BROKEN, UNKNOWN]:
        if numbers[0] <= len(records) and OPERATIONAL not in records[:numbers[0]] and (numbers[0] == len(records) or records[numbers[0]] != BROKEN):
            result += findArrangmentOfLine(records[numbers[0] + 1:], numbers[1:])

    cache[key] = result
    return result

def sumArrangments(lines: list, multiply: int = 1) -> int:
    records, numbers = splitRecords(lines)
    

    result = 0
    for i in range(len(records)):
        record = records[i]
        number = numbers[i]

        if multiply > 1:
            record = UNKNOWN.join([record] * multiply)
            number *= multiply

        result += findArrangmentOfLine(record, number)

    return result


testArray = [
    '???.### 1,1,3',
    '.??..??...?##. 1,1,3',
    '?#?#?#?#?#?#?#? 1,3,1,6',
    '????.#...#... 4,1,1',
    '????.######..#####. 1,6,5',
    '?###???????? 3,2,1'
]

def main():
    lines = readLines()
    #print(sumArrangments(lines))
    print(sumArrangments(lines, 5))

main()