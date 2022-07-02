import enum
import time
import pygame
import Wrapper

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
        if (window.screen == Screen.MAIN_MENU):
            return
        window.screen = Screen.MAIN_MENU
        screen_group = args[0]
        options_screen_group = args[1]
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        screen_group.empty()
        screen_group.add(Wrapper.Text(window, "Algorithm Visualizer", (window.window.get_size()[0]/2, 100), ubuntu_font, "#E0E1DD", Screen.MAIN_MENU))
        screen_group.add(Wrapper.TextButton("Sorting", ((window.window.get_size()[0]/2), 200), MainMenuActions.pressed_sorting, Screen.MAIN_MENU, window))
        screen_group.add(Wrapper.TextButton("Graphs", ((window.window.get_size()[0]/2), 270), MainMenuActions.pressed_graph, Screen.MAIN_MENU, window))
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
        window.options_screen = True
        options_group = args[0]
        screen_group = args[1]
        options_group.add(Wrapper.Background(window, "#1B263B", (window.window.get_size()[0]/2, window.window.get_size()[1]/2), (300, 300)))
        ubuntu_font = pygame.font.Font("Fonts/Ubuntu-Bold.ttf", 50)
        # Where the text starts rendering
        text_start = 100
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
        MainMenuActions.display_main_menu(window, (args[1], args[0]))
        window.options_screen = False