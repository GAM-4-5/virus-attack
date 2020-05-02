#importam module
import pygame
import time
import random

#za prepoznavanje unosa s tipkovnice
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

#neke varijable
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


#klasa player koja nasljeđuje svojstva klase sprite
#E znači da je ovo klasa igrača u Endless modu
class PlayerE(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerE, self).__init__()
        #igrača u endlessu predstavlja nasumična slika iz liste
        self.surf = pygame.image.load(Ljudi[random.randint(0,7)]).convert()
        #colorkey je boja koja koja će na slici biti prozirna, kao greenscreen
        self.surf.set_colorkey(black, RLEACCEL)
        self.rect = self.surf.get_rect()

        self.speed = 10
#funkcija update koja pomiče playera prema stisnutim tipkama
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

#kako igrač nebi mogao izaći s ekrana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#player u Survivalu
class PlayerS(pygame.sprite.Sprite):
    def __init__(self):
        super(PlayerS, self).__init__()
        #igrača u survivalu predstavlja točno određena slika iz liste
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

#funkcija za crtanje papira na ekranu koji isto nasljeđuje sprite
class Papir(pygame.sprite.Sprite):
    def __init__(self):
        super(Papir, self).__init__()
        self.surf = pygame.image.load("wc.jpg").convert()
        self.surf.set_colorkey(white, RLEACCEL)
        self.rect = self.surf.get_rect()

#R znači da se virus stvara s desne strane ekrana 
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
        #virus se pomiče u lijevo zato je predznak negativan
        self.rect.move_ip(-(random.randint(0,10)), random.randint(-10,10))
        #ako izađe iz ekrana virus se briše iz svih grupa
        if self.rect.right < 0:
            self.kill()

#s lijeve strane
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
        #pomiče se u desno
        self.rect.move_ip(abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

#virusi koji se stvaraju u pozadini početnog menua
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

#inicijalizacija mixera i pygamea            
pygame.mixer.init()
pygame.init()
#stvaramo ekran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#imenujemo neke zvune efekte
zaraza=pygame.mixer.Sound('cough.ogg')
win=pygame.mixer.Sound('win.ogg')
swin=pygame.mixer.Sound('victory.ogg')
nema=pygame.mixer.Sound('nema.ogg')
ima=pygame.mixer.Sound('ima.ogg')

#funkcije koje služe za prikazivanje teksta
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def text_objectsb(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#ova funkcija prikazuje poruku kada se igrač zarazi ili sakupi papir
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    
    pygame.display.update()
    #gasimo muziku
    pygame.mixer.music.stop()

#funkcija koja u survival modu prikazuje koliko ljudi ima papira
def kolko_jos(text1, action):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf, TextRect = action('{} od 8 ljudi ima papira'.format(str(text1)), largeText)
    TextRect= (20,20)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

#funkcije koje u endless modu prikazuju broj zaraženih i papira
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

#kada se skupi papir
def pobjeda(action):
    message_display('Čestitam')
    win.play()
    #zaustavljamo vrijeme na 6 sekundi
    pygame.time.delay(6000)
    screen.fill(black)
    action()

#kada se pobijedi u survival modu
def Victory(action):
    message_display('Pobijedio si Kralju')
    swin.play()
    pygame.time.delay(4000)
    screen.fill(black)
    covjek=0
    action()

#naslov na početnom meniju
def Title(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objectsb(text, largeText)
    TextRect.center = (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/3))
    screen.blit(TextSurf, TextRect)
    
    pygame.display.update()
    
#kada se igrač zarazi
def crash(action):
    message_display('Zaražen!')
    zaraza.play()

    pygame.time.delay(3000)
    
    screen.fill(black)

    action()
    
#funkcija za gumbe na početnom meniju. Funkcija prima poruku, x i y koordinate gornjeg lijevog kuta gumba, dimenzije i boju gumba te veličinu fonta
def buttonE(msg,x,y,iw,ih,ic,ac,aw,ah,fi,fa,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #kada se pokazivač nalazi na gumbu, on poprima active dimenzije
    if x+iw > mouse[0] > x and y+ih > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,aw,ah))
        smallText = pygame.font.SysFont("comicsansms",fa)
        textSurf, textRect = text_objectsb(msg, smallText)
        textRect.center = ( (x+(aw/2)), (y+(ah/2)) )
        screen.blit(textSurf, textRect)
        #gumb vrši funkciju kada se na njega klikne
        if click[0] == 1 and action!= None:
            action()
    #kada pokazivač nije na gumbu, on ponovno poprima inactive dimenzije
    else:
        pygame.draw.rect(screen, ic,(x,y,iw,ih))
        smallText = pygame.font.SysFont("comicsansms",fi)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(iw/2)), (y+(ih/2)) )
        screen.blit(textSurf, textRect)

#ista funkcija samo za gumb za povratak na početni meni
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
        #klikom na ovaj gumb sve varijable za brojanje zaraženih i papira se resetiraju
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

    
    
#loop za početni ekran
def game_intro():
#eventi koji se ponavlja svakih 650 milisekundi
    ADDENEMYI = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMYI, 650)
#stvaramo grupu spriteova
    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()

    intro = True

    while intro:

        screen.fill(white)
        
        for event in pygame.event.get():
            #ako je pritisnuta tipka za zatvaranje prozora ili escape tipka, program se gasi
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            #kada je vrijeme za to dodajemo viruse u grupu spriteova
            elif event.type == ADDENEMYI:
                new_enemy = EnemyI()
                all_sprites.add(new_enemy)
                
        #crtamo spriteove na ekran
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        #dobivamo poziciju miša
        mouse = pygame.mouse.get_pos()

        smallText = pygame.font.Font("freesansbold.ttf",20)

        #gumbi zaa endless i survival mode
        buttonE('Endless',SCREEN_WIDTH/3,SCREEN_HEIGHT/2,100,50,green,bright_green,120,60,20,25,endless_loop)
        buttonE('Survival',SCREEN_WIDTH*2/3,SCREEN_HEIGHT/2,100,50,red,bright_red,120,60,20,25,survival_loop)
        

        
        all_sprites.update()
        
        Title('Virus Attack')
        
        pygame.display.update()
        #funkcijom tick namještamo framerate na 15 frameova u sekundu
        clock.tick(15)

#loop za endless mode
def endless_loop():
    #varijable moraju biti globalne da bi ih mogli mijenjati
    global broj_zar
    global broj_pap
    #funkcija clock prati vrijeme
    clock = pygame.time.Clock()
    #započinjemo muziku koja se ponavlja beskonačno dok ju se ne ugasi
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(loops=-1)
    nema.play()
    x=0
    #stvaramo igrača i dodajemo ga u grupu spriteova
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
            #dodajemo viruse i puštamo zvučni efekt
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


        #dobivamo vrijednosti pritisnute na tipkovnici        
        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        enemies.update()


        screen.fill((0, 0, 0))


        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        #razliite funcije za brojač zaraženih i papira radi gramatičke točnosti
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
        #kada se igrač i papir nacrtaju na ekran oni se crtaju u gornjem lijevom kutu. samo u prvom frameu vrijednost x je 0 i tada će se igrač i papir pomaknuti za određen broj piksela
        #do željene pozicije
        if x == 0:
            papir.rect.move_ip(SCREEN_WIDTH-100,random.randint(40,SCREEN_HEIGHT-80))
            player.rect.move_ip(40,SCREEN_HEIGHT/2-40)
            
        #funkcija koja provjerava ako je došlo do sudara između spriteova
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            #odgađamo stvaranje neprijatelja za 3 sekunde i uvećavamo broj zaraženih
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            broj_zar+=1
            nema.stop()
            running = False
            #funkcija crash na kraju izvođenja ponovno pokreće endless looop
            crash(endless_loop)
        #ako igrač skupi papir
        if pygame.sprite.collide_rect(player, papir):
            nema.stop()
            broj_pap+=1
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            ima.play()
            pobjeda(endless_loop)
            
        #crtamo gumb back
        back('Back', SCREEN_WIDTH-50,20,40,25,white,white,45,28,10,15,game_intro)

        pygame.display.flip()

        clock.tick(30)
        x+=1

        
#loop survival modea
def survival_loop():
    #varijabla covjek broji koliko je ljudi dobilo papir
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
        
        kolko_jos(covjek, text_objects)


        screen.blit(player.surf, player.rect)
        screen.blit(papir.surf, papir.rect)
        if x == 0:
            papir.rect.move_ip(SCREEN_WIDTH-100,random.randint(40,SCREEN_HEIGHT-80))
            player.rect.move_ip(40,SCREEN_HEIGHT/2-40)
            

        #kada se ihra sudari s virusom, varijabla covjek se resetira
        if pygame.sprite.spritecollideany(player, enemies):

            player.kill()
            covjek=0
            nema.stop()
            running = False
            crash(game_intro)
        #kada igrač sakupi papir    
        if pygame.sprite.collide_rect(player, papir):
            nema.stop()
            #ako nije bio osmi čovjek
            if covjek < 7:
                #brojač čiji je font bijele boje precrtavamo identičnim crne boje
                kolko_jos(covjek, text_objectsb)
                #uvećavamo varijablu covjek
                covjek+=1
                #prikazujemo poruku s uvećanim brojem ljudi sa papirom odmah nakon što se sakupi
                kolko_jos(covjek, text_objects)
            #ako je došao do papira s osmim likom igrač je pobijedio    
            else:
                kolko_jos(covjek, text_objectsb)
                covjek+=1
                kolko_jos(covjek, text_objects)
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
