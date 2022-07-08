import enum
import threading
import pygame

'''Contains code for various objects that are used frequently as sprites'''
def add_args_to_func(func, *args, **kwargs):
    #@func.wraps(inner) # This is optional TODO: Fix and understand wut this is
    def inner():
        return func(*args, **kwargs)
    return inner

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
       @screen_change = the screen changed screens?
    '''
    def __init__(self, width, height, screen, screen_change, window_size_change):
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.window.fill("#0D1B2A")
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.background = pygame.Surface((width, height))
        self.background.fill("#0D1B2A")
        self.screen_change = screen_change
        self.options_screen = False
        self.window_size_change = window_size_change
        self.mouse_button_down = False
        self.event = threading.Event()

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
        @will_slide = whether the thing will slide into the screen when initialized
    '''
    def __init__(self, window, text, coords, font, color, screen, will_slide):
        super().__init__()
        self.window = window
        self.image = font.render(text, True, color)

        if (will_slide):
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 800, coords[1]))
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

# TODO: There is a double where a click registers as a double click
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
    def __init__(self, images, coords, function, screen, window, options=False):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center = (coords[0], coords[1]))
        self.function = function
        self.screen = screen
        self.window = window
        self.options = options
        self.handled = False

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and (self.options or not self.window.options_screen) and not self.handled:
                self.function()
                self.handled = True
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
    

    def __init__(self, text, coords, function, screen, window, will_slide = True, options = False):
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
        self.handled = False

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and (self.options or not self.window.options_screen) and not self.handled:
                self.function()
                self.handled = True
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

class ScrollBar():

    '''@buttons = ScrollButton classes that will act like buttons'''
    def __init__(self, coords, dim, buttons, scroll_group, window, max_height = 1200):
        self.coords = coords
        self.dim = dim
        self.scroll_group = scroll_group
        self.buttons = buttons
        self.window = window
        self.max_height = max_height

        self.extended = False

        self.selected = buttons[0]
        TRIANGLE_BUTTON_WIDTH = 25
        TRIANGLE_BUTTON_HEIGHT = dim[1]
        triangle_button_1 = pygame.image.load('Button/triangle_button.png').convert_alpha()
        triangle_button_1 = pygame.transform.scale(triangle_button_1, (TRIANGLE_BUTTON_WIDTH, TRIANGLE_BUTTON_HEIGHT))
        triangle_button_2 = pygame.image.load('Button/triangle_button_hovering.png').convert_alpha()
        triangle_button_2 = pygame.transform.scale(triangle_button_2, (TRIANGLE_BUTTON_WIDTH, TRIANGLE_BUTTON_HEIGHT))
        self.scroll_button = Button((triangle_button_1, triangle_button_2), (coords[0]+dim[0]/2 + TRIANGLE_BUTTON_WIDTH/2, coords[1]), self.toggle, Screen.SORTING_SCREEN, window)
        scroll_group.add(self.scroll_button)
        buttons[0].setCoords(coords)
        for button in buttons:
            button.setDim(dim)
        scroll_group.add(self.selected)

    def toggle(self):
        self.extended = not self.extended
        if (self.extended):
            for i in range(len(self.buttons)):
                if (self.coords[1] + i*self.dim[1] > self.max_height):
                    return
                self.buttons[i].setCoords((self.coords[0], self.coords[1] + i*self.dim[1]))
                self.scroll_group.add(self.buttons[i])
        else:
            if (len(self.scroll_group) > 2):
                self.scroll_group.empty()
                self.scroll_group.add(self.scroll_button)
                self.scroll_group.add(self.selected)
                
    

class ScrollButton(pygame.sprite.Sprite):
    '''This is a scroll button class
       Generally default: #415A77
              hovering: #778DA9
              text: #E0E1DD
              Width: 200, Height: 50, Corners Radius: 11
              Bold, Size: 26, 
              Font: Ubuntu (haha get it?)
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

    def __init__(self, text, function, screen, window):
        super().__init__()
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 26)
        self.text = ubuntu_font.render(text, True, "#E0E1DD")
        self.dim = ()
        self.coords = ()
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.function = function
        self.screen = screen
        self.window = window
        self.handled = False

    def setDim(self, dim):
        self.dim = dim

    def setCoords(self, coords):
        self.coords = coords

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and (not self.window.options_screen) and not self.handled:
                self.function()
                self.handled = True
            else:
                self.image.fill("#778DA9")
        else:
            self.image.fill("#415A77")

    def update(self):
        #self.window.window.blit(self.text, (self.rect.x + self.width/2, self.rect.y + self.height/2))
        self.image = pygame.Surface(self.dim)
        self.rect = self.image.get_rect(center = self.coords)
        self.textRect = self.text.get_rect(center = self.coords)
        self.window.window.blit(self.text, self.textRect)
        self.player_input()

    
class Background(pygame.sprite.Sprite):
    # TODO: Make background slide
    '''Creates a background (also used as an array element)
       TODO: make the background have white edges or smth
       @color = the color that the background will be in
       @coords = the coordinates where the rectangle will be centered at
       @dim = the dimensions of the rectangle
    '''
    def __init__(self, color, coords, dim):
        super().__init__()
        self.image = pygame.Surface(dim)
        self.color = color
        self.rect = self.image.get_rect(center = coords)
        self.coords = coords
        self.image.fill(color)
    
    def update(self):
        self.rect = self.image.get_rect(center = self.coords)

    def change_color(self, color):
        self.color = color