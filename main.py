import pygame 
from pygame.locals import*


pygame.init()

screen_width= 864
screen_height= 936

clock = pygame.time.Clock()
fps = 60

screen= pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")


bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")


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
        self.vel += 0.5

        if self.vel >= 8:
            self.vel = 8
        if self.rect.bottom < 768:
            self.rect.y += int(self.vel)

            #jump
        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
            self.clicked = True
            self.vel = -10  
        if pygame.mouse.get_pressed()[0] == 0:
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


bird_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_height/2))
flappy2 = Bird2(100,int(screen_height/3))

bird_group.add(flappy)
bird_group.add(flappy2)

run = True

ground_scroll = 0
scroll_speed = 4

while run:
    #draw
    screen.blit(bg,(0,0))

    clock.tick(fps) 

    bird_group.draw(screen)
    bird_group.update()
  
    #draw and scroll
    screen.blit(ground_img,(ground_scroll,768))
    ground_scroll -= scroll_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
pygame.quit()

