import threading
import time

import Algorithms.Sorting as Sorting
import pygame

import UI.Wrapper as Wrapper
from UI.Arrays import Array

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
    def display_main_menu(window, slide_in, screen_group, options_screen_group):
        # Constants
        TITLE_Y = 100
        SORTING_Y = 200
        GRAPH_Y = 270
        # TODO: Potentially refactor to get rid of window.screen_change and window_size_change
        if (window.screen == Wrapper.Screen.MAIN_MENU and (not window.screen_change and not window.window_size_change)):
            return
        # Remember to change screen
        window.screen = Wrapper.Screen.MAIN_MENU

        # Display everything
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        pressed_sorting = Wrapper.add_args_to_func(MainMenuActions.pressed_sorting, window)
        pressed_graph = Wrapper.add_args_to_func(MainMenuActions.pressed_graph, window)
        screen_group.add(Wrapper.Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, TITLE_Y), ubuntu_font, "#E0E1DD", Wrapper.Screen.MAIN_MENU, slide_in))
        screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), SORTING_Y), pressed_sorting, Wrapper.Screen.MAIN_MENU, window, slide_in))
        screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), GRAPH_Y), pressed_graph, Wrapper.Screen.MAIN_MENU, window, slide_in))
        
        # Options
        OptionActions.display_options_button(window, screen_group, options_screen_group)
    
    # Input code, specifically here for button presses
    def pressed_sorting(window):
        window.switch_screen(Wrapper.Screen.SORTING_SCREEN)
        window.screen_change = True
    def pressed_graph(window):
        window.switch_screen(Wrapper.Screen.GRAPH_MENU)
        window.screen_change = True

class OptionActions():

    def display_options_button(window, screen_group, options_screen_group):
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        display_options = Wrapper.add_args_to_func(OptionActions.display_options, window, options_screen_group)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), display_options, Wrapper.Screen.NONE, window, False))
    
    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(window, options_group):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        # Switch on options
        window.options_screen = True

        # Draw everything
        options_group.add(Wrapper.Background("#1B263B", (window.window.get_size()[0]/2, window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT)))
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        # Where the text starts rendering
        text_start = window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50
        options_group.add(Wrapper.Text(window, "Options", (window.window.get_size()[0]/2, text_start), ubuntu_font, "#E0E1DD", Wrapper.Screen.NONE, False))
        close_options = Wrapper.add_args_to_func(OptionActions.close_options, window, options_group)
        press_main_menu = Wrapper.add_args_to_func(OptionActions.press_main_menu, window, options_group)
        options_group.add(Wrapper.TextButton("Return", (window.window.get_size()[0]/2, text_start + 100), close_options, Wrapper.Screen.NONE, window, False, True))
        options_group.add(Wrapper.TextButton("Main Menu", (window.window.get_size()[0]/2, text_start + 175), press_main_menu, Wrapper.Screen.NONE, window, False, True))
    
    # Input (specifically buttons)

    '''@args = options_group'''
    def close_options(window, options_group):
        options_group.empty()
        # TODO: Fix glitch where when you press the return button, it will simultaneously press the button behind it
        time.sleep(0.30)
        window.options_screen = False

    '''@args[0] = options_group
       @args[1] = screen_group
    '''
    def press_main_menu(window, options_group):
        window.event.set()
        OptionActions.close_options(window, options_group)
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
    def __init__(self, window, sorting_group, midi):
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

        self.array_length = 64

        self.SORTING_X = (window.window.get_size()[0] - self.CONFIG_WIDTH - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        self.sorting_group = sorting_group
        sorting_group.empty()
        #print("{},{}  {},{}".format(self.SORTING_WIDTH, self.SORTING_HEIGHT, self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
        self.array = Array(sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2), self.array_length, midi)

    def display_sorting(self, window, screen_group, options_screen_group, scroll_group):
        if (window.screen == Wrapper.Screen.SORTING_SCREEN and (not window.screen_change and not window.window_size_change)):
            return
        # Change Screen
        window.screen = Wrapper.Screen.SORTING_SCREEN

        # Drawing Everything
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        # TODO: Make it slide by parameter?
        screen_group.add(Wrapper.Text(window, "Sorting", (window.window.get_size()[0]/2, self.TITLE_Y), ubuntu_font, "#E0E1DD", Wrapper.Screen.SORTING_SCREEN, True))
        #print(CONFIG_WIDTH)
        #print(CONFIG_HEIGHT)
        screen_group.add(Wrapper.Background("#1B263B", (self.SORTING_X, self.SORTING_Y), (self.SORTING_WIDTH, self.SORTING_HEIGHT)))
        #screen_group.add(Wrapper.Background("#1B263B", (CONFIG_X, CONFIG_Y), (CONFIG_WIDTH, CONFIG_HEIGHT)))

        def selection_sort():
            selection_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.selection_sort, self.array, window.event), sort_done)
            set_sorting_thread(threading.Thread(target=selection_sort))
            return self.sorting_thread.start()

        def insertion_sort():
            insertion_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.insertion_sort, self.array, window.event), sort_done)
            set_sorting_thread(threading.Thread(target=insertion_sort))
            return self.sorting_thread.start()

        def quick_sort():
            quick_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.quick_sort, self.array, window.event, 0, self.array.length(), True), sort_done)
            set_sorting_thread(threading.Thread(target=quick_sort))
            return self.sorting_thread.start()
        
        def merge_sort():
            merge_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.merge_sort, self.array, window.event, 0, self.array.length(), True), sort_done)
            set_sorting_thread(threading.Thread(target=merge_sort))
            return self.sorting_thread.start()

        def heap_sort():
            heap_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.heap_sort, self.array, window.event), sort_done)
            set_sorting_thread(threading.Thread(target=heap_sort))
            return self.sorting_thread.start()

        def set_sorting_thread(thread):
            if self.sorting_thread is not None:
                window.event.set()
                self.sorting_thread.join()
            window.event.clear()
            self.sorting_thread = thread

        def on_reset():
            window.event.set()

        def sort_done():
            self.sorting_thread = None
            window.event.set()

        screen_group.add(Wrapper.TextButton("Shuffle", ((5*window.window.get_size()[0]/6), 200), Wrapper.sequential_functions(self.array.shuffle, on_reset), Wrapper.Screen.SORTING_SCREEN, window))
        screen_group.add(Wrapper.TextButton("Reset", ((5*window.window.get_size()[0]/6), 270), Wrapper.sequential_functions(self.array.reset, on_reset), Wrapper.Screen.SORTING_SCREEN, window))

        self.sorting_thread = None

        selection_sort_button = Wrapper.ScrollButton("Selection Sort", selection_sort, Wrapper.Screen.SORTING_SCREEN, window)
        insertion_sort_button = Wrapper.ScrollButton("Insertion Sort", insertion_sort, Wrapper.Screen.SORTING_SCREEN, window)
        quick_sort_button = Wrapper.ScrollButton("Quick Sort", quick_sort, Wrapper.Screen.SORTING_SCREEN, window)
        merge_sort_button = Wrapper.ScrollButton("Merge Sort", merge_sort, Wrapper.Screen.SORTING_SCREEN, window)
        heap_sort_button = Wrapper.ScrollButton("Heap Sort", heap_sort, Wrapper.Screen.SORTING_SCREEN, window)
        buttons = (selection_sort_button, quick_sort_button, merge_sort_button, heap_sort_button, insertion_sort_button)
        scroll_bar = (Wrapper.ScrollBar(((5*window.window.get_size()[0]/6), 340), (200, 50), buttons, scroll_group, window))

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
