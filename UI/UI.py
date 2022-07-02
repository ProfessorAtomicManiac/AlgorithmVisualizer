import enum
import time
import pygame
import UI.Wrapper as Wrapper

class Screen(enum.Enum):
    '''Enum for which screen the window is on
    '''
    NONE = -1
    MAIN_MENU = 0
    SORTING_SCREEN = 1
    GRAPH_MENU = 2

class MainMenuActions():
    '''These tend to go in the @func for the button classes
       args[0] = screen_group
       args[1] = options_group
    '''
    def display_main_menu(window, args):
        TITLE_Y = 100
        SORTING_Y = 200
        GRAPH_Y = 270
        if (window.screen == Screen.MAIN_MENU and not window.screen_change):
            return
        window.screen = Screen.MAIN_MENU
        screen_group = args[0]
        options_screen_group = args[1]
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        screen_group.add(Wrapper.Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, TITLE_Y), ubuntu_font, "#E0E1DD", Screen.MAIN_MENU))
        screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), SORTING_Y), MainMenuActions.pressed_sorting, Screen.MAIN_MENU, window))
        screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), GRAPH_Y), MainMenuActions.pressed_graph, Screen.MAIN_MENU, window))
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), OptionActions.display_options, Screen.NONE, window, False, options_screen_group, screen_group))
    
    def pressed_sorting(window, *args):
        window.switch_screen(Screen.SORTING_SCREEN)
        window.screen_change = True
    def pressed_graph(window, *args):
        window.switch_screen(Screen.GRAPH_MENU)
        window.screen_change = True

class OptionActions():
    '''@args = options_group should be passed in first, then screen_group'''
    def display_options(window, args):
        OPTIONS_WIDTH = 300
        OPTIONS_HEIGHT = 300

        window.options_screen = True
        options_group = args[0]
        screen_group = args[1]
        options_group.add(Wrapper.Background(window, "#1B263B", (window.window.get_size()[0]/2, window.window.get_size()[1]/2), (OPTIONS_WIDTH, OPTIONS_HEIGHT)))
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        # Where the text starts rendering
        text_start = window.window.get_size()[1]/2 - OPTIONS_HEIGHT/2 + 50
        options_group.add(Wrapper.Text(window, "Options", (window.window.get_size()[0]/2, text_start), ubuntu_font, "#E0E1DD", Screen.NONE, False))
        options_group.add(Wrapper.TextButton("Return", (window.window.get_size()[0]/2, text_start + 100), OptionActions.close_options, Screen.NONE, window, False, True, options_group))
        options_group.add(Wrapper.TextButton("Main Menu", (window.window.get_size()[0]/2, text_start + 175), OptionActions.press_main_menu, Screen.NONE, window, False, True, options_group, screen_group))
    
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
        window.screen = Screen.MAIN_MENU
        window.screen_change = True
        window.options_screen = False

class SortingActions():
    def display_sorting(window, args):
        if (window.screen == Screen.SORTING_SCREEN and not window.screen_change):
            return
        TITLE_Y = 50

        SORTING_WIDTH = 1000
        SORTING_HEIGHT = 400
        # Can also be considered as "margins"
        SORTING_X = 100
        SORTING_Y = 50

        CONFIG_WIDTH = SORTING_WIDTH
        CONFIG_X = SORTING_X
        CONFIG_Y = SORTING_HEIGHT + 2*SORTING_Y
        CONFIG_HEIGHT = window.window.get_size()[1] - SORTING_HEIGHT - 2*SORTING_Y - SORTING_Y

        window.screen = Screen.SORTING_SCREEN
        screen_group = args[0]
        options_screen_group = args[1]
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        screen_group.add(Wrapper.Text(window, "Sorting", (window.window.get_size()[0]/2, TITLE_Y), ubuntu_font, "#E0E1DD", Screen.SORTING_SCREEN))
        
        print(CONFIG_WIDTH)
        print(CONFIG_HEIGHT)
        screen_group.add(Wrapper.Background(window, "#1B263B", (SORTING_X, SORTING_Y), (SORTING_WIDTH, SORTING_HEIGHT)))
        screen_group.add(Wrapper.Background(window, "#1B263B", (CONFIG_X, CONFIG_Y), (CONFIG_WIDTH, CONFIG_HEIGHT)))
        
        #screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), 200), MainMenuActions.pressed_sorting, Screen.SORTING_SCREEN, window))
        #screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), 270), MainMenuActions.pressed_graph, Screen.SORTING_SCREEN, window))
        
        
        options_button_1 = pygame.image.load('Button/OptionButtons/options.png').convert_alpha()
        options_button_1 = pygame.transform.rotozoom(options_button_1, 0, 0.1)
        options_button_2 = pygame.image.load('Button/OptionButtons/options_hover.png').convert_alpha()
        options_button_2 = pygame.transform.rotozoom(options_button_2, 0, 0.1)
        # TODO: Crop image properly using Figma
        screen_group.add(Wrapper.Button((options_button_1, options_button_2), ((window.window.get_size()[0])-40, 40), OptionActions.display_options, Screen.NONE, window, False, options_screen_group, screen_group))

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