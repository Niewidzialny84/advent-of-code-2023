def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()

LEFT = '<'
RIGHT = '>'
START = 'in'
ACCEPTED = 'A'
REJECTED = 'R'

def formatWorkflows(lines: list[str]) -> dict[str, list[list]]:
    result = {}

    for line in lines:
        key, values = line.split('{')
        values = values.removesuffix('}').split(',')
        rules = []
        for value in values:
            if value.find(LEFT) != -1:
                value = value.split(LEFT)
                destination = value[1].split(':')
                rule = [value[0], LEFT, int(destination[0]), destination[1]]
            elif value.find(RIGHT) != -1:
                value = value.split(RIGHT)
                destination = value[1].split(':')
                rule = [value[0], RIGHT, int(destination[0]), destination[1]]
            else:
                rule = [value]
            rules.append(rule)
        result[key] = rules

    return result

def formatParts(lines: list[str]) -> list[dict[str, int]]:
    result = []

    for line in lines:
        splits = line.removeprefix('{').removesuffix('}').split(',')
        data = {}
        for split in splits:
            key, value = split.split('=')
            data[key] = int(value)
        result.append(data)
    
    return result
        
def formatData(lines: list[str]) -> tuple[dict[str, list[list]], list[dict[str, int]]]:
    splitPoint = lines.index('')
    workflows = lines[:splitPoint]
    parts = lines[splitPoint + 1:]

    workflows = formatWorkflows(workflows)
    parts = formatParts(parts)

    return workflows, parts

def processPart(part: dict[str, int], workflows: dict[str, list[list]]) -> int: 
    nextWorkflow = START

    while nextWorkflow != ACCEPTED and nextWorkflow != REJECTED:
        current = workflows[nextWorkflow]

        if len(current) == 1:
            nextWorkflow = current[3][0]
            continue

        for rule in current:
            if len(rule) == 1:
                nextWorkflow = rule[0]
                break

            category, sign, value, destination = rule
            if sign == LEFT and part[category] < value:
                nextWorkflow = destination
                break

            if sign == RIGHT and part[category] > value:
                nextWorkflow = destination
                break
    
    if nextWorkflow == ACCEPTED:
        result = 0
        for value in part.values():
            result += value
        return result
    else:
        return 0

# Generate parts is for part II 
def processParts(lines: list[str], generateParts: bool = True) -> int:
    workflows, parts = formatData(lines)
    
    start = 1
    end = 4000
    result = 0

    #Not very efficient as this is 4000^4 combinations
    if generateParts:
        for x in range(start, end + 1):
            for m in range(start, end + 1):
                for a in range(start, end + 1):
                    for s in range(start, end + 1):
                        part = {}
                        part['x'] = x
                        part['m'] = m
                        part['a'] = a
                        part['s'] = s
                        value = processPart(part, workflows)
                        
                        if value > 0:
                            result += 1
    else:
        for part in parts:
            value = processPart(part, workflows)
            result += value

    return result

testArray = [
    'px{a<2006:qkq,m>2090:A,rfg}',
    'pv{a>1716:R,A}',
    'lnx{m>1548:A,A}',
    'rfg{s<537:gd,x>2440:R,A}',
    'qs{s>3448:A,lnx}',
    'qkq{x<1416:A,crn}',
    'crn{x>2662:A,R}',
    'in{s<1351:px,qqz}',
    'qqz{s>2770:qs,m<1801:hdj,R}',
    'gd{a>3333:R,R}',
    'hdj{m>838:A,pv}',
    '',
    '{x=787,m=2655,a=1222,s=2876}',
    '{x=1679,m=44,a=2067,s=496}',
    '{x=2036,m=264,a=79,s=2244}',
    '{x=2461,m=1339,a=466,s=291}',
    '{x=2127,m=1623,a=2188,s=1013}',
]

def main():
    lines = read_file()
    print(processParts(lines, False))
    print(processParts(lines))

main()
