import pygame
import enum
from sys import exit

class Background():
    '''Creation of the actual window'''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.screen.fill("#38b566")
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()

class Screen(enum.Enum):
    MAIN_MENU = 0
    SORTING_SCREEN = 1
    GRAPH_MENU = 2

# https://www.clickminded.com/button-generator/
class Button(pygame.sprite.Sprite):
    '''Button Creation
    Images list should have at least two images, one for hover and one for default
    The first one should be default, the second be hover
    Generally default: #6bf3c7
              hovering: #acf9e0
              Width: 200, Height: 50
    '''
    def __init__(self, images, x, y):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center = (x, y))

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                print("button pressed")
            else:
                self.image = self.images[1]
        else:
            self.image = self.images[0]

    def update(self):
        self.player_input()

def main(fps):
    pygame.init()
    window = Background(800, 400)
    screen = Screen.MAIN_MENU
    screenGroup = pygame.sprite.Group()
    screen_change = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # apparentally python has no switch cases?
        # either update to python 3.10 or create a dictionary
        if (screen == Screen.MAIN_MENU and screen_change):
            sorting_button_1 = pygame.image.load('Button/SortingButtons/button_sorting.png').convert_alpha()
            sorting_button_2 = pygame.image.load('Button/SortingButtons/button_sorting_hover.png').convert_alpha()
            screenGroup.add(Button((sorting_button_1, sorting_button_2), window.width/2, 200))
            screen_change = False
            graph_button_1 = pygame.image.load('Button/GraphButtons/button_graph.png')
            graph_button_2 = pygame.image.load('Button/GraphButtons/button_graph_hover.png')
            screenGroup.add(Button((graph_button_1, graph_button_2), window.width/2, 270))
        screenGroup.draw(window.screen)
        screenGroup.update()
        pygame.display.update()
        window.clock.tick(fps)

# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)