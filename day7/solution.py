def readLines(filename: str = 'input.txt') -> []:
    content = []
    with open(filename, "r") as file:
        content = file.readlines()

    return content

def createCardsWinningsPair(lines: []) -> []:
    result = []
    
    for line in lines:
        splits = line.split()
        result.append([splits[0], int(splits[1])])

    return result

CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARDS_J = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
JOKER = 'J'

def getHandTypeJoker(hand: str) -> int:
    cardCount = {}
    three = False
    pair = 0
    single = 0
    jokers = hand.count(JOKER)
    for card in CARDS_J:
        if card == JOKER:
            continue
        cardCount[card] = hand.count(card)

        if cardCount[card] == 5: #Five of a kind
            return 6

        if cardCount[card] == 4 and jokers == 1:
            return 6 #Jokers 5 of a kind
        
        if cardCount[card] == 3 and jokers == 2:
            return 6 #Jokers 5 of a kind
        
        if cardCount[card] == 4: #Four of a kind
            return 5

        if cardCount[card] == 3 and jokers == 1:
            return 5 #Jokers 4 of a kind
        
        if cardCount[card] == 3: #Three of a kind
            three = True
    
        if cardCount[card] == 2:
            pair += 1

        if cardCount[card] == 1:
            single += 1

    if jokers == 5 or jokers == 4:
        return 6 #Joker 5 of kind
    
    if pair == 1 and jokers == 3:
        return 6 #Joker 4 of kind
    
    if jokers == 3:
        return 5 #Joker 4 of kind
    
    if pair == 1 and jokers == 2:
        return 5 #Joker 4 of kind

    if pair == 2 and jokers == 1:
        return 4 #Joker Full hause

    if three and pair == 1: #Full hause
        return 4
    
    if three: #Three of a kind
        return 3
    
    if jokers == 2:
        return 3 #Joker 3 of kind
    
    if pair == 1 and jokers == 1:
        return 3 #Joker 3 of kind

    if pair == 2: #Two Pair  
        return 2
    
    if pair == 1: #Single pair
        return 1
    
    if jokers == 1: #Joker single pair
        return 1
    
    return 0

def getHandType(hand: str) -> int:
    cardCount = {}
    three = False
    pair = 0
    single = 0

    for card in CARDS:
        cardCount[card] = hand.count(card)

        if cardCount[card] == 5: #Five of a kind
            return 6

        if cardCount[card] == 4: #Four of a kind
            return 5
        
        if cardCount[card] == 3:
            three = True
    
        if cardCount[card] == 2:
            pair += 1

        if cardCount[card] == 1:
            single += 1

    if three and pair == 1: #Full hause
        return 4
    
    if three:  #Three of a kind
        return 3

    if pair == 2: #Two Pair
        return 2
    
    if pair == 1: #Single pair
        return 1
    
    return 0

def checkHigher(firstCard: str, secondCard: str, rankType: bool) -> bool:
    cards = CARDS
    if rankType:
        cards = CARDS_J
    for iterator, first in enumerate(firstCard):
        if first != secondCard[iterator]:
            for card in cards:
                if first == card:
                    return True
                elif secondCard[iterator] == card:
                    return False

def rankCards(pairs: [], rankType: bool = True) -> []:
    maxRank = len(pairs)

    types = {}
    types2 = []
    ranks = {}
    count = 0
    for card, win in pairs:
        value = 0
        if rankType:
           value = getHandTypeJoker(card)
        else:
           value = getHandType(card)

        types[card] = value
        types2.append([card, types[card], win])
        ranks[card] = count
        count += 1

    for i in range(len(ranks)):
        for j in range(len(ranks) - i - 1):
            higher = False
            if types2[j][1] == types2[j+1][1]:
                higher = checkHigher(types2[j][0], types2[j+1][0], rankType)

            if types2[j][1] > types2[j+1][1] or higher:
                tmp = types2[j]
                types2[j] = types2[j+1]
                types2[j+1] = tmp
        
    return types2
        
    # for firstCard, firstHand in types.items():
    #     for secondCard, secondHand in types.items():
    #         if firstCard == secondCard:
    #             continue

    #         if firstHand == secondHand:
    #             higher = checkHigher(firstCard, secondCard)
    #             print(firstCard + " " + secondCard)
    #             if higher:
    #                 ranks[firstCard] = maxRank
    #             else:
    #                 ranks[secondCard] = maxRank
            
    #         if firstHand > secondHand:
    #             if ranks[firstCard] > ranks[secondCard]:
    #                 continue
    #             ranks[firstCard] = ranks[secondCard]
            
    #     maxRank -= 1

    # return ranks

def sumWinnings(lines: []) -> int:
    result = 0
    pairs = createCardsWinningsPair(lines)
    cards = rankCards(pairs)
    for iterator, hand in enumerate(cards):
        result += (iterator+1) * hand[2]

    return result

testArray = [
    '32T3K 765',
    'T55J5 684',
    'KK677 28',
    'KTJJT 220',
    'QQQJA 483'
]

def main():
    lines = readLines()
    #print(sumWinnings(testArray))
    print(sumWinnings(lines))

main()
