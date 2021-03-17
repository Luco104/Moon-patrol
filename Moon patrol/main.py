import g2d
from MoonPatrolGame import *
from MoonPatrolGui import *
import os

def main():
    n = 3
    g2d.init_canvas((500, 400))
    g2d.alert("defeat all the aliens!")
    background = g2d.load_image("moon-patrol-bg.png")
    sprites = g2d.load_image("moon-patrol.png")

    if os.path.isfile("config.txt"):
        with open('config.txt', 'r') as file:
            for i in file:
                if i.startswith('alien'):
                    i = i.strip()
            gui = MoonPatrolGui(sprites, background, n)
    else:
        gui = MoonPatrolGui(sprites, background, n)
        with open('config.txt', 'w') as file1:
            file1.write("number of aliens:")
            file1.write("3")
    g2d.main_loop(gui.tick)

if __name__ == '__main__':
        main()
