
import pygame
import time
import random


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE, 
    KEYDOWN,
    QUIT,
)


SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 600
black = (0,0,0)
green=(0,200,0)
bright_green=(0,255,0)
bright_red=(255,0,0)
white = (255,255,255)
red = (200,0,0)
Ljudi=['man.jpg','man2.jpg','man3.jpg','man4.jpg','woman1.jpg','woman2.jpg','woman3.jpg','woman4.jpg']
covjek=0
broj_zar =0
broj_pap=0



class PlayerE(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerE, self).__init__()
        self.surf = pygame.image.load(Ljudi[random.randint(0,7)]).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.speed = 10

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class PlayerS(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerS, self).__init__()
        self.surf = pygame.image.load(Ljudi[covjek]).convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.speed = 10

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Papir(pygame.sprite.Sprite):
    def __init__(self):
        super(Papir, self).__init__()
        self.surf = pygame.image.load("wc.jpg").convert()
        self.surf.set_colorkey(white, RLEACCEL)
        self.rect = self.surf.get_rect()


class EnemyR(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyR, self).__init__()
        self.surf = pygame.image.load("virus.png").convert()
        self.surf.set_colorkey(black, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )


    def update(self):
        self.rect.move_ip(-(random.randint(0,10)), random.randint(-10,10))
        if self.rect.right < 0:
            self.kill()

class EnemyL(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyL, self).__init__()
        self.surf = pygame.image.load("virus.png").convert()
        self.surf.set_colorkey(black, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-150,-100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )


    def update(self):
        self.rect.move_ip(abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right > SCREEN_WIDTH:
            self.kill()


class EnemyI(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyI, self).__init__()
        self.surf = pygame.image.load("virusI.png").convert()
        self.surf.set_colorkey(white, RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )


    def update(self):
        self.rect.move_ip(-abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right < 0:
            self.kill()
            
pygame.mixer.init()

pygame.init()



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
zaraza=pygame.mixer.Sound('cough.ogg')
win=pygame.mixer.Sound('win.ogg')
swin=pygame.mixer.Sound('victory.ogg')
nema=pygame.mixer.Sound('nema.ogg')
ima=pygame.mixer.Sound('ima.ogg')

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def text_objectsb(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    
    pygame.display.update()

    pygame.mixer.music.stop()

def kolko_jos(text1):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects('{} od 8 ljudi ima papira'.format(str(text1)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()


def count(text1, text2):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects('{} Zaraženih   {} Papira'.format(str(text1), str(text2)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def count11(text1, text2):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects('{} Zaražen   {} Papir'.format(str(text1), str(text2)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def count1(text1, text2):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects('{} Zaražen   {} Papira'.format(str(text1), str(text2)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def count01(text1, text2):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = text_objects('{} Zaraženih   {} Papir'.format(str(text1), str(text2)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
    
def pobjeda(action):
    message_display('Čestitam')
    win.play()
    pygame.time.delay(6000)
    screen.fill(black)
    action()

def Victory(action):
    message_display('Pobijedio si Kralju')
    swin.play()
    pygame.time.delay(4000)
    screen.fill(black)
    action()

def Title(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objectsb(text, largeText)
    TextRect.center = (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/3))
    screen.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
    
def crash(action):
    message_display('Zaražen!')
    zaraza.play()

    pygame.time.delay(3000)
    
    screen.fill(black)

    action()

def buttonE(msg,x,y,iw,ih,ic,ac,aw,ah,fi,fa,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+iw > mouse[0] > x and y+ih > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,aw,ah))
        smallText = pygame.font.SysFont("comicsansms",fa)
        textSurf, textRect = text_objectsb(msg, smallText)
        textRect.center = ( (x+(aw/2)), (y+(ah/2)) )
        screen.blit(textSurf, textRect)

        if click[0] == 1 and action!= None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,iw,ih))
        smallText = pygame.font.SysFont("comicsansms",fi)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(iw/2)), (y+(ih/2)) )
        screen.blit(textSurf, textRect)

def back(msg,x,y,iw,ih,ic,ac,aw,ah,fi,fa,action=None):
    global broj_zar
    global broj_pap
    global covjek
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+iw > mouse[0] > x and y+ih > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,aw,ah))
        smallText = pygame.font.SysFont("comicsansms",fa)
        textSurf, textRect = text_objectsb(msg, smallText)
        textRect.center = ( (x+(aw/2)), (y+(ah/2)) )
        screen.blit(textSurf, textRect)

        if click[0] == 1 and action!= None:
            running = False
            nema.stop()
            pygame.mixer.music.stop()
            broj_zar =0
            broj_pap=0
            covjek = 0
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,iw,ih))
        smallText = pygame.font.SysFont("comicsansms",fi)
        textSurf, textRect = text_objectsb(msg, smallText)
        textRect.center = ( (x+(iw/2)), (y+(ih/2)) )
        screen.blit(textSurf, textRect)

    
    

def game_intro():

    ADDENEMYI = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMYI, 650)
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    intro = True

    while intro:

        screen.fill(white)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == ADDENEMYI:
                new_enemy = EnemyI()
                all_sprites.add(new_enemy)
                
        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        mouse = pygame.mouse.get_pos()

        smallText = pygame.font.Font("freesansbold.ttf",20)

        buttonE('Endless',SCREEN_WIDTH/3,SCREEN_HEIGHT/2,100,50,green,bright_green,120,60,20,25,endless_loop)
        buttonE('Survival',SCREEN_WIDTH*2/3,SCREEN_HEIGHT/2,100,50,red,bright_red,120,60,20,25,survival_loop)
        

        
        all_sprites.update()
        
        Title('Virus Attack')
        
        pygame.display.update()
        clock.tick(15)

def endless_loop():

    global broj_zar
    global broj_pap
    clock = pygame.time.Clock()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(loops=-1)
    nema.play()
    x=0
    player = PlayerE()
    papir = Papir()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    ADDENEMYR = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMYR, 700)
    ADDENEMYL = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMYL, 700)
    NEMAPAPIRA = pygame.USEREVENT +3
    pygame.time.set_timer(NEMAPAPIRA, 4500)

        
    running = True

    while running:
        
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()

            elif event.type == QUIT:
                running = False
                pygame.quit()
                quit()

            elif event.type == ADDENEMYR:
                new_enemy = EnemyR()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDENEMYL:
                new_enemy = EnemyL()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == NEMAPAPIRA:
                nema.play()


                
        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        enemies.update()


        screen.fill((0, 0, 0))


        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if broj_zar==1:
            if broj_pap==1:
                count11(broj_zar,broj_pap)
            else:
                count1(broj_zar, broj_pap)
        elif broj_pap==1:
            count01(broj_zar, broj_pap)          
        else:
            count(broj_zar, broj_pap)
            
        screen.blit(player.surf, player.rect)
        screen.blit(papir.surf, papir.rect)
        if x == 0:
            papir.rect.move_ip(SCREEN_WIDTH-100,random.randint(40,SCREEN_HEIGHT-80))
            player.rect.move_ip(40,SCREEN_HEIGHT/2-40)
            

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            broj_zar+=1
            nema.stop()
            running = False
            crash(endless_loop)
            
        if pygame.sprite.collide_rect(player, papir):
            nema.stop()
            broj_pap+=1
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            ima.play()
            pobjeda(endless_loop)

        back('Back', SCREEN_WIDTH-50,20,40,25,white,white,45,28,10,15,game_intro)

        pygame.display.flip()

        clock.tick(30)
        x+=1

        

def survival_loop():
    global covjek
    clock = pygame.time.Clock()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(loops=-1)
    nema.play()
    x=0
    player = PlayerS()
    papir = Papir()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    ADDENEMYR = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMYR, 700)
    ADDENEMYL = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMYL, 700)
    NEMAPAPIRA = pygame.USEREVENT +3
    pygame.time.set_timer(NEMAPAPIRA, 4500)

        
    running = True

    while running:
        
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()

            elif event.type == QUIT:
                running = False
                pygame.quit()
                quit()

            elif event.type == ADDENEMYR:
                new_enemy = EnemyR()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDENEMYL:
                new_enemy = EnemyL()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == NEMAPAPIRA:
                nema.play()


                
        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)


        enemies.update()



        screen.fill((0, 0, 0))



        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        kolko_jos(covjek)


        screen.blit(player.surf, player.rect)
        screen.blit(papir.surf, papir.rect)
        if x == 0:
            papir.rect.move_ip(SCREEN_WIDTH-100,random.randint(40,SCREEN_HEIGHT-80))
            player.rect.move_ip(40,SCREEN_HEIGHT/2-40)
            


        if pygame.sprite.spritecollideany(player, enemies):

            player.kill()
            covjek=0
            nema.stop()
            running = False
            crash(game_intro)
            
        if pygame.sprite.collide_rect(player, papir):
            nema.stop()
            if covjek < 7:
                covjek+=1
            else:
                Victory(game_intro)
                
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            ima.play()
            pobjeda(survival_loop)

        back('Back', SCREEN_WIDTH-50,20,40,25,white,white,44,28,10,15,game_intro)
        
        pygame.display.flip()


        clock.tick(30)
        x+=1
    
game_intro()
