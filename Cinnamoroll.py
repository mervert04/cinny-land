import pygame
from pygame import Rect
fire_image = pygame.image.load('images/fire.png')

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        # Scale the platform image to the specified width and a fixed height
        self.image = pygame.transform.scale(fire_image, (width, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y+15
        self.dx =x
        self.dy =y

class Zamok(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Scale the platform image to the specified width and a fixed height
        self.image = pygame.transform.scale(pygame.image.load("images\zamok.png"),(280,280))
        self.rect = self.image.get_rect()
        self.rect.x = x-160
        self.rect.y = y-370
  

class Cinny(pygame.sprite.Sprite):
    # Class attribute for game over state
    game_over = False
    game_win = False
    score = 0

    def __init__(self, cinny_size, screen_size, platform_group,candy_group,kuromi,zamok_x,zamok_y):
        pygame.sprite.Sprite.__init__(self)
        
        # Initialize Cinny attributes
        self.cinny_size = cinny_size
        self.image_dash_r = pygame.transform.scale(
            pygame.image.load("images\CinnamorollRight32.png"),
            cinny_size
        )
        self.image_dash_l = pygame.transform.scale(
            pygame.image.load("images\CinnamorollLeft32.png"),
            cinny_size
        )
        self.image_default = pygame.transform.scale(
            pygame.image.load("images\Cinnamoroll6.png"),
            cinny_size
        )
        self.image_jump = pygame.transform.scale(
            pygame.image.load("images\Cinnamoroll7.png"),
            cinny_size
        )
        self.image_fire = pygame.transform.scale(
            pygame.image.load("images\cinny_fire.png"),
            cinny_size
        )
        
        self.image = self.image_default
        self.rect = self.image.get_rect()
        self.rect.midbottom = (screen_size[0] // 2, screen_size[1])  # Spawn at the bottom center of the screen
        self.screen = pygame.display.get_surface()
        self.dx = 0
        self.dy = 0
        self.on_the_ground = True
        self.looking_right = False
        self.jumping = False
        self.platform_group = platform_group  # Group of platforms for collision detection
        self.back_pos_global = 0  # Global background position
        self.candy_group = candy_group
        self.kuromi = kuromi
        self.cinny_shoot = False
        self.fire_group = pygame.sprite.Group()
        self.press_time = 0
        self.zamok = Zamok(zamok_x, zamok_y)
        
        

    def update(self):
        # Gravity effect: Cinny accelerates downward
        self.dy += 1
        if self.dy > 30:
            self.dy = 30
        
        # Check if Cinny is at the bottom of the screen
        if self.rect.bottom > self.screen.get_height()-self.back_pos_global:           
            self.game_over = True
            self.dy = 0
        
        prev_y = self.rect.y
        self.rect.move_ip(self.dx, self.dy)

        # Check for collisions with platforms
        platform_collisions = pygame.sprite.spritecollide(self, self.platform_group, False)
        for platform in platform_collisions:
            if  prev_y < platform.rect.top:
                # Cinny lands on top of the platform
                self.rect.bottom = platform.rect.top
                self.dy = 0
                self.on_the_ground = True
            elif  prev_y > platform.rect.bottom:
                # Cinny hits the bottom of the platform while jumping
                self.rect.top = platform.rect.bottom
                self.dy = 0

        candy_collisions = pygame.sprite.spritecollide(self, self.candy_group, True)  # Use True to remove the candy when collided
        for candy in candy_collisions:
            if self.rect.colliderect(candy.rect):
                # Cinny collides with the candy
                self.score += 1

        kuromi_collisions = pygame.sprite.spritecollide(self, self.kuromi, False)
        for kuromi_sprite in kuromi_collisions:
            if self.rect.colliderect(kuromi_sprite.rect):
                # Cinny столкнулся с Kuromi
                self.game_over = True

        fires_kuromis_collisions = pygame.sprite.groupcollide(self.fire_group, self.kuromi, True, True)
        if fires_kuromis_collisions:
            self.fire_group.empty()  # Remove all sprites in the fire_group

        for fire, kuromis in fires_kuromis_collisions.items():
            # Check each collision pair
            for kuromi in kuromis:
                # Handle each kuromi sprite in the collision
                if fire.rect.colliderect(kuromi.rect):
                    # Cinny collides with the kuromi
                    self.score += 2

        platforms_fires_collision = pygame.sprite.groupcollide(self.platform_group, self.fire_group, False, False)

        for platform, fires in platforms_fires_collision.items():
            # Check each collision pair
            for fire in fires:
                if platform.rect.bottom >= fire.rect.top:
                    # Переместить огонь под платформу и остановить его вертикальное движение
                    fire.rect.top = platform.rect.bottom
                    
        
        if  self.rect.colliderect(self.zamok.rect):
            self.game_win = True

            # elif prev_y > candy.rect.bottom:
            #     # Cinny hits the bottom of the platform while jumping
                
            #     self.dy = 0

        # Keep Cinny within the screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen.get_width():
            self.rect.right = self.screen.get_width()
        
        if self.rect.bottom > self.screen.get_height():
            # Cinny falls off the screen
            self.game_over = True
            self.on_the_ground = False

        self.select_image()
        

    def select_image(self):
        # Selects the appropriate image based on Cinny's state
        if self.dx == 0 and self.dy == 0: 
            self.image = self.image_default
            if self.cinny_shoot:
                self.image = self.image_fire
        else:
            if self.looking_right:
                self.image = self.image_dash_r
            elif self.jumping:
                self.image = self.image_jump
            elif self.cinny_shoot:
                self.image = self.image_fire
            else:
                self.image = self.image_dash_l

    def move_left(self):
        # Move Cinny left
        self.dx = -self.cinny_size[1] / 8
        self.dy -= 1  # Apply upward force (simulate jump)
        self.jumping = False
        self.looking_right = False

    def move_right(self):
        # Move Cinny right
        self.dx = self.cinny_size[1] / 8
        self.dy -= 1  # Apply upward force (simulate jump)
        self.jumping = False
        self.looking_right = True

    def stop(self):
        # Stop Cinny's horizontal movement
        self.dx = 0

    def jump(self):
        # Make Cinny jump if on the ground
        if self.on_the_ground:
            self.looking_right = False
            self.jumping = True
            self.dy = -self.cinny_size[1] / 6.5
            self.on_the_ground = False
            
    def fire_picture(self):
        self.cinny_shoot =True
        self.score -= 3
        self.fire_group = pygame.sprite.Group()
        for i in range(3):
            fire =Fire(self.rect.x,self.rect.y,60)
            self.fire_group.add(fire)
    current_time = 0
    times=0
    def fire_movement(self, fire):
        self.current_time = pygame.time.get_ticks()
        if self.times == 0:
            fire.dx = self.rect.x
            fire.dy = fire.rect.y - 3            
            self.times += 1
        elif self.times == 1:
            fire.dx = fire.rect.x + 3
            fire.dy = self.rect.y
            self.times += 1
        elif self.times == 2:
            fire.dx = fire.rect.x - 3
            fire.dy = self.rect.y
            self.times += 1

        if self.current_time - self.press_time >= 900:
            self.cinny_shoot =False

        fire.rect.topleft = (fire.dx, fire.dy)
            
                
            
    
  
    
