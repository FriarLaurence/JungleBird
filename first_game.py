import pygame
import numpy as np
import random

#initialize pygame
pygame.init()

#create screen
screen = pygame.display.set_mode( (800,800) )

#Level
background = pygame.image.load('test_map.png')
def first_map_boundaries(x):
    #somehow make a function that stalls movement when player makes contact with white pixel in the background
    pass


#Title and Icon
pygame.display.set_caption("Jake")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)
pygame.SYSTEM_CURSOR_CROSSHAIR

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX = 10
scoreY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

#Level
level_value = 1
levelX = 600
levelY = 10

def show_level(x,y):
    level = font.render("Level: " + str(level_value), True, (255,255,255))
    screen.blit(level, (x,y))

#Player
playerImg = pygame.image.load('monster.png')
playerX = 400
playerY = 400
playerX_move = 0
playerY_move = 0
move_speed = 0.25

def player(x,y):
    screen.blit(playerImg, (x, y)) #blit means draw
def check_boundaries(x):
    if x <= 0:
        x = 0
        return x
    elif x >= 768:
        x = 768
        return x
    else:
        return x


#Player Weapon
bulletImg = pygame.image.load('rec.png').convert_alpha()
bulletImg = pygame.transform.scale(bulletImg, (15, 15))
shooting = False
bulletState = "ready"
playXshoot = 400
playYshoot = 400
weapon_speed = 2.0
def shootL(x,y):
    screen.blit(bulletImg, (x,y))


#Enemy
enemy_speed = 0.05
enemyImg = []
enX = []
enY = []
number_of_enemies = 5
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('zombie.png'))
    enX.append(random.randint(0, 768))
    enY.append(random.randint(0,768))


enDieImg = pygame.image.load('explosion.png')


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
def enemy_spawn():
    loc = np.array([0,0])
    loc[0] = random.randint(-32,0)
    loc[1] = random.randint(800,832)
    i = random.randint(0,1)
    return loc[i]

def enDie(x,y):
    screen.blit(enDieImg, (x,y))

#Collision function
def isCollision(x1,y1, x2, y2):
    pos = np.array([x1,x2,y1,y2]) + 16 #go to centre of two objects rather than top left corner
    dist = np.sqrt( ((pos[1]-pos[0])**2) + ((pos[3]-pos[2])**2) )
    if dist <= 16:
        return True
    else:
        return False

font_end = pygame.font.Font('freesansbold.ttf',70)
text_end_X = 150
text_end_Y = 300

def GAME_OVER(x,y):
    end_game = font_end.render("GAME OVER", True, (255,255,255))
    screen.blit(end_game,(x,y))

iter = 1
running  = True



while running:
    #Set backround
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    #Main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keyboard movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playerY_move = -1*(move_speed)
            if event.key == pygame.K_s:
                playerY_move = (move_speed)
            if event.key == pygame.K_a:
                playerX_move = -1*(move_speed)
            if event.key == pygame.K_d:
                playerX_move = (move_speed)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                playerY_move = 0
            if event.key == pygame.K_s:
                playerY_move = 0
            if event.key == pygame.K_a:
                playerX_move = 0
            if event.key == pygame.K_d:
                playerX_move = 0

        #mouse actions
        #left click sends image from player to click coordinates
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bulletState == "ready":
                bulletState = "fire"
                c1 = 1
                c2 = 0
                shoot_target = pygame.mouse.get_pos()
                playXshoot = playerX
                playYshoot = playerY
                #normalize change in coefficients or else short vecs go slow, big vecs go fast
                c = 1 / (np.sqrt( ((playXshoot-shoot_target[0])**2) + ((playYshoot-shoot_target[1])**2) ))
        if event.type == pygame.MOUSEBUTTONUP:
            # shooting = False
            pass

    #Player movement
    playerX += playerX_move
    playerY += playerY_move

    #CREATE FUNCTION TO CHECK BOUNDARIES FOR PLAYER AND ENEMIES
    #Set player boundaries
    playerX = check_boundaries(playerX)
    playerY = check_boundaries(playerY)

    #draw player ontop if the screen fill
    player(playerX, playerY)

    #Player weapon and bullet movement TRY TO MAKE BULLET CONSTANT SPEED
    if bulletState == "fire":
        c1 -= c
        c2 += c
        bulletX = c1*playXshoot + c2*shoot_target[0]
        bulletY = c1*playYshoot + c2*shoot_target[1]
        shootL(bulletX,bulletY)
        if bulletX <= 0:
            bulletState = 'ready'
        if bulletY <= 0:
            bulletState = 'ready'
        if bulletX >= 800:
            bulletState = 'ready'
        if bulletY >= 800:
            bulletState = 'ready'

    #Find the vector between the player and zombie.
    for i in range(number_of_enemies):
        vecX = playerX - enX[i]
        vecY = playerY - enY[i]
        #Normalize the vector for movement to remain slow speed
        enX[i] += (vecX / np.sqrt( (vecX**2) + (vecY**2) ))*enemy_speed
        enY[i] += (vecY / np.sqrt( (vecX**2) + (vecY**2)))*enemy_speed
        enemy(enX[i],enY[i],i)

    #all events involving zombies
    for i in range(number_of_enemies):
        if isCollision(enX[i],enY[i], playerX, playerY) == True:
            GAME_OVER(text_end_X,text_end_Y)

        #if bullet hits zombie, kill zombie, spawn new one
        if bulletState == "fire":
            if isCollision(enX[i]+12,enY[i]+12,bulletX, bulletY) == True:
                enDie(enX[i],enY[i])
                score_value += 1
                if score_value == 20 or score_value == 50 or score_value == 75 or score_value == 100:
                    level_value +=1
                    enemy_speed += 0.05
                enX[i] = enemy_spawn() #randomize outside border of game
                enY[i] = enemy_spawn()
                bulletState = "ready"

    #Show score
    show_score(scoreX,scoreY)
    show_level(levelX,levelY)
    #update the screen
    pygame.display.update()





"""
Goals:
map is like a labrynth - white squares are walls,
Once Score reaches 25:
    Zombies go faster
    Increased number of enemies
    background changes to grow complexity


Eventually:
left click is fast shot bullet trails at slow speed
right click is slow AOE - emanates from player
Player has a health bar
Different types of Zombies
Weapons
Items
Ammo
Co-op



"""
