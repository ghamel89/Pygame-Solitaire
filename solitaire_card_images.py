import sys
import pygame

class SpriteSheet:
    def __init__(self, filename) -> None:
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print("Unable to load spritesheet:", filename)
            raise SystemExit(e)

    def load_card_back(self):
        try:
            card_back = pygame.image.load("solitaire_images/card_back.png").convert()
        except pygame.error as e:
            print("Unable to load: card_back.png")
            raise SystemExit(e)

        return card_back


    def image_at(self, rectangle, colorkey=None):
        # Load specific image from specific rectangle
        # loads image from x, y, x+offset, y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    def images_at(self, rects, colorkey=None):
        # load multiple images and return as list
        return [self.image_at(rect, colorkey) for rect in rects]


    def load_strip(self, rect, image_count, colorkey=None):
        # Load strip of images and return as list
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                    for x in range(image_count)]
        return self.images_at(tups, colorkey)


    def load_grid_images(self, rows, cols, x_margin, x_padding, y_margin, y_padding):
        # Margin -> space between edge of sheet and start of cards
        # Padding -> space between cards

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # calculate size of sprites
        x_card_size = (sheet_width - 2 * x_margin - (cols - 1) * x_padding) / cols
        y_card_size = (sheet_height - 2 * y_margin - (rows - 1) * y_padding) / rows

        # print("Card Width", x_card_size)
        # print("Card Height", y_card_size)

        sprite_rects = []
        for row in range(rows):
            for col in range(cols):
                # position of sprite rect is margin + one sprite size
                x = x_margin + col * (x_card_size + x_padding)
                y = y_margin + row * (y_card_size + y_padding)
                sprite_rect = (x, y, x_card_size, y_card_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects)
        print(f"Loaded {len(grid_images)} Images")

        return grid_images