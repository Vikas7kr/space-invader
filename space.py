import pygame
import random
import math
from pygame import mixer

#intialise the pygame
pygame.init()

#create the screen
screen=pygame.display.set_mode((800,600))  #800=width,600=height
#background
background=pygame.image.load("images/bck.png")

#sound
mixer.music.load("images/back.wav")
mixer.music.play(-1)
#title and icon.......window screen
pygame.display.set_caption("SPACE INVADERS")
icon = pygame.image.load('images/spaceship.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load("images/player1.png")
playerX=370
playerY=480
playerX_change=0


#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num=6 #number of enemies

for i in range(num):
    enemyImg.append(pygame.image.load("images/enemy.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2.5)
    enemyY_change.append(40)

#bullet
#ready - can't see the bullet on the screen
bulletImg=pygame.image.load("images/bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=7
bullet_state="ready"

score=0
font=pygame.font.Font("freesansbold.ttf",32) #dafont
textX=10
textY=10

#game over
over_text=pygame.font.Font("freesansbold.ttf",64)

def show_score(x,y):
    scor=font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(scor,(x,y))
def game_over():
    over=over_text.render("GAME OVER",True,(255,255,255))
    screen.blit(over,(200,250))

def player(x,y):
    screen.blit(playerImg,(x,y))                             #blit stands for draw

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))                             #blit stands for draw

def bullet_fire(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def iscollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+ (math.pow(enemyY-bulletY,2)))
    if distance <27:
        return True
#game loop>>>.......everything in while loop
running =True
while running:

    screen.fill((0,0,0))      #rgb=red green blue===rapid table
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #to exit game
            running=False

        #keystroke
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key == pygame.K_RIGHT:
                playerX_change=5
            if event.key == pygame.K_SPACE:
                if bullet_state =="ready":
                    bullet_sound=mixer.Sound("audio/laser.wav")
                    bullet_sound.play()
                    bulletX=playerX
                    bullet_fire(bulletX,bulletY)
        if event.type==pygame.KEYUP:        #keystroke is removed
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0


    playerX+=playerX_change

    if playerX<=0:
        playerX=0
    elif playerX>=736: #800(width)-64(imagepixel)
        playerX=736
#enemy movement
    for i in range(num):

        #game over
        if enemyY[i]>400:
            for j in range(num):
                enemyY[j]=2000
            game_over()
            break

        enemyX[i]+=enemyX_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=2.5
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736: #800(width)-64(imagepixel)
            enemyX_change[i]=-2.5
            enemyY[i]+=enemyY_change[i]

            #iscollision
        collision=iscollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            gun_sound=mixer.Sound("audio/gun.wav")
            gun_sound.play()
            bulletY=480
            bullet_state="ready"
            score+=1
            enemyX[i]=random.randint(0,735)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)

#bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"

    if bullet_state== "fire":
        bullet_fire(bulletX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()      #update screen
