import threading
import time

import Algorithms.Sorting as Sorting
import pygame

import UI.Wrapper as Wrapper
from UI.Arrays import Array

import tkinter
from tkinter import filedialog

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
    def display_main_menu(window, slide_in, screen_group, options_screen_group, midi):
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
        screen_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Sorting", Wrapper.FontSizes.BUTTON_SIZE), ((window.window.get_size()[0] / 2), SORTING_Y), pressed_sorting, window, slide_in))
        screen_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Graphs", Wrapper.FontSizes.BUTTON_SIZE), ((window.window.get_size()[0] / 2), GRAPH_Y), pressed_graph, window, slide_in))
        
        # Options
        return OptionActions(window, screen_group, options_screen_group, midi, slide_in)
        
    # Input code, specifically here for button presses
    def pressed_sorting(window):
        window.switch_screen(Wrapper.Screen.SORTING_SCREEN)
    def pressed_graph(window):
        window.switch_screen(Wrapper.Screen.GRAPH_MENU)

class OptionActions():

    def __init__(self, window, screen_group, options_screen_group, midi, slide_in):
        options_button_1 = pygame.image.load('Images/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Images/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        display_options = Wrapper.add_args_to_func(self.display_options, window, options_screen_group)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), display_options, window, slide_in))
        self.slider = None
        self.midi = midi
        self.volume = None
    
    # Input (specifically buttons)

    '''@args = options_group'''
    def close_options(self, window, options_group):
        options_group.empty()
        self.slider.do_func()
        # TODO: Fix glitch where when you press the return button, it will simultaneously press the button behind it
        time.sleep(0.30)
        window.display = False

    '''@args[0] = options_group
       @args[1] = screen_group
    '''
    def press_main_menu(self, window, options_group):
        window.event.set()
        self.close_options(window, options_group)
        window.screen = Wrapper.Screen.MAIN_MENU
        window.screen_change = True
        window.display = False

    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(self, window, options_group):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        # Switch on options
        window.display = True
        options_group.empty()

        # Draw everything
        options_group.add(Wrapper.Background((window.window.get_size()[0]/2, window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR, window, None, False, 3))
        
        # Where the text starts rendering
        text_start = window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50

        exit_1 = pygame.image.load('Images/remove.png').convert_alpha()
        exit_1 = pygame.transform.rotozoom(exit_1, 0, 0.05)
        exit_2 = pygame.image.load('Images/remove_hover.png').convert_alpha()
        exit_2 = pygame.transform.rotozoom(exit_2, 0, 0.05)
        close_options = Wrapper.add_args_to_func(self.close_options, window, options_group)
        press_main_menu = Wrapper.add_args_to_func(self.press_main_menu, window, options_group)
        options_group.add(Wrapper.Button((exit_1, exit_2), (window.window.get_size()[0]/2 + OPTIONS_WIDTH/2 - 25, text_start - 25), close_options, window, False, Wrapper.Screen.NONE))

        self.low = pygame.image.load('Images/Volume/volume_low.png').convert_alpha()
        self.low = pygame.transform.rotozoom(self.low, 0, 0.15)
        self.medium = pygame.image.load('Images/Volume/volume_medium.png').convert_alpha()
        self.medium = pygame.transform.rotozoom(self.medium, 0, 0.15)
        self.high = pygame.image.load('Images/Volume/volume_max.png').convert_alpha()
        self.high = pygame.transform.rotozoom(self.high, 0, 0.15)
        self.volume = Wrapper.Background((window.window.get_size()[0]/2 - 105, text_start + 150), (0, 0), None, window, self.medium)
        options_group.add(self.volume)
        options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Options", Wrapper.FontSizes.TITLE_SIZE), (window.window.get_size()[0]/2, text_start), window, False, Wrapper.Screen.NONE))
        options_group.add(Wrapper.TextButton(Wrapper.DefaultText.text("Main Menu", Wrapper.FontSizes.BUTTON_SIZE), (window.window.get_size()[0]/2, text_start + 75), press_main_menu, window, False, Wrapper.Screen.NONE))
        self.slider = Wrapper.Slider((window.window.get_size()[0]/2 + 25, text_start + 150), 200, lambda a : self.midi.change_volume(a), window, options_group, self.midi.volume)

    def update(self):
        if (self.slider != None):
            self.slider.update()
        
        if (self.volume != None):
            if (self.slider.val <= 0.333):
                self.volume.change_image(self.low)
            elif (self.slider.val > 0.333 and self.slider.val <= 0.6666):
                self.volume.change_image(self.medium)
            elif (self.slider.val > 0.6666):
                self.volume.change_image(self.high)

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
        scroll_group[0].empty()
        scroll_group[1].empty()
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
        self.scroll_bar = []

        self.file = None

        self.SORTING_X = (window.window.get_size()[0] - self.CONFIG_WIDTH - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        self.sorting_group = sorting_group
        self.aux_sorting_group = aux_sorting_group
        sorting_group.empty()

        self.array_config = [self.array_length, 1, self.array_length]
        self.list = [i for i in range(1, self.array_length+1)]
        #print("{},{}  {},{}".format(self.SORTING_WIDTH, self.SORTING_HEIGHT, self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
        self.array = Array(sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2), 1, self.array_length, midi)
        self.aux_array = None

        self.handled = 0


    def update(self):
        # self.scroll_bar[0] = reset scroll
        # self.scroll_bar[1] = sort scroll
        # Glitch where it will click the button behind it
        #print(len(self.list))
        if (len(self.scroll_bar) == 2):
            #print(self.scroll_bar[0].can_press)
            if (self.window.display and self.handled != 1):
                #print("options extended")
                self.scroll_bar[0].set_unpressable()
                self.scroll_bar[1].set_unpressable()
                self.toggle_aux.set_unpressable()
                self.generate.set_unpressable()
                self.advanced.set_unpressable()
                self.handled = 1
            elif (self.scroll_bar[0].extended and self.handled != 2):
                #print("reset scroll extended")

                self.scroll_bar[1].set_unpressable()
                self.toggle_aux.set_unpressable()
                self.generate.set_unpressable()
                self.advanced.set_unpressable()
                self.handled = 2
            elif (self.scroll_bar[1].extended and self.handled != 3):
                #print("sorts scroll extended")

                self.scroll_bar[0].set_unpressable()
                self.toggle_aux.set_unpressable()
                self.generate.set_unpressable()
                self.advanced.set_unpressable()
                self.handled = 3
            elif (not self.window.display and not self.scroll_bar[0].extended and not self.scroll_bar[1].extended and self.handled != 0):
                #print("nothing extended")

                self.scroll_bar[0].set_pressable()
                self.scroll_bar[1].set_pressable()
                self.toggle_aux.set_pressable()
                self.generate.set_pressable()
                self.advanced.set_pressable()
                self.handled = 0

        if (self.options_actions != None):
            self.options_actions.update()

    def on_reset(self):
        self.window.event.set()

    def display_sorting(self, screen_group, options_screen_group, slide_in = True):
        self.scroll_bar = []
        if (self.window.screen == Wrapper.Screen.SORTING_SCREEN and (not self.window.screen_change and not self.window.window_size_change)):
            return
        # Change Screen
        self.window.screen = Wrapper.Screen.SORTING_SCREEN

        # Drawing Everything
        screen_group.empty()
        self.scroll_group[0].empty()
        self.scroll_group[1].empty()
        self.SORTING_WIDTH = (3*self.window.window.get_size()[0]/4 - 2*self.MARGIN_X) # Ideally is ~800
        self.SORTING_HEIGHT = (self.window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)
        self.SORTING_X = (3*self.window.window.get_size()[0]/4 - 2*self.MARGIN_X)/2 + self.MARGIN_X
        self.SORTING_Y = 2*self.TITLE_Y + self.MARGIN_Y + (self.window.window.get_size()[1] - 2*self.TITLE_Y - 2*self.MARGIN_Y)/2
        #print(self.SORTING_X, self.SORTING_Y, self.SORTING_WIDTH, self.SORTING_HEIGHT)
        self.array = Array(self.sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.MARGIN_X, self.SORTING_Y - self.SORTING_HEIGHT/2), 1, self.array_length, self.midi)

        screen_group.add(Wrapper.Text(Wrapper.DefaultText.text("Sorting", Wrapper.FontSizes.TITLE_SIZE), (self.window.window.get_size()[0]/2, self.TITLE_Y), self.window, slide_in))
        screen_group.add(Wrapper.Background((self.MARGIN_X + self.SORTING_WIDTH/2, self.SORTING_Y), (self.SORTING_WIDTH, self.SORTING_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR, self.window, None, False))
        
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

        buttons = []
        resets = []
        def bind_function(sort_input):
            def func():
                sort_algo = Wrapper.sequential_functions(Wrapper.add_args_to_func(sort_input.sort, self.array, self.window.event, self.aux_array), sort_done)
                set_sorting_thread(threading.Thread(target=sort_algo))
                return self.sorting_thread.start()
            func.__name__ = sort_input.name
            return func

        for sort_input in Sorting.sorting_algos:
            buttons.append(Wrapper.ScrollButton(Wrapper.DefaultText.text(sort_input.name, Wrapper.FontSizes.BUTTON_SIZE), bind_function(sort_input), self.window))
        
        resets.append(Wrapper.ScrollButton(Wrapper.DefaultText.text("Sorted", Wrapper.FontSizes.BUTTON_SIZE), Wrapper.sequential_functions(self.on_reset, self.array.reset), self.window))
        resets.append(Wrapper.ScrollButton(Wrapper.DefaultText.text("Reverse", Wrapper.FontSizes.BUTTON_SIZE), Wrapper.sequential_functions(self.on_reset, self.array.reverse), self.window))
        resets.append(Wrapper.ScrollButton(Wrapper.DefaultText.text("Previous File", Wrapper.FontSizes.BUTTON_SIZE), Wrapper.sequential_functions(self.on_reset, self.array.load_config), self.window))

        # Button Constants
        button_col_top = 130 # Where the buttons start
        button_margin = 70

        self.shuffle_button = Wrapper.TextButton(Wrapper.DefaultText.text("Shuffle", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top), Wrapper.sequential_functions(self.on_reset, self.array.shuffle), self.window, slide_in)
        #self.reset_button = Wrapper.TextButton(Wrapper.DefaultText.text("Reset", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + button_margin), Wrapper.sequential_functions(self.on_reset, self.array.reset), self.window)
        
        
        self.toggle_aux = Wrapper.TextButton(Wrapper.DefaultText.text("Auxillary Array", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 3 * button_margin), Wrapper.sequential_functions(self.on_reset, self.toggle_aux_array), self.window, slide_in)
        self.generate = Wrapper.TextButton(Wrapper.DefaultText.text("Generate", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 4 * button_margin), Wrapper.sequential_functions(self.on_reset, self.array.generate), self.window, slide_in)
        self.advanced = Wrapper.TextButton(Wrapper.DefaultText.text("Advanced", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 5 * button_margin), Wrapper.sequential_functions(self.on_reset, self.show_advanced), self.window, slide_in)
        self.input = Wrapper.TextButton(Wrapper.DefaultText.text("Input", Wrapper.FontSizes.BUTTON_SIZE), ((5*self.window.window.get_size()[0]/6), button_col_top + 6 * button_margin), Wrapper.sequential_functions(self.on_reset, self.custom_array), self.window, slide_in)
        self.screen_group.add(self.shuffle_button)
        self.screen_group.add(self.toggle_aux)
        self.screen_group.add(self.generate)
        self.screen_group.add(self.advanced)
        self.screen_group.add(self.input)

        # scroll_group[0] = reset
        # scroll_group[1] = sorts
        # This scroll bar looks so shit cuz its off by a bit, make it better somehow
        self.scroll_bar = []
        self.scroll_bar.append(Wrapper.ScrollBar(resets, ((5*self.window.window.get_size()[0]/6), button_col_top + button_margin), (200, 50), self.scroll_group[0], self.window, "Reset", slide_in, 124.9))
        self.scroll_bar.append(Wrapper.ScrollBar(buttons, ((5*self.window.window.get_size()[0]/6), button_col_top + 2 * button_margin), (200, 50), self.scroll_group[1], self.window, "Choose Sorted", slide_in))
        # Options button

        # TODO: RETURNS STUPID STUFF, reduce returns and make it so that you don't have to call update manually in main file
        self.options_actions = OptionActions(self.window, screen_group, options_screen_group, self.midi, slide_in)
        return self.scroll_bar

    def toggle_aux_array(self):
        if self.aux_array == None:
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = Array(self.aux_sorting_group, (self.SORTING_WIDTH, self.SORTING_HEIGHT/2), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y), 1, self.array_length, self.midi)
        else:
            self.aux_array.kill()
            self.array.change((self.SORTING_WIDTH, self.SORTING_HEIGHT), (self.SORTING_X - self.SORTING_WIDTH/2, self.SORTING_Y - self.SORTING_HEIGHT/2))
            self.aux_array = None

    def show_advanced(self):
        # Constants
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 400

        # Switch on options
        self.window.display = True

        # Where the text starts rendering
        text_start = self.window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50

        # Draw everything
        self.options_group.empty()
        self.options_group.add(Wrapper.Background((self.window.window.get_size()[0]/2, self.window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT), Wrapper.Colors.SMALL_BACKGROUND_COLOR, self.window, None, False, 3))
        
        # Exit button
        exit_1 = pygame.image.load('Images/remove.png').convert_alpha()
        exit_1 = pygame.transform.rotozoom(exit_1, 0, 0.05)
        exit_2 = pygame.image.load('Images/remove_hover.png').convert_alpha()
        exit_2 = pygame.transform.rotozoom(exit_2, 0, 0.05)
        self.options_group.add(Wrapper.Button((exit_1, exit_2), (self.window.window.get_size()[0]/2 + OPTIONS_WIDTH/2 - 25, text_start - 25), self.close_window, self.window, False, Wrapper.Screen.NONE))

        self.options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Time Delay", Wrapper.FontSizes.SUB_TITLE_SIZE), (self.window.window.get_size()[0]/2, text_start), self.window, False, Wrapper.Screen.NONE))
        self.delay_textbox = Wrapper.TextBox(Wrapper.TextArgs(str(self.array.delay), Wrapper.Fonts(Wrapper.FontSizes.BUTTON_SIZE).UBUNTU_FONT, True, "#000000"), (self.window.window.get_size()[0]/2, text_start + 50), (200, 50), lambda a : self.array.change_delay(a), self.window, " secs", 1)
        
        self.options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Array Size", Wrapper.FontSizes.SUB_TITLE_SIZE), (self.window.window.get_size()[0]/2, text_start + 100), self.window, False, Wrapper.Screen.NONE))
        self.size_textbox = Wrapper.TextBox(Wrapper.TextArgs(str(self.array.size), Wrapper.Fonts(Wrapper.FontSizes.BUTTON_SIZE).UBUNTU_FONT, True, "#000000"), (self.window.window.get_size()[0]/2, text_start + 150), (200, 50), lambda a : self.array.change_size(a), self.window, "", 1)
                
        self.options_group.add(Wrapper.Text(Wrapper.DefaultText.text("Instrument", Wrapper.FontSizes.SUB_TITLE_SIZE), (self.window.window.get_size()[0]/2, text_start + 200), self.window, False, Wrapper.Screen.NONE))
        self.instrument_textbox = Wrapper.TextBox(Wrapper.TextArgs(str(self.midi.instrument), Wrapper.Fonts(Wrapper.FontSizes.BUTTON_SIZE).UBUNTU_FONT, True, "#000000"), (self.window.window.get_size()[0]/2, text_start + 250), (200, 50), lambda a : self.midi.change_instrument(a), self.window, "", 1)
        self.text_box_group.add(self.delay_textbox)
        self.text_box_group.add(self.size_textbox)
        self.text_box_group.add(self.instrument_textbox)
        
    # Input (specifically buttons)

    '''@args = options_group'''
    def close_window(self):
        self.delay_textbox.do_func()
        self.size_textbox.do_func()
        self.instrument_textbox.do_func()
        self.array_length = self.array.size
        self.options_group.empty()
        self.text_box_group.empty()
        # TODO: Fix glitch where when you press the return button, it will simultaneously press the button behind it
        time.sleep(0.30)    
        self.window.display = False

    def custom_array(self):
        tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
        self.file = filedialog.askopenfilename()
        if (self.file == ''):
            return
        f = open(self.file, 'r')
        self.array_config.clear()
        self.list.clear()
        self.array_config = list(map(int, f.readline().split()))
        self.list = list(map(int, f.readline().split()))
        self.array.change_array(self.array_config[1], self.array_config[2], self.array_config[0], self.list)
        