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
    def __init__(self, window, screen_group, sorting_group, aux_sorting_group, scroll_group, midi):
        screen_group.empty()
        sorting_group.empty()
        aux_sorting_group.empty()
        scroll_group.empty()
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

        self.midi = midi
        self.window = window
        self.screen_group = screen_group
        self.scroll_group = scroll_group

        self.SORTING_X = (window.window.get_size()[0] - self.CONFIG_WIDTH - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        self.sorting_group = sorting_group
        self.aux_sorting_group = aux_sorting_group
        sorting_group.empty()
        #print("{},{}  {},{}".format(self.SORTING_WIDTH, self.SORTING_HEIGHT, self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
        self.array = Array(sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2), self.array_length, midi)
        self.aux_array = None

        # Debug variable
        self.mode = "Not Aux"
    def update(self):
        if (self.scroll_bar.extended):
            self.toggle_aux.set_unpressable()
        else:
            self.toggle_aux.set_pressable()

    def on_reset(self):
        self.window.event.set()

    def display_sorting(self, window, screen_group, options_screen_group):
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
            selection_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.selection_sort, self.array, self.window.event), sort_done)
            set_sorting_thread(threading.Thread(target=selection_sort))
            return self.sorting_thread.start()

        def insertion_sort():
            insertion_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.insertion_sort, self.array, self.window.event), sort_done)
            set_sorting_thread(threading.Thread(target=insertion_sort))
            return self.sorting_thread.start()

        def quick_sort():
            quick_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.quick_sort, self.array, self.window.event, 0, self.array.length(), True), sort_done)
            set_sorting_thread(threading.Thread(target=quick_sort))
            return self.sorting_thread.start()
        
        def merge_sort():
            merge_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.merge_sort, self.array, self.window.event, 0, self.array.length(), True), sort_done)
            set_sorting_thread(threading.Thread(target=merge_sort))
            return self.sorting_thread.start()

        def heap_sort():
            heap_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.heap_sort, self.array, self.window.event), sort_done)
            set_sorting_thread(threading.Thread(target=heap_sort))
            return self.sorting_thread.start()

        def radix_sort():
            radix_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.radix_sort, self.array, self.window.event, self.aux_array), sort_done)
            set_sorting_thread(threading.Thread(target=radix_sort))
            return self.sorting_thread.start()
        
        def counting_sort():
            counting_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.counting_sort, self.array, self.window.event, 0, self.array_length, self.aux_array), sort_done)
            set_sorting_thread(threading.Thread(target=counting_sort))
            return self.sorting_thread.start()

        def set_sorting_thread(thread):
            if self.sorting_thread is not None:
                self.window.event.set()
                self.sorting_thread.join()
            self.window.event.clear()
            self.sorting_thread = thread

        def sort_done():
            self.sorting_thread = None
            self.window.event.set()

        self.sorting_thread = None

        self.shuffle_button = Wrapper.TextButton("Shuffle", ((5*self.window.window.get_size()[0]/6), 200), Wrapper.sequential_functions(self.array.shuffle, self.on_reset), Wrapper.Screen.SORTING_SCREEN, self.window)
        self.reset_button = Wrapper.TextButton("Reset", ((5*self.window.window.get_size()[0]/6), 270), Wrapper.sequential_functions(self.array.reset, self.on_reset), Wrapper.Screen.SORTING_SCREEN, self.window)
        self.toggle_aux = Wrapper.TextButton("Auxillary Array", ((5*self.window.window.get_size()[0]/6), 410), Wrapper.sequential_functions(self.toggle_aux_array, self.on_reset), Wrapper.Screen.SORTING_SCREEN, self.window)
        self.generate = Wrapper.TextButton("Generate", ((5*self.window.window.get_size()[0]/6), 480), Wrapper.sequential_functions(self.array.generate, self.on_reset), Wrapper.Screen.SORTING_SCREEN, self.window)
        self.screen_group.add(self.shuffle_button)
        self.screen_group.add(self.reset_button)
        self.screen_group.add(self.toggle_aux)
        self.screen_group.add(self.generate)

        self.selection_sort_button = Wrapper.ScrollButton("Selection Sort", selection_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.insertion_sort_button = Wrapper.ScrollButton("Insertion Sort", insertion_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.quick_sort_button = Wrapper.ScrollButton("Quick Sort", quick_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.merge_sort_button = Wrapper.ScrollButton("Merge Sort", merge_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.heap_sort_button = Wrapper.ScrollButton("Heap Sort", heap_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.radix_sort_button = Wrapper.ScrollButton("Radix Sort", radix_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        self.counting_sort_button = Wrapper.ScrollButton("Counting Sort", counting_sort, Wrapper.Screen.SORTING_SCREEN, self.window)
        buttons = (self.radix_sort_button, self.quick_sort_button, self.merge_sort_button, self.heap_sort_button, self.insertion_sort_button, self.selection_sort_button, self.counting_sort_button)
        self.scroll_bar = (Wrapper.ScrollBar(((5*self.window.window.get_size()[0]/6), 340), (200, 50), buttons, self.scroll_group, self.window))
        # Options button
        OptionActions.display_options_button(window, screen_group, options_screen_group)
        return self.scroll_bar

    def toggle_aux_array(self):
        if self.aux_array == None:
            self.mode = "Aux"
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = Array(self.aux_sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y), self.array_length, self.midi)
        else:
            self.mode = "Not Aux"
            self.aux_array.kill()
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = None

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
