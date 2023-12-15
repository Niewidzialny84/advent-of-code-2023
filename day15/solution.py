def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.read().strip().splitlines()

    return content[0].split(',')

def hashAlgorithm(sequence: str) -> int:
    current = 0

    for character in sequence:
            value = ord(character)
            current += value
            current *= 17
            current %= 256
    
    return current

def sumHashes(inputs: list) -> int:
    result = 0

    for sequence in inputs:
         result += hashAlgorithm(sequence)

    return result

EQUALS = '='
DASH = '-'

def processLenses(inputs: list) -> list:
    boxes = []
    for i in range(256):
        boxes.append([])
    
    for sequence in inputs:
        isEqual = sequence.find(EQUALS)
        isDash = sequence.find(DASH)

        value = sequence

        if isDash != -1:
            value = sequence.replace(DASH, '')
            key = hashAlgorithm(value)

            currentBoxes = boxes[key]
            if currentBoxes == []:
                continue

            for index, box in enumerate(currentBoxes):
                if box[0] == value:
                    boxes[key] = currentBoxes[:index] + currentBoxes[index + 1:]
                    break

        if isEqual != -1:
            value = sequence.split(EQUALS)
            key = hashAlgorithm(value[0])
            wasAdded = False

            currentBoxes = boxes[key]
            for index, box in enumerate(currentBoxes):
                if box[0] == value[0]:
                    boxes[key] = currentBoxes[:index] + [value] + currentBoxes[index + 1:]
                    wasAdded = True
                    break
            
            if not wasAdded:
                boxes[key].append(value)
    
    return boxes

def calculateFocusingPower(inputs: str) -> int:
    boxes = processLenses(inputs)
    result = 0

    for index, box in enumerate(boxes):
        lensBox = index + 1
        for lensIndex, lens in enumerate(box):
            lensValue = 0
            lensValue = lensIndex + 1
            lensValue *= int(lens[1])
            lensValue *= lensBox
            result += lensValue
    
    return result


testArray = [
'rn=1','cm-','qp=3','cm=2','qp-','pc=4','ot=9','ab=5','pc-','pc=6','ot=7'
]

def main():
    inputs = readLines()
    print(sumHashes(inputs))
    print(calculateFocusingPower(inputs))

main()
    