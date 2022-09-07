import random
import time
import pygame
import unittest
from solitaire_card_v2 import Card
from solitaire_card_images import SpriteSheet
from solitaire_board import Table
from solitaire_icons import Icon

RUN_MODE = 1                 # Mode changer (1 -> runs main() // else -> runs unittests())

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 800
FPS = 30

SPADES = ['Ace_Sp', '2_Sp', '3_Sp', '4_Sp', '5_Sp', '6_Sp', '7_Sp', '8_Sp', '9_Sp', '10_Sp', 'J_Sp', 'Q_Sp', 'K_Sp']
CLUBS = ['Ace_Cl', '2_Cl', '3_Cl', '4_Cl', '5_Cl', '6_Cl', '7_Cl', '8_Cl', '9_Cl', '10_Cl', 'J_Cl', 'Q_Cl', 'K_Cl']
DIAMONDS = ['Ace_Di', '2_Di', '3_Di', '4_Di', '5_Di', '6_Di', '7_Di', '8_Di', '9_Di', '10_Di', 'J_Di', 'Q_Di', 'K_Di']
HEARTS = ['Ace_He', '2_He', '3_He', '4_He', '5_He', '6_He', '7_He', '8_He', '9_He', '10_He', 'J_He', 'Q_He', 'K_He']

DECK = SPADES + HEARTS + CLUBS + DIAMONDS


def gameLoop(surface, gameTable):
    clock = pygame.time.Clock()
    running = True
    click = (0, 0)
    grabbed_card = None
    printOnce = False
    card_group = pygame.sprite.Group()
    card_stack = []
    while running:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # holding_card, stack, index = gameTable.get_card_under_mouse(surface)
                grabbed_card = gameTable.new_get_clicked_card(event.pos)
                if grabbed_card and grabbed_card.showing:
                    if grabbed_card.in_found or grabbed_card.in_stock:
                        grabbed_card.held = True
                        card_group.add(grabbed_card)
                        card_stack.append(grabbed_card)
                        continue
                    grabbed_card.held = True
                    card_group.add(grabbed_card)
                    card_stack.append(grabbed_card)
                    if not grabbed_card.in_stock or not grabbed_card.in_found:
                        for card in gameTable.table[grabbed_card.stack_no][grabbed_card.stack_pos:]:
                            if card in card_stack:
                                continue
                            card_group.add(card)
                            card_stack.append(card)
                        for card in card_stack:
                            card.held = True
                click = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if grabbed_card:
                    # check drop position is on top of another card
                    is_valid, dropped_on = gameTable.check_card_drop(grabbed_card)

                    if not is_valid:
                        gameTable.snap_back(surface, card_stack)
                    elif is_valid and len(card_stack) == 1 and (dropped_on in ["sp", "cl", "di", "he"]):
                        if len(card_stack) == 1:
                            gameTable.add_to_foundation(surface, grabbed_card, dropped_on)
                        elif grabbed_card != gameTable.table[grabbed_card.stack_no][-1]:
                            gameTable.snap_back(surface, card_stack)
                        else:
                            gameTable.snap_back(surface, card_stack)
                    elif is_valid and type(dropped_on) is Card:
                        gameTable.drop_cards(surface, card_stack, dropped_on)
                    elif is_valid and dropped_on[:4] == "king":
                        gameTable.add_to_empty(surface, card_stack, dropped_on)
                        

                    for card in card_stack:
                        card.held = False
                    grabbed_card = None
                    card_group.empty()
                    card_stack = []
                    dropped_on = None

            if event.type == pygame.MOUSEMOTION and grabbed_card:
                card_group.update(surface, event.rel)
    

        if 480 < click[0] < 540 and 110 > click[1] > 30:
            gameTable.deal_stock(surface)

        click = (0, 0)
        clock.tick(FPS)

        # Redraw Game Board
        surface.fill(pygame.Color(9, 200, 38))
        gameTable.draw_board(surface)
        gameTable.refresh_table(surface)
        gameTable.place_cards(surface)
        
        pygame.display.flip()


def main():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Solitaire")
    surface.fill(pygame.Color(9, 200, 38))
    deck_sheet = SpriteSheet("solitaire_images/card_sprite_sheet.png")



    card_images = deck_sheet.load_grid_images(4, 13, 0, 1, 0, 1)
    card_back = deck_sheet.load_card_back()
    # spades_cards = card_images[:13]     # cards from 0-12  -> 13 cards
    # clubs_cards = card_images[13:27]    # cards from 13-26 -> 13 cards
    # diamond_cards = card_images[27:40]  # cards from 27-39 -> 13 cards
    # heart_cards = card_images[40:52]    # cards from 40-52 -> 13 cards

    # seed = 0xFEEB
    # random.seed(seed)
    table_shuffle = []
    card_counter = 0
    for card in DECK:
        temp = Card(card, card_images[card_counter], card_back)
        card_counter += 1
        table_shuffle.append(temp)

    random.shuffle(table_shuffle)

    gameTable = Table(table_shuffle, surface)
    #gameTable.show_stacks()
    gameTable.deal_cards(surface)

    gameLoop(surface, gameTable)
    



################################################## UNITTESTS ##################################################

class SolitaireDeckFunctionsTestCases(unittest.TestCase):
    def setUp(self):
        self.seed = 0xFEEB
        self.deck = DECK
        

    def test_a_deck_shuffled(self):
        random.seed(self.seed)
        random.shuffle(self.deck)
        # print(self.deck)          # grab seed shuffle for testing
        self.assertEqual(self.deck, ['K_Sp', '8_Di', '4_Cl', '3_Di', '7_He', 'J_Sp', 'J_Di', '5_Cl',
                                    '10_Di', '2_Sp', '3_Cl', '4_Di', 'Ace_Cl', 'Q_Di', '10_Cl', '5_Sp', 
                                    '8_Cl', '10_He', '3_He', '7_Cl', '2_Di', 'K_Cl', '10_Sp', '5_He', '4_He', 
                                    '8_Sp', 'Ace_Sp', 'J_Cl', '6_Di', 'Ace_He', '9_Sp', '7_Sp', 'J_He', '6_Cl', 
                                    '9_He', '8_He', 'Ace_Di', '9_Di', '9_Cl', '6_Sp', '7_Di', '5_Di', 'Q_Sp', 
                                    '6_He', 'K_He', '2_Cl', '3_Sp', 'Q_Cl', 'Q_He', 'K_Di', '4_Sp', '2_He'])

    def test_b_card_object(self):
        random.seed(self.seed)
        card_shuffle = []
        for card in self.deck:
            temp = Card(card)
            card_shuffle.append(temp)

        for card in card_shuffle:
            self.assertIsInstance(card, Card)


    def test_c_card_value(self):
        card_deck = []
        
        for card in SPADES:
            temp = Card(card)
            card_deck.append(temp)

        for card_no in range(len(SPADES)):
            self.assertEqual((card_no + 1), card_deck[card_no].value)


    @unittest.skip  # Comment out to test 'd' leave to test 'e'
    def test_d_create_gameTable(self):        
        random.seed(self.seed)
        table_shuffle = []
        for card in self.deck:
            temp = Card(card)
            table_shuffle.append(temp)

        gameTable = Table(table_shuffle)
        self.assertEqual(len(gameTable.table), 7)

        # gameTable.show_stacks()

        for stackNo in range(len(gameTable.table)):
            if stackNo == 0:
                self.assertEqual(gameTable.table[stackNo][0].face, "K_Sp")
                self.assertTrue(gameTable.table[stackNo][0].showing)
            elif stackNo == 1:
                self.assertEqual(gameTable.table[stackNo][1].face, "4_Di")
                self.assertTrue(gameTable.table[stackNo][1].showing)
            elif stackNo == 2:
                self.assertEqual(gameTable.table[stackNo][2].face, "J_He")
                self.assertTrue(gameTable.table[stackNo][2].showing)
            elif stackNo == 3:
                self.assertEqual(gameTable.table[stackNo][3].face, "4_He")
                self.assertTrue(gameTable.table[stackNo][3].showing)
            elif stackNo == 4:
                self.assertEqual(gameTable.table[stackNo][4].face, "10_Cl")
                self.assertTrue(gameTable.table[stackNo][4].showing)
            elif stackNo == 5:
                self.assertEqual(gameTable.table[stackNo][5].face, "4_Cl")
                self.assertTrue(gameTable.table[stackNo][5].showing)
            elif stackNo == 6:
                self.assertEqual(gameTable.table[stackNo][6].face, "J_Cl")
                self.assertTrue(gameTable.table[stackNo][6].showing)
            else:
                print("end else")


    def test_e_stack_index(self):
        random.seed(self.seed)
        table_shuf = []
        for card in self.deck:
            temp = Card(card)
            table_shuf.append(temp)

        stack_table = Table(table_shuf)
        self.assertEqual(stack_table.table[6][0].stack_pos, 0)
        self.assertEqual(stack_table.table[6][1].stack_pos, 1)
        self.assertEqual(stack_table.table[6][2].stack_pos, 2)
        self.assertEqual(stack_table.table[6][3].stack_pos, 3)
        self.assertEqual(stack_table.table[6][4].stack_pos, 4)
        self.assertEqual(stack_table.table[6][5].stack_pos, 5)
        self.assertEqual(stack_table.table[6][6].stack_pos, 6)

        

    #@unittest.skip                 # UnComment to view console easier
    def test_f_deal_stock(self):
        # works when previous test is removed, problem with creating multiple 'Table' instances
        random.seed(self.seed)
        stock_shuffle = []
        for card in self.deck:
            temp = Card(card)
            stock_shuffle.append(temp)

        stockTable = Table(stock_shuffle)
        self.assertEqual(len(stockTable.table), 7)
        self.assertEqual(len(stockTable.down_stock), 18)
        self.assertEqual(len(stockTable.used_stock), 0)

        # deal one
        stockTable.deal_stock()
        self.assertEqual(len(stockTable.down_stock), 17)
        self.assertEqual(len(stockTable.used_stock), 1)

        # deal all
        for i in range(17):
            stockTable.deal_stock()

        self.assertEqual(len(stockTable.down_stock), 0)
        self.assertEqual(len(stockTable.used_stock), 18)

        # reset
        stockTable.deal_stock()
        self.assertEqual(len(stockTable.down_stock), 18)
        self.assertEqual(len(stockTable.used_stock), 0)


if __name__ == "__main__":
    # version changer:
    if RUN_MODE == 1:
        main()
    else:
        unittest.main(verbosity=2)
    