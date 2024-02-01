import pygame
import random

class Kuromi(pygame.sprite.Sprite):
    def __init__(self, kuromi_size,x,y, screen_size, platform_group):
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize Cinny attributes
        self.kuromi_size = kuromi_size
        self.image_dash_r = pygame.transform.scale(
            pygame.image.load("images\KuromiRigth.png"),
            kuromi_size
        )
        self.image_dash_l = pygame.transform.scale(
            pygame.image.load("images\KuromiLeft.png"),
            kuromi_size
        )
        self.image = self.image_dash_r
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.screen = pygame.display.get_surface()
        self.dx = 0
        self.dy = 0
        self.direction_change_interval = 1600  # Интервал времени в миллисекундах (например, 2000 мс = 2 секунды)
        self.last_direction_change_time = pygame.time.get_ticks()
        self.direction = random.choice(["left", "right"])
        

    def KuromiMovements(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_direction_change_time >= self.direction_change_interval:
            self.last_direction_change_time = current_time
            if self.direction == "left":
                self.image = self.image_dash_l
                self.dx = -self.kuromi_size[1] / 6
                self.direction = "right"
            else:
                self.image = self.image_dash_r
                self.dx = self.kuromi_size[1] / 6
                self.direction = "left"
                
        
        self.rect.move_ip(self.dx, self.dy)

   
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        

