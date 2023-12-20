from collections import deque
from math import gcd

def read_file(file: str = 'input.txt') -> list[str]:
    with open(file) as f:
        return f.read().splitlines()
    
FLIP_FLOP = '%'
CONJUNCTION = '&'
MEMORY_DISABLED = 'off'
MEMORY_ENABLED = 'on'
BROADCASTER = 'broadcaster'
LOW = 'low'
HIGH = 'high'
RX_MODULE = 'rx'

class Module:
    def __init__(self, name: str, type: str, outputs: list[str]) -> None:
        self.name = name
        self.type = type
        self.outputs = outputs

        if type == FLIP_FLOP:
            self.memory = MEMORY_DISABLED
        else:
            self.memory = {}
        
        def __repr__(self) -> str:
            result = self.name
            result += "{"
            result += "type=" + self.type
            result += ",outputs=" + ",".join(self.outputs)
            result += ",memory=" + str(self.memory)
            result +=  + "}"
            return  result

def parseModules(lines: list[str]) -> tuple[dict[str, Module], list[str]]:
    modules = {}
    broadcast = []

    for line in lines:
        left, right = line.strip().split(' -> ')
        outputs = right.split(', ')

        if left == BROADCASTER:
            broadcast = outputs
        else:
            type = left[0]
            name = left[1:]
            modules[name] = Module(name, type, outputs)
    
    for name, module in modules.items():
        for output in module.outputs:
            if output in modules and modules[output].type == CONJUNCTION:
                modules[output].memory[name] = LOW

    return modules, broadcast


def findLowAndHigh(modules: dict[str, Module], broadcast: list[str], clicks: int = 1000) -> tuple[int, int]:
    low = high = 0

    for _ in range(clicks):
        low += 1

        queue = deque([(BROADCASTER, x, LOW) for x in broadcast])

        while queue:
            origin, target, pulse = queue.popleft()

            if pulse == LOW:
                low += 1
            else:
                high += 1

            if target not in modules:
                continue

            module = modules[target]

            if module.type == FLIP_FLOP:
                if pulse == LOW:
                    module.memory = MEMORY_ENABLED if module.memory == MEMORY_DISABLED else MEMORY_DISABLED
                    outgoing = HIGH if module.memory == MEMORY_ENABLED else LOW
                    for output in module.outputs:
                        queue.append((module.name, output, outgoing))
            else:
                module.memory[origin] = pulse
                outgoing = LOW if all(x == HIGH for x in module.memory.values()) else HIGH
                for output in module.outputs:
                        queue.append((module.name, output, outgoing))
            
    return low, high

def calculateTotalPulses(lines: list[str]) -> int:
    modules, broadcast = parseModules(lines)
    low, high = findLowAndHigh(modules, broadcast)

    return low * high

def findLowestClics(lines: list[str]) -> int:
    modules, broadcast = parseModules(lines)

    (feed,) = [name for name, module in modules.items() if RX_MODULE in module.outputs]

    cycle_lengths = {}
    seen = {name: 0 for name, module in modules.items() if feed in module.outputs}

    clicks = 0

    while True:
        clicks += 1
        queue = deque([(BROADCASTER, x, LOW) for x in broadcast])
        
        while queue:
            origin, target, pulse = queue.popleft()
            
            if target not in modules:
                continue
            
            module = modules[target]
            
            if module.name == feed and pulse == HIGH:
                seen[origin] += 1

                if origin not in cycle_lengths:
                    cycle_lengths[origin] = clicks
   
                if all(seen.values()):
                    x = 1
                    for cycle_length in cycle_lengths.values():
                        x = x * cycle_length // gcd(x, cycle_length)
                    return x
            
            if module.type == FLIP_FLOP:
                if pulse == LOW:
                    module.memory = MEMORY_ENABLED if module.memory == MEMORY_DISABLED else MEMORY_DISABLED
                    outgoing = HIGH if module.memory == MEMORY_ENABLED else LOW
                    for output in module.outputs:
                        queue.append((module.name, output, outgoing))
            else:
                module.memory[origin] = pulse
                outgoing = LOW if all(x == HIGH for x in module.memory.values()) else HIGH
                for output in module.outputs:
                        queue.append((module.name, output, outgoing))


testArray1 = [
    'broadcaster -> a, b, c',
    '%a -> b',
    '%b -> c',
    '%c -> inv',
    '&inv -> a'
]

testArray2 = [
    'broadcaster -> a',
    '%a -> inv, con',
    '&inv -> b',
    '%b -> con',
    '&con -> output'
]

def main():
    lines = read_file()
    print(calculateTotalPulses(lines))
    print(findLowestClics(lines))

main()