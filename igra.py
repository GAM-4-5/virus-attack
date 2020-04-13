#importam pygame
import pygame
import time
import random

# ovo je za lakši pristup tipkama za pomicanje
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


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# radimo klasu player pomoću pyvirusovog spritea
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("man.jpg").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
##        self.rect+=((SCREEN_WIDTH/2, SCREEN_HEIGHT/2),(0,0))
        self.speed = 10
    # funkcija update pomiče igrača s obzirom na pritisnute tipke
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # ovo služi da igrač nemože izaći iz ekrana
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
# stvaramo viruse
#posebne klase za viruse koji ce dolazitisa lijeve i desne strane
class EnemyR(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyR, self).__init__()
        self.surf = pygame.image.load("virus.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # funkcija koja pomiče viruse određenom brzinom
    # virus se briše iz svih grupa kada izađe s ekrana
    def update(self):
        self.rect.move_ip(-abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right < 0:
            self.kill()

class EnemyL(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyL, self).__init__()
        self.surf = pygame.image.load("virus.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(-100,-0),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # funkcija koja pomiče virus određenom brzinom
    # virus se briše iz svih grupa kada izaže s ekrana
    def update(self):
        self.rect.move_ip(abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right < 0:
            self.kill()

#funkcijom mixer upravljat ćemo zvukom
pygame.mixer.init()

# initializacija 
pygame.init()



# stvaramo prozor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
zaraza=pygame.mixer.Sound('zaraza.ogg')
win=pygame.mixer.Sound('win.ogg')
nema=pygame.mixer.Sound('nema.ogg')
ima=pygame.mixer.Sound('ima.ogg')
# stvaramo novi event koji će se ponavljati svakij 250 milisekundi



#funkcije kojima ćemo prikazati tekst na ekranu
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
    screen.blit(TextSurf, TextRect)
    
    pygame.display.update()

    pygame.mixer.music.stop()

    
    

def pobjeda():
    message_display('Čestitam')
    win.play()
    pygame.time.delay(6000)
    screen.fill(black)
    game_loop()
def crash():
    message_display('Zaražen!')
    zaraza.play()


    
    screen.fill(black)

    game_loop()
    
    
# stvaramo grupe za viruse i za sve objekte na ekranu(spriteove)

# stvaramo playera

#dodajemo muziku i zvučne efekte u mixer 


def game_loop():
    # pokrećemo loop
    # clock nam određuje framerate
    clock = pygame.time.Clock()
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(loops=-1)
    nema.play()
    x=0
    player = Player()
    papir = Papir()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    ADDENEMYR = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMYR, 450)
    ADDENEMYL = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMYL, 450)
    NEMAPAPIRA = pygame.USEREVENT +3
    pygame.time.set_timer(NEMAPAPIRA, 4500)
    
    running = True

    while running:

        
        # za svaki događaj
        for event in pygame.event.get():
             # ako je pritisnuta tipka
            if event.type == KEYDOWN:
                # ako je pritisnut escape, loop se zatvara
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()

            # ako je pritisnut gump za zatvaranje prozora loop se zatvara
            elif event.type == QUIT:
                running = False
                pygame.quit()
                quit()

            # ako je event za dodavanje virusa, stvaramo ga i dodajemo ga u grupu
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


                
        # dobivamo rjecnik svih pritisnutih tipki
        pressed_keys = pygame.key.get_pressed()

        # funkcijom update pomičemo igrača
        player.update(pressed_keys)

        # pa virus
        enemies.update()


        # bojamo prozor u bijelo
        screen.fill((0, 0, 0))

        # funkcijom blit crtamo objekte(spriteove) na prozoru
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            
        #pa igrača
        screen.blit(player.surf, player.rect)
        screen.blit(papir.surf, papir.rect)
        if x == 0:
            papir.rect.move_ip(1000,280)
            player.rect.move_ip(40,260)

        # pygame ima funkciju za provjeravanje ako je došlo do sudara igrača i virusa
        if pygame.sprite.spritecollideany(player, enemies):
        # ako jest, loop se gasi
            player.kill()
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            nema.stop()
            running = False
            crash()
            
        if pygame.sprite.collide_rect(player, papir):
            nema.stop()
            pygame.time.set_timer(ADDENEMYR, 3000)
            pygame.time.set_timer(ADDENEMYL, 3000)
            pygame.time.set_timer(NEMAPAPIRA, 8000)
            ima.play()
            pobjeda()
            print(papir.rect)
            print(player.rect)
            
##            papir.kill()
##            papir = Papir()
##            player.surf.blit(papir.surf, papir.rect)
        # flip funkcija prikazuje sve ovo na prozoru
        pygame.display.flip()

        #za 30 fps-a
        clock.tick(30)
        x+=1
    #gasimo muziku 
    
game_loop()
