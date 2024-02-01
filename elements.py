import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        # Initialize Button attributes
        self.rect = pygame.Rect(x, y, width, height)  # Create a rectangular button
        self.color = color  # Default color
        self.hover_color = hover_color  # Color when hovered
        self.text = text  # Text displayed on the button
        self.is_hovered = False  # Flag to track if the button is being hovered over
        self.font = pygame.font.Font('button_font_file.ttf', 23)  # Replace with your font file path and size

    def draw(self, screen):
        # Draw the button on the screen
        if self.is_hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        # Check if the mouse pointer is hovering over the button
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class Decor:
    def Begin_image():
        # Load and scale the "Begin_Cinny.png" image
        image = pygame.transform.scale(
            pygame.image.load("images\Begin_Cinny.png"),
            (500, 500)
        )
        return image

    def End_image():
        # Load and scale the "Game_Over.gif" image
        image = pygame.transform.scale(
            pygame.image.load("images\Game_Over.gif"),
            (330, 310)
        )
        return image
 
    def Win_image():
        # Load and scale the "Game_Over.gif" image
        image = pygame.transform.scale(
            pygame.image.load("images\win.png"),
            (330, 310)
        )
        return image