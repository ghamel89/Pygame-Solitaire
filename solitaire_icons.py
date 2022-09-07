import pygame

# Class to display background images with hitboxes
class Icon(pygame.sprite.Sprite):
    image = None

    def __init__(self, x, y, surface, image=None):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        surface.blit(self.image, self.rect)