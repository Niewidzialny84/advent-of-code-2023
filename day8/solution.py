def readLines(filename: str = 'input.txt') -> list:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

def processLines(lines: str) -> list:
    instructions = lines[0]
    instructions = instructions.strip()

    result = {}
    shortLines = lines[2:]
    for line in shortLines:
        rootNode, nodes = line.split('=')
        rootNode = rootNode.removesuffix(' ')
        left, right = nodes.split(',')
        left = left.removeprefix(' (')
        right = right.removesuffix('\n')
        right = right.removesuffix(')')
        right = right.removeprefix(' ')

        result[rootNode] = [left, right]

    return instructions, result

def navigateUntilFound(instructions: str, nodes: dict) -> int:
    firstNode = 'AAA'
    currentNode = firstNode
    count = 0
    while(currentNode != "ZZZ"):
        for instruction in instructions:
            count += 1
            if instruction == 'L':
                currentNode = nodes[currentNode][0]
            else:
                currentNode = nodes[currentNode][1]

    return count

#Slow solution as calculates all paths ~1h of processing in worst O(n^n)
def navigateUntilFoundAZ(instructions: str, nodes: dict) -> int:
    firstNodes = []
    for node in nodes:
        if node[2] == 'A':
            firstNodes.append(node)

    currentNodes = firstNodes
    count = 0
    found = True
    while found:
        zEnds = 0
        for node in currentNodes:
            if node[2] == 'Z':
                zEnds += 1
        if zEnds == len(firstNodes):  
            found = False
            break

        for instruction in instructions:

            count += 1
            if instruction == 'L':
                for i, node in enumerate(currentNodes):
                    currentNodes[i] = nodes[node][0]
            else:
                for i, node in enumerate(currentNodes):
                    currentNodes[i] = nodes[node][1]
        if count % 100_000 == 0:
            print(count)
    return count

def getSteps(lines: list, part2: bool = True) -> int:
    instruction, nodes = processLines(lines)
    if part2:
        return navigateUntilFoundAZ(instruction, nodes)
    else:
        return navigateUntilFound(instruction, nodes)

testArray = [
    'RL',
    '',
    'AAA = (BBB, CCC)',
    'BBB = (DDD, EEE)',
    'CCC = (ZZZ, GGG)',
    'DDD = (DDD, DDD)',
    'EEE = (EEE, EEE)',
    'GGG = (GGG, GGG)',
    'ZZZ = (ZZZ, ZZZ)'
]

testArray2 = [
    'LLR',
    '',
    'AAA = (BBB, BBB)',
    'BBB = (AAA, ZZZ)',
    'ZZZ = (ZZZ, ZZZ)'
]

testArray3 = [
    'LR',
    '',
    '11A = (11B, XXX)',
    '11B = (XXX, 11Z)',
    '11Z = (11B, XXX)',
    '22A = (22B, XXX)',
    '22B = (22C, 22C)',
    '22C = (22Z, 22Z)',
    '22Z = (22B, 22B)',
    'XXX = (XXX, XXX)'
]

def main():
    lines = readLines()
    print(getSteps(lines))

main()
