# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
outcome2 = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos, back):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if back :
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_BACK_SIZE)
        else :
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        for card in self.cards :
            print card[0]       

    def add_card(self, card, back=False):
        self.cards.append([card,back])      

    def get_value(self):
        val = 0
        a = False
        for card in self.cards :
            if card[0].get_rank() == 'A' :
                a = True
            val += VALUES[card[0].get_rank()]
        if a :
            if val + 10 <= 21 :
                return val + 10
        return val
    
    def draw(self, canvas, pos):
        for card in self.cards :
            card[0].draw(canvas, pos, card[1])
            pos[0] += 70 
        
class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS :
            for r in RANKS :
                self.cards.append(Card(s, r))
        
    def shuffle(self):
        random.shuffle(self.cards)        

    def deal_card(self):
        return self.cards.pop()       
    
    def __str__(self):
        print 'len Deck',len(self.cards)
        
    def draw(self, canvas, pos):
        for card in self.cards :
            card.draw(canvas, pos, True)
            pos[1] += 3 
        


#define event handlers for buttons
def deal():
    global outcome, outcome2, in_play, score, Player, Computer, Allcard
    if in_play :
        score -= 1
        outcome2 = 'you lost the round'
    else :
        outcome2 = ''
        
    if len(Allcard.cards) < 26 :
        Allcard = Deck()        
    Allcard.shuffle()    
    Player = Hand()
    Computer = Hand()
    Computer.add_card(Allcard.deal_card(),True)
    Player.add_card(Allcard.deal_card())
    Computer.add_card(Allcard.deal_card())
    Player.add_card(Allcard.deal_card())
    
    outcome = 'Hit or stand?'
    in_play = True

def hit():
    global score, outcome, outcome2, in_play
    if in_play :
        if Player.get_value() <= 21 :
            Player.add_card(Allcard.deal_card())
            
            if Player.get_value() > 21 :
                score -= 1
                Computer.cards[0][1] = False
                outcome = 'new deal?'
                outcome2 = 'You have busted and lose'
                in_play = False
   
def stand():
    global score, in_play, outcome, outcome2
    if in_play :
        in_play = False        
        Computer.cards[0][1] = False
        while Computer.get_value() < 17 :
            Computer.add_card(Allcard.deal_card())           
         
        if Player.get_value() <= Computer.get_value() <= 21 :
            score -= 1
            outcome2 = 'you lose'            
        elif Computer.get_value() > 21 \
        or Computer.get_value() < Player.get_value() :
            score += 1
            outcome2 = 'you win'
            
        outcome = 'new deal?'
             
# draw handler    
def draw(canvas):
    Allcard.draw(canvas, [450,150])
    Player.draw(canvas, [100,400])
    Computer.draw(canvas, [100,200])
  
    canvas.draw_text('Blackjack', (150, 100), 42, 'black')
    canvas.draw_text('Dealer', (100, 179), 35, 'black')
    canvas.draw_text(outcome2, (300, 179), 25, 'black')
    canvas.draw_text('Player', (100, 380), 35, 'black')
    canvas.draw_text(outcome, (300, 380), 25, 'black')
    canvas.draw_text('score: ' + str(score), (400, 100), 35, 'white')


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
Allcard = Deck()
deal()
frame.start()

