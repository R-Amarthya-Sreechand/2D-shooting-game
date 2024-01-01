"""pygame = 2D graphics library - lets you make games"""
# First you should make the main surface
"""ctrl + shift + space -- to find the parameters in function"""
"""ctrl + space -- to find the methods list for an object or module"""

import pygame  # pygame = a package, # display = a module, #set_mode = a function

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Until here, when you run, the screen only blinks.
# Using the for loop below, When you iterate through all the events continuously at speed, the screen remains open


def main():
    # Set up a while loop - game/events loop

    run = True
    # pygame library has its own loop and is handling events,
    # causing the program to pause or stop when certain conditions are met.
    # When you click the cross button in the surface, then condition is met, and run = False.
    # and pygame.quit() happens
    while run:
        # get() gives List of all of the events
        # for loop goes through all the events (quit, open, play, etc..) and
        # if something is activated, then it does something according to condition given in the loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT = 256 when printed
                run = False

    pygame.quit()
    """IF ONLY while run loop is present (ie; inner for loop not present), then also black display is shown. ie; When a loop runs, the display of pygame opens automatically"""


if __name__ == "__main__":
    main()
