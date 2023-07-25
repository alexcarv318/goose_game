import pygame
import random 
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()                                       # method of initialisation

FPS = pygame.time.Clock()                           # create FPS variable with Clock method

screen = width, height = 800, 600                   # define screen size

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 255, 0

main_surface = pygame.display.set_mode(screen)      # main surface inherit screen size

ball = pygame.Surface((20, 20))                     # create new object 'ball'
ball.fill(WHITE)                                    # ball's color
ball_rect = ball.get_rect()
ball_speed = 5                                      # define the ball's speed 

def create_enemy():                                 # create enemy function
    enemy = pygame.Surface((20, 20))                    
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

enemies = []                                        # empty list for enemies definitions

CREATE_ENEMY = pygame.USEREVENT + 1                 # for every new enemy we create new event
pygame.time.set_timer(CREATE_ENEMY, 1500)           # for ever CREATE_ENEMY event we define the time 1.5s for this event

def create_bonus():                                 # create bonus function
    bonus = pygame.Surface((20,20))
    bonus.fill(GREEN)
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(2, 5)
    return [bonus, bonus_rect, bonus_speed]

bonuces = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)



is_working = True                                   
                                                    
while is_working:                                   # the loop for quiting the game
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:              # every 1.5s for our CREATE_ENEMY event we do the condition
            enemies.append(create_enemy())          # in every iteration we create a new enemy with create enemy function
        if event.type == CREATE_BONUS:
            bonuces.append(create_bonus())

    FPS.tick(60)                                    # define our Frames per second

    main_surface.fill(BLACK)                        # define the main surface's color
    main_surface.blit(ball, ball_rect)              # demonstrate our ball's surface on the main surface

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)      # move our enemy in x coordinate in direction to the start
        main_surface.blit(enemy[0], enemy[1])       # demonstrate our enemy surface on the main surface
        
        if enemy[1].left < 0:                       # if enemy dissapear from ou screen we delete him from array
            del enemies[enemies.index(enemy)]

        # if ball_rect.colliderect(enemy[1]):         # if our ball collide with enemy, ball eats enemy
            # del enemies[enemies.index(enemy)]

    
    for bonus in bonuces:                           # the same thing that for enemies, but they move on y coordinate
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            del bonuces[bonuces.index(bonus)]

        if ball_rect.colliderect(bonus[1]):
            del bonuces[bonuces.index(bonus)]


    pressed_keys = pygame.key.get_pressed()         #create array with all pressed keys

    if pressed_keys[K_DOWN] and ball_rect.bottom <= height:         # if key down (from all keys array) is pressed we move our ball down
        ball_rect = ball_rect.move(0, ball_speed)                   # use the move method, to move the ball with speed 'ball_speed' in y coordinate
    if pressed_keys[K_UP] and ball_rect.top >= 0:                   # if key up is pressed we move our ball up
        ball_rect = ball_rect.move(0, -ball_speed)

    if pressed_keys[K_RIGHT] and ball_rect.right <= width:          # the same for x coordinate
        ball_rect = ball_rect.move(ball_speed, 0) 
    if pressed_keys[K_LEFT] and ball_rect.left >= 0:                  
        ball_rect = ball_rect.move(-ball_speed, 0)


    pygame.display.flip()                            # call our display
