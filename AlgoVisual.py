from sys import exit

import pygame
import pygame.midi
import this

import UI.UI as UI
import UI.Wrapper as Wrapper


def main(fps):
    '''Equivalent of public static void main(String[] args)'''
    pygame.init()
    pygame.midi.init()

    window = Wrapper.Window(1200, 600, Wrapper.Screen.NONE, True, False)
    midi = Wrapper.Midi()

    screen_group = pygame.sprite.Group()
    options_screen_group = pygame.sprite.Group()
    sorting_group = pygame.sprite.Group()
    aux_sorting_group = pygame.sprite.Group()
    # TODO: Find a way to not have to make an entire sprite group
    scroll_group_1 = pygame.sprite.Group()
    scroll_group_2 = pygame.sprite.Group()
    text_box_group = pygame.sprite.Group()
    scroll_bar = []
    sorting_actions = None

    UI.MainMenuActions.display_main_menu(window, True, screen_group, options_screen_group)

    while True:
        # General Events should be placed here
        events_list = pygame.event.get()
        for event in events_list:
            # If window changes size
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = Wrapper.Window(width, height, window.screen, False, True)
            if event.type == pygame.QUIT:
                window.event.set()
                del midi
                pygame.midi.quit()
                pygame.quit()
                exit()
        # apparentally python has no switch cases?
        # This should only have logic for what to do when its on screen x or something like that
        if (window.screen == Wrapper.Screen.MAIN_MENU and window.window_size_change):
            UI.MainMenuActions.display_main_menu(window, False, screen_group, options_screen_group)
            window.window_size_change = False
        elif (window.screen == Wrapper.Screen.MAIN_MENU and window.screen_change):
            UI.MainMenuActions.display_main_menu(window, True, screen_group, options_screen_group)
            window.screen_change = False
        elif (window.screen == Wrapper.Screen.SORTING_SCREEN and window.screen_change):
            sorting_actions = UI.SortingActions(window, screen_group, sorting_group, aux_sorting_group, [scroll_group_1, scroll_group_2], options_screen_group, text_box_group, midi)
            scroll_bar = sorting_actions.display_sorting(screen_group, options_screen_group)
            window.screen_change = False
        # TODO: make screen size change work for sorting screen
        elif (window.screen == Wrapper.Screen.SORTING_SCREEN and window.window_size_change):
            #UI.SortingActions.display_sorting(window, True, screen_group, options_screen_group)
            window.window_size_change = False

        # This should update everything (Logic to update everything)
        window.update() # Clears the screen
        screen_group.draw(window.window)
        screen_group.update()
        
        if (window.screen == Wrapper.Screen.SORTING_SCREEN):
            sorting_group.draw(window.window)
            sorting_group.update()
            aux_sorting_group.draw(window.window)
            aux_sorting_group.update()

            # find a way to just get rid of this logic for future
            extended = -1
            for i in range(len(scroll_bar)):
                if (scroll_bar[i].extended):
                    extended = i
            scroll_group_1.draw(window.window)
            scroll_group_1.update()
            scroll_group_2.draw(window.window)
            scroll_group_2.update()
            # Maybe make enum class instead
            if (extended != -1):
                if (extended == 0):
                    scroll_group_1.draw(window.window)
                    scroll_group_1.update()
                elif (extended == 1):
                    scroll_group_2.draw(window.window)
                    scroll_group_2.update()
            
            if (scroll_bar is not None):
                for scroll in scroll_bar:
                    scroll.button_checks()
            if (sorting_actions is not None):
                sorting_actions.update()

        if (window.options_screen):
            options_screen_group.draw(window.window)
            options_screen_group.update()
        text_box_group.draw(window.window)
        text_box_group.update(events_list)
        
        # Must have to update
        pygame.display.update()
        midi.update()
        window.clock.tick(fps)


# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)
