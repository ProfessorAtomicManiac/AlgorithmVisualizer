import time
import pygame
from UI.Arrays import Array
import UI.Wrapper as Wrapper

''' This should only have code concerning the UI duh
    Specifically the display of screens, and functions for input (button presses)
    Everything here should just to be to display stuff and inputs
'''

class MainMenuActions():
    '''These tend to go in the @func for the button classes
       slide_in = the object will slide in from the right of the screen
       args[0] = screen_group
       args[1] = options_group
    '''
    def display_main_menu(window, slide_in, args):
        # Constants
        TITLE_Y = 100
        SORTING_Y = 200
        GRAPH_Y = 270
        # TODO: Potentially refactor to get rid of window.screen_change and window_size_change
        if (window.screen == Wrapper.Screen.MAIN_MENU and (not window.screen_change and not window.window_size_change)):
            return
        # Remember to change screen
        window.screen = Wrapper.Screen.MAIN_MENU

        screen_group = args[0]
        options_screen_group = args[1]

        # Display everything
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        screen_group.add(Wrapper.Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, TITLE_Y), ubuntu_font, "#E0E1DD", Wrapper.Screen.MAIN_MENU, slide_in))
        screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), SORTING_Y), MainMenuActions.pressed_sorting, Wrapper.Screen.MAIN_MENU, window, slide_in))
        screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), GRAPH_Y), MainMenuActions.pressed_graph, Wrapper.Screen.MAIN_MENU, window, slide_in))
        
        # Options
        OptionActions.display_options_button(window, screen_group, options_screen_group)
    
    # Input code, specifically here for button presses
    def pressed_sorting(window, *args):
        window.switch_screen(Wrapper.Screen.SORTING_SCREEN)
        window.screen_change = True
    def pressed_graph(window, *args):
        window.switch_screen(Wrapper.Screen.GRAPH_MENU)
        window.screen_change = True

class OptionActions():

    def display_options_button(window, screen_group, options_screen_group):
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), OptionActions.display_options, Wrapper.Screen.NONE, window, False, options_screen_group, screen_group))
    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(window, args):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        # Switch on options
        window.options_screen = True
        options_group = args[0]
        screen_group = args[1]

        # Draw everything
        options_group.add(Wrapper.Background("#1B263B", (window.window.get_size()[0]/2, window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT)))
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        # Where the text starts rendering
        text_start = window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50
        options_group.add(Wrapper.Text(window, "Options", (window.window.get_size()[0]/2, text_start), ubuntu_font, "#E0E1DD", Wrapper.Screen.NONE, False))
        options_group.add(Wrapper.TextButton("Return", (window.window.get_size()[0]/2, text_start + 100), OptionActions.close_options, Wrapper.Screen.NONE, window, False, True, options_group))
        options_group.add(Wrapper.TextButton("Main Menu", (window.window.get_size()[0]/2, text_start + 175), OptionActions.press_main_menu, Wrapper.Screen.NONE, window, False, True, options_group, screen_group))
    
    # Input (specifically buttons)

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
        window.screen = Wrapper.Screen.MAIN_MENU
        window.screen_change = True
        window.options_screen = False

'''TODO: These classes are inconsistent with being entirely static and being an instance based class. Make it consistent
so initalization is easier'''
class SortingActions():
    ''' Displays the sorting screen duh
        window = window class
        args[0] = screen_group
        args[1] = options_group
        args[2] = sorting_group
    '''
    '''This class has constructor so we can construct one array that all methods can access'''
    def __init__(self, window, sorting_group):
        # Constants
        self.TITLE_Y = 50
        # Margins for all boxes
        self.MARGIN_X = 25
        self.MARGIN_Y = 25
        # Calculations for certain values
        self.SORTING_WIDTH = (window.window.get_size()[0] - 3*self.MARGIN_X)*(3/4) # Ideally is ~800
        self.SORTING_HEIGHT = (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)
        self.CONFIG_WIDTH = 300
        #CONFIG_X = SORTING_MARGIN_X
        #CONFIG_Y = SORTING_HEIGHT + 2*SORTING_MARGIN_Y
        self.CONFIG_HEIGHT = self.SORTING_HEIGHT

        self.SORTING_X = (window.window.get_size()[0] - self.CONFIG_WIDTH - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        self.sorting_group = sorting_group
        sorting_group.empty()
        #print("{},{}  {},{}".format(self.SORTING_WIDTH, self.SORTING_HEIGHT, self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
        self.array = Array(sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2), 20)

    def display_sorting(self, window, args):
        if (window.screen == Wrapper.Screen.SORTING_SCREEN and (not window.screen_change and not window.window_size_change)):
            return
        # Change Screen
        window.screen = Wrapper.Screen.SORTING_SCREEN

        screen_group = args[0]
        options_screen_group = args[1]

        # Drawing Everything
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        # TODO: Make it slide by parameter?
        screen_group.add(Wrapper.Text(window, "Sorting", (window.window.get_size()[0]/2, self.TITLE_Y), ubuntu_font, "#E0E1DD", Wrapper.Screen.SORTING_SCREEN, True))
        #print(CONFIG_WIDTH)
        #print(CONFIG_HEIGHT)
        screen_group.add(Wrapper.Background("#1B263B", (self.SORTING_X, self.SORTING_Y), (self.SORTING_WIDTH, self.SORTING_HEIGHT)))
        #screen_group.add(Wrapper.Background("#1B263B", (CONFIG_X, CONFIG_Y), (CONFIG_WIDTH, CONFIG_HEIGHT)))
        
        #screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), 200), MainMenuActions.pressed_sorting, Screen.SORTING_SCREEN, window))
        #screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), 270), MainMenuActions.pressed_graph, Screen.SORTING_SCREEN, window))
        
        # Options button
        OptionActions.display_options_button(window, screen_group, options_screen_group)

    def pressed_sort():
        pass

    def pressed_shuffle():
        pass

    def pressed_generate():
        pass

    def input_generate():
        pass

    def input_size():
        pass

    def pressed_pause():
        pass

    def pressed_forward():
        pass

    def pressed_backward():
        pass

    def checked_step_delay():
        pass

    def input_time_delay():
        pass