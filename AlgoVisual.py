import pygame
from sys import exit
import UI.Wrapper as Wrapper
import UI.UI as UI

def main(fps):
    '''Equivalent of public static void main(String[] args)'''
    pygame.init()
    window = Wrapper.Window(1200, 600, Wrapper.Screen.NONE, True, False)
    screen_group = pygame.sprite.Group()
    options_screen_group = pygame.sprite.Group()
    sorting_group = pygame.sprite.Group()
    UI.MainMenuActions.display_main_menu(window, True, (screen_group, options_screen_group))

    while True:

        # General Events should be placed here
        for event in pygame.event.get():
            # If window changes size
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = Wrapper.Window(width, height, window.screen, False, True)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # apparentally python has no switch cases?
        # TODO: either update to python 3.10 or create a dictionary
        # This should only have logic for what to do when its on screen x or something like that
        if (window.screen == Wrapper.Screen.MAIN_MENU and window.window_size_change):
            print("window changes size")
            UI.MainMenuActions.display_main_menu(window, False, (screen_group, options_screen_group))
            window.window_size_change = False
        elif (window.screen == Wrapper.Screen.MAIN_MENU and window.screen_change):
            UI.MainMenuActions.display_main_menu(window, True, (screen_group, options_screen_group))
            window.screen_change = False
        elif (window.screen == Wrapper.Screen.SORTING_SCREEN and window.screen_change):
            sorting_actions = UI.SortingActions(window, sorting_group)
            sorting_actions.display_sorting(window, (screen_group, options_screen_group, sorting_group))
            window.screen_change = False

        # This should update everything (Logic to update everything)
        window.update() # Clears the screen
        screen_group.draw(window.window)
        screen_group.update()
        options_screen_group.draw(window.window)
        options_screen_group.update()

        if (window.screen == Wrapper.Screen.SORTING_SCREEN):
            sorting_group.draw(window.window)
            sorting_group.update()
        
        # Must have to update
        pygame.display.update()
        window.clock.tick(fps)
        

# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)