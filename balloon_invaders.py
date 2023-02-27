import pygame
import math
import random
import time
from pygame import mixer

# Initialize pygame
pygame.init()

# Create window
display = pygame.display.set_mode((800, 600))
pygame.display.update()

# Background
background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title & Icon
pygame.display.set_caption("Balloon Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


# Enemy
enemyImg = [] 
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    print (enemyX)   
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(10, 400))
    enemyX_change.append(0.3)
    enemyY_change.append(25)
    
# print(str(enemyY[0]) + str(enemyY[1]) + str(enemyY[2]) + str(enemyY[3]) + str(enemyY[4]) + str(enemyY[5]))

def enemy(x, y, i):
    display.blit(enemyImg[i],(x, y))
    

# Player
playerImg = pygame.image.load('player.png')
playerX = 368
playerY = 480
playerX_change = 0

def player(x,y):
    display.blit(playerImg, (x, y))
    
# Missile
# Ready - Can't see missile
# Fire - Bullet is currently moving
missileImg = pygame.image.load('missile.png')
missileX = 0
missileY = 480
missleX_change = 0
missleY_change = 0.1
missileState = "ready"

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    display.blit(over_text, (200, 250))
# Score 
score = 0

# missile functions

def fire_missile(x,y):
    global missileState
    global missileImg
    missileState = "fire"
    display.blit(missileImg, (x+16,y+10))
    
def isCollision(enemyX,enemyY,missileX,missileY):
    distance = math.sqrt(math.pow(enemyX-missileX, 2) + math.pow(enemyY-missileY, 2))
    if distance < 27:
        return True
    else:
        return False

gameOver = False
gameOverAcknowledged = False
# Game Loop
open = True
while open:
    
    # RGB screen color
    display.fill((123, 133, 71))
    # Background image
    display.blit(background, (0,0))
    
    #print(str(enemyY[0]) + str(enemyY[1]) + str(enemyY[2]) + str(enemyY[3]) + str(enemyY[4]) + str(enemyY[5]))
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            print("A keystroke is pressed.")
            if event.key == pygame.K_a:
                print("A key pressed.")
                playerX_change = -0.3
            if event.key == pygame.K_d:
                print("D key pressed.")
                playerX_change = +0.3
            if event.key == pygame.K_SPACE:
                print("Space has been pressed")
                if missileState is "ready":
                    missileSound = mixer.Sound('missile.wav')
                    missileSound.play()
                    missileX = playerX
                    fire_missile(missileX,missileY)
                    #missileState = "fire"
                    print("Missile has been fired.")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or pygame.K_d:
                print("Keystroke has been released.")
                playerX_change = 0
            
        if event.type == pygame.QUIT:
            print("**Display closed by user.**")
            open = False
    
    # Checking for boundaries so plane doesn't go out of bounds
    playerX += playerX_change
    
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
    
    
    # Enemy Movement
    for i in range(num_of_enemies):
        
        # Game Over
        if enemyY[i] > 448:
            for j in range(num_of_enemies):
                enemyY[j] = -2000
            gameOver = True
        
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <=0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
            
        # Collision
        collision = isCollision(enemyX[i],enemyY[i],missileX,missileY)
        if collision and missileState == 'fire':
            collisionSound = mixer.Sound('collision.wav')
            collisionSound.play()
            missileY = 480
            missileState = "ready"
            score += 1
            print("Enemy hit! Score: " + str(score))
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(10, 200)
       
        
        enemy(enemyX[i], enemyY[i], i)
        
        # Missile movement
        if missileY <= 0:
            missileY = 480
            missileState = "ready"
            
        if missileState is "fire":
            fire_missile(missileX,missileY)
            missileY -= missleY_change
        
        if gameOver is True:
            gameOverSound = mixer.Sound('biden.wav')
            gameOverSound.play(0)
            gameOver = False
            gameOverAcknowledged = True
    
    if gameOverAcknowledged == True:
        game_over_text()
            

                
    player(playerX,playerY)
    
    pygame.display.update()
            
