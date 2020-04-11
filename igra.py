#importam pygame
import pygame

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


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# radimo klasu player pomoću pygameovog spritea
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("man.jpg").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
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


# stvaramo neprijatelje
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
        self.speed = random.randint(-10,10)

    # funkcija koja pomiče neprijatelja određenom brzinom
    # neprijatelj se briše iz svih grupa kada izaže s ekrana
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
        self.speed = random.randint(-10,10)

    # funkcija koja pomiče neprijatelja određenom brzinom
    # neprijatelj se briše iz svih grupa kada izaže s ekrana
    def update(self):
        self.rect.move_ip(abs(random.randint(-10,10)), random.randint(-10,10))
        if self.rect.right < 0:
            self.kill()

pygame.mixer.init()

# initializacija 
pygame.init()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# stvaramo prozor
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# stvaramo novi event koji će se ponavljati svakij 250 milisekundi
ADDENEMYR = pygame.USEREVENT + 2
pygame.time.set_timer(ADDENEMYR, 350)
ADDENEMYL = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMYL, 350)


# stvaramo playera
player = Player()

# stvaramo grupe za neprijatelje i za sve objekte na ekranu(spriteove)
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(loops=-1)

zaraza=pygame.mixer.Sound('zaraza.ogg')

# pokrećemo loop
running = True

while running:



    # za svaki događaj
    for event in pygame.event.get():
         # ako je pritisnuta tipka
        if event.type == KEYDOWN:
            # ako je pritisnut escape, loop se zatvara
            if event.key == K_ESCAPE:
                running = False

        # ako je pritisnut gump za zatvaranje prozora loop se zatvara
        elif event.type == QUIT:
            running = False

        # ako je event za dodavanje neprijatelja, stvaramo ga i dodajemo ga u grupu
        elif event.type == ADDENEMYR:
            new_enemy = EnemyR()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDENEMYL:
            new_enemy = EnemyL()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    # dobivamo rjecnik svih pritisnutih tipki
    pressed_keys = pygame.key.get_pressed()

    # funkcijom update pomičemo igrača
    player.update(pressed_keys)

    # pa neprijatelja
    enemies.update()


    # bojamo prozor u bijelo
    screen.fill((0, 0, 0))

     # funkcijom blit crtamo objekte(spriteove) na prozoru
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # pygame ima funkciju za provjeravanje ako je došlo do sudara igrača i neprijatelja
    if pygame.sprite.spritecollideany(player, enemies):
    # ako jest, loop se gasi
        player.kill()
        zaraza.play
        running = False
        
    # flip funkcija prikazuje sve ovo na prozoru
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)
# At this point, we're done, so we can stop and quit the mixer

