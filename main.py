import pygame 
from pygame.locals import*
import random

pygame.init()

screen_width= 864
screen_height= 936

clock = pygame.time.Clock()
fps = 60

screen= pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")


bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")

flying = False
flying2 = False
game_over = False
game_over2 = False
pipe_gap = 150
pipe_freq = 1500 ## 1.5 seconds
last_pipe = pygame.time.get_ticks()


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame .sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num  in range(1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image= self.images[self.index] 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        ##varibales
        self.counter += 1
        flap_cooldown = 5
       
        if flying == True:
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

            #jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.clicked == False:
            self.clicked = True
            self.vel = -10  
        if not keys[pygame.K_w] and self.clicked == True:
            self.clicked = False

        #flapping
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= 3:
                self.index = 0
        self.image = self.images[self.index]

        #flopping
        self.image = pygame.transform.rotate(self.images[self.index], self.vel *-2)
        

class Bird2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame .sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num  in range(1,4):
            img = pygame.image.load(f'img/bird2{num}.png')
            self.images.append(img)
        self.image= self.images[self.index] 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False



    def update(self):
        ##varibales
        self.counter += 1
        flap_cooldown = 5
        
        if flying2 == True:
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
                #jump

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.clicked == False:
            self.clicked = True
            self.vel = -10  
        if not keys[pygame.K_SPACE] and self.clicked == True:
            self.clicked = False

        #flapping
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= 3:
                self.index = 0
        self.image = self.images[self.index]

        #flopping
        self.image = pygame.transform.rotate(self.images[self.index], self.vel *-2)


class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipe_gap)/2]
        elif position == -1:
            self.rect.topleft = [x,y + int(pipe_gap)/2]

    def update(self):
        self.rect.x -= scroll_speed





bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(220,int(screen_height/2))
flappy2 = Bird2(40,int(screen_height/2))


bird_group.add(flappy)
bird_group.add(flappy2)

run = True

ground_scroll = 0
scroll_speed = 4

keys = pygame.key.get_pressed()

while run:
    #draw
    screen.blit(bg,(0,0))

    clock.tick(fps) 

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    if flappy.rect.bottom > 768 and flappy2.rect.bottom > 768:
        game_over = True
        flying = False
        game_over2 = True
        flying2 = False
    elif flappy.rect.bottom > 768 and flappy2.rect.bottom < 768:
        game_over = True
        flying = False
        game_over2 = False
        flying2 = True
    elif flappy.rect.bottom < 768 and flappy2.rect.bottom > 768:
        game_over = False
        flying = True
        game_over2 = True
        flying2 = False

    #draw and scroll
    screen.blit(ground_img,(ground_scroll,768))


    if ((game_over == False and game_over2 == False) or (game_over == True and game_over2 == False) or (game_over == False and game_over2 == True))and flying == True and flying2 == True:
        # pipes
        time_now = pygame.time.get_ticks() 
        if time_now - last_pipe > pipe_freq:
            btm_pip = pipe(screen_width, int(screen_height/2), -1)
            top_pip = pipe(screen_width, int(screen_height/2), 1)
            pipe_group.add(btm_pip)
            pipe_group.add(top_pip)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and flying == False and flying2 == False and game_over == False and game_over2 == False:
            flying = True
            flying2 = True
    pygame.display.update()
    
pygame.quit()

