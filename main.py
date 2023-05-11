import math
import random

import pygame
from pygame import mixer

# to initialize pygame
pygame.init()

# screen                         #height,width
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('icons8-ufo-32.png')
pygame.display.set_icon(icon)

# setting background opacity
BACKGROUND_OPACITY = 100

# Load the background image
background_image = pygame.image.load('star.jpg')
background_scaled_img = pygame.transform.scale(background_image, (
    background_image.get_width() * 0.8, background_image.get_height() * 0.8))
# Set the alpha value of the background image
background_scaled_img.set_alpha(BACKGROUND_OPACITY)

# background music
mixer.music.load('594223__szegvari__battle-cinematic-soundtrack-music-atmo-background.wav')
mixer.music.play(-1)

# score

score_value = 0
font = pygame.font.Font('CoffeCake.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('CoffeCake.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 255, 0))
    screen.blit(over_text, (200, 250))


# player
player_img = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy - has a random position each time
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_scaled_img = []
num_of_enemies = 6

for i in range(num_of_enemies):



    enemy_img.append(pygame.image.load('deathstar.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(1)
    enemyY_change.append(10)

    # Scale the  enemy image
    enemy_scaled_img.append(
        pygame.transform.scale(enemy_img[i], (enemy_img[i].get_width() * 2, enemy_img[i].get_height() * 2)))


# bullet

# ready- you cant see the bullet on  the screen
# fire- the bullet is currently moving
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# scaled player img
scaled_img = pygame.transform.scale(player_img, (player_img.get_width() * 2, player_img.get_height() * 2))


def player(x, y):
    screen.blit(scaled_img, (x, y))  # drawing the image of player


def enemy(x, y):
    screen.blit(enemy_scaled_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x + 16, y + 16))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))
    if distance < 27:
        return True
    else:
        return False

def Collision_enemy(enemyX, enemyY, playerX,playerY):
    distance = math.sqrt(math.pow((playerX - enemyX), 2) + math.pow((playerY - enemyY), 2))
    if distance < 27:
        return True
    else:
        return False



# Title and icon
pygame.display.set_caption("Space Invaders")

# Create a surface with a vertical gradient
gradient = pygame.Surface((800, 600))
for y in range(600):
    r, g, b = (y // 3) % 256, (y // 7) % 256, (y // 3) % 256
    color = pygame.Color(r, g, b)
    pygame.draw.line(gradient, color, (0, y + 300), (800, y + 100))

    # Fill the screen with the gradient surface
screen.blit(gradient, (0, 0))
pygame.display.flip()

# To add a normal background add
# screen.fill((r,g,b))
# pygame.display.update()
# inside the game loop under while loop

# game loop
running = True
while running:

    screen.blit(gradient, (0, 0))  # redraw the gradient

    screen.blit(background_scaled_img, (0, 0))  # Blit the background image onto the screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -1
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 1
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                playerY_change = -1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerY_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet sound
                    bullet_sound = mixer.Sound('324137__robinhood76__06012-fast-missile-flyby.wav')
                    bullet_sound.play()
                    # it gets the current x-coordinate and y-coordinate
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_s or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
    # player
    playerX += playerX_change
    playerY += playerY_change
    if playerX <= -68:
        playerX = 800
    elif playerX >= 800:
        playerX = -68
    if playerY <= 0:
        playerY = 0
    elif playerY >= 532:
        playerY = 532

    # enemy movement
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # game over
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            game_over_text()

            break






            # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("506823__mrthenoronha__explosion-4-8-bit.wav")
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 100)

        enemy(enemyX[i], enemyY[i])

        #enemy collision
        enemy_collision =Collision_enemy(enemyX[i], enemyY[i], playerX, playerY)
        if enemy_collision:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

    # bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    # game over

    pygame.display.update()
