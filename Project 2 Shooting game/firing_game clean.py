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


import pygame
import os
import cv2

# Load an external video
VIDEO = cv2.VideoCapture("./Assets/video.mp4")
FPS2 = VIDEO.get(cv2.CAP_PROP_FPS)


pygame.font.init()
pygame.mixer.init()


BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

HEALTH_FONT = pygame.font.SysFont("comicsans", 20)

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

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)


RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)),
    270,
)


SPACE_IMAGE = pygame.transform.scale(
    pygame.image.load("./Assets/space2.png"), (WIDTH, HEIGHT)
)
# MAIN_MENU_IMAGE = pygame.transform.scale(
#     pygame.image.load("./Assets/main_menu.jpg"), (WIDTH, HEIGHT)
# )


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
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        if red.colliderect(bullet):
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
    pygame.time.delay(4000)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE_IMAGE, (0, 0))

    red_health_text_image = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)

    yellow_health_text_image = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE
    )

    WIN.blit(
        red_health_text_image, (WIDTH - red_health_text_image.get_width() - 10, 10)
    )
    WIN.blit(yellow_health_text_image, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_main_screen(video_frame_image):
    # WIN.blit(MAIN_MENU_IMAGE, (0, 0))
    WIN.blit(video_frame_image, (0, 0))
    pygame.display.update()


def play_music(main_screen, run):
    # When you play a MUSIC, then its not like it will go to the next code after playing it full. But rather, it starts playing AND GOES TO NEXT CODE. The music continues so in the background until stopped.

    if main_screen:
        pygame.mixer.music.load("./Assets/main_music.mp3")
        pygame.mixer.music.play(-1)
        # Plays in the background for infinity (-1)
    if run:
        pygame.mixer.music.load("./Assets/game_music.mp3")
        pygame.mixer.music.play(-1)
    if not run and not main_screen:
        pygame.mixer.music.load("./Assets/game_over_music.mp3")
        pygame.mixer.music.play(1)


def main():
    """Define two areas( RECANGULAR ), where the images will be placed.(Movement of image depends on movement of Rectangle)."""
    red = pygame.Rect(700, 290, SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()

    """MAIN MENU SCREEN LOOP"""
    main_screen = True
    run = False
    play_music(main_screen, run)
    while main_screen:
        clock.tick(FPS2)  # FPS of the video given

        # for loop for only manipulating events . Don't add into it any functions unrelated.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_screen = False
                    pygame.mixer.music.stop()
                    break

        # Read one frame in this mainmenuloop, then another in the next loop and so on.
        success, frame = VIDEO.read()
        if success:
            video_frame_image = pygame.image.frombuffer(
                frame.tobytes(), frame.shape[1::-1], "BGR"
            )
            scaled_video_frame_image = pygame.transform.scale(
                video_frame_image, (WIDTH, HEIGHT)
            )
        else:
            VIDEO.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        draw_main_screen(scaled_video_frame_image)

    """GAMEPLAY LOOP"""
    run = True
    play_music(main_screen, run)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
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
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(yellow, keys_pressed)
        red_handle_movement(red, keys_pressed)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        winner_text = ""
        if red_health == 0:
            winner_text = "YELLOW WINS !"
        if yellow_health == 0:
            winner_text = "RED WINS !"
        if winner_text != "":
            run = False
            pygame.mixer.music.stop()
            play_music(main_screen, run)
            draw_winner(winner_text)
            break
    main()


if __name__ == "__main__":
    main()


"""However, when you press keys during the delay, the key events are still being generated and stored in the event queue. These events are not processed immediately because the program is in a delay, but once the delay is over, the program resumes and starts processing the events in the queue.
So, when you check for event.type == pygame.KEYDOWN after the delay, it will detect and handle all the key events that occurred during the delay, leading to the behavior you've observed. If you want to prevent this, you might consider using other mechanisms to control the flow of your program without blocking it, such as timers or event-driven architectures."""
