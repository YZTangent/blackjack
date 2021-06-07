"BLACKJACK: A simple game of Blackjack that can be played on the command line. Players can hit, stand, double down or all in on their hand but not split. Accomodates up to 10 players playing simultaneously against the house, but this limit can be increased."
#This is code I threw together in a few days as practice. Even though it works, please do not use it for any actual purposes lest it shits itself.

from random import *
from time import sleep


class Deck:

    SUITE = "Clubs Diamonds Hearts Spades".split()
    RANK = "2 3 4 5 6 7 8 9 10 J K Q A".split()

    # fills the deck with 52 cards upon initialisation
    def __init__(self):
        self.cards = [(i,j) for i in self.RANK for j in self.SUITE]

    def shuffle(self):
        shuffle(self.cards)
        print("The Deck Has Been Shuffled!")

    def __repr__(self):
        return str(self.cards)

    def cleardeck(self):
        self.cards = []


class Shoe(Deck):

    # adds more decks of cards to form a shoe (a stack of multiple decks in a casino)
    def adddeck(self,num):
            self.cards += [(i,j) for i in self.RANK for j in self.SUITE for k in range(num)]
            print(f'{num} fresh decks has been added into the Shoe!')


class Hand:

    # hand is the cards the player have in their hand, handvalue is the amount of points
    # bust is to check if the player has busted by having more than 21 points.
    def __init__(self):
        self.hand = []
        self.handvalue = 0
        self.bust = False

    # draws some number of cards.
    def draw_card(self, deck, cards = 1):
        self.hand.extend(deck.cards.pop(0) for i in range(cards))

    # returns hand to a clean slate for next round
    def clearhand(self):
        self.hand = []
        self.handvalue = 0
        self.bust = False

    # checks the cards in the player's hand and updates handvalue to the correct number of points.
    def numhandvalue(self):
        value = 0
        for i in self.hand:
            if i[0] == "A":
                pass
            elif i[0] in ("J", "Q", "K"):
                value += 10
            else: value += int(i[0])

        # Aces are evaluated after all other cards for the optimal score, to prevent the situation of
        # counting an ace as 11 which busts the hand when counting the ace as 1 does not.
        for j in self.hand:
            if j[0] == "A":
                if value <= 10:
                    value += 11
                else: value += 1
            else: pass

        self.handvalue = value

        #updates bust depending if the points exceed 21.
        if value > 21:
            self.bust = True


class Player(Hand):

    # sets players' starting money as $200, and gives them a bank/wallet and bet attribute.
    def __init__(self):
        super().__init__()
        self.bank = 2000
        self.bet = 0

#     def hitorstand(self, deck):
# #        hitorstand = ["Hit", "hit", "H", "h", "Stand", "stand", "S", "s"]
# #        stand = ["Stand", "stand", "S", "s"]
#         if self.handvalue <= 20:
#             hs = input("Do you want to Hit or Stand?")
#             if hs == "Hit" or hs == "hit" or hs == "H" or hs == "h":
#                 self.draw_card(deck, 1)
#                 self.numhandvalue()
#                 if handvalue <= 20:
#                     self.hitorstand()
#                 elif self.handvalue == 21:
#                     print("Your hand is worth 21 points now, a perfect score!")
#                 else: print("You have gone bust, you cannot Hit anymore!")
#             if hs == "Stand" or hs == "stand" or hs == "S" or hs == "s":
#                 return
#         elif self.handvalue == 21:
#             print("Your hand is worth 21 points now, a perfect score!")
#         else: print("You have gone bust, you cannot Hit anymore!")

    # asks the player if they want to hit (draw a card) or stand (pass)
    # draws the card and evaluates the new hand score when the player chooses to hit
    # will not allow the player to hit if his hand have 21 or more points.
    def hitorstand(self, deck):
#        hitorstand = ["Hit", "hit", "H", "h", "Stand", "stand", "S", "s"]
#        stand = ["Stand", "stand", "S", "s"]
        if self.handvalue <= 20:
            hs = input("Do you want to Hit or Stand?")
            if hs in ("Hit", "hit" , "H", "h") :
                self.draw_card(deck, 1)
                self.numhandvalue()
                print(f"You have drawn {self.hand[-1]}, and currently have {self.handvalue} points!")
                self.hitorstand(deck)
            else:
                print(f"You have chosen to stand with {self.hand} at {self.handvalue} points!")
                return
        elif self.handvalue == 21:
            print("Your hand is worth 21 points now, a perfect score!")
        else: print("You have gone bust, you cannot Hit anymore!")

    # asks the player how much they want to bet. bet amount must be between $1 and the total amount the player have.
    def setbet(self):

        # wraps the input in try except to handle non integer values
        try:
            bet = int(input(f"Please place down your bets! You currently have ${self.bank} avaliable."))

            # rejects bet if it is more than what the player have
            if bet > self.bank:
                print(f'You don\'t have enought money to put down that bet! You only have ${self.bank}!')
                self.setbet()

            # rejects bet if its less than a dollar
            elif bet < 1:
                print('You must bet at least 1 dollar!')
                self.setbet()

            # sets the bet and deducts the amount from the player's bank/wallet
            else:
                self.bank -= bet
                self.bet += bet

        except Exception:
            print("Please input a valid integer amount!")
            self.setbet()

    # doubles the player's bet.
    def doubledown(self):
        self.bank -= self.bet
        self.bet += self.bet
        print(f"You have Doubled Down! You are now betting ${self.bet} on this hand, and have ${self.bank} left!")

    # puts all the players money in the bet.
    def allin(self):
        self.bet += self.bank
        self.bank = 0
        print(f"You have All Inned! You are now betting ${self.bet} on this hand, and have ${self.bank} left!")

    # def lost(self):
    #     self.bet = 0
    #
    # def won(self):
    #     self.bank += self.bet
    #     self.bank += self.bet
    #     self.bet = 0

    def __repr__(self):
        self.numhandvalue()
        return "Your Hand is {}, and you currently have {} points!. You have betted ${} on this hand, and have ${} left!".format(str(self.hand),int(self.handvalue),int(self.bet),int(self.bank))

class House(Hand):

    # makes the house draw until they have 17 or more points.
    def autodraw(self, deck):
        while self.handvalue < 17:
            sleep(0.5)
            self.draw_card(deck, 1)
            self.numhandvalue()
            print(f"The House has drawn {self.hand[-1]}, and currently have {self.handvalue} points!")

    def __repr__(self):
        return "The House has {}, and currently have {} points!".format(str(self.hand),int(self.handvalue))

# makes the shoe by shuffling 6 decks into it.
def make_shoe():
    global shoe
    shoe = Shoe()
    # shoe.adddeck(5)
    shoe.shuffle()

# asks players for the number of players and their names, and assigns them the player object.
def make_players():

    # wraps input with try except to ensure the input is an integer
    try:
        max_players = 10
        no_of_players = int(input(f"How many players are playing today? We can take up to {max_players} players!"))

        # rejects if there are more players than the maximum stipulated
        if no_of_players > max_players:
            print(f"Sorry, we can only take up to {max_players} players!")
            make_players()

        # rejects if there is less than 1 player
        elif no_of_players < 1:
            print(f"Sorry, we need at least 1 player to start!")
            make_players()


        else:

            # adds all the inputted player names into the list
            playerlist = []
            player = input("Please input your name!")
            playerlist.append(player)
            print("Current Players: ", playerlist)


            curr_player = 1
            while curr_player < no_of_players:
                player = input(f"Please input your name! (Enter 'Start' to begin without all {no_of_players} players!)")

                # rejects name if its a duplicate
                if player in playerlist:
                    print("Your name cannot be the same as another player's!")

                # rejects empty string as name
                elif player == "":
                    print("Please input a non-empty name!")

                # starts game with less players than declared
                elif player in ("Start", "start", "S", "s"):
                    print("Current Players: ", playerlist)
                    break


                else:
                    playerlist.append(player)
                    curr_player +=1
                    print("Current Players: ", playerlist)

            # loops through the list of player names to assign each player name a Player object in a dictionary
            # the key is the player name and the associated value is the Player object
            global pd
            pd = {}
            for players in playerlist:
                pd[players] = Player()
            global house
            house = House()

    except Exception:
        print("Please input a valid number of players!")
        make_players()

def game():
    print("Welcome to the game of Blackjack! Aim for 21, or go bust trying! Good luck, and have fun! ;)")

    # removes the first card as per blackjack rules
    shoe.cards.pop(0)

    # sets the counter for the number of rounds
    round = 1

    # removes the last 20 to 40 cards of the shoe, so the game ends slightly before the shoe runs out
    cut = randrange(20, 40)
    while len(shoe.cards) > cut:
        print(f'Round {round} is starting. Please place your bets.')

        # loops through all players and ask them to place their bets for the round
        for players in pd:
            sleep(0.5)
            print(f"Player {players}'s turn:")
            pd[players].setbet()
        sleep(0.5)
        print("The bets are placed. Dealing cards.")

        # loop through all players and deals them their cards, and evaluate their points
        for players in pd:
            pd[players].draw_card(shoe, 2)
            pd[players].numhandvalue()

        # the house draws 2 cards and evaluate their points
        house.draw_card(shoe, 2)
        house.numhandvalue()

        sleep(0.5)
        print("The cards are dealt.")

        # loops through each player to ask them if they want to double down, all in or hit or stand.
        # players who doubled down or all inned cannot hit (draw cards) anymore as per rules.
        for players in pd:
            sleep(0.5)

            # displays the relevant info for player to make a decision.
            print(f"Player {players}'s turn:'")
            print(pd[players])
            print(f"The House's hand is {house.hand[0]} and a hidden card.")

            # ask player if they want to all in or double down if they have the money to.
            if pd[players].bank >= pd[players].bet:
                choice = str(input("Do you want to Double Down on your hand, or go ALL IN? Please bear in mind you cannot hit after you do so."))
                if choice in ("double", "Double", "Double Down", "double down", "d", "D"):
                    pd[players].doubledown()
                elif choice in ("ALL IN", "All In", "all in", "all", "a", "A"):
                    pd[players].allin()
                else:
                    pd[players].hitorstand(shoe)

            # ask player if they want to all in if they have the money to, but not enough to double down.
            elif pd[players].bank > 0:
                choice = str(input("Do you want to go ALL IN? Please bear in mind you cannot hit after you do so."))
                if choice in ("ALL IN", "All In", "all in", "all", "a", "A", "Yes", 'yes', "Y", "y"):
                    pd[players].allin()
                else:
                    pd[players].hitorstand(shoe)

            # directly ask the player to hit or stand if they have no money left.
            else:
                    pd[players].hitorstand(shoe)

        # after every player's turn, the house now reveals his hidden card and draws until 17 or above.
        sleep(0.5)
        print("The Players have finished their turn. The House will now reveal his cards.")
        print(house)
        if house.handvalue < 17:
            sleep(0.5)
            print("The House will now draw until their hand values at 17 or above.")
            house.autodraw(shoe)

        # initialises a list to contain all players who ran out of moeny, and removes them from the game at the end of the round.
        # this is because the players cannot be removed while still looping through the dictionary of players.
        out_players = []

        # rewards all players who did not go bust if the house goes bust.
        # clears the player's hand after its been evaluated
        if house.bust:
            print("The House has gone bust! All players who did not go bust will win!")
            for players in pd:
                if pd[players].bust == False:
                    earnt = pd[players].bet*2
                    pd[players].bank += earnt
                    print(f"{players} won ${pd[players].bet} and now have ${pd[players].bank}.")
                    pd[players].bet = 0
                    pd[players].clearhand()
                else:
                    print(f"{players} lost as he has gone bust. All his bets are lost and he have ${pd[players].bank} left.")
                    pd[players].bet = 0
                    pd[players].clearhand()
                    if pd[players].bank == 0:
                        print("With no money left, you're out of the game! Better luck next time!")
                        out_players.append(players)


        # checks players hand against the house, and gives/take away money accordingly
        # clears the player's hand after its been evaluated
        else:
            for players in pd:
                sleep(0.5)
                print(f"Evaluating Player {players}'s bet:")

                if pd[players].bust:
                    print(f"You went bust! All your bets are lost :( You have ${pd[players].bank} left!")
                    pd[players].bet = 0
                    pd[players].clearhand()
                    if pd[players].bank == 0:
                        print("With no money left, you're out of the game! Better luck next time!")
                        out_players.append(players)

                elif pd[players].handvalue > house.handvalue:
                    earnt = pd[players].bet*2
                    pd[players].bank += earnt
                    print(f"You won! You won ${pd[players].bet} and you now have ${pd[players].bank}!")
                    pd[players].bet = 0
                    pd[players].clearhand()
                    
                elif pd[players].handvalue < house.handvalue:
                    print(f"The House beat you with {house.handvalue} points to your {pd[players].handvalue} points! All your bets are lost :( You have ${pd[players].bank} left!")
                    pd[players].bet = 0
                    pd[players].clearhand()
                    if pd[players].bank == 0:
                        print("With no money left, you're out of the game! Better luck next time!")
                        out_players.append(players)

                elif pd[players].handvalue == house.handvalue:
                    pd[players].bank  += pd[players].bet
                    pd[players].bet = 0
                    pd[players].clearhand()
                    print(f"You tied with the House at {house.handvalue} points! Your bet is returned to you and you have ${pd[players].bank} left!")


        # remove all players who have ran out of money
        for players in out_players:
            del pd[players]
        out_players.clear()


        # ends the game if all players have ran out of money
        if len(pd) == 0:
            print("The game is over! All players have gone bust.")
            break

        # clears the house's hand
        house.clearhand()

        # waits for the user to confirm before going to the next round.
        go_on = input(f"Round {round} is over! Press any key to continue.")
        round += 1

        # if the cards are running out, the players are asked if they want to continue playing
        if len(shoe.cards) <= cut:
            print("We have ran out of cards and reached the end of the game!")
            cont = input("Input \"Yes\" if you want to continue the game")

            # if the players want to continue, more cards are added to the deck and it is shuffled again
            if cont in ("Yes", "yes", "Y", "y"):
                shoe.cleardeck()
                shoe.adddeck(6)
                shoe.shuffle()

            # if not, the game ends
            else:
                print("We have come to the end of the game, thank you for playing!")

if __name__ == '__main__':
    make_shoe()
    make_players()
    game()
