import pygame
import random

# init
pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("COME GET ME UNITED STATES")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# background
background_img = pygame.image.load('back.png')
background_image = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

# setup
player_width = 100
player_height = 100 
player_x = 50
player_y = WINDOW_HEIGHT/2 - player_height/2
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
player_hp = 3
MAX_HP = 3
HEALTH_BAR_WIDTH = 200
HEALTH_BAR_HEIGHT = 20
health_bar_width = int((player_hp / MAX_HP) * HEALTH_BAR_WIDTH)

# player image
player_img = pygame.image.load('xelikopter.png')
player_img = pygame.transform.scale(player_img, (player_width, player_height))

# enemy image
enemy_img = pygame.image.load('chinisbalun.png')
enemy_width = 75
enemy_height = 75
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))


# bullets
bullet_width = 10
bullet_height = 5
bullet_speed = 10
bullet_list = []
bullet_img = pygame.image.load('bullet.png')

# enemies
enemy_width = 100
enemy_height = 100
enemy_speed = 3
enemy_list = []

# fps
clock = pygame.time.Clock()

# load the BossMain.wav sound file
pygame.mixer.music.load("freedom.mp3")

# play the sound file continuously while the game is running
pygame.mixer.music.play(-1)

# load main menu image and font
menu_img = pygame.image.load('chinisbalun.png')
menu_font = pygame.font.SysFont("Comic Sans", 40)

# set up main menu text
menu_text = menu_font.render("COME GET ME UNITED STATES", True, WHITE)
menu_text_rect = menu_text.get_rect()
menu_text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/3) 

# set up image position
menu_img_rect = menu_img.get_rect()
menu_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

# display main menu
menu_running = True
while menu_running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                menu_running = False

    # draw main menu
    WINDOW.fill(BLACK)
    WINDOW.blit(menu_img, menu_img_rect)
    WINDOW.blit(menu_text, menu_text_rect)
    pygame.display.update()

# game loop
game_running = True
while game_running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_rect.right
                bullet_y = player_rect.centery - bullet_height/2
                bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
                bullet_list.append(bullet_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 0:
        player_rect.move_ip(0, -player_speed)
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.move_ip(0, player_speed)

    for bullet in bullet_list:
        bullet.move_ip(bullet_speed, 0)
        if bullet.right > WINDOW_WIDTH:
            bullet_list.remove(bullet)

    if len(enemy_list) < 5:
        enemy_x = WINDOW_WIDTH
        enemy_y = random.randint(0, WINDOW_HEIGHT-enemy_height)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        enemy_list.append(enemy_rect)

    for enemy in enemy_list:
        enemy.move_ip(-enemy_speed, 0)
        if enemy.right < 0:
            enemy_list.remove(enemy)

        # collision bullet player
        for bullet in bullet_list:
            if bullet.colliderect(enemy):
                enemy_list.remove(enemy)
                bullet_list.remove(bullet)

        # collision enemy player
        if enemy.colliderect(player_rect):
            enemy_list.remove(enemy)
            player_hp -= 1

    WINDOW.fill(BLACK)
    WINDOW.blit(background_image, (0, 0))

    for bullet in bullet_list:
        pygame.draw.rect(WINDOW, RED, bullet)

    # draw player
    WINDOW.blit(player_img, (player_rect.x, player_rect.y))

    # draw enemies
    for enemy in enemy_list:
        WINDOW.blit(enemy_img, (enemy.x, enemy.y))


    font = pygame.font.SysFont("Comic Sans", 30)
    health_bar_rect = pygame.Rect(10, 10, health_bar_width, HEALTH_BAR_HEIGHT)
    pygame.draw.rect(WINDOW, RED, health_bar_rect)
    pygame.draw.rect(WINDOW, WHITE, health_bar_rect, 2)
    pygame.display.update()

    if player_hp <= 0:
        game_running = False
    clock.tick(60)
pygame.quit()