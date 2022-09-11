import enum
import threading
import time
from queue import Queue

import pygame

'''Contains code for various objects that are used frequently as sprites'''
def add_args_to_func(func, *args, **kwargs):
    #@func.wraps(inner) # This is optional TODO: Fix and understand wut this is
    def inner():
        return func(*args, **kwargs)
    return inner

'''Runs multiple functions sequentially'''
def sequential_functions(*funcs):
    def inner():
        for func in funcs:
            func()
    return inner

class Screen(enum.Enum):
    '''Enum for which screen the window is on
    '''
    NONE = -1
    MAIN_MENU = 0
    SORTING_SCREEN = 1
    GRAPH_MENU = 2

class Colors():
    BACKGROUND_COLOR = "#0D1B2A"
    SMALL_BACKGROUND_COLOR = "#1B263B"
    BUTTON_COLOR = "#415A77"
    HOVER_BUTTON_COLOR = "#778DA9"
    TEXT_COLOR = "#E0E1DD"
    BACKGROUND_SCROLL_COLOR = BUTTON_COLOR
    SCROLLBAR_COLOR = TEXT_COLOR

class FontSizes():
    BUTTON_SIZE = 25
    SUB_TITLE_SIZE = 35
    TITLE_SIZE = 50

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
        self.window.fill(Colors.BACKGROUND_COLOR)
        pygame.display.set_caption("Algorithm Visualizer")
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.background = pygame.Surface((width, height))
        self.background.fill(Colors.BACKGROUND_COLOR)

        self.screen_change = screen_change
        self.options_screen = False
        self.window_size_change = window_size_change
        self.mouse_button_down = False
        self.event = threading.Event()

    def update(self):
        self.window.blit(self.background, (0, 0))

    def switch_screen(self, screen):
        self.screen = screen
        self.screen_change = True

''' Seperate class to make it so that you don't have 9 parameters when making text
        @text = the text to be displayed
        @font = the font
        @alias = whether to have anti-aliasing or not (in general, set to True)
        @color = the color of the text      
'''    
class TextArgs():
    def __init__(self, text, font, alias, color):
        self.text = text
        self.font = font
        self.alias = alias
        self.color = color

    def render(self):
        return self.font.render(self.text, self.alias, self.color)

class DefaultText():
    def text(text, font_size):
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", font_size)
        return TextArgs(text, ubuntu_font, True, Colors.TEXT_COLOR)

class Fonts():

    def __init__(self, font_size):
        self.UBUNTU_FONT = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", font_size)

class Text(pygame.sprite.Sprite):
    ''' Creates text
        @window = the window class
        @coords = where the text will be centered at
        @text_arg = TextArgs class object
        @will_slide = whether the thing will slide into the screen when initialized
    '''
    def __init__(self, text_arg, coords, window, will_slide = True, screen = None):
        super().__init__()
        self.window = window
        self.image = text_arg.render()
        self.will_slide = will_slide

        if (will_slide):
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 800, coords[1]))
        else: 
            self.rect = self.image.get_rect(center = coords)
        # Will automatically set screen to whatever screen it is currently on
        if screen == None:
            self.screen = window.screen
        else:
            self.screen = screen
        self.accel = 0
        self.coords = coords

    def slide(self):
        if ((self.screen != self.window.screen and self.screen != Screen.NONE) or self.rect.x > self.coords[0]):
            self.accel += -1
            self.rect.x += self.accel
        else:
            self.accel = 0
            self.rect = self.image.get_rect(center = self.coords)

    def destroy(self):
        if (self.rect.x <= -600):
            self.kill()

    def update(self):
        if self.will_slide:
            self.slide()
        
        self.destroy()

# TODO: There is a double where a click registers as a double click
class Button(pygame.sprite.Sprite):
    '''This is an icon button class
       @images = image background of the button
       @coords = the icon will be centered at those coords
       @function = the function that will be called when the button is pressed
       @window = the Window class object
    '''
    def __init__(self, images, coords, function, window, will_slide = True, screen = None):
        super().__init__()
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect(center = (coords[0], coords[1]))
        self.function = function
        self.coords = coords
        self.will_slide = will_slide

        if will_slide:
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 200, coords[1]))
        else:
            self.rect = self.image.get_rect(center = coords)

        # Will automatically set screen to whatever screen it is currently on
        if screen == None:
            self.screen = window.screen
        else:
            self.screen = screen
        self.screen = window.screen
        self.window = window
        self.handled = False
        self.accel = 0

        self.can_press = True # if in options and you don't want buttons behind the options to be pressed

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and not self.handled and self.can_press:
                self.function()
                self.handled = True
            else:
                self.image = self.images[1]
        else:
            self.image = self.images[0]

    # If its in options, advanced tools, etc where a window would pop up, the button shouldn't be pressed
    def check_overlap(self):
        if (self.window.screen == Screen.NONE and self.screen != Screen.NONE):
            self.set_unpressable()
        else:
            self.set_pressable()

    def slide(self):
        if ((self.screen != self.window.screen and self.screen != Screen.NONE) or self.rect.x > self.coords[0]):
            self.accel += -1
            self.rect.x += self.accel
        else:
            self.accel = 0
            self.rect = self.image.get_rect(center = self.coords)

    def destroy(self):
        if (self.rect.x <= -200):
            self.kill()

    def set_pressable(self):
        self.can_press = True

    def set_unpressable(self):
        self.can_press = False

    def update(self):
        self.player_input()
        self.check_overlap()
        if self.will_slide:
            self.slide()
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
       @text_arg = the text that will be displayed at the center of the button (TextArg class object)
       @coords = the icon will be centered at those coords
       @function = the function that will be called when the button is pressed
       @screen = what screen the button will stay on (will do a sliding animation when its the wrong screen)
       @window = the Window class object
       @will_slide = whether the button will slide onto the screen or just appear
    '''

    def __init__(self, text_arg, coords, function, window, will_slide = True, screen = None):
        super().__init__()
        self.text = text_arg.render()
        self.image = pygame.image.load("Button/button.png").convert_alpha()
        self.coords = coords
        self.will_slide = will_slide

        if will_slide:
            self.rect = self.image.get_rect(center = (window.window.get_size()[0] + 200, coords[1]))
            self.textRect = self.text.get_rect(center = (window.window.get_size()[0] + 200, coords[1]))
        else:
            self.rect = self.image.get_rect(center = coords)
            self.textRect = self.text.get_rect(center = coords)
        self.function = function
        # Will automatically set screen to whatever screen it is currently on
        if screen == None:
            self.screen = window.screen
        else:
            self.screen = screen
        self.window = window

        self.accel = 0
        # default dimensions, cannot change now
        self.width = 200
        self.height = 50
        self.handled = False

        self.can_press = True

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and not self.handled and self.can_press:
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

    # If its in options, advanced tools, etc where a window would pop up, the button shouldn't be pressed
    def check_overlap(self):
        if (self.window.screen == Screen.NONE and self.screen != Screen.NONE):
            self.set_unpressable()
        else:
            self.set_pressable()

    def change_func(self, function):
        self.function = function
    
    def set_pressable(self):
        self.can_press = True

    def set_unpressable(self):
        self.can_press = False

    def update(self):
        #self.window.window.blit(self.text, (self.rect.x + self.width/2, self.rect.y + self.height/2))
        self.window.window.blit(self.text, self.textRect)
        self.player_input()
        self.check_overlap()
        if self.will_slide:
            self.slide()
        self.destroy()

# TODO : Fixed scuffed position for scrollbar when scrolling thru the first two elements using arrow keys
class ScrollBar():

    ''' Implements a drop down menu with a scroll bar
        The top (chosen) button will always be visible along with a drop-down button (triangle button)
        @coords = Coordinates of the center of the top-most button that will always be visible
        @dim = Dimensions of the buttons
        @buttons = ScrollButton classes that will act like buttons
        @scroll_group = Sprite group needed to display the elements
        @window = Window class object
        @max_height = the drop down menu will only expand to this height (not including the first button)

        self.selected = which button is selected/chosen from the drop-down
        self.extended = if the drop down menu is displayed
        self.shift = how much the buttons should shift because of scroll
        
    '''
    def __init__(self, buttons, coords, dim, scroll_group, window, max_height = 200):
        self.coords = coords
        self.dim = dim
        self.scroll_group = scroll_group
        self.buttons = buttons
        self.window = window
        self.max_height = max_height

        self.extended = False

        TRIANGLE_BUTTON_WIDTH = 25
        self.TRIANGLE_BUTTON_HEIGHT = dim[1]
        triangle_button_1 = pygame.image.load('Button/triangle_button.png').convert_alpha()
        triangle_button_1 = pygame.transform.scale(triangle_button_1, (TRIANGLE_BUTTON_WIDTH, self.TRIANGLE_BUTTON_HEIGHT))
        triangle_button_2 = pygame.image.load('Button/triangle_button_hovering.png').convert_alpha()
        triangle_button_2 = pygame.transform.scale(triangle_button_2, (TRIANGLE_BUTTON_WIDTH, self.TRIANGLE_BUTTON_HEIGHT))
        self.scroll_button = Button((triangle_button_1, triangle_button_2), (coords[0]+dim[0]/2 + TRIANGLE_BUTTON_WIDTH/2, coords[1]), self.toggle, window)
        scroll_group.add(self.scroll_button)

        self.scroll_back = Background((coords[0]+dim[0]/2 + TRIANGLE_BUTTON_WIDTH/2, coords[1] + self.TRIANGLE_BUTTON_HEIGHT/2 + max_height/2), (TRIANGLE_BUTTON_WIDTH, max_height), Colors.BACKGROUND_SCROLL_COLOR)
        self.scroll_bar_height = (max_height * max_height / (dim[1] * (len(buttons)))) 
        self.scroll_bar = Background((coords[0]+dim[0]/2 + TRIANGLE_BUTTON_WIDTH/2, coords[1] + self.TRIANGLE_BUTTON_HEIGHT/2 + self.scroll_bar_height/2), (TRIANGLE_BUTTON_WIDTH, self.scroll_bar_height), Colors.SCROLLBAR_COLOR)

        self.selected = ScrollButton(DefaultText.text("Choose Sort", FontSizes.BUTTON_SIZE), None, window)
        self.selected.setCoords(coords)
        self.selected.setDim(dim)
        for button in buttons:
            button.setDim(dim)
        scroll_group.add(self.selected)

        # Variables concerning the scroll bar
        self.drag = False
        self.shift = 0
        self.init_mouse_y = 0
        # Rounding errors can make buttons not appear, so this is to circumvent that
        self.tolerance = 0.1

        # arrow keys on scroll_bar
        # -1 = no keys
        # 0 = up key pressed
        # 1 = down key pressed
        self.handled = -1

    def button_checks(self):
        # inefficient way of checking if buttons were pressed (TODO : Find faster way?)
        if (self.extended):
            for sprite in self.scroll_group.sprites():
                if (type(sprite) == ScrollButton and sprite.is_chosen and sprite != self.selected):
                    self.selected.is_chosen = False
                    self.selected.kill()
                    sprite.is_chosen = False
                    self.selected = sprite.copy()
                    self.selected.setCoords(self.coords)
                    self.selected.setDim(self.dim)
                    self.selected.is_chosen = True
                    time.sleep(0.5) # TODO : Fix bug to not click buttons behind it
                    self.toggle()
                    return
            
            # Drags the scroll bar
            max_shift = len(self.buttons)*self.dim[1] - self.max_height
            
            if not pygame.mouse.get_pressed()[0]:
                self.drag = False
            elif self.scroll_bar.get_rect().collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not self.drag:
                self.drag = True
            elif (self.drag):
                dist = (self.scroll_bar.coords[1] - self.scroll_bar_height/2 - (self.coords[1] + self.dim[1]/2))
                scroll_dist = (self.max_height - self.scroll_bar_height)
                self.shift = dist * max_shift / scroll_dist
                
                self.draw_drop_menu()

            keys = pygame.key.get_pressed()
            
            if (keys[pygame.K_UP] and self.handled == -1):
                if (self.shift - self.dim[1] >= 0):
                    self.shift -= self.dim[1]
                    self.draw_drop_menu()
                    self.handled = 0

            elif (keys[pygame.K_DOWN] and self.handled == -1):
                if (self.shift + self.dim[1] <= max_shift):
                    self.shift += self.dim[1]
                    self.draw_drop_menu()
                    self.handled = 1
            elif (self.handled == 0 and not keys[pygame.K_UP]):
                self.handled = -1
            elif (self.handled == 1 and not keys[pygame.K_DOWN]):
                self.handled = -1

    def draw_drop_menu(self):
        self.scroll_group.empty()
        self.scroll_group.add(self.scroll_button)
        keys = pygame.key.get_pressed()

        if (pygame.mouse.get_pressed()[0]):
            self.scroll_bar.set_coords((self.scroll_bar.coords[0], pygame.mouse.get_pos()[1]))
        elif (keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            self.scroll_bar.set_coords((self.scroll_bar.coords[0], self.coords[1] + self.dim[1]/2 + self.shift))
        if (self.scroll_bar.coords[1] + self.scroll_bar_height/2 > self.coords[1] + self.dim[1]/2 + self.max_height):
            self.scroll_bar.set_coords((self.scroll_bar.coords[0], self.coords[1] + self.dim[1]/2 + self.max_height - self.scroll_bar_height/2))
        if (self.scroll_bar.coords[1] - self.scroll_bar_height/2 < self.coords[1] + self.dim[1]/2):
            self.scroll_bar.set_coords((self.scroll_bar.coords[0], self.coords[1] + self.TRIANGLE_BUTTON_HEIGHT/2 + self.scroll_bar_height/2))

        self.scroll_group.add(self.scroll_back)
        self.scroll_group.add(self.scroll_bar)
        self.scroll_group.add(self.selected)

        for i in range(len(self.buttons)):
            if (self.coords[1] + (i + 1)*self.dim[1] - self.shift - self.tolerance > self.coords[1] + self.max_height):
                return
            if (self.coords[1] + (i + 1)*self.dim[1] - self.shift + self.tolerance < self.coords[1] + self.dim[1]/2):
                continue
            self.buttons[i].setCoords((self.coords[0], self.coords[1] + (i + 1)*self.dim[1] - self.shift))
            self.scroll_group.add(self.buttons[i])
        
        self.init_mouse_y = pygame.mouse.get_pos()[1]


    def toggle(self):
        if (not self.drag):
            self.extended = not self.extended
            if (self.extended):
                self.draw_drop_menu()
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
       @window = the Window class object

       @is_chosen - if the button is selected
    '''
    def __init__(self, text_arg, function, window):
        super().__init__()
        self.text = text_arg.render()
        self.copy_text = text_arg # Used for duplicating purposes
        self.dim = ()
        self.coords = ()
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.function = function
        self.screen = window.screen
        self.window = window
        self.handled = False

        self.is_chosen = False

    def copy(self):
        copy = ScrollButton(self.copy_text, self.function, self.window)
        return copy

    def setDim(self, dim):
        self.dim = dim

    def setCoords(self, coords):
        self.coords = coords

    def player_input(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                self.handled = False
            if pygame.mouse.get_pressed()[0] and (not self.window.options_screen) and not self.handled:
                if (self.function != None):
                    self.function()
                if (not self.is_chosen):
                    self.is_chosen = True
                self.handled = True
            else:
                self.image.fill("#778DA9")
        else:
            self.image.fill("#415A77")

    # If its in options, advanced tools, etc where a window would pop up, the button shouldn't be pressed
    def check_overlap(self):
        if (self.window.screen == Screen.NONE and self.screen != Screen.NONE):
            self.set_unpressable()
        else:
            self.set_pressable()

    def set_pressable(self):
        self.can_press = True

    def set_unpressable(self):
        self.can_press = False

    def change_func(self, func):
        self.function = func

    def update(self):
        #self.window.window.blit(self.text, (self.rect.x + self.width/2, self.rect.y + self.height/2))
        self.image = pygame.Surface(self.dim)
        self.rect = self.image.get_rect(center = self.coords)
        self.textRect = self.text.get_rect(center = self.coords)
        self.window.window.blit(self.text, self.textRect)
        self.check_overlap()
        self.player_input()

    
class Background(pygame.sprite.Sprite):
    # TODO: Make background slide
    '''Creates a background (also used as an array element)
       TODO: make the background have white edges or smth
       @color = the color that the background will be in
       @coords = the coordinates where the rectangle will be centered at
       @dim = the dimensions of the rectangle
    '''
    def __init__(self, coords, dim, color):
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

    def get_rect(self):
        return self.rect

    def get_coords(self):
        return self.coords

    def set_coords(self, coords):
        self.coords = coords

class TextBox(pygame.sprite.Sprite):

    ''' default_text = the text that will show up when first initialized
        coords = the coordinates of the textbox (centered at those coords)
        dim = the dimensions of the textbox
        function = what the textbox will do with the new values (MUST HAVE the text as an argument)
        it should also return what value it accepted and what the textbox will change to
        window = window class object
        after_text = what will appear after the text (That the user cannot change)
        is_integer = whether the input should only be in decimal numbers
            1 = decimals only
            0 = no restrictions
    '''
    def __init__(self, default_text, coords, dim, function, window, after_text, restrict):
        super().__init__()

        # Constants
        self.margin = 15

        # Initialization
        self.default_text = default_text
        self.coords = coords
        self.dim = dim
        self.restrict = restrict
        self.func = function
        self.image = pygame.Surface(dim)
        self.rect = self.image.get_rect(center = coords)
        self.window = window
        self.image.fill("#FFFFFF")
        self.after_text = after_text

        self.text_arg = default_text
        self.text = default_text.text
        self.text_rect = self.text_arg.render().get_rect(center = coords)
        self.render()

        # If you can type in the box
        self.active = False

        # extra thread to make typing feasible
        #self.thread = None
    
    def set_text(self, text):
        self.text = text
        self.render()

    def render(self):
        self.text += self.after_text
        self.text_arg.text = self.text

        
        self.text_rect = self.text_arg.render().get_rect(center = self.coords)
        # check if the box can fit all the stuff
        if (self.text_rect.width > self.rect.width - 2 * self.margin):
            if (len(self.after_text) > 0):
                self.text = self.text[:-len(self.after_text)]
            return -1

        self.window.window.blit(self.text_arg.render(), self.text_rect)
        if (len(self.after_text) > 0):
            self.text = self.text[:-len(self.after_text)]
        return 0

    '''
    def set_thread(self, thread):
        if self.thread is not None:
            self.window.event.set()
            self.thread.join()
        self.window.event.clear()
        self.thread = thread

    def clear_thread(self):
        self.thread = None
        self.window.event.set()
    '''

    def update(self, events_list):
        self.window.window.blit(self.text_arg.render(), self.text_rect)
        self.update_func(events_list)
        #update_func_thread = sequential_functions(add_args_to_func(self.update_func, events_list), self.clear_thread)
        #self.set_thread(threading.Thread(target=update_func_thread))
        #self.thread.start()

    
    def update_func(self, events_list):
        for event in events_list:
            self.window.window.blit(self.text_arg.render(), self.text_rect)
            # if mouse down and mouse outside of box
            if (event.type == pygame.MOUSEBUTTONDOWN):
                
                self.active = self.rect.collidepoint(event.pos)

            if (event.type == pygame.KEYDOWN and self.active):
                if (event.key == pygame.K_RETURN):
                    self.active = False

                elif (event.key == pygame.K_BACKSPACE):
                    self.text = self.text[:-1]

                else:
                    self.text += event.unicode
                    if (self.restrict == 1):
                        # check that it is a valid number
                        try:
                            float(self.text)
                        except ValueError:
                            print("Cannot type in characters")
                            self.text = self.text[:-1]
                
                    # check if number fits in box
                    if (self.render() == -1):
                        print("Text too large")
                        self.text = self.text[:-1]
                self.render()

    def do_func(self):
        self.set_text(str(self.func(self.text)))        

class Midi():

    C = 74
    MAX = 127
    brief = .5

    def __init__(self):
        port = pygame.midi.get_default_output_id()
        self.player = pygame.midi.Output(port, 0)
        self.player.set_instrument(13) # Grand_piano

        self.notes = []
        for i in range(1, 128):
            self.notes.append(False)
        # Constants
        self.brief = .5
        self.MAX = 127
        self.queue = Queue()

    def play(self, note, volume = MAX, length = brief):
        self.player.note_on(note, volume)
        self.queue.put((note, volume))

    def update(self):
        if (not self.queue.empty()):
           pop = self.queue.get()
           self.player.note_off(pop[0], pop[1])
