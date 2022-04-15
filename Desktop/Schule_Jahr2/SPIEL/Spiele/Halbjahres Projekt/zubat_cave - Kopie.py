from typing import Set
import pygame
import os
from random import randint 
from settings import Settings, Background
from timer import Timer
#from animation import Animation

#Ich besitze keinerlei Rechte an den, in diesem Programm, verwendeten Bildern.
#Mit den diesem Programm wird kein kommerzieller Gewinn erzielt.
#Die in diesem Programm verwendeten Bilder stammen von den vollgenden Internetseiten:
#'djungle_rain.png' stammt von https://www.umdiewelt.de/t4455_18 (www.umdiewelt.de)
#'dragonfly.png' stammt von https://miausmiles.com/2011/incredible-random-stuff/draw-something-every-day-035 (www.miausmiles.com)
#'drop.png' stammt von http://www.clipartpanda.com/clipart_images/domain-raindrop-clip-art-19285059 (www.clipartpanda.com)
#Ich bedanke mich bei den Contan Creatorn für ihre gute Arbeit

class Animation(object):
    def __init__(self, namelist, endless, animationtime, colorkey=None):
        self.images = []
        self.endless = endless
        self.timer = Timer(animationtime)
        for filename in namelist:
            if colorkey == None:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert_alpha()
            else:
                bitmap = pygame.image.load(Settings.imagepath(filename)).convert()
                bitmap.set_colorkey(colorkey)
            self.images.append(bitmap)
        self.imageindex = -1

    def next(self):
        if self.timer.is_next_stop_reached():
            self.imageindex += 1 
            if self.imageindex >= len(self.images):
                #game.FLY = False
                if self.endless:
                    self.imageindex = len(self.images) - 1
                else:
                    self.imageindex = 0 
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False

class Dragonfly(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.dragonfly_size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)       
        self.rect.centerx = Settings.dragonfly_size[0] + 10
        self.rect.bottom = Settings.window_height // 2
        self.speed = 5
        self.fly = Animation([f"zubat{i}.png" for i in range(0, 8)], False, 100)

    def update(self):
        #if game.FLY == False:
            #self.image = pygame.image.load(Settings.imagepath(f"zubat0.png")).convert_alpha()
        c = self.rect.bottom
        x = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = c
        self.rect.centerx = x

    #Bewegen des Spielers
    def watch_for_move(self):
        press = pygame.key.get_pressed()                       #registiert Tastendruck
        if press[pygame.K_UP]:
            self.rect.top -= self.speed
            self.image = self.fly.next()
            self.update()
        if press[pygame.K_DOWN]:
            self.rect.top += self.speed
            self.image = self.fly.next()
            self.update()
        #Wandkollision
        if self.rect.top <= 5:
            self.rect.top += 5
        if self.rect.bottom >= Settings.window_height -5:
            self.rect.top -= 5  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game(object):
    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        pygame.display.set_caption(Settings.title)
        self.clock = pygame.time.Clock()
        self.background = Background("Cave_Stage_Background.png")
        self.dragonfly_group = pygame.sprite.Group()
        self.running = True
        self.counter = 0
        self.dragonflys = 0
        self.lives = 3
        #self.FLY = False

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.watch_for_events()
            self.player()
            self.draw()
        pygame.quit()
        pygame.font.quit()      

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:        
                if event.key == pygame.K_ESCAPE:   
                    self.running = False
            elif event.type == pygame.QUIT:         
                self.running = False

    def player(self):
        if self.dragonflys == 0 and self.lives > 0:           #falls der Spieler kollidiert und er noch Leben übrig hat
            self.dragonfly = Dragonfly('zubat0.png')
            self.dragonfly_group.add(self.dragonfly)          #wird ein neuer Spieler erstellt
            self.dragonflys = 1                               #self.dragonflys ist 1 wenn der Spieler noch nicht collidiert ist
        else:
            pass
        self.dragonfly.watch_for_move()
        
    def draw(self):
        self.background.draw(self.screen)
        self.dragonfly_group.draw(self.screen)
        #falls alle Leben verbraucht sind wird der End Screen gezeigt
        pygame.display.flip()



if __name__ == "__main__":
    os.environ["SDL_VIDEO_WINDOW_POS"] = "500, 50"

    game = Game()
    game.run()