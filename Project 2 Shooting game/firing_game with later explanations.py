"""pygame = 2D graphics library - lets you make games"""

""" WHEN ONE WHILE LOOP RUNS, only ONE FRAME IS DISPLAYED BY USING draw_window FUNCTION (After running through the for loop, and some other lines of code, the display function or one frame is displayed).
 So, Imagine everything (bullet formation, bullet movement, vehicle movement) being done on ONE frame. 
 SO imagine/think GIVING Commands to be done on that frame only. ---USE THIS MINDSET"""
"""MINDSET - WE ARE DRAWING BY HAND EACH FRAME START TO END of the display, THEN OTHER FRAME drawn FROM START TO END
ie; When we remove a bullet from the list, then for the next frame, we draw the drawing of the frame without that bullet ((DONT THINK LIKE WE ARE DELETING bullet from VIDEO. IN REALITY, WE are drawing the next frame without that bullet))"""

"""THINK only Origin at top-left corner (with x,y coord) and a bare drawing of rectangle classes wrt that origin-[[[[FOR ALL RECTANGLES]]]] (WHICH ARE INVISIBLE AND CHANGING COORDINATES IN EACH FRAME) MOVING THROUGH THE REGION OF RECTANGLES"""
"""WHEN you import modules, then we are using their functions, not their objects. So we mostly want to do like this pygame.image.rotate(YELLOW_SPACESHIP)- instead of YELLOW_SPACESHIP.rotate() """
# First you should make the main surface
"""ctrl + shift + space -- to find the parameters in function"""
"""ctrl + space -- to find the methods list for an object or module"""
"""FileArg(shown in yellow_space.. constant's bracket's hints) is a class which is taken as a datatype (All datatypes are classes.)"""
import pygame  # pygame = a package, # display = a module, #set_mode = a function
import os  # Operating System(os): To help us define the path to things in the system

pygame.font.init()  # init() in font module is used for instantiating some font objects (which may be intialized by empty strings on the top level-outside of function) which are to be used in other functions in that module
pygame.mixer.init()

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 20)
# Returns an object of Font class (Font class is in font module) --GIVEN IN TYPE HINT ( A DATA TYPE IS returned --all data types are classes).
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLETS_VEL = 8
MAX_BULLETS = 5
SPACESHIIP_WIDTH, SPACESHIP_HEIGHT = 50, 50

# pygame.USEREVENT represents the code or number for NEW Custom user events, when you add 1, then it is added and we create 2 separate UNIQUE EVENT IDs to separate USEREVENTS
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(
        YELLOW_SPACESHIP_IMAGE, (SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)
    ),
    90,
)
# Joins both the directory and file
# IMPPPPPPP::: FileArg is a class which is taken as a datatype (All datatypes are classes.)
# Depending on Operating system, directory separator might be different, so used join function (we can use slashes as given in directory too)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
# left and top are the coordinates of the topleft corner point of a new rectangle -to be placed.
# width and height are the lengths from that point to the right and to the down respectively.


RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
# or use this -- D:\\Rich\\Python\\Project 2\\Assets\\spaceship_red.png
# os.getcwd()
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)


SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load("./Assets/space2.png"), (WIDTH, HEIGHT)
)


# Keys are not action based things . ie; Its a state focused..So used class.(And we can create 2 objects for it)
# x attribute is the x position of the top-left corner wrt screen(Eg: Border.x --> border's top-left corner's x position, yellow.x)
# Always consider only the origin of the boxes and the boxes' shape -which are moving around when subtracting and adding lengths
def yellow_handle_movement(yellow, keys_pressed):
    if keys_pressed[pygame.K_a] and VEL <= yellow.x:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x <= BORDER.x - VEL - yellow.width:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and VEL <= yellow.y:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y <= HEIGHT - VEL - yellow.height:  # DOWN
        yellow.y += VEL


def red_handle_movement(red, keys_pressed):
    if keys_pressed[pygame.K_LEFT] and BORDER.x + BORDER.width + VEL <= red.x:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x <= WIDTH - VEL - red.width:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and VEL <= red.y:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y <= HEIGHT - VEL - red.height:  # DOWN
        red.y += VEL


def handle_bullets(
    yellow_bullets: list[pygame.Rect],
    red_bullets: list[pygame.Rect],
    yellow: pygame.Rect,
    red: pygame.Rect,
):
    # for every bullet to move 1 BULLET_VEL distance, for loop given.
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        # if bullet.x + 40 == red.x and red.y-bullet.height <= bullet.y <= red.y+red.height: # Lower limit and upper limit defined
        if red.colliderect(bullet):
            # Did red's rectangle hit the rectange of bullet ? return True or False
            # A Custom event created, with an object of class EVENT (pygame.event.Event(RED_HIT)) passed into post function-which posts the event object to the event array (event array - .event).
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    winner_text_image = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(
        winner_text_image,
        (
            WIDTH / 2 - winner_text_image.get_width() / 2,
            HEIGHT / 2 - winner_text_image.get_height() / 2,
        ),
    )
    
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE_IMAGE, (0, 0))

    red_health_text_image = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    # Returns a Surface class's object- ie; a surface image is returned.

    yellow_health_text_image = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE
    )

    WIN.blit(
        red_health_text_image, (WIDTH - red_health_text_image.get_width() - 10, 10)
    )
    WIN.blit(yellow_health_text_image, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    # blit = surface copied on the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # pygame.draw.
    pygame.display.update()


def main():
    """Define two areas( RECANGULAR ), where the images will be placed.(Movement of image depends on movement of Rectangle)."""
    # Rect() is a class, so red & yellow are objects
    red = pygame.Rect(700, 290, SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)
    # Here, width,height is of the boundary Rectangle Class created with attribute.  (IMAGINE RECTANGLES :Which can't be seen with our eyes), it helps with collision detection, hitboxes, and rendering.
    yellow = pygame.Rect(100, 300, SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)

    # Here a red : is a rectangle which has top left corner at 700,300 and width&height as given
    # When we call WIN.blit (as in the draw_window()), destination given as 700,300.
    # So the Real image is positioned with it's top left corner at the top left corner of the rectangle of that image.

    red_bullets = []
    yellow_bullets = []

    red_health = 10  # Variables - which vary the value ((NOT A CONSTANT))
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Makes the speed of while loop cap at 60fps
        for event in pygame.event.get():
            # event (light blue) is an object of Event() class. .event is a module CONTAINING all these events
            if event.type == pygame.QUIT:  # Only when quit is pressed.
                run = False
                pygame.quit()

            # for bullets firing
            if event.type == pygame.KEYDOWN:
                # When ony pressing key downwards(not staying pressed-ie; then key is not pressed down.)
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # on the screen at a time we only want atmost 3 bullets of yellow always. When it goes off screen, we can fire another one
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 3,
                        40,
                        6,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 40, red.y + red.height // 2 - 3, 40, 6)
                    red_bullets.append(bullet)
                    # // put to make the divsion cast to integer.
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health == 0:
            # 1 or more bullets coming parallely can't hit the target simultaneously. So can't be less than 0
            winner_text = "YELLOW WINS !"
        if yellow_health == 0:
            winner_text = "RED WINS !"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        # Keys are like variables, Values in the dictionary-like datatype are 0 or 1 (True or False)
        # every time the loop passes, pressed down keys are returned (ie; at 60 keys per sec). ie; if we touch the keyboard 0.5/60 sec time duration, then it may not register- bcs when the interpretor runs the get_pressed() function, then key might not have been pressed

        yellow_handle_movement(yellow, keys_pressed)
        red_handle_movement(red, keys_pressed)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
        # Every second many whites backgrounds are drawn on screen(According to speed of while loop) (in default, black is drawn continously- hence we see black screen staying there.)

    main()


if __name__ == "__main__":
    main()


"""However, when you press keys during the delay, the key events are still being generated and stored in the event queue. These events are not processed immediately because the program is in a delay, but once the delay is over, the program resumes and starts processing the events in the queue.
So, when you check for event.type == pygame.KEYDOWN after the delay, it will detect and handle all the key events that occurred during the delay, leading to the behavior you've observed. If you want to prevent this, you might consider using other mechanisms to control the flow of your program without blocking it, such as timers or event-driven architectures."""


# The actual display update occurs later in the main loop, outside the event loop, in the following lines:
# draw_window(red, yellow, red_bullets, yellow_bullets)
# The draw_window function is where the graphical elements are drawn, and it's typically responsible for updating the display based on the current game state. The event loop, on the other hand, is focused on handling input events from the user.
