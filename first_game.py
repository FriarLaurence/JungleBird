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
pygame.display.set_caption("Jungle Bird") # Title
icon = pygame.image.load('alien.png') # Icon
pygame.display.set_icon(icon)

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
scoreX = 10 # X position of score
scoreY = 10 # Y position of score

def show_score(x,y):
    """Draw score on the screen"""
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

#Level
level_value = 1
levelX = 600 # X position of score
levelY = 10 # Y position of score

def show_level(x,y):
    level = font.render("Level: " + str(level_value), True, (255,255,255))
    screen.blit(level, (x,y))

#Player
playerImg = pygame.image.load('monster.png')
playerX = 400 # playerX = X coord of player
playerY = 400 # playerY = Y coord of player (start at middle of screen)
playerX_move = 0 #no movement initially
playerY_move = 0
move_speed = 0.25

def player(x,y):
    """Draw player on screen"""
    screen.blit(playerImg, (x, y)) #blit means draw

def check_boundaries(x):
    """Prevent movement off of the screen"""
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
bulletImg = pygame.transform.scale(bulletImg, (15, 15)) #shrink image
bulletState = "ready"

def shoot(x,y):
    """Draw bullet on the screen"""
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

def enemy(x,y,i):
    """Draw enemy"""
    screen.blit(enemyImg[i], (x,y))

def enemy_spawn():
    """Spawn enemy out of game screen"""
    loc = np.array([0,0])
    loc[0] = random.randint(-32,0)
    loc[1] = random.randint(800,832)
    i = random.randint(0,1)
    return loc[i]

#Enemy death event
enemyDeathImg = pygame.image.load('explosion.png')

def enemy_death(x,y):
    """Draw explosion over enemy death"""
    screen.blit(enemyDeathImg, (x,y))

#Collision function
def isCollision(x1,y1, x2, y2):
    """Determine if collision between objects has occurred"""
    pos = np.array([x1,x2,y1,y2]) + 16 #go to centre of two objects rather than top left corner
    dist = np.sqrt( ((pos[1]-pos[0])**2) + ((pos[3]-pos[2])**2) )
    if dist <= 16:
        return True
    else:
        return False

#Game over scenario
font_end = pygame.font.Font('freesansbold.ttf',70) # set font and size of GAME OVER
text_end_X = 150 # X coord of GAME OVER display
text_end_Y = 300 # Y coord of GAME OVER display

def GAME_OVER(x,y):
    """Draw GAME OVER on screen"""
    end_game = font_end.render("GAME OVER", True, (255,255,255))
    screen.blit(end_game,(x,y))

iter = 1
running  = True

while running:
    #Set background
    # screen.fill((0,0,0)) # straight black background
    screen.blit(background, (0,0)) # draw background

    #Main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if you hit the exit window button, quit the loop
            running = False

        #keyboard movements
        if event.type == pygame.KEYDOWN: #if a key has been pressed
            if event.key == pygame.K_w: # if key pressed is 'w'
                playerY_move = -1*(move_speed) #set Y movement
            if event.key == pygame.K_s:
                playerY_move = (move_speed)
            if event.key == pygame.K_a:
                playerX_move = -1*(move_speed)
            if event.key == pygame.K_d:
                playerX_move = (move_speed)
        if event.type == pygame.KEYUP: #if key is released
            if event.key == pygame.K_w: # if 'w' is released
                playerY_move = 0 # reset Y movement to 0
            if event.key == pygame.K_s:
                playerY_move = 0
            if event.key == pygame.K_a:
                playerX_move = 0
            if event.key == pygame.K_d:
                playerX_move = 0

        #Mouse action
        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse button pressed
            if bulletState == "ready": #only if no bullet is on the screen
                bulletState = "fire" #set the state to 'fire'
                #bullet position is set as a linear combination of player position as well as mouse position
                c1 = 1   #coefficient for player vector, bullet starts at player coordinate
                c2 = 0   #coefficient for  mouse position on click vector
                target = pygame.mouse.get_pos() # get vector of position on screen where clicked
                playXshoot = playerX #save playerX on click
                playYshoot = playerY #save playerY on click
                #normalize change in coefficients or else short vecs go slow, big vecs go fast
                c = 1 / (np.sqrt( ((playXshoot-target[0])**2) + ((playYshoot-target[1])**2) ))

    #Player movement
    playerX += playerX_move
    playerY += playerY_move

    #Set player boundaries
    playerX = check_boundaries(playerX)
    playerY = check_boundaries(playerY)

    #draw player ontop if the screen
    player(playerX, playerY)

    #Player weapon and bullet movement TRY TO MAKE BULLET CONSTANT SPEED
    if bulletState == "fire": #if bullet has been fired/ is active
        c1 -= c #moves away from player
        c2 += c #moves towards clicked location
        bulletX = c1*playXshoot + c2*target[0]
        bulletY = c1*playYshoot + c2*target[1]
        shoot(bulletX,bulletY) #draw bullet
        #if bullet goes out of bounds, reset bullet state
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
        enemy(enX[i],enY[i],i) # draw new enemy position

    #all events involving zombies
    for i in range(number_of_enemies):
        if isCollision(enX[i],enY[i], playerX, playerY) == True:
            GAME_OVER(text_end_X,text_end_Y)

        #if bullet hits zombie, kill zombie, increment score (and possibly level), spawn new zombie, reset bullet state
        if bulletState == "fire":
            if isCollision(enX[i]+12,enY[i]+12,bulletX, bulletY) == True:
                enemy_death(enX[i],enY[i])
                score_value += 1
                if score_value == 20 or score_value == 50 or score_value == 75 or score_value == 100:
                    level_value +=1
                    enemy_speed += 0.05
                enX[i] = enemy_spawn() #randomize outside border of game
                enY[i] = enemy_spawn()
                bulletState = "ready"

    #Show score
    show_score(scoreX,scoreY)
    #Show level
    show_level(levelX,levelY)
    #update the screen
    pygame.display.update()


"""
Goals:
map is like a labrynth - white squares are walls,
Once Score of 100 is reached, change map

Eventually:
left click is fast shot bullet trails at slow speed
right click is AOE - emanates from player
Space bar drops mines
Player has a health bar
Different types of Zombies, with health, or just change image once hit
Weapons
Items
Ammo
Co-op



"""
