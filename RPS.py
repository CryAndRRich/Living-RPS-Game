import pygame, random, time, sys
from pygame.locals import *
import numpy as np

pygame.mixer.init()
pygame.init()

window_width = 600
window_height = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption('Rock Paper Scissors')

font = pygame.font.SysFont('consolas', 18)
sound_collide = pygame.mixer.Sound('collide.mp3')
sound_appear = pygame.mixer.Sound('appear.mp3')
sound_collide.set_volume(0.5)
sound_appear.set_volume(0.2)

radius = 12
rock = pygame.transform.scale(pygame.image.load("rock.png"), (radius * 2, radius * 2))
paper = pygame.transform.scale(pygame.image.load("paper.png"), (radius * 2, radius * 2))
scissors = pygame.transform.scale(pygame.image.load("scissors.png"), (radius * 2, radius * 2))

FPS = 60
fpsClock = pygame.time.Clock()


def trim(v, upper, lower):
    if v > upper:
        return upper
    if v < lower:
        return lower
    return v

def Trim(V, Upper, Lower):
    return np.array([trim(V[0], Upper[0], Lower[0]), trim(V[1], Upper[1], Lower[1])], dtype=np.float64)

max_vel = 2
max_accel = 2
choices = {0: rock, 1: paper, 2: scissors}
win = {0: 2, 1: 0, 2: 1}
class Object():
    def __init__(self, img, position, velocity, acceleration):
        self.img = img
        self.pos = position
        self.vel = velocity
        self.accel = acceleration

        self.ticks = 0
    
    def update_pos(self, targets):
        self.pos += self.vel + random.random() * (random.randint(-1, 1))
        self.vel += self.accel + random.random() * (random.randint(-1, 1))

        self.ticks += 1
        if self.ticks == 20:
            self.ticks = 0

            target = self.pos
            dist = float('inf')
            for tar in targets:
                if tar.img == win[self.img]:
                    if dist > (tar.pos[0] - self.pos[0]) ** 2 + (tar.pos[1] - self.pos[1]) ** 2:
                        dist = (tar.pos[0] - self.pos[0]) ** 2 + (tar.pos[1] - self.pos[1]) ** 2
                        target = tar.pos
            
            if target[0] == self.pos[0] and target[1] == self.pos[1]:
                target = np.array([random.randint(window_width // 5, 4 * window_width // 5), random.randint(window_height // 5, 4 * window_height // 5)], dtype=np.float64)
            vector = target - self.pos
            self.accel = max_accel * vector / np.array([window_width, window_height], dtype=np.float64)


        self.pos = Trim(self.pos, np.array([4 * window_width / 5, 4 * window_height / 5], dtype=np.float64), np.array([window_width / 5, window_height / 5], dtype=np.float64))
        self.vel = Trim(self.vel, np.array([max_vel, max_vel], dtype=np.float64), np.array([-max_vel, -max_vel], dtype=np.float64))
        self.accel = Trim(self.accel, np.array([max_accel, max_accel], dtype=np.float64), np.array([-max_accel, -max_accel], dtype=np.float64))
    
    def update_img(self):
        self.img += 1
        self.img %= 3


class gamePlay():
    def __init__(self):
        self.objects = []
    
    def fill_obj(self):
        for i in range(3):
            for _ in range(20):
                position = np.array([random.randint(window_width // 5, 4 * window_width // 5), random.randint(window_height // 5, 4 * window_height // 5)], dtype=np.float64)
                velocity = np.array([random.randint(-max_vel, max_vel), random.randint(-max_vel, max_vel)], dtype=np.float64)
                acceleration = np.array([random.randint(-max_accel, max_accel), random.randint(-max_accel, max_accel)], dtype=np.float64)
                self.objects.append(Object(i, position, velocity, acceleration))
        random.shuffle(self.objects)
    
    def clear_obj(self):
        self.objects = []
    
    def draw_img(self): 
        for obj in self.objects:
            DISPLAYSURF.blit(choices[obj.img], obj.pos)
    
    def draw_text(self):
        count = [0, 0, 0]
        for obj in self.objects:
            count[obj.img] += 1
        
        res_text = 'Rock: ' + str(count[0]) + ' Paper: ' + str(count[1]) + ' Scissors: ' + str(count[2])
        DISPLAYSURF.blit(font.render(res_text, True, WHITE), (15, window_height - 30))
    
    def check_collide(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1, obj2 = self.objects[i], self.objects[j]
                if obj1.img == obj2.img:
                    continue

                x1, y1 = obj1.pos
                x2, y2 = obj2.pos

                dist = (x1 - x2) ** 2 + (y1 - y2) ** 2
                if dist < (radius * 2) ** 2:
                    if obj1.img < obj2.img:
                        if obj1.img == 0 and obj2.img == 2:
                            obj2.update_img()
                        else:
                            obj1.update_img()
                    elif obj1.img > obj2.img:
                        if obj1.img == 2 and obj2.img == 0:
                            obj1.update_img()
                        else:
                            obj2.update_img()
                    
                    sound_collide.play()

    def update(self, ticks):
        if ticks >= 150:
            DISPLAYSURF.fill(BLACK)
            self.draw_img()
            for obj in self.objects:
                obj.update_pos(self.objects)
            self.check_collide()
        elif ticks < 120:
            if ticks % 2 == 0:
                obj = self.objects[ticks // 2]
                DISPLAYSURF.blit(choices[obj.img], obj.pos)
                sound_appear.play()

def RPS():
    play = gamePlay()
    play.fill_obj()
    ticks = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                DISPLAYSURF.fill(BLACK)
                play.clear_obj()
                ticks = 0
                pygame.display.flip()
                
                time.sleep(1 / FPS)
                play.fill_obj()

        play.update(ticks)
        ticks += 1

        play.draw_text()
        
        time.sleep(1 / FPS)
        pygame.display.update()
        fpsClock.tick(FPS)
    

if __name__ == '__main__':
    RPS()