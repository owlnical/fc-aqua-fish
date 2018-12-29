# Class Bubble_map
# Ritar en bild med X antal bubblor
# Bilden flytta uppåt på skärmen i en loop
# Flyttas ner när den är utanför skärmen

import arcade,random
from vars import SCREEN_WIDTH, SCREEN_HEIGHT

class Bubble_map():

    def __init__(self, w=SCREEN_WIDTH, h=SCREEN_HEIGHT, amount=50, size=3, border_width=1, color=(255,255,255,random.randrange(32, 128)), speed=50):

        # Höjd / Bredd
        self.w = w
        self.h = h

        # Grundhastighet / nuvarande hastighet
        self.speed = speed
        self.base_speed = speed

        # Rita alla bubblor i lista
        self.bubble_list = arcade.ShapeElementList()
        #self.bubble_list.append(arcade.create_rectangle_outline((self.w/2), (self.h/2), self.w, self.h, (random.randrange(255),random.randrange(255),random.randrange(255)), border_width * 2))
        for b in range(0, amount):
            radius = random.randrange(1, size)
            self.bubble_list.append(arcade.create_ellipse_outline(random.randrange(w), random.randrange(h), radius, radius, color, border_width))

        # Kalla direkt på objektet för att rita listan
        self.draw = self.bubble_list.draw

        # Flytta ner karta en liten bit under skärmen
        self.move_below_screen(2)
        
    # Flytta ner random distans under skärmen och ändra till ny hastighet
    def move_below_screen(self, depth=1):
        self.bubble_list.center_y = 0 - (random.randrange(self.h, depth * self.h + 1))
        self.speed = random.randrange(self.base_speed * 0.5, self.base_speed * 1.5)
        
    # Flyt uppåt och flytta ner vid behov
    def update(self, dt):
        self.bubble_list.center_y += self.speed * dt
        if (self.bubble_list.center_y > self.h - 50):
            self.move_below_screen()
