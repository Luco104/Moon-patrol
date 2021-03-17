
from time import time
import g2d
import random
from  MoonPatrolActors import *
from actor import Actor, Arena 

class MoonpatrolGame:
    
    def __init__(self, n):
        self._arena = Arena(500, 400)
        #cielo
        self._sky1 = Background(self._arena, 0, 0, (0, 0, 512, 256), 0)
        self._sky2 = Background(self._arena, 500, 0, (0, 0, 512, 256), 0)
        #montagne
        self._mountain1 = Background(self._arena, 0, 188, (0, 256, 512, 128), 0.2)
        self._mountain2 = Background(self._arena, 500, 188, (0, 256, 512, 128), 0.2)
        #sfondo con città 
        self._city1 = Background(self._arena, 0, 250, (0, 385, 512, 128), 0.5)
        self._city2 = Background(self._arena, 500, 250, (0, 385, 512, 128), 0.5)
        #terreno
        self._ground1 = Background(self._arena, 0, 350, (0, 514, 512, 126), 1.75)
        self._ground2 = Background(self._arena, 500, 350, (0, 514, 512, 126), 1.75)
        self._rover = Rover(self._arena, 100, 352)
        self._alien = []
        for i in range(0, n):
            self._alien.append(Alien(self._arena, (200, 20), self._alien))
        self._t = 0
        self._start = time()
        self._countrock = 0
        self._holecount = 0
        self._playtime = 60
        
    def getArena(self) -> Arena: #getter arena
        return self._arena

    def getRover(self) -> Rover: #getter rover
        return self._rover
    
    def getAlien(self):  #getter lista alieni
        return self._alien
    
    def spawnRock(self): #spawn rocce
        
        if random.randint(0, 100) == 69 and not self._arena.getStop() and \
           self._countrock >= 35 and \
           self._holecount >= 30:
            flag = bool(random.getrandbits(1))
            if flag:
                Rock(self._arena, 520, 333, (95, 200, 15, 15))
            else:
                self._countrock = 0
        else:
            self._countrock += 1

    def spawnHole(self): #spawn buche
        
        if random.randint(0, 150) == 69 and \
           not self._arena.getStop() and self._countrock >= 30 and self._holecount >= 30:
            flag1 = bool(random.getrandbits(1))
            if flag1:
                Hole(self._arena, 520, 350, (131, 167, 22, 26)) #(arena, x, y, clip)
            else:
                self._holecount = 0
        else:
            self._holecount += 1
    
        
    def game_over(self) -> bool:
        if self._rover.boom():
            if self._t <= 60:
                self._t += 2
                return False
            return True
        return False
    
    def game_won(self) -> bool:
        if not self._alien:
            return True
        return False


    def remaining_time(self) -> int:
        return int(self._start + self._playtime - time())
