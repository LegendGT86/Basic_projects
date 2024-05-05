# Card
# Suit,Rank,Value
from random import shuffle
from IPython.display import clear_output

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
class Card:
    
    def __init__(self,suits,ranks):
        self.suit = suits
        self.rank = ranks
        self.value = values[ranks]
        
    def __str__(self):
        return self.rank + " of " + self.suit
class Deck:
    
    def __init__(self):
        self.full_deck = []
        
        for suit in suits:
            for rank in ranks:
                self.full_deck.append(Card(suit,rank))
                
    def shuffle_it(self):
        shuffle(self.full_deck)
        
    def deal_one(self):
        return self.full_deck.pop()    
    
    def opening_deal(self):
        opening = []
        for x in range(0,2):
            opening.append(self.full_deck.pop(x))
        return opening
    
    def __str__(self):
        deck_pack = ''
        for card in self.deck:
            deck_pack += '\n' + card.__str__()
            return "Total deck: " + deck_pack
           
 
class Player():
    
    def __init__(self,name):
        self.name = name        
        self.wallet = 100
        self.hand = []
        self.hand_value = 0
        self.aces = 0
        
    def raise_value(self):
        print(f' Your current balance is {self.wallet}')
        while True:
            amount = int(input("Please select your raise amount :"))
            if amount > self.wallet :
                print(f' Im sorry but that bet is {amount - self.wallet} over your available funds')
            else:
                self.wallet = self.wallet - amount
                return amount
                break
                
    def hit_stand(self):
        while True:
            hit_stand = input("do you want to hit or stand (H or S)").lower().strip()
            if hit_stand == 'h':
                return 'h'
            elif hit_stand == 's':
                return 's'
            elif hit_stand != 'h' or 's':
                print("Sorry, that is an invalid input, select h (hit) or s (stand)")
        
    # Will be called to show the player/ dealers hand after he/she/bot has 'hit' and thus added another card to their hand
    def updated_hand(self):
        for i in range(0,len(self.hand)):
            print(Card(self.hand[i].suit,self.hand[i].rank))
            
    # Will not only determine ace value , but adjust the hands final value to be displayed during the game for player reference
    def aces_high(self):
        for i in range(0,len(self.hand)):
            self.hand_value += values[self.hand[i].rank]
            
        while self.hand_value > 21 and self.aces > 0:
            self.hand_value -= 10
            self.aces -= 1
        return self.hand_value
class Progress_Checker:
    
    def status(curr_value):
                
        if curr_value > 21:
            return "bust"
        elif curr_value == 21:
            return "BlackJack 21 winner"
        else:
            return "proceed"  
        
    def replay():
        while True:
            continuation = input("Do you want to deal another hand: Y or N").lower().strip()
            if continuation == 'y':
                return 'y'
            elif continuation == 'n':
                return 'n'
            else:
                print('That is an invalid option, please select Y or N')                        
# The final board

pot = 0
player_name = input("please enter your name")
player1 = Player(player_name)  
dealer = Player("dealer")
deck = Deck()
redeal = True

while redeal:  
    status = ''
    play_on = True
    game_start = True
    h_value_player = 0
    h_value_dealer = 0
    
    while game_start:
        deck.shuffle_it()
        player1.hand.clear()
        dealer.hand.clear()
        player1.hand.extend(deck.opening_deal())
        dealer.hand.extend(deck.opening_deal())
        print(f'{player_name} s hand: {player1.hand[0]} , {player1.hand[1]}')
        print(f'hand value: {player1.aces_high()}')
        print(f'Dealers hand: {dealer.hand[0]} and X')
    
        while play_on == True:
            choice = player1.hit_stand() 
            if choice == 'h':
                pot += player1.raise_value()
                player1.hand.append(deck.deal_one())
                player1.updated_hand()
                h_value_player = player1.aces_high()
                status = Progress_Checker.status(h_value_player)
    
                if  status == 'bust':
                    print (f'the current status for player is: {status}')
                    pot = 0
                    game_start = False
                    break
                
                elif status == 'winner':
                    print (f'the current status for player is: {status}')
                    player1.wallet += pot
                    game_start = False
                    break                
                
            elif choice == 's':
                play_on = False
                status == ''
                

            
        while play_on == False:
            h_value_dealer = dealer.aces_high
            status = Progress_Checker.status(h_value_dealer)
            print(f'hand value: {h_value_dealer}')
            print (f'the current status for bot is: {status}')
        
            if  status == 'bust':
                game_start = False
                print(f'dealer hand value: {h_value_dealer} and is {status}')
                break
                
            elif status == 'winner':
                game_start = False
                print(f'dealer hand value: {h_value_dealer} and is {status}')
                break   
            
            elif num_value_dealer > 17:
                game_start = False
                print(f'dealer hand value: {h_value_dealer}')
                break
            
            else:
                dealer.hand.append(deck.deal_one())
    
    if h_value_dealer > 21:
        print ("Dealer Busts, Player wins")
    elif h_value_player > 21:
        print ("Player Busts, Dealer wins")
    else:
        
        if h_value_dealer > h_value_player:
            print (f'Dealer wins with a card count of {h_value_dealer} to {h_value_player}')
        elif h_value_dealer < h_value_player:
            print (f'{player1.name} wins with a card count of  {h_value_player} to dealers {h_value_dealer}')
        elif h_value_dealer == h_value_player:
            print("We have a draw")
        #A draw will result in only 50% of bet repaid to player
            player1.wallet += pot/2
        
    #Does the player want to go another round
    if player1.wallet !=0:
        
        if Progress_Checker.replay() == 'n':
            redeal = False
            break
        
        elif Progress_Checker.replay() == 'y':
            clear_output()
            pot = 0
            print("new deal beginning")
            
    else:
        print("Sorry, you're broke, back to the slot machines for you!")
        
            
if __name__ == '__main__':
    Deck()

 