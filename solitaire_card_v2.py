import pygame

class Card(pygame.sprite.Sprite):
    face = ""               # Main identifier of card (ie, Ace of Spades, 2 of Clubs, etc)
    color= ""               # Secondary identifier of card (Black or Red)
    showing = False         # Bool, is card face up (True) or down (False)
    value = None            # For checking position, integer representation of rank (1 - 13)
    face_image = None       # Contains image for displaying face of card
    back_image = None       # Contains image for displaying back of card
    in_stock = False        # Bool, Locator, True if card is in either stock pile
    in_found = False        # Bool, Locator, True if card has been moved to foundation
    stack_no = None         # Int, Locator, Contains number of stack card is found in
    stack_pos = None        # Int, Locator, Contains position of card within stack
    held = False            # Bool, signals if card is being held by player
    

    # Construct card
    def __init__(self, face, face_image, back_image):

        # construct parent class
        pygame.sprite.Sprite.__init__(self)

        # save images for later display
        self.face = face
        self.face_image = face_image
        self.back_image = back_image
        self.rect = None

        # convert face value to int
        card_value = face[0]
        if card_value == "A":
            self.value = 1
        elif card_value == "1":
            self.value = 10
        elif card_value == "J":
            self.value = 11
        elif card_value == "Q":
            self.value = 12
        elif card_value == "K":
            self.value = 13
        else:
            self.value = int(card_value)

        # determine color from suit
        if face[-2:] == "Di" or face[-2:] == "He":
            self.color = "red"
        else:
            self.color = "black"

    
    # UPDATES MOVING POSITION OF CARD
    def update(self, surface, loc):
        self.rect.move_ip(loc)
        if self.showing:
            surface.blit(self.face_image, self.rect)


    # FINALIZES CARD PLACEMENT ON GAME BOARD
    def place_card(self, surface, x, y):
        if self.rect:
            self.rect.x = x
            self.rect.y = y
            if self.showing:
                surface.blit(self.face_image, self.rect)
            else:
                surface.blit(self.back_image, self.rect)
        else:
            if self.showing:
                self.rect = self.face_image.get_rect()
                self.rect.x = x
                self.rect.y = y
                surface.blit(self.face_image, self.rect)
            else:
                self.rect = self.back_image.get_rect()
                self.rect.x = x
                self.rect.y = y
                surface.blit(self.back_image, self.rect)

    
    # TEST FUNCTION TO PRINT CARD FACE VALUE TO CONSOLE
    def show_card(self):
        # Check if card is face up or down
        # if face up print identity to console, else print face down
        if self.showing:
            print("Card is", self.face, end=", ")
        else:
            print("Card is Face Down", end=", ")