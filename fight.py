from email.mime import image
import pygame
from pygame.constants import (QUIT, K_ESCAPE, KEYDOWN)
import os

#für Herrn Adams zum testen
# Space Taste: Rekeln des Charakters
# P Taste: ein einzelner Schlag
# J Taste: ein Sprung in die Luft
# K Taste: ein doppel Kick
class Settings(object):
    window = {'width':800, 'height':400}
    fps = 60
    title = "Animation"
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")

    @staticmethod
    def dim():
        return (Settings.window['width'], Settings.window['height'])

    @staticmethod
    def filepath(name):
        return os.path.join(Settings.path['file'], name)

    @staticmethod
    def imagepath(name):
        return os.path.join(Settings.path['image'], name)


class Background(pygame.sprite.Sprite):
    def __init__(self, filename) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path['image'], filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window['width'], Settings.window['height']))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass


class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0


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
                anim.STAND = False
                anim.PUNCH = False
                anim.JUMP = False
                anim.KICK = False
                if self.endless:
                    self.imageindex = 0 
                else:
                    self.imageindex = len(self.images) - 1
        return self.images[self.imageindex]

    def is_ended(self):
        if self.endless:
            return False
        elif self.imageindex >= len(self.images) - 1:
            return True
        else:
            return False
        

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(Settings.imagepath(f"stand{0}.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window['width'] // 2
        self.rect.bottom = Settings.window['height'] - 30
        self.stand = Animation([f"stand{i}.png" for i in range(0, 8)], True, 50)
        self.punch = Animation([f"punch{i}.png" for i in range(0, 4)], True, 50)
        self.jump = Animation([f"jump{i}.png" for i in range(0, 8)], True, 50)
        self.kick = Animation([f"kick{i}.png" for i in range(0, 8)], True, 50)
        

    def update(self):
        if anim.STAND == False and anim.JUMP == False and anim.PUNCH == False and anim.KICK == False:
            self.image = pygame.image.load(Settings.imagepath(f"stand0.png")).convert_alpha()
        c = self.rect.bottom
        x = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = c
        self.rect.centerx = x
        
    def anim_stand(self):
        self.image = self.stand.next()
        self.update()
    
    def anim_punch(self):
        self.image = self.punch.next()
        self.update()
    
    def anim_jump(self):
        self.image = self.jump.next()
        self.update()
    
    def anim_kick(self):
        self.image = self.kick.next()
        self.update()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)       


class SteetFighter(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
        pygame.init()
        self.screen = pygame.display.set_mode(Settings.dim())
        pygame.display.set_caption(Settings.title)
        self.background = Background("street_fighter_roof.png")
        self.clock = pygame.time.Clock()
        self.ryu = Fighter()
        self.running = False
        self.STAND = False
        self.PUNCH = False
        self.JUMP = False
        self.KICK = False


    def run(self) -> None:
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.stand()
                if event.key == pygame.K_p:
                    self.punch()
                if event.key == pygame.K_j:
                    self.jump()
                if event.key == pygame.K_k:
                    self.kick()            
                    
    def update(self) -> None:
        if self.STAND == True:
            self.ryu.anim_stand()
        elif self.PUNCH == True:
            self.ryu.anim_punch()
        elif self.JUMP == True:
            self.ryu.anim_jump()
        elif self.KICK == True:
            self.ryu.anim_kick()

    def stand(self):
        if self.JUMP or self.PUNCH == True or self.KICK == True:
            pass
        else:
            self.STAND = True
    
    def punch(self):
        if self.JUMP or self.STAND == True or self.KICK == True:
            pass
        else:
            self.PUNCH = True

    def jump(self):
        if self.PUNCH or self.STAND == True or self.KICK == True:
            pass
        else:
            self.JUMP = True
    
    def kick(self):
        if self.PUNCH or self.STAND == True or self.JUMP == True:
            pass
        else:
            self.KICK = True

    def draw(self) -> None:
        self.background.draw(self.screen)
        self.ryu.draw(self.screen)
        pygame.display.flip()



if __name__ == '__main__':
    anim = SteetFighter()
    anim.run()