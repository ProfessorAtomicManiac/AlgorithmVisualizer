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
        screen_group.empty()
        pressed_sorting = Wrapper.add_args_to_func(MainMenuActions.pressed_sorting, window)
        pressed_graph = Wrapper.add_args_to_func(MainMenuActions.pressed_graph, window)
        screen_group.add(Wrapper.Text(Wrapper.DefaultText.text("Algorithm Visualizer", Wrapper.FontSizes.TITLE_SIZE), (window.window.get_size()[0]/2, TITLE_Y), window, slide_in))
        screen_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Sorting", Wrapper.FontSizes.BUTTON_SIZE), ((window.window.get_size()[0]/2), SORTING_Y), pressed_sorting, window, slide_in))
        screen_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Graphs", Wrapper.FontSizes.BUTTON_SIZE), ((window.window.get_size()[0]/2), GRAPH_Y), pressed_graph, window, slide_in))
        
        # Options
        OptionActions.display_options_button(window, screen_group, options_screen_group)
    
    # Input code, specifically here for button presses
    def pressed_sorting(window):
        window.switch_screen(Wrapper.Screen.SORTING_SCREEN)
    def pressed_graph(window):
        window.switch_screen(Wrapper.Screen.GRAPH_MENU)

class OptionActions():

    def display_options_button(window, screen_group, options_screen_group):
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        display_options = Wrapper.add_args_to_func(OptionActions.display_options, window, options_screen_group)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), display_options, window, False, Wrapper.Screen.NONE))
    
    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(window, options_group):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        # Switch on options
        window.options_screen = True
        options_group.empty()

        # Draw everything
        options_group.add(Wrapper.Background((window.window.get_size()[0]/2, window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR))
        
        # Where the text starts rendering
        text_start = window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50

        options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Options", Wrapper.FontSizes.TITLE_SIZE), (window.window.get_size()[0]/2, text_start), window, False, Wrapper.Screen.NONE))
        close_options = Wrapper.add_args_to_func(OptionActions.close_options, window, options_group)
        press_main_menu = Wrapper.add_args_to_func(OptionActions.press_main_menu, window, options_group)
        options_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Return", Wrapper.FontSizes.BUTTON_SIZE), (window.window.get_size()[0]/2, text_start + 100), close_options, window, False, Wrapper.Screen.NONE))
        options_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Main Menu", Wrapper.FontSizes.BUTTON_SIZE), (window.window.get_size()[0]/2, text_start + 175), press_main_menu, window, False, Wrapper.Screen.NONE))
    
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
so initalization is consistent'''
class SortingActions():
    ''' Displays the sorting screen duh
        window = window class
        args[0] = screen_group
        args[1] = options_group
        args[2] = sorting_group
    '''
    # TODO: Auxillary array kinda broken when you change size
    '''This class has constructor so we can construct one array that all methods can access'''
    def __init__(self, window, screen_group, sorting_group, aux_sorting_group, scroll_group, options_group, text_box_group, midi):
        screen_group.empty()
        sorting_group.empty()
        aux_sorting_group.empty()
        scroll_group.empty()
        options_group.empty()
        text_box_group.empty()
        # Constants
        self.TITLE_Y = 50
        # Margins for all boxes
        self.MARGIN_X = 25
        self.MARGIN_Y = 10
        # Calculations for certain values
        self.SORTING_WIDTH = (window.window.get_size()[0] - 3*self.MARGIN_X)*(3/4) # Ideally is ~800
        self.SORTING_HEIGHT = (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)
        self.CONFIG_WIDTH = 300
        #CONFIG_X = SORTING_MARGIN_X
        #CONFIG_Y = SORTING_HEIGHT + 2*SORTING_MARGIN_Y
        self.CONFIG_HEIGHT = self.SORTING_HEIGHT

        self.array_length = 256

        self.midi = midi
        self.window = window
        self.screen_group = screen_group
        self.scroll_group = scroll_group
        self.options_group = options_group
        self.text_box_group = text_box_group

        self.SORTING_X = (window.window.get_size()[0] - self.CONFIG_WIDTH - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        self.sorting_group = sorting_group
        self.aux_sorting_group = aux_sorting_group
        sorting_group.empty()
        #print("{},{}  {},{}".format(self.SORTING_WIDTH, self.SORTING_HEIGHT, self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
        self.array = Array(sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2), self.array_length, midi)
        self.aux_array = None

    def update(self):
        # TODO: add if options window is open too
        if (self.scroll_bar.extended):
            self.toggle_aux.set_unpressable()
            self.generate.set_unpressable()
            self.advanced.set_unpressable()
        else:
            self.toggle_aux.set_pressable()
            self.generate.set_pressable()
            self.advanced.set_pressable()

    def on_reset(self):
        self.window.event.set()

    def display_sorting(self, screen_group, options_screen_group):
        if (self.window.screen == Wrapper.Screen.SORTING_SCREEN and (not self.window.screen_change and not self.window.window_size_change)):
            return
        # Change Screen
        self.window.switch_screen(Wrapper.Screen.SORTING_SCREEN)

        # Drawing Everything
        screen_group.empty()
        screen_group.add(Wrapper.Text(Wrapper.DefaultText.text("Sorting", Wrapper.FontSizes.TITLE_SIZE), (self.window.window.get_size()[0]/2, self.TITLE_Y), self.window))
        screen_group.add(Wrapper.Background((self.SORTING_X, self.SORTING_Y), (self.SORTING_WIDTH, self.SORTING_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR))

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

        def bogo_sort():
            bogo_sort = Wrapper.sequential_functions(Wrapper.add_args_to_func(Sorting.bogo_sort, self.array, self.window.event), sort_done)
            set_sorting_thread(threading.Thread(target=bogo_sort))
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

        # Button Constants
        button_col_top = 130 # Where the buttons start
        button_margin = 70

        self.shuffle_button = Wrapper.TextButton(Wrapper.DefaultText.text("Shuffle", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top), Wrapper.sequential_functions(self.array.shuffle, self.on_reset), self.window)
        self.reset_button = Wrapper.TextButton(Wrapper.DefaultText.text("Reset", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + button_margin), Wrapper.sequential_functions(self.array.reset, self.on_reset), self.window)
        self.toggle_aux = Wrapper.TextButton(Wrapper.DefaultText.text("Auxillary Array", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 3 * button_margin), Wrapper.sequential_functions(self.toggle_aux_array, self.on_reset), self.window)
        self.generate = Wrapper.TextButton(Wrapper.DefaultText.text("Generate", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 4 * button_margin), Wrapper.sequential_functions(self.array.generate, self.on_reset), self.window)
        self.advanced = Wrapper.TextButton(Wrapper.DefaultText.text("Advanced", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 5 * button_margin), Wrapper.sequential_functions(self.show_advanced, self.on_reset), self.window)
        self.screen_group.add(self.shuffle_button)
        self.screen_group.add(self.reset_button)
        self.screen_group.add(self.toggle_aux)
        self.screen_group.add(self.generate)
        self.screen_group.add(self.advanced)

        self.selection_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Selection Sort", Wrapper.FontSizes.BUTTON_SIZE), selection_sort, self.window)
        self.insertion_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Insertion Sort", Wrapper.FontSizes.BUTTON_SIZE), insertion_sort, self.window)
        self.quick_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Quick Sort", Wrapper.FontSizes.BUTTON_SIZE), quick_sort, self.window)
        self.merge_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Merge Sort", Wrapper.FontSizes.BUTTON_SIZE), merge_sort, self.window)
        self.heap_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Heap Sort", Wrapper.FontSizes.BUTTON_SIZE), heap_sort, self.window)
        self.radix_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Radix Sort", Wrapper.FontSizes.BUTTON_SIZE), radix_sort, self.window)
        self.counting_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Counting Sort", Wrapper.FontSizes.BUTTON_SIZE), counting_sort, self.window)
        self.bogo_sort_button = Wrapper.ScrollButton(Wrapper.DefaultText.text("Bogo Sort", Wrapper.FontSizes.BUTTON_SIZE), bogo_sort, self.window)

        buttons = (self.radix_sort_button, self.quick_sort_button, self.merge_sort_button, self.heap_sort_button, self.insertion_sort_button, self.selection_sort_button, self.counting_sort_button, self.bogo_sort_button)
        self.scroll_bar = (Wrapper.ScrollBar(buttons, ((5*self.window.window.get_size()[0]/6), button_col_top + 2 * button_margin), (200, 50), self.scroll_group, self.window))
        # Options button
        OptionActions.display_options_button(self.window, screen_group, options_screen_group)
        return self.scroll_bar

    def toggle_aux_array(self):
        if self.aux_array == None:
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = Array(self.aux_sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y), self.array_length, self.midi)
        else:
            self.aux_array.kill()
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = None

    def show_advanced(self):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        # Switch on options
        self.window.options_screen = True

        # Draw everything
        self.options_group.empty()
        self.options_group.add(Wrapper.Background((self.window.window.get_size()[0]/2, self.window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR))
        
        # Where the text starts rendering
        text_start = self.window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50
        
        self.options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Time Delay", Wrapper.FontSizes.SUB_TITLE_SIZE), (self.window.window.get_size()[0]/2, text_start), self.window, False, Wrapper.Screen.NONE))
        self.delay_textbox = Wrapper.TextBox(Wrapper.TextArgs(str(self.array.delay), Wrapper.Fonts(Wrapper.FontSizes.BUTTON_SIZE).UBUNTU_FONT, True, "#000000"), (self.window.window.get_size()[0]/2, text_start + 50), (200, 50), lambda a : self.array.change_delay(a), self.window, " secs", 1)
        
        self.options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Array Size", Wrapper.FontSizes.SUB_TITLE_SIZE), (self.window.window.get_size()[0]/2, text_start + 100), self.window, False, Wrapper.Screen.NONE))
        self.size_textbox = Wrapper.TextBox(Wrapper.TextArgs(str(self.array.size), Wrapper.Fonts(Wrapper.FontSizes.BUTTON_SIZE).UBUNTU_FONT, True, "#000000"), (self.window.window.get_size()[0]/2, text_start + 150), (200, 50), lambda a : self.array.change_size(a), self.window, "", 1)
        self.options_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Return", Wrapper.FontSizes.BUTTON_SIZE), (self.window.window.get_size()[0]/2, text_start + 210), self.close_window, self.window, False, Wrapper.Screen.NONE))
        self.text_box_group.add(self.delay_textbox)
        self.text_box_group.add(self.size_textbox)
        
    # Input (specifically buttons)

    '''@args = options_group'''
    def close_window(self):
        self.delay_textbox.do_func()
        self.size_textbox.do_func()
        self.array_length = self.array.size
        self.options_group.empty()
        self.text_box_group.empty()
        # TODO: Fix glitch where when you press the return button, it will simultaneously press the button behind it
        time.sleep(0.30)
        self.window.options_screen = False
