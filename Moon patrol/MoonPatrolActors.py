
import g2d
import random
from MoonPatrolGame import *
from actor import Actor, Arena

class Rover(Actor):
    
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 31, 22
        self._speed = 2
        self._dx, self._dy = 0, 0
        self._arena = arena
        self._i = 0    #contatore per animazioni
        arena.add(self)
        self._exploding = False   #per avvio animazione esplosione
        self._landed = True
        self._right = False #booleano per movimento a dx 
        self._left = False #booleano per movimento a sx

    def move(self):
        arena_w, arena_h = self._arena.size()
        
        self._y += self._dy
        if self._y < 0:
            self._y = 0
            self._landed = False
            
        elif self._y > 351 - self._h:
            self._y = 351 - self._h
            self._landed = True

        if not self._landed:
            self._dy += 0.3
            
        if self._i == 60:
            self._arena.getStop()
            self._arena.remove(self)

        self._x += self._dx
        if self._x < 0:
            self._x = 0
        elif self._x > arena_w - self._w:
            self._x = arena_w - self._w

    def go_right(self):
        self._right = True
        self._left = False
        self._dx, self._dy = 2.5, 0

    def go_left(self):
        self._right = False
        self._left = True
        self._dx, self._dy = -2.5, 0
        
    def jump(self):
        if self._landed:
            self._landed = False
            self._dy = -3 * self._speed
            #print("JUMP") #debugging

    def stay(self):
        self._dx, self._dy = 0, 0

    def collide(self, other):
            
        if isinstance(other, Hole):
            self._exploding = True
            #print("BOOM") #debugging

        if isinstance(other, Rock):
            self._exploding = True
            #print("THUD") #debugging

        if isinstance(other, Ray):
            self._exploding = True
            #print("DEAD") #debugging
            
    def boom(self):
        return self._exploding

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        
        if self._exploding:
            
            self._arena.stay_all()
            
            if 0 <= self._i <= 15:
                self._i += 2
                return 113, 101, 47, 32
            if 15 < self._i <= 30:
                self._i += 2
                return 164, 102, 43, 32
            if 30 < self._i <= 45:
                self._i += 2
                return 212, 102, 41, 30
            if 45 < self._i <= 60:
                self._i += 2
                return 262, 117, 33, 17
            if i > 60:
                self._arena.stay_all()
        else:
            return 212, 159, self._w, self._h
    
    
class Alien(Actor):
    
    def __init__(self, arena, pos, alien):
        self._x, self._y = pos
        self._w, self._h = 17, 8
        self._xmin, self._xmax = 0, arena.size()[1]
        self._dx, self._dy = 2, 2
        self._arena = arena
        arena.add(self)
        self._countshots = 0
        self._alien = alien

    def move(self):
        if 0 <= self._x + self._w <= self._xmax and \
           0 < self._y + self._h <= 400:
            self._x += self._dx
            self._y += self._dy
            self._dx = random.choice([-5, 0, 5])
            self._dy = random.choice([-5, 0, 5])
            
        #proiettili alieni

            if random.randint(0, 500) == 420 and not self._arena.getStop() and \
               self._countshots >= 30:
                Ray(self._arena, self._x, self._y)
            else:
                self._countshots += 1
        else:
            self._dx = 0
            self._dy = 2
            self._y += self._dy
            
    def stay(self):
        self._dx = 0
        self._dy = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 66, 230, self._w, self._h

    def collide(self, other):
        if isinstance(other, Bullet):
            self._alien.remove(self)
            self._arena.remove(other)
    

class Bullet(Actor):
    
    def __init__(self, arena, x0: int, y0: int):
        self._w, self._h = 3, 8
        self._x, self._y = x0, y0
        self._dy = -5
        self._arena = arena
        arena.add(self)

    def move(self):
        self._y += self._dy
        
        if self._y < 0:
            self._arena.remove(self)
            
    def stay(self):
        self._dy = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 126, 116, self._w, self._h

    def collide(self, other):
        if isinstance(other, Alien):
            self._arena.remove(other)
            self._arena.remove(self)

class Ray(Actor):
    
    def __init__(self, arena, x0: int, y0: int):
        self._w, self._h = 3, 8
        self._x, self._y = x0, y0
        self._dy = 5
        self._arena = arena
        arena.add(self)

    def move(self):
        self._y += self._dy
        #print("PEW PEW") #debugging
        if self._y >= 350:
            self._arena.remove(self)
    
    def stay(self):
        self._dy = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 126, 116, self._w, self._h

    def collide(self, other):
        if isinstance(other, Rover):
            self._arena.remove(self)


class Missile(Actor):
    
    def __init__(self, arena, x0: int, y0: int):
        self._w, self._h = 8, 3
        self._x, self._y = x0, y0
        self._dx = 5
        self._arena = arena
        arena.add(self)
        self._destroy = 0

    def move(self):
        self._x += self._dx
        if self._x > 500:
            self._arena.remove(self)
            
    def stay(self):
        self._dx = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        return 126, 116, self._w, self._h

    def collide(self, other):
            
        if isinstance(other, Rock):
            self._arena.remove(other)
            self._arena.remove(self)
            

class Hole(Actor):
    
    def __init__(self, arena, x, y, clip: (int, int, int, int)):
        self._w, self._h = 15, 25
        self._x, self._y = x, y
        self._dx = -1.75
        self._clip= clip
        self._arena = arena
        arena.add(self)

    def move(self):
        self._x += self._dx
        if self._x < 0:
            self._arena.remove(self)
            
    def stay(self):
        self._dx = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        #passo al costruttore i parametri di ritaglio immagine
        return self._clip

    def collide(self, other):
        pass

class Rock(Actor):
    
    def __init__(self, arena, x, y, clip: (int, int, int, int)):
        self._w, self._h = 20, 20 
        self._x, self._y = x, y
        self._dx = -1.75
        self._clip= clip
        self._arena = arena
        arena.add(self)

    def move(self):
        self._x += self._dx
        if self._x < 0:
            self._arena.remove(self)
            
    def stay(self):
        self._dx = 0
        
    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        #passo al costruttore i parametri di ritaglio immagine
        return self._clip

    def collide(self, other):
        if isinstance(other, Hole):
            self._arena.remove(self)

        
            
class Background(Actor):
    
    def __init__(self, arena, x, y, clip: (int, int, int, int), speed):
        self._w, self._h = 500, 256
        self._x, self._y = x, y
        self._speed = speed
        self._clip = clip
        self._dx = -self._speed
        self._initx = self._x
        self._arena = arena
        arena.add(self)

    def move(self):
        self._x += self._dx
        if self._initx - self._x >= self._w:
            self._x = self._initx
            
    def stay(self):
        self._dx = 0

    def position(self):
        return self._x, self._y, self._w, self._h

    def symbol(self):
        #passo al costruttore i parametri di ritaglio immagine
        return self._clip

    def collide(self, other):
        pass
    
