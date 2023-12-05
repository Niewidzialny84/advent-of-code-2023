def read(filename: str = 'input.txt') -> str:
    content = ''
    with open(filename, "r") as file:
        content = file.read()

    return content

def getSeeds(file: str) -> []:
    seeds = file.replace('seeds: ', '')
    end = seeds.find('\n')
    seeds = seeds[:end]
    result = []
    for seed in seeds.split(' '):
        result.append(int(seed))
    
    return result

def getMaps(file: str) -> []:
    seedEnd = file.find('\n\n')
    file = file[seedEnd:]

    maps = file.split('map:')

    resultMap = []
    for m in maps:
        lines = m.split('\n')
        resultLine = []
        for line in lines:
            splits = line.split(' ')
            numbers = []
            for split in splits:
                if split.isnumeric():
                    numbers.append(int(split))
            if numbers != []:
                resultLine.append(numbers)
        if resultLine != []:
            resultMap.append(resultLine)

    return resultMap

DESTINATION_RANGE_START = 0
SOURCE_RANGE_START = 1
RANGE_LENGTH = 2
#MAX_RANGE = 4_999_999_999
MAX_RANGE = 100_000_000

def processMap(processMap: []) -> []:
    sourceArray = [i for i in range(MAX_RANGE)]
    destinationArray = [i for i in range(MAX_RANGE)]
    for line in processMap:
        dest = line[DESTINATION_RANGE_START]
        source = line[SOURCE_RANGE_START]
        length = line[RANGE_LENGTH]
        for i in range(length):
            if dest + i >= MAX_RANGE or source + i >= MAX_RANGE:
                break

            sourceArray[source + i] = destinationArray[dest + i] 
    return sourceArray

def processMaps(maps: []) -> []:
    result = []
    source = []
    for m in maps:
        source = processMap(m)
        result.append(source)
    return result

def processSeeds(seeds: [], maps: []) -> []:
    procesedMaps = processMaps(maps)
    
    locations = []
    current = 0
    for seed in seeds:
        current = seed
        for m in procesedMaps:
            current = m[current]
        locations.append(current)
    return locations

## Too much memory required for this solution
def findLowestLocation(file: str) -> int:
    seeds = getSeeds(file)
    maps = getMaps(file)

    locations = processSeeds(seeds, maps)
    return min(locations)

def findLocationQuick(seeds: [], maps: []) -> []:
    for m in maps:  
        array = []
        for seed in seeds:
            for destination, source, length in m:
                if source <= seed < source + length:
                    val = seed - source + destination
                    array.append(val)
                    break
            else:
                array.append(seed)
        seeds = array 
    return seeds 

def populateSeeds(file: str) -> []:
    seeds = getSeeds(file)

    result = []

    for i in range(0, len(seeds), 2):
        for seed in range(seeds[i], seeds[i] + seeds[i+1]):
            result.append(seed)
    
    return result

#Part 2 is handled by setting ranges to True
#But it is similar to first solution very memory consuming, like 128 GB of memory
def findLowestLocationQuick(file: str, ranges: bool = True) -> int:     
    if ranges:
        seeds = populateSeeds(file)
    else:
        seeds = getSeeds(file)
    maps = getMaps(file)
    location = findLocationQuick(seeds, maps)

    return min(location)


testInput = """seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4"""

def main():
    file = read()
    #print(findLowestLocationQuick(testInput))
    print(findLowestLocationQuick(file))

main()
