import pygame
from sys import exit
import UI.Wrapper as Wrapper
import UI.UI as UI

def main(fps):
    '''Equivalent of public static void main(String[] args)'''
    pygame.init()
    window = Wrapper.Window(1200, 600, UI.Screen.NONE)
    screen_group = pygame.sprite.Group()
    options_screen_group = pygame.sprite.Group()
    UI.MainMenuActions.display_main_menu(window, (screen_group, options_screen_group))

    while True:
        window.update()

        for event in pygame.event.get():
            # If window changes size
            # TODO: Window changing size no longer works anymore
            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                window = Wrapper.Window(width, height, window.screen)
                window.screen_change = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # apparentally python has no switch cases?
        # either update to python 3.10 or create a dictionary
        if (window.screen == UI.Screen.MAIN_MENU and window.screen_change):
            UI.MainMenuActions.display_main_menu(window, (screen_group, options_screen_group))
            print("Main Menu")

            window.screen_change = False
        elif (window.screen == UI.Screen.SORTING_SCREEN and window.screen_change):

            UI.SortingActions.display_sorting(window, (screen_group, options_screen_group))
            print("Sorting")

            window.screen_change = False

        screen_group.draw(window.window)
        screen_group.update()
        options_screen_group.draw(window.window)
        options_screen_group.update()
        pygame.display.update()
        window.clock.tick(fps)

# If only this file is run, then the code is executed
if __name__ == "__main__":
    main(60)