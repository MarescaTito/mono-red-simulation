from enum import Enum
from itertools import combinations 
import random
    
TRIALS = 10000
NUM_LANDS = 18
            
def doIWinWithScamp(leylines, hand_scamps, hand_swifties, m_rages, insides, maws, felons, swords, lands):
    if(leylines == 1):
        if(lands < 2):
            return False
        #Two insides creates (1+(3*2*2))=13 power scamp which gets in for 13, sacs, then goes face for 13, 26 total damage
        if(insides > 1):
            return True
        #One inside creates (1+3*2)=7 power scamp, swords kills on the spot, any other buff gets us over 10 power, killing after sac 
        if(insides>0):
            return (swords + m_rages + maws + felons > 0)
        #One m_rage creates (1+3+2)=6 power scamp, maw, felon, or another m_rage can give us 4 more power to get 10, killing after sac
        return (m_rages > 1) or (m_rages > 0 and (maws + felons > 0))
    
    #One inside kills by itself with more than one leyline (1+3*3) = 10 power, killing after sac
    if(insides > 0):
        return True
    
    if(leylines == 2):
        #One buff gives us at least (1+(2*3))=7 power, killing with a sword, two buffs gives us at least (1+(2*3*2))=13 power, killing after sac
        return (lands > 1) and (m_rages + maws + felons + swords > 1)
        
    if(leylines == 3):
        if(lands == 1):
            #Only way to kill with one land is m_rage (1+3+2*3) = 10, killing after sac
            return m_rages > 0
        
        #One m_rage kills by itself, as seen from above
        #Two scamps, one felon, both can attack due to haste from felon, 1+1+(2*4)=10 total scamp power, killing after double sac
        #One scamp, one swifty, one buff, 1+(2*4)=9 scamp power, swifty gets in for 2 from prowess and haste, 9 + 2 + 9 = 20 after sac
        #One buff, one swords, 1+(2*4)=9 scamp power, sword wins
        return (m_rages>0) or (felons>0 and hand_scamps > 0) or ((hand_swifties > 0 or swords > 0) and (maws + felons > 0))
        
    if(leylines == 4):
        #any buff (1 + 2*5) = 11 scamp power, killing after sac
        return (m_rages + maws + felons) > 0
            
    return False
    
    
def doIWinWithHero(leylines, m_rages, insides, maws, felons, swords, lands):
    #Hero needs a buff and a swords to take advantage of death trigger, needing two lands
    if(lands < 2 or swords < 1):
        return False

    if(leylines == 1):
        #Insides gives 1+1+3+3=8 power, m_rage gives 1+1+3+2=7 power, these both kill after swords
        return (m_rages + insides > 0)
     
    #with more than one leyline any buff gives at least 1+1+(2*3)=8 power, killing after swords
    return (m_rages + insides + maws + felons) > 0
    

def doIWinWithSwifty(leylines, hand_scamps, m_rages, insides, maws, felons, swords, lands):
    #Swifty needs a lot of help since it doesn't have a death trigger and prowess only triggers on cast
    if(lands < 2 or leylines < 2):
        return False

    if(leylines == 2):
        #One inside gives 1+1+3*3=11 power, killing with swords or another inside
        #One m_rage gives us 1+1+3+2*2=9 power, after attacking we are left with 10 health since haste enabled one damage on turn one
            #Swords triggers prowess before resolving so we deal exactly 10 more damage
        return (swords + insides > 1) or (swords > 0 and m_rages > 0)
    if(leylines == 3):
        #any buff gives at least 1+1+(2*4)=10 power killing with swords or another buff since we only need 19 damage turn two
        #giving a hand scamp haste and 1+2*4=9 power with felon kills with 2 damage from prowess trigger swifty
        return (felons + maws + m_rages + insides + swords > 1) or (hand_scamps > 0 and felons > 0)
    if(leylines == 4):
        #we run out of handspace for playing another creature from hand
        return (felons + maws + m_rages + insides + swords > 1)
        
    

#Prereq: hand creatures and swords should be capped at 1, since we never cast more than one of each and I do some arithmetic later assuming this
def doIWin(leylines, scamps, heroes, swifties, hand_scamps, hand_swifties, m_rages, insides, maws, felons, swords, lands):
    if(scamps == 1):
        return doIWinWithScamp(leylines, hand_scamps, hand_swifties, m_rages, insides, maws, felons, swords, lands)
    if(heroes == 1):
        return doIWinWithHero(leylines, m_rages, insides, maws, felons, swords, lands)
    else:
        return doIWinWithSwifty(leylines, hand_scamps, m_rages, insides, maws, felons, swords, lands)

class Card:
    def __init__(self, num):
            self.num = num
    
class CardEnum(Enum):
    LEYLINE = 0
    SCAMP = 1
    HERO = 2
    MONSTROUS = 3
    INSIDE_OUT = 4
    DREADMAWS = 5
    FELONIOUS = 6
    SELLSWORD = 7
    SWIFTSPEAR = 8
    MOUNTAIN = 9
    JUNK = 10


def fullDeck():
    deck = []
    for i in range(4):
        deck.append(Card(CardEnum.LEYLINE.value))
        deck.append(Card(CardEnum.SCAMP.value))
        deck.append(Card(CardEnum.HERO.value))
        deck.append(Card(CardEnum.MONSTROUS.value))
        deck.append(Card(CardEnum.INSIDE_OUT.value))
        deck.append(Card(CardEnum.FELONIOUS.value))
        deck.append(Card(CardEnum.SELLSWORD.value))
        deck.append(Card(CardEnum.SWIFTSPEAR.value))
    
    for i in range(2):
        deck.append(Card(CardEnum.DREADMAWS.value))

    for i in range(NUM_LANDS):
        deck.append(Card(CardEnum.MOUNTAIN.value))

    for i in range(8):
        deck.append(Card(CardEnum.JUNK.value))

    return deck
    
def drawEight(smoothed):
    deck1 = fullDeck()
    deck2 = fullDeck()
    eight1 = []
    eight2 = []
    idealRatio = NUM_LANDS/60
    
    for i in range(7):
        popped = random.sample(deck1,1)[0]
        deck1.remove(popped)
        eight1.append(popped) 
    if(not smoothed):
        eight1.append(random.sample(deck1,1)[0])
        return eight1
        
        
    for i in range(7):
        popped = random.sample(deck2,1)[0]
        deck2.remove(popped)
        eight2.append(popped) 
    
    landCount1 = 0
    landCount2 = 0
    for c in eight1:
        if(c.num == CardEnum.MOUNTAIN.value):
            landCount1+=1
    for c in eight2:
        if(c.num == CardEnum.MOUNTAIN.value):
            landCount2+=1
    
    diff1 = abs(idealRatio - (landCount1/8))
    diff2 = abs(idealRatio - (landCount2/8))
    hand1Wins = diff1 <= diff2
    handToReturn = eight1 if hand1Wins else eight2
    deckToDrawFrom = deck1 if hand1Wins else deck2
    handToReturn.append(random.sample(deckToDrawFrom,1)[0])
    return handToReturn

def handWinsNoEighth(hand):
    leylines = 0
    base_hand_scamps = 0
    base_hand_heroes = 0
    base_hand_swifties = 0
    m_rages = 0
    insides = 0
    maws = 0
    felons = 0
    swords = 0
    lands = 0

    for c in hand:
        match c.num:
            case CardEnum.LEYLINE.value:
                leylines+=1
            case CardEnum.SCAMP.value:
                base_hand_scamps+=1
            case CardEnum.HERO.value:
                base_hand_heroes+=1
            case CardEnum.MONSTROUS.value:
                m_rages+=1
            case CardEnum.INSIDE_OUT.value:
                insides+=1
            case CardEnum.DREADMAWS.value:
                maws +=1
            case CardEnum.FELONIOUS.value:
                felons +=1
            case CardEnum.SELLSWORD.value:
                swords +=1
            case CardEnum.SWIFTSPEAR.value:
                base_hand_swifties += 1
            case CardEnum.MOUNTAIN.value:
                lands +=1
            case _:
                junk = 0

    if(lands == 0 or leylines == 0 or (base_hand_scamps + base_hand_heroes + base_hand_swifties) == 0):
        return False  

    for i in range(3):
        hand_scamps = base_hand_scamps
        hand_swifties = base_hand_swifties
        hand_heroes = base_hand_heroes
        scamps = 0
        swifties = 0
        heroes = 0
        if(i == 0):
            if(hand_scamps):
                scamps+=1
                hand_scamps-=1
            else:
                continue
        elif(i==1):
            if(hand_swifties):
                scamps+=1
                hand_swifties-=1
            else:
                continue
        else:
            if(hand_heroes):
                heroes+=1
                hand_heroes-=1
            else:
                continue
        if(doIWin(leylines, scamps, heroes, swifties, min(hand_scamps,1), min(hand_swifties,1), m_rages, insides, maws, felons, min(swords,1), lands)):
            return True

    return False
        

def handWins(hand, eighth):
    if(handWinsNoEighth(hand)):
        return True
    leylines = 0
    hand_scamps = 0
    hand_heroes = 0
    hand_swifties = 0
    m_rages = 0
    insides = 0
    maws = 0
    felons = 0
    swords = 0
    lands = 0

    for c in hand:
        match c.num:
            case CardEnum.LEYLINE.value:
                leylines+=1
            case CardEnum.SCAMP.value:
                hand_scamps+=1
            case CardEnum.HERO.value:
                hand_heroes+=1
            case CardEnum.MONSTROUS.value:
                m_rages+=1
            case CardEnum.INSIDE_OUT.value:
                insides+=1
            case CardEnum.DREADMAWS.value:
                maws +=1
            case CardEnum.FELONIOUS.value:
                felons +=1
            case CardEnum.SELLSWORD.value:
                swords +=1
            case CardEnum.SWIFTSPEAR.value:
                hand_swifties += 1
            case CardEnum.MOUNTAIN.value:
                lands +=1
            case _:
                junk = 0

    if(lands == 0 or leylines == 0 or (hand_scamps + hand_heroes + hand_swifties) == 0):
        return False

    scamps = 0
    swifties = 0
    heroes = 0

    if(hand_scamps):
        scamps+=1
        hand_scamps-=1
    elif(hand_swifties and hand_heroes):
        #TODO, create perfect algorithm to choose which to play, checking for 7 winning without 8 and then swords is a hueristic
        if(swords):
            heroes+=1
            hand_heroes-=1
        else:
            swifties+=1
            hand_swifties-=1
    elif(hand_swifties):
        swifties+=1
        hand_swifties-=1
    else:
        heroes+=1
        hand_heroes-=1
    
    match eighth.num:
        case CardEnum.SCAMP.value:
            hand_scamps+=1
        case CardEnum.HERO.value:
            hand_heroes+=1
        case CardEnum.MONSTROUS.value:
            m_rages+=1
        case CardEnum.INSIDE_OUT.value:
            insides+=1
        case CardEnum.DREADMAWS.value:
            maws +=1
        case CardEnum.FELONIOUS.value:
            felons +=1
        case CardEnum.SELLSWORD.value:
            swords +=1
        case CardEnum.SWIFTSPEAR.value:
            hand_swifties += 1
        case CardEnum.MOUNTAIN.value:
            lands +=1
        case _:
            junk = 0

    return doIWin(leylines, scamps, heroes, swifties, min(hand_scamps,1), min(hand_swifties,1), m_rages, insides, maws, felons, min(swords,1), lands)

def noMulls(smoothed):
    eight = drawEight(smoothed)

    return handWins(eight[0:7], eight[7])

def tryWithMullNoPeeking(smoothed, eight):
    seven = eight[0:7]
    eighth = eight[7]

    for i in range(6):
        sixToCheck = seven[0:i] + seven[i+1:7]
        if(handWinsNoEighth(sixToCheck)):
            return True

    sixToCheck = seven[0:6]
    if(handWinsNoEighth(sixToCheck)):
        return True
    
    six = []
    for c in seven:
        six.append(c)
    #TODO: Do something intelligent here to put back the least important card
    orderOfCardsToShip = [CardEnum.JUNK.value,CardEnum.MOUNTAIN.value,CardEnum.DREADMAWS.value,CardEnum.FELONIOUS.value,CardEnum.HERO.value,
        CardEnum.SELLSWORD.value,CardEnum.MONSTROUS.value,CardEnum.SWIFTSPEAR.value,CardEnum.INSIDE_OUT.value,CardEnum.SCAMP.value, CardEnum.LEYLINE.value]
    for n in orderOfCardsToShip:
        if(len(six) < 7):
            break
        for c in six:
            if(c.num == n):
                six.remove(c)
                break

    return handWins(six, eighth)
    
def tryWithMullToFiveNoPeeking(smoothed):
    eight = drawEight(smoothed)
    seven = eight[0:7]
    eighth = eight[7]

    for p in combinations(seven, 5):
        if(handWinsNoEighth(p)):
            return True
    
    five = []
    for c in seven:
        five.append(c)
    #TODO: Do something intelligent here to put back the least important card
    #TODO: Especially complicated on a mull to 5
    orderOfCardsToShip = [CardEnum.JUNK.value,CardEnum.MOUNTAIN.value,CardEnum.DREADMAWS.value,CardEnum.FELONIOUS.value,CardEnum.HERO.value,
        CardEnum.SELLSWORD.value,CardEnum.MONSTROUS.value,CardEnum.SWIFTSPEAR.value,CardEnum.INSIDE_OUT.value,CardEnum.SCAMP.value, CardEnum.LEYLINE.value]
    for n in orderOfCardsToShip:
        if(len(five) < 6):
            break
        for c in five:
            if(c.num == n):
                five.remove(c)
                break

    return handWins(five, eighth)

def tryWithMullPeeking(smoothed):
    eight = drawEight(smoothed)
    seven = eight[0:7]
    eighth = eight[7]

    for i in range(6):
        sixToCheck = seven[0:i] + seven[i+1:7]
        if(handWins(sixToCheck,eighth)):
            return True

    sixToCheck = seven[0:6]
    if(handWins(sixToCheck,eighth)):
        return True
        
    return False
    
def tryWithMullToFivePeeking(smoothed):
    eight = drawEight(smoothed)
    seven = eight[0:7]
    eighth = eight[7]

    for p in combinations(seven, 5):
        lp = p
        if(handWins(p,eighth)):
            return True
        
    return False

def reasonableMulling(smoothed):
    eight = drawEight(smoothed)
    seven = eight[0:7]
    eighth = eight[7]

    if(handWinsNoEighth(seven)):
        return True

    leylines = 0
    hand_scamps = 0
    hand_heroes = 0
    hand_swifties = 0
    m_rages = 0
    insides = 0
    maws = 0
    felons = 0
    swords = 0
    lands = 0
    for c in seven:
        match c.num:
            case CardEnum.LEYLINE.value:
                leylines+=1
            case CardEnum.SCAMP.value:
                hand_scamps+=1
            case CardEnum.HERO.value:
                hand_heroes+=1
            case CardEnum.SWIFTSPEAR.value:
                hand_swifties += 1
            case CardEnum.MOUNTAIN.value:
                lands +=1
            case _:
                junk = 0

    if(leylines and (hand_scamps + hand_heroes + hand_swifties) and (lands)):
        return handWins(seven,eighth)
    
    eight = drawEight(smoothed)
    seven = eight[0:7]
    eighth = eight[7]
    
    leylines = 0
    hand_scamps = 0
    hand_heroes = 0
    hand_swifties = 0
    m_rages = 0
    insides = 0
    maws = 0
    felons = 0
    swords = 0
    lands = 0
    for c in seven:
        match c.num:
            case CardEnum.LEYLINE.value:
                leylines+=1
            case CardEnum.SCAMP.value:
                hand_scamps+=1
            case CardEnum.HERO.value:
                hand_heroes+=1
            case CardEnum.SWIFTSPEAR.value:
                hand_swifties += 1
            case CardEnum.MOUNTAIN.value:
                lands +=1
            case _:
                junk = 0
    
    if(leylines and (hand_scamps + hand_heroes + hand_swifties) and (lands)):
        return tryWithMullNoPeeking(smoothed, eight)
    
    return tryWithMullToFiveNoPeeking(smoothed)


def peekingPlusMull(smoothed):
    if(noMulls(smoothed) or tryWithMullPeeking(smoothed)):
        return True

    return tryWithMullToFivePeeking(smoothed)
    

print("NO SMOOTHING:")
total = TRIALS
wins = 0
for i in range(total):
    if(noMulls(False)):
        wins+=1
print("No mulligans: ")
print(wins/total)
print(flush=True)
 
total = TRIALS
wins = 0
for i in range(total):
    if(reasonableMulling(False)):
        wins+=1
print("Reasonable mulligans down to five: ")
print(wins/total)
print(flush=True)

total = TRIALS
wins = 0
for i in range(total):
    if(peekingPlusMull(False)):
        wins+=1
print("Clairvoyant mulligans to five: ")
print(wins/total)
print(flush=True)

print("SMOOTHING:")
total = TRIALS
wins = 0
for i in range(total):
    if(noMulls(True)):
        wins+=1
print("No mulligans: ")
print(wins/total)
print(flush=True)
 
total = TRIALS
wins = 0
for i in range(total):
    if(reasonableMulling(True)):
        wins+=1
print("Reasonable mulligans down to five: ")
print(wins/total)
print(flush=True)

total = TRIALS
wins = 0
for i in range(total):
    if(peekingPlusMull(True)):
        wins+=1
print("Clairvoyant mulligans to five: ")
print(wins/total)
