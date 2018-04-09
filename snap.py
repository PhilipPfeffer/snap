# SNAP! A test for 9fin. 07/04/2018 Phil Pfeffer
'''
This is a game of SNAP! The rules are written in the welcome() method below.
'''

import random
from pynput.keyboard import Key, Listener
from collections import deque



# Playing card Class: each card has a rank and a suit.
class Card:
    def __init__(self, suit, rank):
        self.s = suit
        self.r = rank
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            getattr(other, 's', None) == self.s and
            getattr(other, 'r', None) == self.r)
        
    def __hash__(self):
        return hash(self.s + str(self.r))
      


# Global Variables      
suits = {'H','D','C','S'}
cardMaxVal = 13
numPlayers = 2
oneDeck = [Card(s,r) for s in suits for r in range(1,cardMaxVal+1)]
playerDecks = {}
snapPot = []
playerTurn = False 


# Welcome messages and rules
def welcome():
    print("Welcome to Snap! Let's have a little fun.")
    print("""Here are the rules:
          1. All of the cards are shuffled and dealt equally to both players.
          2. Then each player in turn QUICKLY turns over the top card from their 
             face down dealt pile and puts it on top of their face up pile.
          3. When someone turns over a card that matches a card on top of another 
             player's face up pile,the players race to be the first to say 'Snap!'
          4. The player who says “Snap!” first wins both piles and adds them to 
             the bottom of his face down pile.
          5. If more than one player says “Snap!” at the same time, the two 
             piles are combined into the snap pot.
          6. Whoever wins the next snap wins the whole pot.
          7. The player who wins all the cards wins the game.
          ____________________________________________________________________
          
          Controls:
          Left Player Flip Card: Left 'shift' Key
          Left Player Snap: Left 'option' or 'alt' Key
          Right Player Flip Card: Right 'shift' Key
          Right Player Snap: Right 'option' or 'alt' Key""")
          


# Randomly distributes cards to players from the desired number of decks
def initDecks():
    while True:
        try:
            deckNum = int(input("How many card decks would you like to use? "))
        except ValueError:
           print("Please enter an integer.")
           continue
        else:
           break
   
    # Composite deck made from deckNum 52-card decks
    fullDeck = []
    for num in range(deckNum):
        fullDeck.extend(oneDeck)
    totalCards = len(fullDeck)
    
    # Distribute the cards to the players randomly
    for player in range(1,numPlayers+1):
        playerName = input("Player " + str(player) + " name: ")
        for cards in range(int(totalCards/numPlayers)):
            randCard = fullDeck.pop(random.randint(0,len(fullDeck)-1))
            global playerDecks
            playerDecks.setdefault(playerName,list())
            playerDecks[playerName] = playerDecks[playerName] + [randCard]
            
    print("Player to the left goes first!")
    return playerDecks




# Initialises a game of Snap!
if __name__ == "__main__":
    welcome()
    playerDecks = initDecks()



# Print, remove and return the top card from the player's deck
def flipCard(playerName):
    cardQueue = deque(playerDecks[playerName])
    if not cardQueue:
        return 0
    else:
        playerCard = cardQueue.popleft()
    playerDecks[playerName] = list(cardQueue)
    print("New Top Card: " + str(playerCard.r) + " " + playerCard.s)
    return playerCard


# Adds snap cards to player who called a valid snap
def snap(playerName):
    if len(snapPot) < 2:
        print("There are fewer than two cards in the pot.")
    elif snapPot[len(snapPot)-1].r == snapPot[len(snapPot)-2].r:
        print("Snap for " + playerName + "!")
        playerDecks[playerName] = playerDecks[playerName] + snapPot
        snapPot.clear()
    else:
        print("Careful with those trigger fingers, that's an invalid snap!")

        
        
# Card flips and snaps executed depending on key pressed
def on_press(key):
    global winnerName 
    global winner
    global snapPot
    global playerTurn
    nameList = list(playerDecks.keys())
    nameList.sort()
    player1Name = nameList[0]
    player2Name = nameList[1]
    
    # Player 1
    if key == Key.shift_r and playerTurn:
        playerTurn = False
        topCard = flipCard(player1Name)
        if topCard == 0:
            winnerName = player1Name
            print(player2Name + " wins!")
            return False
        else:
            snapPot += [topCard]
    elif key == Key.alt_r:
        snap(player1Name)
        
    # Player 2
    elif key == Key.shift and not playerTurn :
        playerTurn = True
        topCard = flipCard(player2Name)
        if topCard == 0:
            winnerName = player2Name
            print(player1Name + " wins!")
            return False
        else:
            snapPot += [topCard]
    elif key == Key.alt:
        snap(player2Name)


# Collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()





    
        
    

