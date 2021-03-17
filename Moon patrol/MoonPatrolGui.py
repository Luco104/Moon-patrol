
import g2d
import random
from MoonPatrolGame import *
from MoonPatrolActors import *

class MoonPatrolGui:
    
    def __init__(self, sprites, background, n):
        self._game = MoonpatrolGame(n)
        g2d.init_canvas(self._game.getArena().size())
        self._sprites = sprites
        self._background = background
        
    def handle_keyboard(self):
        
        if not self._game.getArena().getStop():
            
            if g2d.key_pressed("ArrowUp"):
                self._game.getRover().jump()
            elif g2d.key_released("ArrowUp"):
                self._game.getRover().stay()
                
            if g2d.key_pressed("ArrowRight"):
                self._game.getRover().go_right()
            elif g2d.key_released("ArrowRight"):
                self._game.getRover().stay()
                
            if g2d.key_pressed("ArrowLeft"):
                self._game.getRover().go_left()
            elif g2d.key_released("ArrowLeft"):
                self._game.getRover().stay()
                
            if g2d.key_pressed("Spacebar"):
                Bullet(self._game.getArena(), \
                       self._game.getRover().position()[0] + (self._game.getRover().position()[2] / 3), \
                       self._game.getRover().position()[1]) #(arena, x, y)
                
                Missile(self._game.getArena(), \
                        self._game.getRover().position()[0] + self._game.getRover().position()[2], \
                        self._game.getRover().position()[1] + (self._game.getRover().position()[3] / 2) )  #(arena, x, y)
    
    def tick(self):
        
        self.handle_keyboard()
        arena = self._game.getArena()
        self._game.getArena().move_all()  
        self._game.spawnHole() #spawn buche
        self._game.spawnRock() #spawn rocce
        
        g2d.clear_canvas()
        for a in arena.actors():
            if a.symbol != (0, 0, 0, 0):
                if isinstance(a, Background):
                    g2d.draw_image_clip(self._background, a.symbol(), a.position())
    
                else:
                    g2d.draw_image_clip(self._sprites, a.symbol(), a.position())
            else:
                g2d.fill_rect(a.position())
                
        toplay = "Time: " + str(self._game.remaining_time())
        g2d.draw_text(toplay, (0, 0), 24)

        if self._game.game_over():
            g2d.alert("Game over")
            g2d.close_canvas()

        elif self._game.game_won():
            g2d.alert("Game won")
            g2d.close_canvas()
            
                

