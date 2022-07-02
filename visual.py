import time
import pygame
import enum
from sys import exit

class Screen(enum.Enum):
    '''Enum for which screen the window is on
    '''
    NONE = -1
    MAIN_MENU = 0
    SORTING_SCREEN = 1
    GRAPH_MENU = 2

class Window():
    '''Creation of the actual window
       Color Palette: https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd
       @width = width of the window
       @height = height of the window
       @screen = which screen the window is on
    '''
    def __init__(self, width, height, screen):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.window.fill("#0D1B2A")
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.background = pygame.Surface((width, height))
        self.background.fill("#0D1B2A")
        self.screen_change = True
        self.options_screen = False

    def update(self):
        self.window.blit(self.background, (0, 0))

    def switch_screen(self, screen):
        self.screen = screen
    
class Text(pygame.sprite.Sprite):
    ''' Creates text
        @window = the window class
        @text = the text to be displayed
        @coords = where the text will be centered at
        @font = the font
        @color = the color of the text
        @screen = the text will stay put if its the right screen, otherwise it will do a scrolling animation
        @will_slide = whether the thing will slide
    '''
    def __init__(self, window, text, coords, font, color, screen, will_slide = True):
        super().__init__()
        self.window = window
        self.image = font.render(text, True, color)

        if (will_slide):
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 1000, coords[1]))
        else: 
            self.rect = self.image.get_rect(center = coords)
        self.screen = screen
        self.accel = 0
        self.coords = coords

    def destroy(self):
        if (self.rect.x <= -600):
            self.kill()

    def update(self):
        if ((self.screen != self.window.screen and self.screen != Screen.NONE) or self.rect.x > self.coords[0]):
            self.accel += -1
            self.rect.x += self.accel
        else:
            self.accel = 0
            self.rect = self.image.get_rect(center = self.coords)
        self.destroy()

class Button(pygame.sprite.Sprite):
    '''This is an icon button class
       @coords = the icon will be centered at those coords
       @function = the function that will be called when the button is pressed
       @screen = what screen the button will stay on (will do a sliding animation when its the wrong screen)
       @window = the Window class object
       @screen_group = a typical argument used for the @function
       @options = whether the button is part of the options menu or not (There was a bug where when you have the options screen
       you can still use buttons on the main screen)
       @args = arguments to pass to the function
    '''
    def __init__(self, images, coords, function, screen, window, options=False, *args):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center = (coords[0], coords[1]))
        self.function = function
        self.screen = screen
        self.window = window
        self.args = args
        self.options = options

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and (self.options or not self.window.options_screen):
                print(self.args)
                self.function(self.window, self.args)
            else:
                self.image = self.images[1]
        else:
            self.image = self.images[0]

    def destroy(self):
        if (self.rect.x <= -200):
            self.kill()

    def update(self):
        if (self.screen != self.window.screen and self.screen != Screen.NONE):
            self.rect.x -= 15
        self.player_input()
        self.destroy()

class TextButton(pygame.sprite.Sprite):
    # https://www.clickminded.com/button-generator/
    '''Button Creation
    Images list should have at least two images, one for hover and one for default
    The first one should be default, the second be hover
    Generally default: #415A77
              hovering: #778DA9
              text: #E0E1DD
              Width: 200, Height: 50, Corners Radius: 11
              Bold, Size: 26, 
              Font: Ubuntu (haha get it?)
    The window should be the background class
    '''
    '''This is a text button class
       @text = the text that will be displayed at the center of the button
       @coords = the icon will be centered at those coords
       @function = the function that will be called when the button is pressed
       @screen = what screen the button will stay on (will do a sliding animation when its the wrong screen)
       @window = the Window class object
       @will_slide = whether the button will slide onto the screen or just appear
       @options = whether the button is part of the options menu or not (There was a bug where when you have the options screen
       you can still use buttons on the main screen)
       @args = arguments to pass to the function
    '''
    def __init__(self, text, coords, function, screen, window, will_slide = True, options = False, *args):
        super().__init__()
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 26)
        self.text = ubuntu_font.render(text, True, "#E0E1DD")
        self.image = pygame.image.load("Button/button.png").convert_alpha()
        self.coords = coords
        self.options = options
        if will_slide:
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 200, coords[1]))
            self.textRect = self.text.get_rect(center = (window.window.get_size()[0] + 200, coords[1]))
        else:
            self.rect = self.image.get_rect(center = coords)
            self.textRect = self.text.get_rect(center = coords)
        self.function = function
        self.screen = screen
        self.window = window
        self.accel = 0
        self.width = 200
        self.height = 50
        self.args = args

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and (self.options or not self.window.options_screen):
                self.function(self.window, self.args)
            else:
                self.image = pygame.image.load("Button/button_hovering.png").convert_alpha()
        else:
            self.image = pygame.image.load("Button/button.png").convert_alpha()

    def destroy(self):
        if (self.rect.x <= -200):
            self.kill()

    def slide(self):
        if ((self.screen != self.window.screen and self.screen != Screen.NONE) or self.rect.x + self.width/2 > self.coords[0]):
            self.accel += -1
            self.rect.x += self.accel
            self.textRect.x += self.accel
        else:
            self.accel = 0
            self.rect = self.image.get_rect(center = self.coords)
            self.textRect = self.text.get_rect(center = self.coords)

    def update(self):
        #self.window.window.blit(self.text, (self.rect.x + self.width/2, self.rect.y + self.height/2))
        self.window.window.blit(self.text, self.textRect)
        self.player_input()
        self.slide()
        self.destroy()
    
class Background(pygame.sprite.Sprite):
    '''Creates a background
       TODO: make the background have white edges or smth
       @window = the window class
       @color = the color that the background will be in
       @coords = the coordinates where the rectangle will be centered at
       @dim = the dimensions of the rectangle
    '''
    def __init__(self, window, color, coords, dim):
        super().__init__()
        self.image = pygame.Surface(dim)
        self.rect = self.image.get_rect(center = coords)
        self.window = window
        self.coords = coords
        self.image.fill(color)
    
    def update(self):
        self.rect = self.image.get_rect(center = self.coords)

class MainMenuActions():
    '''These tend to go in the @func for the button classes
       args[0] = screen_group
       args[1] = options_group
    '''
    def display_main_menu(window, args):
        if (window.screen == Screen.MAIN_MENU):
            return
        window.screen = Screen.MAIN_MENU
        screen_group = args[0]
        options_screen_group = args[1]
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        screen_group.add(Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, 100), ubuntu_font, "#E0E1DD", Screen.MAIN_MENU))
        screen_group.add(TextButton("Sorting", ((window.window.get_size()[0]/2), 200), MainMenuActions.pressed_sorting, Screen.MAIN_MENU, window))
        screen_group.add(TextButton("Graphs", ((window.window.get_size()[0]/2), 270), MainMenuActions.pressed_graph, Screen.MAIN_MENU, window))
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        # TODO: Crop image properly using Figma
        screen_group.add(Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), OptionActions.display_options, Screen.NONE, window, False, options_screen_group, screen_group))
    
    def pressed_sorting(window, *args):
        window.switch_screen(Screen.SORTING_SCREEN)
        window.screen_change = True
    def pressed_graph(window, *args):
        window.switch_screen(Screen.GRAPH_MENU)
        window.screen_change = True

class OptionActions():
    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(window, args):
        window.options_screen = True
        options_group = args[0]
        screen_group = args[1]
        options_group.add(Background(window, "#1B263B", (window.window.get_size()[0]/2, window.window.get_size()[1]/2), (300, 300)))
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        # Where the text starts rendering
        text_start = 100
        options_group.add(Text(window, "Options", (window.window.get_size()[0]/2, text_start), ubuntu_font, "#E0E1DD", Screen.NONE, False))
        options_group.add(TextButton("Return", (window.window.get_size()[0]/2, text_start + 100), OptionActions.close_options, Screen.NONE, window, False, True, options_group))
        options_group.add(TextButton("Main Menu", (window.window.get_size()[0]/2, text_start + 175), OptionActions.press_main_menu, Screen.NONE, window, False, True, options_group, screen_group))
    
    '''@args = options_group'''
    def close_options(window, args):
        screen_group = args[0]
        screen_group.empty()
        # TODO: Fix glitch where when you press the return button, it will simultaneously press the button behind it
        time.sleep(0.30)
        window.options_screen = False

    '''@args[0] = options_group
       @args[1] = screen_group
    '''
    def press_main_menu(window, args):
        OptionActions.close_options(window, args)
        MainMenuActions.display_main_menu(window, (args[1], args[0]))
        window.options_screen = False

def main(fps):
    '''Equivalent of public static void main(String[] args)'''
    pygame.init()
    window = Window(800, 400, Screen.NONE)
    screen_group = pygame.sprite.Group()
    options_screen_group = pygame.sprite.Group()
    MainMenuActions.display_main_menu(window, (screen_group, options_screen_group))

    while True:
        window.update()

        for event in pygame.event.get():
            # If window changes size
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = Window(width, height)
                window.screen_change = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # apparentally python has no switch cases?
        # either update to python 3.10 or create a dictionary
        if (window.screen == Screen.MAIN_MENU and window.screen_change):
            MainMenuActions.display_main_menu(window, (screen_group, options_screen_group))
            window.screen_change = False
        screen_group.draw(window.window)
        screen_group.update()
        options_screen_group.draw(window.window)
        options_screen_group.update()
        pygame.display.update()
        window.clock.tick(fps)

# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)