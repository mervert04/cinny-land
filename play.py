import pygame
from Cinnamoroll import Cinny
from Kuromi import Kuromi
from elements import Button, Decor
import random
import pygame.mixer


# Define constants for the game
MAX_PLATFORMS = 20
pygame.mixer.init()
platform_image = pygame.image.load('images/donut.png')
candy_image = pygame.image.load('images/candies.png')
background_music = pygame.mixer.Sound('music.mp3')
shoot_sound = pygame.mixer.Sound('fire_music.mp3')
game_over_music = pygame.mixer.Sound('game_over_music.wav')
win_music = pygame.mixer.Sound('win_music.wav')
# Create a Platform class for defining platform objects
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        
        # Scale the platform image to the specified width and a fixed height
        self.image = pygame.transform.scale(platform_image, (width, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Candy(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        # Scale the platform image to the specified width and a fixed height
        self.image = pygame.transform.scale(candy_image, (width, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Create a Play class for managing the game
class Play:
    def __init__(self, screen_size=(500, 500), cinny_size=(50, 50), fps=20, background_color=(255, 255, 255), caption="Game"):
        pygame.init()
        

        # Initialize game parameters
        self.screen_size = screen_size  # Screen size (width, height)
        self.cinny_size = cinny_size  # Cinny character size (width, height)
        self.fps = fps  # Frames per second
        self.background_color = background_color  # Background color
        self.caption = caption  # Window title caption

        # Initialize Pygame screen with the specified size and set the caption
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.playing = False  # Flag to indicate if the game is currently being played
        self.cinny = None  # Stores the main character (Cinny) object
        self.kuromi = None
        self.font = pygame.font.Font('font_file.ttf', 65)
        # self.font = pygame.font.Font(None, 54)  # Create a font for displaying text
        self.begin_img = Decor.Begin_image()  # Load the "Begin" image
        self.end_img = Decor.End_image()  # Load the "End" image
        self.win_img = Decor.Win_image()  
        self.title_img = self.font.render(f'Sweet Cinny Land', True, (114, 198, 237))  # Create a title image
        self.end_title_img = self.font.render(f'Game Over', True, (255, 255, 255))
        self.win_title_img = self.font.render(f'You Win!', True, (255, 255, 255))
        self.back_pos = 0  # Vertical background position

        # Create a group for storing platform objects
        self.platform_group = pygame.sprite.Group()
        self.candy_group = pygame.sprite.Group()
        self.kuromi_group = pygame.sprite.Group()
        self.game_win = False
        self.zamok_x = 0
        self.zamok_y = 0
        self.start_time=0

        # Generate platforms and add them to the platform group
        current = 680 # For creating first platform at bottom of the window --> y coordinate
        for p in range(MAX_PLATFORMS): #50 times
            ponchik_width = 50 #constant width 
            if current == 680:
                ponchik_x = 250 # x coordinate
            else:
                ponchik_x = random.randint(5, 500 - ponchik_width)
            ponchik_y = current # y coordinate
            current -= 150 # making next ponchik's y coordinate higher from bottom of the window 
            platform = Platform(ponchik_x, ponchik_y, ponchik_width) # create platform 
            
            self.platform_group.add(platform) #adding platform 
            # надо добавить рандом 

            # Randomly determine the number of additional platforms to create horizontally
            ponchik_colvo = random.choice([3, 4])
            for i in range(ponchik_colvo - 1):
                ponchik_width = ponchik_width
                ponchik_x = ponchik_x + ponchik_width - 5
                ponchik_y = ponchik_y
                platform = Platform(ponchik_x, ponchik_y, ponchik_width)
                self.zamok_x = ponchik_x
                self.zamok_y = ponchik_y
                self.platform_group.add(platform) #and adding them
                
       
           

    game_over = False  # Flag to indicate whether the game is over

    play_once =True
    # Display the game menu
    def menu(self):
        show_menu = True
        while show_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    show_menu = False
           
            if self.game_over:
             print("r")
             if not self.game_over and not self.game_win:
                game_over_music.stop()
                win_music.stop()
                background_music.play()
             elif self.game_over and self.play_once:
                background_music.stop()
                game_over_music.play()
                self.play_once = False
             
             start_button = Button(114, 366, 120, 54, "Try again!", (128, 199, 217), (116, 180, 196))
            elif self.game_win:
                if not self.game_over and not self.game_win:
                    game_over_music.stop()
                    win_music.stop()
                    background_music.play()
                elif self.game_win and self.play_once:
                    background_music.stop()
                    win_music.play()
                    self.play_once = False
                start_button = Button(114, 385, 100, 54, "Start!", (128, 199, 217), (230, 172, 250))
              
            else:
                info_button = Button(250, 570, 150, 50, "Instructions", (255, 183, 206), (230, 172, 190))
                start_button = Button(280, 500, 100, 50, "Start", (255, 183, 206), (230, 172, 190))

            mouse_pos = pygame.mouse.get_pos()
            start_button.check_hover(mouse_pos)
            # Check if the mouse is hovering over the button
            if pygame.mouse.get_pressed()[0] and start_button.is_hovered:
                    self.run()

            if not self.game_over and not self.game_win:
                if info_button:
                 info_button.check_hover(mouse_pos)
                # Handle button click to start/restart the game --> calling run function
                
                if info_button and pygame.mouse.get_pressed()[0] and info_button.is_hovered:
                    self.display_info_popup()
            # Display appropriate menu screen based on game state
            if self.game_over:  # Game Over Menu
                self.back_pos = 0
               
                info_button = False
                self.screen.fill((255, 177, 193))
                self.screen.blit(self.end_img, (287, 157))
                self.screen.blit(self.end_title_img, (84, 295))
               
            elif self.game_win:  # Game Over Menu
                info_button = False
                self.back_pos = 0
                self.screen.fill((255, 177, 193))
                self.screen.blit(self.win_img, (287, 157))
                self.screen.blit(self.win_title_img, (84, 295))
            else: # Start Menu
                background_music.stop()
                game_over_music.stop()
                win_music.stop()
                self.back_pos = 0 
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.begin_img, (80, 110))
                self.screen.blit(self.title_img, (146, 160))
            start_button.draw(self.screen)

            if info_button:
                info_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
       
            
    # Start the game
    def start_game(self):
        background_music.stop()
        game_over_music.stop()
        win_music.stop()

        self.start_time = pygame.time.get_ticks()
        self.kuromi_group.empty()
        self.candy_group.empty()
        times_4 = 0
        kuri = 0
        self.playing = True
        for platform in self.platform_group:
            if times_4 == 7 or times_4 == 18 :
                candy = Candy(platform.rect.x+25, platform.rect.y-50, 50)
                self.candy_group.add(candy)
                if times_4 == 18:
                    times_4 = 0
            if kuri == 18:
             xx = platform.rect.x
             yy = platform.rect.y
             self.kuromi = Kuromi((70,70) ,xx,yy+self.back_pos, self.screen_size, self.platform_group) 
             self.kuromi_group.add(self.kuromi)
             kuri=0
           
            times_4+=1            
            kuri+=1
            
        self.cinny = Cinny(self.cinny_size, self.screen_size, self.platform_group,self.candy_group,self.kuromi_group,self.zamok_x,self.zamok_y) #create character
        
        self.cinny.game_over = False
        self.cinny.game_win = False
        self.game_over = False
        self.game_win = False

        if not self.game_over and not self.game_win:
                game_over_music.stop()
                win_music.stop()
                background_music.play()
        elif self.game_over and self.play_once:
                background_music.stop()
                win_music.stop()
                game_over_music.play()
                self.play_once = False
        elif self.game_win and self.play_once:
                background_music.stop()
                game_over_music.stop()
                win_music.play()
                self.play_once = False
        

    # Run the game loop
    def run(self):
        self.start_game()
        self.play_once =True
        self.game_over = False
        self.game_win = False
        while self.playing and not self.cinny.game_over and not self.cinny.game_win:  #checking game over or not 
            now = pygame.time.get_ticks()
            hours_string = ""
            if now - self.start_time >=130000:
                self.cinny.game_over = True
            else:
                seconds = (now - self.start_time)
                hour = 0
                if seconds >= 60000 :
                    hour += 1
                    seconds = seconds - 60000*hour
                hours_string = f"{hour}:{int(seconds/1000)}"
                

            for event in pygame.event.get(): #initiating  keys 
                if event.type == pygame.QUIT:
                    self.playing = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.cinny.move_left()
                    if event.key == pygame.K_RIGHT:
                        self.cinny.move_right()
                    if event.key == pygame.K_UP:
                        self.cinny.jump()
                    if event.key == pygame.K_SPACE:
                        if self.cinny.score >=3:
                            self.cinny.press_time =  pygame.time.get_ticks()
                            shoot_sound.play()
                            self.cinny.fire_picture()
                if event.type == pygame.KEYUP: #just stopping
                    if event.key == pygame.K_LEFT and self.cinny.dx < 0:
                        self.cinny.stop()
                    if event.key == pygame.K_RIGHT and self.cinny.dx > 0:
                        self.cinny.stop()
                    if event.key == pygame.K_SPACE:
                        self.cinny.fire_group.empty()
                        shoot_sound.stop()
                        self.cinny.cinny_shoot = False

            # Clear the screen with the background color
            self.screen.fill(self.background_color)
            # pygame.draw.rect(self.screen, (255, 0, 0), self.cinny.rect, 50)
            # pygame.draw.rect(self.screen, (255, 0, 0), self.cinny.zamok.rect, 50)
            # for platform in self.platform_group:
            #     pygame.draw.rect(self.screen, (0, 255, 0), platform.rect, 200)
            # for kuromi in self.kuromi_group:
            #     pygame.draw.rect(self.screen, (0, 0, 255), kuromi.rect, 60)
            # for fire in self.cinny.fire_group:
            #     pygame.draw.rect(self.screen, (255, 0, 0), fire.rect, 60)
            
            # Update Cinny's position and animation
            self.cinny.update()
            for kuro in self.kuromi_group:
              kuro.KuromiMovements() 
            
            for fire in self.cinny.fire_group:
              self.cinny.fire_movement(fire)
            
            self.cinny.times = 0

            # Scroll the background based on Cinny's position
            if self.cinny.rect.y + self.back_pos < self.screen_size[1] * 0.5:
                self.back_pos += self.cinny_size[1] // 2 
                self.cinny.back_pos_global = self.back_pos # We used for idetify game over when character falls from platform 

            # Draw the level (platforms) and Cinny on the screen
            self.draw_level(self.screen, self.back_pos)
            self.screen.blit(self.cinny.image, (
                self.cinny.rect.x,
                self.cinny.rect.y + self.back_pos #For moving to the top of the screen  
            ))
            self.screen.blit(self.cinny.zamok.image, (
               self.cinny.zamok.rect.x,
              self.cinny.zamok.rect.y + self.back_pos #For moving to the top of the screen  
            ))
            for kuro in self.kuromi_group:
                self.screen.blit(kuro.image, (
                    kuro.rect.x,
                    kuro.rect.y + self.back_pos #For moving to the top of the screen  
                ))

            if self.cinny.cinny_shoot:
             for fire in self.cinny.fire_group:
                self.screen.blit(fire.image, (
                    fire.dx,
                    fire.dy + self.back_pos #For moving to the top of the screen  
                ))
                
            background = pygame.Surface((660, 50))  # Задайте желаемые размеры фона
            font = pygame.font.Font('font_file.ttf', 45)
            # Задаем цвет фона
            background.fill((255, 183, 206))
            text = font.render("Score: " + str(self.cinny.score), True, (255, 255, 255))
            text2 = font.render("Time: " + hours_string, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect2 = text2.get_rect()
            text_rect.topleft = (3, 0)
            text_rect2.topleft = (520, 0)

            # Отрисовываем фон
            self.screen.blit(background, (0, 0))

            # Отрисовываем текстовую поверхность на фоне
            self.screen.blit(text, text_rect)
            self.screen.blit(text2, text_rect2)
            pygame.display.flip() # To display all the drawings and objects that have been modified or created on the current frame
            self.clock.tick(self.fps) # Frame refresh rate limit
            

        self.game_win = self.cinny.game_win
        self.game_over = self.cinny.game_over #for using boolean value in Play's function

    # Draw the level (platforms) on the screen with vertical background offset
    def draw_level(self, screen, back_pos):

        for platform in self.platform_group:
            screen.blit(platform.image, (platform.rect.x, platform.rect.y + back_pos))

        for candy in self.candy_group:
            screen.blit(candy.image, (candy.rect.x, candy.rect.y + back_pos))
    def display_info_popup(self):
            info_font = pygame.font.Font("button_font_file.ttf", 15)
            info_text = [
                "Instructions:",
                "Use arrow keys to move left, right, and jump.",
                "Press space to shoot enemies.",
                "Avoid falling off the platforms!",
                "Collect candies for 1 point each.",
                "To shoot, you need 3 points.",
                "Defeating an enemy earns you 2 points.",
                "Reach the castle to win the game.",
                "Press 'Esc' to close this window."
            ]


            popup_surface = pygame.Surface((400, 280))  # Increase width and height here
            popup_surface.fill((119, 203, 250))
            pygame.draw.rect(popup_surface, (0, 0, 0), (0, 0, 400, 280),1)

            for i, line in enumerate(info_text):
                text = info_font.render(line, True, (0, 0, 0))
                popup_surface.blit(text, (10, 10 + i * 30))

            popup_rect = popup_surface.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(popup_surface, popup_rect)
            pygame.display.flip()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        return
