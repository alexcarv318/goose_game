import pygame
from pygame. constants import QUIT

pygame.init()                                       # method of initialisation

screen = width, height = 800, 600                   # define screen size

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BLUE = 0, 0, 255

main_surface = pygame.display.set_mode(screen)      # main surface inherit screen size

ball = pygame.Surface((20, 20))                     # create new object 'ball'
ball.fill((WHITE))                                  #ball's color
ball_rect = ball.get_rect()
ball_speed = [1, 1]                                 # define the ball's speed 

is_working = True                                   
                                                    
while is_working:                                   # the floop for quiting the game
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    ball_rect = ball_rect.move(ball_speed)          # use the move method, to move the ball with speed 'ball_speed'
    main_surface.fill((BLACK))                      # define the main surface's color
    main_surface.blit(ball, ball_rect)              # demonstrate our ball's surface on the main surface

    if ball_rect.bottom >= height or ball_rect.top <= 0:  # if ball's y coordinate >= height of window, ball change direction
        ball_speed[1] = -ball_speed[1]                    # change y coordinate direction
        ball.fill((RED))                                  # when change direction - change color

    if ball_rect.right >= width or ball_rect.left <= 0:   # change x coordinate direction
        ball_speed[0] = -ball_speed[0]
        ball.fill((BLUE))