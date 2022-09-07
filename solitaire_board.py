from inspect import stack
import click
from solitaire_card_v2 import Card
from solitaire_icons import Icon
import pygame

# dictionary representing y-coordinates for cards in stacks
Y_INDEX_DICT = {
    0 : 130, 1 : 160, 2 : 190, 3 : 220, 4 : 250,
    5 : 280, 6 : 310, 7 : 340, 8 : 370, 9 : 400,
    10: 430, 11: 460, 12: 490, 13: 520, 14: 550,
    15: 580, 16: 610, 17: 640, 18: 670, 19: 700
}
# X-coordinates for each stack
X_INDEX_DICT = {
    0 : 35, 1 : 105, 2 : 175, 3 : 245, 4 : 315, 5 : 385, 6 : 455
}

# Coordinates for stock piles
STOCK_XY = (480, 30)
DEALT_XY = (410, 30)

# Coordinates for foundation piles
SP_FOUND_PILE = (20, 30)
CL_FOUND_PILE = (90, 30)
DI_FOUND_PILE = (160, 30)
HE_FOUND_PILE = (230, 30)

# pygame pre-loading images used for foundations and blank stacks
SP_ICON = pygame.image.load("solitaire_images/spade_icon.png")
CL_ICON = pygame.image.load("solitaire_images/club_icon.png")
DI_ICON = pygame.image.load("solitaire_images/diamond_icon.png")
HE_ICON = pygame.image.load("solitaire_images/heart_icon.png")

BLANK_ICON = pygame.image.load("solitaire_images/blank_icon.png")


# Primary game class, contains game board where cards are placed and moved
# Functions to manipulate and store cards all contained here
class Table():
    table = []          # where cards will mainly be played / contains 7 stacks
    down_stock = []     # extra cards to be shown one at a time, else face down
    used_stock = []     # cards dealt from down_stock placed here, face up
    sp_found = []       # SPADES foundation => end goal place all spades here increasing order (Ace -> King)
    di_found = []       # DIAMONDS foundation => end goal place all diamonds here increasing order (Ace -> King)
    he_found = []       # HEARTS foundation => end goal place all hearts here increasing order (Ace -> King)
    cl_found = []       # CLUBS foundation => end goal place all clubs here increasing order (Ace -> King)


    def __init__(self, deck, surface):
        # Takes shuffled deck of cards, adding them to piles in order
        self.create_drop_zones(surface)
        for i in range(7):
            self.table.append([])
        # iterate through deck, adding cards to stack
        # Numbering {1, 2, 3, 4, 5, 6, 7} with last card in each stack face up
        stack_count = 1
        card_count = 0
        for card in deck:
            if stack_count == 1:
                card.stack_no = 1
                card.showing = True
                card.stack_pos = card_count
                self.table[stack_count-1].append(card)
                stack_count += 1

            elif stack_count == 2:
                card.stack_no = 2
                if card_count < 2:
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][1].showing = True
                    stack_count += 1
                    card_count = 0

            elif stack_count == 3:
                card.stack_no = 3
                if card_count < 3:
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][2].showing = True
                    stack_count += 1
                    card_count = 0

            elif stack_count == 4:
                card.stack_no = 4
                if card_count < 4:
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][3].showing = True
                    stack_count += 1
                    card_count = 0

            elif stack_count == 5:
                card.stack_no = 5
                if card_count < 5:                    
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][4].showing = True
                    stack_count += 1
                    card_count = 0

            elif stack_count == 6:
                card.stack_no = 6
                if card_count < 6:
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][5].showing = True
                    stack_count += 1
                    card_count = 0
                    
            elif stack_count == 7:
                card.stack_no = 7
                if card_count < 7:
                    card.stack_pos = card_count
                    self.table[stack_count-1].append(card)
                    card_count += 1
                else:
                    card.stack_pos = card_count
                    self.table[stack_count-1][6].showing = True
                    stack_count += 1
                    card_count = 0

            else:
                card.in_stock = True
                self.down_stock.append(card)



    # CREATES BLANK HITBOXES FOR EACH SUIT FOUNDATION AND EACH STACK WHEN EMPTY
    def create_drop_zones(self, surface):
        self.SP_FOUND = Icon(SP_FOUND_PILE[0], SP_FOUND_PILE[1], surface, SP_ICON)
        self.CL_FOUND = Icon(CL_FOUND_PILE[0], CL_FOUND_PILE[1], surface, CL_ICON)
        self.DI_FOUND = Icon(DI_FOUND_PILE[0], DI_FOUND_PILE[1], surface, DI_ICON)
        self.HE_FOUND = Icon(HE_FOUND_PILE[0], HE_FOUND_PILE[1], surface, HE_ICON)

        self.EMPTY_HITBOXES = []
        # for i in range(0, 6, 1):
        #     hitbox = Icon(X_INDEX_DICT[i], Y_INDEX_DICT[0], surface, BLANK_ICON)
        #     self.EMPTY_HITBOXES.append(hitbox)

        STACK1_HITBOX = Icon(X_INDEX_DICT[0], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK1_HITBOX)
        STACK2_HITBOX = Icon(X_INDEX_DICT[1], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK2_HITBOX)
        STACK3_HITBOX = Icon(X_INDEX_DICT[2], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK3_HITBOX)
        STACK4_HITBOX = Icon(X_INDEX_DICT[3], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK4_HITBOX)
        STACK5_HITBOX = Icon(X_INDEX_DICT[4], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK5_HITBOX)
        STACK6_HITBOX = Icon(X_INDEX_DICT[5], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK6_HITBOX)
        STACK7_HITBOX = Icon(X_INDEX_DICT[6], Y_INDEX_DICT[0], surface, BLANK_ICON)
        self.EMPTY_HITBOXES.append(STACK7_HITBOX)

    
    # DRAWS BACKGROUND AND BORDERS
    def draw_board(self, surface):
        ## Testing where piles need to go
        sp_found_pile = pygame.draw.rect(surface, pygame.Color(0, 0, 0), (20, 30, 60, 80), 2)
        surface.blit(SP_ICON, (20, 30))
        cl_found_pile = pygame.draw.rect(surface, pygame.Color(0, 0, 0), (90, 30, 60, 80), 2)
        surface.blit(CL_ICON, (90, 30))
        di_found_pile = pygame.draw.rect(surface, pygame.Color(255, 0, 0), (160, 30, 60, 80), 2)
        surface.blit(DI_ICON, (160, 30))
        he_found_pile = pygame.draw.rect(surface, pygame.Color(255, 0, 0), (230, 30, 60, 80), 2)
        surface.blit(HE_ICON, (230, 30))

        down_stock_pile = pygame.draw.rect(surface, pygame.Color(0, 0, 255), (480, 30, 60, 80), 2)
        used_stock_pile = pygame.draw.rect(surface, pygame.Color(0, 0, 255), (410, 30, 60, 80), 2)

        surface.blit(BLANK_ICON, (X_INDEX_DICT[0], Y_INDEX_DICT[0]))
        stack1 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (35, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[1], Y_INDEX_DICT[0]))
        stack2 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (105, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[2], Y_INDEX_DICT[0]))
        stack3 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (175, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[3], Y_INDEX_DICT[0]))
        stack4 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (245, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[4], Y_INDEX_DICT[0]))
        stack5 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (315, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[5], Y_INDEX_DICT[0]))
        stack6 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (385, 130, 60, 80), 2)
        surface.blit(BLANK_ICON, (X_INDEX_DICT[6], Y_INDEX_DICT[0]))
        stack7 = pygame.draw.rect(surface, pygame.Color(255, 255, 255), (455, 130, 60, 80), 2)
        

    # DISPLAYS CARDS IN STACKS IN CONSOLE
    def show_stacks(self):
        # Print stacks to console
        for stack in range(len(self.table)):
            print("Stack", stack + 1, "----------------")
            for card in range(len(self.table[stack])):
                self.table[stack][card].show_card()
        print("----------")
        print("Cards in Stock:", len(self.down_stock))


    # UPDATES CARD ATTRIBUTES WITH STACK POSITIONS
    def deal_cards(self, surface):
        # Display all cards in location on game board        
        for stack in range(len(self.table)):
            for card in range(len(self.table[stack])):
                self.table[stack][card].place_card(surface, X_INDEX_DICT[stack], Y_INDEX_DICT[card])
                self.table[stack][card].stack_no = stack
                self.table[stack][card].stack_pos = card

        for card in self.down_stock:
            card.place_card(surface, STOCK_XY[0], STOCK_XY[1])

    
    # PLACES CARDS IN DEALT POSITIONS ON GAME BOARD
    def place_cards(self, surface):
        # Display all cards in location on game board
        held_card = []    # create for later check
        for stack in range(len(self.table)):
            for card in self.table[stack]:
                # Make sure last card in stack is showing
                if self.table[stack].index(card) == len(self.table[stack]) - 1:
                    card.showing = True
                if card.held:
                    held_card.append(card)
                card.place_card(surface, card.rect.x, card.rect.y)

        # place undealt stock cards
        for card in self.down_stock:
            if card.in_stock:
                card.place_card(surface, STOCK_XY[0], STOCK_XY[1])

        # place dealt stock cards
        for card in self.used_stock:
            if card.in_stock:
                card.place_card(surface, card.rect.x, card.rect.y)

        # place foundations
        for card in self.sp_found:
            card.place_card(surface, SP_FOUND_PILE[0], SP_FOUND_PILE[1])
        for card in self.cl_found:
            card.place_card(surface, CL_FOUND_PILE[0], CL_FOUND_PILE[1])
        for card in self.di_found:
            card.place_card(surface, DI_FOUND_PILE[0], DI_FOUND_PILE[1])
        for card in self.he_found:
            card.place_card(surface, HE_FOUND_PILE[0], HE_FOUND_PILE[1])

        if held_card:
            for card in held_card:
                card.place_card(surface, card.rect.x, card.rect.y)



    # DEALS A SINGLE CARD FROM STOCK, IF EMPTY, REFILLS
    def deal_stock(self, surface):
        # Deal one card from stock, removing it from stock and adding to used
        if self.down_stock:
            dealt = self.down_stock.pop()
            if dealt.in_stock:
                dealt.showing = True
                self.used_stock.append(dealt)
                dealt.update(surface, DEALT_XY)
                dealt.rect.x = DEALT_XY[0]
                dealt.rect.y = DEALT_XY[1]
            if not self.down_stock:
                # if stock pile is empty, clear visual
                pass
        elif self.used_stock:
            # reload stock
            self.reload_stock()
        else:
            print("Stock piles empty")


    # TAKES REMAINING STOCK CARDS AND PLACES THEM BACK INTO FACE DOWN PILE
    def reload_stock(self):
        # Places used stock cards back in stock in same order dealt
        for card in self.used_stock:
            card.showing = False
            self.down_stock.append(card)
        self.down_stock.reverse()
        self.used_stock.clear()


    # RETRIEVES CARD THAT IS CLICKED ON, CHECKING THAT IT IS AVAILABLE
    def new_get_clicked_card(self, click_loc):
        # check if a card is clicked on, checking that it is face up and available
        cards_clicked = []
        # clicked cards in table stacks, checking for overlap
        for stack in range(len(self.table)):
            for card in self.table[stack]:
                if card.rect.collidepoint(click_loc):
                    if card.showing:
                        cards_clicked.append(card)

        # if stock cards have been dealt, check for interaction
        if self.used_stock:
            card = self.used_stock[-1]
            if card.rect.collidepoint(click_loc):
                if card.showing and card.in_stock:
                    cards_clicked.append(card)

        if len(cards_clicked) == 0:
            return None

        # if clicking on a card with overlap, selects the topmost card
        if len(cards_clicked) == 1:
            card = cards_clicked[0]
            return card
        else:
            card1 = cards_clicked[0]
            card2 = cards_clicked[1]
            if card1.stack_pos > card2.stack_pos:
                return card1
            else:
                return card2


    # CHECKS IF WHERE A CARD IS RELEASED IS A VALID LOCATION
    def check_card_drop(self, held_card):
        # Checks drop location of held card
        # check for regular drop
        for stack in range(len(self.table)):
            # only need to check last card in each stack
            if self.table[stack]:
                dropping_on = self.table[stack][-1]

                # can't interact with card being held
                if held_card == dropping_on:
                    continue

                if (pygame.sprite.collide_rect(held_card, dropping_on) and dropping_on.showing):
                    if self.is_valid_drop(held_card, dropping_on):
                        return True, dropping_on

            elif pygame.sprite.collide_rect(held_card, self.EMPTY_HITBOXES[stack]):
                if held_card.value == 13:
                    return True, "king_" + str(stack)

        if pygame.sprite.collide_rect(held_card, self.SP_FOUND):
            valid_drop = self.add_sp_to_foundation(held_card)
            return valid_drop, "sp"
        if pygame.sprite.collide_rect(held_card, self.CL_FOUND):
            valid_drop = self.add_cl_to_foundation(held_card)
            return valid_drop, "cl"
        if pygame.sprite.collide_rect(held_card, self.DI_FOUND):
            valid_drop = self.add_di_to_foundation(held_card)
            return valid_drop, "di"
        if pygame.sprite.collide_rect(held_card, self.HE_FOUND):
            valid_drop = self.add_he_to_foundation(held_card)
            return valid_drop, "he"

        return False, None


    # RETURNS TRUE IF CARD IS OF OPPOSITE COLOR AND ONE VALUE LOWER
    def is_valid_drop(self, moving_card, target_card):
        return (target_card.value - 1) == moving_card.value and target_card.color != moving_card.color

    
    # IF NOT DROPPED IN A VALID LOCATION, SNAPS CARD STACK BACK TO ORIGINAL POSITION
    def snap_back(self, surface, card_stack):
        # Will snap to table if dropped on valid card, will snap back to original position if invalid
        for card in card_stack:
            if card.in_stock:
                card.place_card(surface, DEALT_XY[0], DEALT_XY[1])
            else:
                card.place_card(surface, X_INDEX_DICT[card.stack_no], Y_INDEX_DICT[card.stack_pos])


    # IF VALID, PLACES CARDS WHERE DROPPED AND UPDATES INFO TABLE
    def drop_cards(self, surface, stacked_cards, dropped_on):
        # from stock only one card is grabbed
        if len(stacked_cards) == 1:
            card = stacked_cards[0]
            if card.in_stock:
                card.in_stock = False
                self.used_stock.remove(card)
                self.update_table(surface, card.stack_no, dropped_on.stack_no, card)

            # out of foundation only one card is grabbed
            if card.in_found:
                card.in_found = False
                suit = card.face[-2:]
                if suit == "Sp":
                    self.sp_found.remove(card)
                elif suit == "Cl":
                    self.cl_found.remove(card)
                elif suit == "Di":
                    self.di_found.remove(card)
                elif suit == "He":
                    self.he_found.remove(card)
                self.update_table(surface, card.stack_no, dropped_on.stack_no, card)

            else:
                self.update_table(surface, card.stack_no, dropped_on.stack_no, card)

        else:
            for card in stacked_cards:
                self.update_table(surface, card.stack_no, dropped_on.stack_no, card)


    # SPECIAL DROP CASE FOR PLACING KINGS ON EMPTY STACK
    def add_to_empty(self, surface, card_stack, drop):
        king = card_stack[0]
        if king.value != 13:
            print(f"ERROR, CARD {king.face} NOT KING")
            self.snap_back(surface, card_stack)

        stack_no = int(drop[-1])

        if king.in_stock:
            self.used_stock.remove(king)
            king.in_stock = False

            self.update_table(surface, None, stack_no, king)
            return
        
        king.place_card(surface, X_INDEX_DICT[stack_no], Y_INDEX_DICT[0])
        
        
        for card in card_stack:
            self.update_table(surface, card.stack_no, stack_no, card)

    
    # SPECIAL DROP CASE FOR PLACING CARDS IN FOUNDATION
    def add_to_foundation(self, surface, card, suit):
        # places the card into foundation and updates table
        if suit == "sp":
            # places in spades
            if not card.in_stock:
                self.table[card.stack_no].remove(card)
            elif card.in_stock:
                self.used_stock.remove(card)
                
            card.in_found = True
            card.stack_no = None
            card.stack_pos = None
            card.in_stock = False

            self.sp_found.append(card)
            
            card.place_card(surface, SP_FOUND_PILE[0], SP_FOUND_PILE[1])
            self.refresh_table(surface)

        elif suit == "cl":
            # places in clubs
            if not card.in_stock:
                self.table[card.stack_no].remove(card)
            elif card.in_stock:
                self.used_stock.remove(card)
                
            card.in_found = True
            card.stack_no = None
            card.stack_pos = None
            card.in_stock = False

            self.cl_found.append(card)

            card.place_card(surface, CL_FOUND_PILE[0], CL_FOUND_PILE[1])
            self.refresh_table(surface)

        elif suit == "di":
            # places in diamonds
            if not card.in_stock:
                self.table[card.stack_no].remove(card)
            elif card.in_stock:
                self.used_stock.remove(card)

            card.in_found = True
            card.stack_no = None
            card.stack_pos = None
            card.in_stock = False

            self.di_found.append(card)

            card.place_card(surface, DI_FOUND_PILE[0], DI_FOUND_PILE[1])
            self.refresh_table(surface)

        elif suit == "he":
            # places in hearts
            if not card.in_stock:
                self.table[card.stack_no].remove(card)
            elif card.in_stock:
                self.used_stock.remove(card)
                
            card.in_found = True
            card.stack_no = None
            card.stack_pos = None
            card.in_stock = False

            self.he_found.append(card)

            card.place_card(surface, HE_FOUND_PILE[0], HE_FOUND_PILE[1])
            self.refresh_table(surface)

        else:
            print(f"Card {card.face} not valid option")
            fix = [card]
            self.snap_back(surface, fix)


    # UPDATES TABLE WITH NEW CARD INFORMATION  
    def refresh_table(self, surface):
        # updates the table with new card information
        for stack_no in self.table:
            if len(stack_no) != 0:
                last_card = stack_no[-1]
                last_card.showing = True
        self.place_cards(surface)


    # UPDATES CARDS WITH NEW LOCATIONS ON TABLE
    def update_table(self, surface, old_stack, new_stack, card):
        if old_stack or old_stack == 0:
            self.table[old_stack].remove(card)
        
        if not card in self.table[new_stack]:
            self.table[new_stack].append(card)
        card.stack_no = new_stack
        card.stack_pos = self.table[new_stack].index(card)

        card.place_card(surface, X_INDEX_DICT[card.stack_no], Y_INDEX_DICT[card.stack_pos])

        self.place_cards(surface)

              
    def add_sp_to_foundation(self, card):
        # adds card to spades foundation
        # checks for correct order
        if card.face[-2:] != "Sp":
            print("Not Spades")
            return False
        if not self.sp_found and card.face == "Ace_Sp" and card.showing:
            return True
        elif self.sp_found:
            recent_card_val = self.sp_found[-1].value
            if card.value == recent_card_val + 1:
                return True
            else:
                return False
        else:
            return False


    def add_cl_to_foundation(self, card):
        # adds card to clubs foundation
        # checks for correct order
        if card.face[-2:] != "Cl":
            print("Not Clubs")
            return False
        if not self.cl_found and card.face == "Ace_Cl" and card.showing:
            return True
        elif self.cl_found:
            recent_card_val = self.cl_found[-1].value
            if card.value == recent_card_val + 1:
                return True
            else:
                return False
        else:
            return False


    def add_di_to_foundation(self, card):
        # adds card to diamond foundation
        # checks for correct order
        if card.face[-2:] != "Di":
            print("Not Diamond")
            return False
        if not self.di_found and card.face == "Ace_Di" and card.showing:
            return True
        elif self.di_found:
            recent_card_val = self.di_found[-1].value
            if card.value == recent_card_val + 1:
                return True
            else:
                return False
        else:
            return False

    def add_he_to_foundation(self, card):
        # adds card to hearts foundation
        # checks for correct order
        if card.face[-2:] != "He":
            print("Not Hearts")
            return False
        if not self.he_found and card.face == "Ace_He" and card.showing:
            return True
        elif self.he_found:
            recent_card_val = self.he_found[-1].value
            if card.value == recent_card_val + 1:
                return True
            else:
                return False
        else:
            return False