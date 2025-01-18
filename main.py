from itertools import filterfalse
import pygame 
from pygame.locals import*
import random ,asyncio


pygame.init()

screen_width= 864
screen_height= 936

clock = pygame.time.Clock()
fps = 60


import time

screen= pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flopping Birds")

font = pygame.font.SysFont("Bauhaus 93", 60)
small_font = pygame.font.SysFont("Bauhaus 93", 40)
white = (255,255,255)
red = (255,0,0)

bg = pygame.image.load("img/bg.png")
ground_img = pygame.image.load("img/ground.png")
button_img = pygame.image.load("img/restart.png")


def display_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 220
    flappy.rect.y = int(screen_height/2)
    flappy2.rect.x = 40
    flappy2.rect.y = int(screen_height/2)
    flappy.just_revived = False
    flappy2.just_revived = False    
    score = 0
    return score


flying = False
flying2 = False
game_over = False
game_over2 = False
pipe_gap = 180
pipe_freq = 1500 ## 1.5 seconds
last_pipe = pygame.time.get_ticks()

class Button():
    def __init__(self, x,y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        action = False
        pos  = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        elif pygame.key.get_pressed()[K_r]:
            action = True

        screen.blit(self.image , (self.rect.x  , self.rect.y))

        return action


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
        self.just_revived = False
        self.revive_index = 0
    def update(self):
        ##varibales
        self.counter += 1
        flap_cooldown = 5
        if self.just_revived == True :
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom <= 768:
                self.rect.y += int(self.vel)

            #jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.clicked == False:
                self.clicked = True
                self.vel = -10  
            if not keys[pygame.K_UP] and self.clicked == True:
                self.clicked = False

            #flapping
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index ==2:
                    self.image = self.images[self.index].set_alpha(100)
                if self.index >= 3:
                    self.index = 0
                    self.revive_index +=1
                if self.revive_index >= 10:
                    self.just_revived = False
                    self.revive_index  = 0 
                    self.image = self.images[2].set_alpha(255)
            self.image = self.images[self.index]

            #flopping
            self.image = pygame.transform.rotate(self.images[self.index], self.vel *-2)
        

        if flying == True and not self.just_revived:
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom <= 768:
                self.rect.y += int(self.vel)

            #jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.clicked == False:
                self.clicked = True
                self.vel = -10  
            if not keys[pygame.K_UP] and self.clicked == True:
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
        
        elif flying  == False and game_over == True:
            self.image.set_alpha(100)
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
        self.just_revived = False
        self.revive_index = 0
        

    def update(self):
        ##varibales
        self.counter += 1
        flap_cooldown = 5
        if self.just_revived == True :
             
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom <= 768:
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
                if self.index  == 2:
                    self.image  = self.images[self.index].set_alpha(100)
                if self.index >= 3:
                    self.index = 0
                    self.revive_index +=1 
            self.image = self.images[self.index]
            if self.revive_index >= 10:
                self.just_revived = False
                self.revive_index = 0
                self.image = self.images[2].set_alpha(255)
            #flopping
            self.image = pygame.transform.rotate(self.images[self.index], self.vel *-2)

            
        if flying2 == True and not self.just_revived:
            self.vel += 0.5
            if self.vel >= 8:
                self.vel = 8
            if self.rect.bottom <= 768:
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
        elif flying2  == False and game_over2 == True:
            self.image.set_alpha(100)

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
        if self.rect.right < 0:
            self.kill()



button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(220,int(screen_height/2))
flappy2 = Bird2(40,int(screen_height/2))


bird_group.add(flappy)
bird_group.add(flappy2)

run = True

ground_scroll = 0
scroll_speed = 4

pass_pipe_bird_1 = False
pass_pipe_bird_2 = False
score = 0
revive_count = 5
flappy_countdown = False
flappy2_countdown = False


## game 
while run:
    #draw
    current_time = pygame.time.get_ticks()
    screen.blit(bg,(0,0))

    clock.tick(fps) 

    bird_group.draw(screen)
    
    pipe_group.draw(screen)
    bird_group.update()

    #collision logic
    collision = pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
         ##game and flight logic for 2 birds
    if (flappy.rect.bottom > 768 and flappy2.rect.bottom > 768) or (flappy.rect.bottom < 0 and flappy2.rect.bottom < 0) :
        game_over = True
        flying = False
        game_over2 = True
        flying2 = False
        flappy2.just_revived = False
        flappy2.images[2].set_alpha(255)
        flappy2.revive_index = 0
        
    elif (flappy.rect.bottom > 768 and flappy2.rect.bottom < 768) or (flappy.rect.bottom < 0 and flappy2.rect.bottom > 0) and (flappy2_countdown == False) :
        game_over2 = False
        flying2 = True
        game_over = True
        flying = False
        flappy_countdown = True
        flappy.just_revived = False
        flappy.images[2].set_alpha(255)
        flappy.revive_index = 0
        
        
    elif (flappy.rect.bottom < 768 and flappy2.rect.bottom > 768) or (flappy.rect.bottom > 0 and flappy2.rect.bottom < 0) and (flappy_countdown == False) :
        game_over = False
        flying = True
        game_over2 = True
        flying2 = False
        flappy2_countdown = True
        flappy.just_revived = False
        flappy2.just_revived = False
        flappy.images[2].set_alpha(255)
        flappy2.images[2].set_alpha(255)
        flappy.revive_index = 0
        flappy2.revive_index = 0
        

    ##scoring logic

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe_bird_1 == False and flying == True:
            pass_pipe_bird_1 = True

        elif bird_group.sprites()[1].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[1].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe_bird_2 == False and flying2 == True:
            pass_pipe_bird_2 = True


        elif pass_pipe_bird_1 == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 10
                pass_pipe_bird_1 = False
                if flappy2_countdown  == True and revive_count > 1:
                    revive_count -= 1     
                elif flappy2_countdown == True and revive_count == 1:
                    flappy2_countdown = False
                    flappy2.rect.x = 40
                    flappy2.rect.y = int(screen_height/2)
                    revive_count = 5
                    flying2 = True
                    game_over2 = False
                    flappy2.just_revived = True
                   
        elif pass_pipe_bird_2 == True:
            if bird_group.sprites()[1].rect.left > pipe_group.sprites()[0].rect.right:
                score += 10
                pass_pipe_bird_2 = False
                if flappy_countdown == True and revive_count > 1:
                    revive_count -= 1
                elif flappy_countdown == True and revive_count == 1:           
                    flappy_countdown = False
                    flappy.rect.x = 220
                    flappy.rect.y = int(screen_height/2)
                    revive_count = 5  
                    flying = True 
                    game_over = False
                    flappy.just_revived = True





    display_text(str(score), font, white, int(screen_width/2), 20)
    ##collision logic
    for bird in collision:
        if bird == flappy and flying == True and not flappy.just_revived:
            game_over = True
            flying = False
            flappy_countdown = True
            
        elif bird == flappy2 and flying2 == True and not flappy2.just_revived:     
            game_over2 = True
            flying2 = False
            flappy2_countdown = True
               
    #draw and scroll
    screen.blit(ground_img,(ground_scroll,768))
    display_text(str(score), font, white, int(screen_width/2), 20)
    if flappy_countdown == True or flappy2_countdown == True:
        display_text(f' Revive In: {str(revive_count)}', font, red, int(screen_width/3), 80)

        #works
    if (((game_over == False and game_over2 == False) or (game_over == True and game_over2 == False) or (game_over == False and game_over2 == True))) and (((flying == True and flying2 == True) or (flying == True and flying2 == False) or (flying == False and flying2 == True))) :
        
        # pipes
        time_now = pygame.time.get_ticks() 

        if time_now - last_pipe > pipe_freq:
            pipe_height = random.randint(-100, 100)
            btm_pip = pipe(screen_width, int(screen_height/2)+pipe_height, -1)
            top_pip = pipe(screen_width, int(screen_height/2)+pipe_height, 1)
            pipe_group.add(btm_pip)
            pipe_group.add(top_pip)
            last_pipe = time_now
         

        pipe_group.update()



        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    elif (game_over == True and game_over2 == True):
        if button.draw():
            score = reset_game()
            game_over = False
            game_over2 = False
            flappy2_countdown = False
            flappy_countdown = False
            revive_count = 5



        ##start and quit 

    if flying == False and flying2 == False and game_over == False and game_over2 == False:
        display_text("Press Space to Play", small_font, white ,                  int(10),int(20))
        display_text("Use 'R' or MOUSE to Restart", small_font, white,           int(10),int(100))
        display_text("Player 1: UP arrow to Jump", small_font, white ,           int(10),int(160))
        display_text("Player 2: SPACE to Jump", small_font, white,               int(10),int(200))
        display_text("Pass through pipes to revive!", small_font, white,         int(10),int(260))
        display_text("Brief Immunity from PIPES after revive", small_font, white,int(10),int(340))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and flying == False and flying2 == False and game_over == False and game_over2 == False:
            flying = True
            flying2 = True
            flappy.just_revived = False
            flappy2.just_revived = False
    pygame.display.update()
    
pygame.quit()

