import pygame
import random 
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_ESCAPE, K_SPACE
from os import listdir

pygame.init()                                       # method of initialisation

FPS = pygame.time.Clock()                           # create FPS variable with Clock method

screen = width, height = 1200, 700                  # define screen size

IMG_PATH = 'goose'

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 255, 0

font = pygame.font.Font('font/Verdana.ttf', 20)     # define game's font
loose_font = pygame.font.Font('font/Verdana.ttf', 60) 

main_surface = pygame.display.set_mode(screen)      # main surface inherit screen size



player_imgs = [pygame.image.load(IMG_PATH + '/' + file).convert_alpha() for file in listdir(IMG_PATH)] # list comprehension for images in directive IMG_PATH and convert method for them
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 10                                   # define the player's speed 

GOOSE_ANIMATION = pygame.USEREVENT + 3              # event for goose animation
pygame.time.set_timer(GOOSE_ANIMATION, 125)

img_index = 0



def create_enemy():                                     # create enemy function
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size()) # *** можно обмежити кількість
    enemy_speed = random.randint(4, 8)
    return [enemy, enemy_rect, enemy_speed]

enemies = []                                        # empty list for enemies definitions

CREATE_ENEMY = pygame.USEREVENT + 1                 # for every new enemy we create new event
pygame.time.set_timer(CREATE_ENEMY, 1000)           # for ever CREATE_ENEMY event we define the time 1.5s for this event



def create_bonus():                                 # create bonus function
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, (bonus.get_width() // 1.5, bonus.get_height() // 1.5))
    bonus_rect = pygame.Rect(random.randint(0, width), -20, *bonus.get_size())
    bonus_speed = random.randint(4, 8)
    return [bonus, bonus_rect, bonus_speed]

bonuces = []

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)


bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)  # convert background image and adapte it for our screen
bg_x1 = 0                                                                           # define bg coordinates
bg_x2 = bg.get_width()
bg_speed = 3


scores = 0


is_working = True

gameplay = True
                                                    
while is_working:                                   # the loop for quiting the game
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:              # every 1.5s for our CREATE_ENEMY event we do the condition
            enemies.append(create_enemy())          # in every iteration we create a new enemy with create enemy function

        if event.type == CREATE_BONUS:
            bonuces.append(create_bonus())

        if event.type == GOOSE_ANIMATION:           # when animation event happens we change the image
            img_index += 1                          # image index counter
            if img_index == len(player_imgs):       # "repeat the loop"
                img_index = 0
            player = player_imgs[img_index]

    FPS.tick(60)                                    # define our Frames per second

    bg_x1 -= bg_speed                               # move our background position with bg_speed
    bg_x2 -= bg_speed

    if bg_x1 < -bg.get_width():                     # with another words, when our bg ends we repeat it
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_surface.blit(bg, (bg_x1, 0))               #demonstrate two of our backgrounds
    main_surface.blit(bg, (bg_x2, 0))               # for moving effect

    if gameplay:
    
        main_surface.blit(player, player_rect)          # demonstrate our player's surface on the main surface
        main_surface.blit(font.render('SCORE: ' + str(scores), True, BLACK), (width - 120, 10))

        for enemy in enemies:
            enemy[1] = enemy[1].move(-enemy[2], 0)      # move our enemy in x coordinate in direction to the start
            main_surface.blit(enemy[0], enemy[1])       # demonstrate our enemy surface on the main surface
            
            if enemy[1].left < 0:                       # if enemy dissapear from ou screen we delete him from array
                del enemies[enemies.index(enemy)]

            if player_rect.colliderect(enemy[1]):       # if our player collide with enemy, player eats enemy
                scores = 0
                enemies.clear()
                bonuces.clear()
                gameplay = False

        
        for bonus in bonuces:                           # the same thing that for enemies, but they move on y coordinate
            bonus[1] = bonus[1].move(0, bonus[2])
            main_surface.blit(bonus[0], bonus[1])

            if bonus[1].bottom >= height:
                del bonuces[bonuces.index(bonus)]

            if player_rect.colliderect(bonus[1]):
                del bonuces[bonuces.index(bonus)]
                scores += 1


        pressed_keys = pygame.key.get_pressed()                           #create array with all pressed keys

        if (pressed_keys[K_DOWN] or pressed_keys[K_s]) and player_rect.bottom <= height:         # if key down (from all keys array) is pressed we move our player down
            player_rect = player_rect.move(0, player_speed)                   # use the move method, to move the player with speed 'player_speed' in y coordinate
        if (pressed_keys[K_UP] or pressed_keys[K_w]) and player_rect.top >= 0:                   # if key up is pressed we move our player up
            player_rect = player_rect.move(0, -player_speed)

        if (pressed_keys[K_RIGHT] or pressed_keys[K_d]) and player_rect.right <= width:          # the same for x coordinate
            player_rect = player_rect.move(player_speed, 0) 
        if (pressed_keys[K_LEFT] or pressed_keys[K_a]) and player_rect.left >= 0:                  
            player_rect = player_rect.move(-player_speed, 0)

        if pressed_keys[K_ESCAPE]:
            is_working = False

    else:
        main_surface.blit(loose_font.render('GAME OVER', True, BLACK), (410, 200))
        main_surface.blit(font.render('Press "space"', True, BLACK), (540, 300))

        pressed_keys = pygame.key.get_pressed() 

        if pressed_keys[K_SPACE]:
            gameplay = True
            

        if pressed_keys[K_ESCAPE]:
            is_working = False

    pygame.display.flip()                                              # call our display
