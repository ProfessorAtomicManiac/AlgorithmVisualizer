import pygame
import enum
from sys import exit

class Screen(enum.Enum):
    NONE = -1
    MAIN_MENU = 0
    SORTING_SCREEN = 1
    GRAPH_MENU = 2

class Background():
    '''Creation of the actual window
       Color Palette: https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd
    '''
    def __init__(self, width, height, screen):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.window.fill("#0D1B2A")
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.background = pygame.Surface((width, height))
        self.background.fill("#0D1B2A")

    def update(self):
        self.window.blit(self.background, (0, 0))

    def switch_screen(self, screen):
        self.screen = screen

class Text(pygame.sprite.Sprite):

    def __init__(self, window, text, pos, font, color, screen):
        super().__init__()
        self.window = window
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(center = pos)
        self.screen = screen
    

    def destroy(self):
        if (self.rect.x <= -600):
            self.kill()

    def update(self):
        if (self.screen != self.window.screen and self.screen != Screen.NONE):
            self.rect.x -= 15
        self.destroy()

# https://www.clickminded.com/button-generator/
class Button(pygame.sprite.Sprite):
    '''Button Creation
    Images list should have at least two images, one for hover and one for default
    The first one should be default, the second be hover
    Generally default: #415A77
              hovering: #778DA9
              text: #E0E1DD
              Width: 200, Height: 50, Corners Radius: 11
              Bold, Size: 26, 
              Font: Ubuntu (haha get it?)
    '''
    def __init__(self, images, coords, function, screen, background):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center = (coords[0], coords[1]))
        self.function = function
        self.screen = screen
        self.background = background

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.function(self.background)
            else:
                self.image = self.images[1]
        else:
            self.image = self.images[0]

    def destroy(self):
        if (self.rect.x <= -200):
            self.kill()

    def update(self):
        if (self.screen != self.background.screen and self.screen != Screen.NONE):
            self.rect.x -= 15
        self.player_input()
        self.destroy()

class DisplayScreen():
    def display_main_menu(window, screenGroup):
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screenGroup.empty()
        screenGroup.add(Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, 100), ubuntu_font, "#E0E1DD", Screen.MAIN_MENU))
        sorting_button_1 = pygame.image.load('Button/SortingButtons/button_sorting.png').convert_alpha()
        sorting_button_2 = pygame.image.load('Button/SortingButtons/button_sorting_hover.png').convert_alpha()
        screenGroup.add(Button((sorting_button_1, sorting_button_2), ((window.window.get_size()[0]/2), 200), DisplayScreen.pressed_sorting, Screen.MAIN_MENU, window))
        graph_button_1 = pygame.image.load('Button/GraphButtons/button_graph.png').convert_alpha()
        graph_button_2 = pygame.image.load('Button/GraphButtons/button_graph_hover.png').convert_alpha()
        screenGroup.add(Button((graph_button_1, graph_button_2), ((window.window.get_size()[0]/2), 270), DisplayScreen.pressed_graph, Screen.MAIN_MENU, window))
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        screenGroup.add(Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), DisplayScreen.pressed_options, Screen.NONE, window))
    def pressed_sorting(window):
        window.switch_screen(Screen.SORTING_SCREEN)
    def pressed_graph(window):
        window.switch_screen(Screen.GRAPH_MENU)
    def pressed_options():
        pass

def main(fps):
    pygame.init()
    window = Background(800, 400, Screen.MAIN_MENU)
    screenGroup = pygame.sprite.Group()
    screen_change = True

    while True:
        window.update()

        for event in pygame.event.get():
            # If window changes size
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = Background(width, height)
                screen_change = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # apparentally python has no switch cases?
        # either update to python 3.10 or create a dictionary
        if (window.screen == Screen.MAIN_MENU and screen_change):
            DisplayScreen.display_main_menu(window, screenGroup)
            screen_change = False
        screenGroup.draw(window.window)
        screenGroup.update()
        pygame.display.update()
        window.clock.tick(fps)

# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)