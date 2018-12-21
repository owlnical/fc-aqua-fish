"""
Aqua Fish

A game by furniture corporation

https://github.com/owlnical/fc-aqua-fish
"""
import arcade, random, types
from movefunctions import *
from classes.state import State
from classes.button import Button

VERSION = 0.2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SPRITE_SCALING_PFISH = 0.1
PFISH_NUMBER = 5

# Test att ändra två filer samtidigt

class MyGame(arcade.Window, State):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        # BLUE_SAPPHIRE eller BLUE_YONDER, båda är rätt snygga
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # If you have sprite lists, you should create them here,
        # and set them to None

        self.pfish_list = None                  # Skapa en lista där lila fiskar kommer simma
        self.button_list = None                 # (Jag fattar inte varför den måste in här)

        #self.player_list = None

    def setup(self):
        # Create your sprites and sprite lists here

        self.pfish_list = arcade.SpriteList()   # Listan blir en arcadelista
        # Loop som skapar "PFISH_NUMBER" många lila fiskar
        for i in range(PFISH_NUMBER):
            pfish = PfishSprite()
            self.pfish_list.append(pfish)           # Lägg till fiskarna i fisklistan

        # Skapa en lista på knappar
        self.button_list = []
        self.button_list.append(Button(30, 585, 50, 20, "Exit", 11, arcade.window_commands.close_window))
        self.button_list.append(Button(115, 585, 100, 20, "New Game", 11, self.setup))
        self.button_list.append(Button(225, 585, 100, 20, "Do it!", 11, self.do_it))

        # Setup klar
        self.state = "playing"

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        self.pfish_list.draw()

        # Rita alla knappar
        if self.is_paused():
            for button in self.button_list:
                    button.draw()

        # Call draw() on all your sprite lists below

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.is_playing():
            self.pfish_list.update()
            pfishbehaviour(self.pfish_list,SCREEN_WIDTH,SCREEN_HEIGHT)

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

        # key är en int
        # Se: http://arcade.academy/arcade.key.html
    def on_key_release(self, key, key_modifiers):
        # Avsluta AL
        if (key == arcade.key.Q):
            arcade.window_commands.close_window()
        # Starta om
        elif (key == arcade.key.R):
            self.setup()
        elif (key == arcade.key.ESCAPE):
            self.toggle_pause()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Kolla om vi klickat på någon knapp
        if self.is_paused():
            for b in self.button_list:
                if b.is_mouse_on_buttom(x, y):
                    b.click()

    def do_it(self):
        global PFISH_NUMBER
        PFISH_NUMBER = PFISH_NUMBER * 50
        self.setup()

# Klass för lila fiskar (Purple_fish)
class PfishSprite(arcade.Sprite):
    def __init__(self):
        # Anropa Sprite konstruktor
        super().__init__()

        # texture för höger och vänster
        self.texture_left1 = arcade.load_texture("images/purple_fish1.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_left2 = arcade.load_texture("images/purple_fish2.png", mirrored=True, scale=SPRITE_SCALING_PFISH)
        self.texture_right1 = arcade.load_texture("images/purple_fish1.png", scale=SPRITE_SCALING_PFISH)
        self.texture_right2 = arcade.load_texture("images/purple_fish2.png", scale=SPRITE_SCALING_PFISH)
        # Default = right
        self.texture = self.texture_right1
        self.ani_left = 0       # variabler som styr animeringen
        self.ani_left_add = 0
        self.ani_right = 0
        self.ani_right_add = 0

        # Placera ut fiskarna
        self.center_x = random.randrange(SCREEN_WIDTH * 0.8) + SCREEN_WIDTH * 0.1
        self.center_y = random.randrange(SCREEN_HEIGHT * 0.8) + SCREEN_HEIGHT * 0.1
        # Starthastihet
        self.change_x = 0  # x_hastighet
        self.change_y = 0  # y_hastighet
        self.pathcounter = random.random() * 200        # Variable som styr hur länge de gör saker
        self.relaxed = [True, True]                     # Pfish blir nervös nära kanter

def main():
    print("Starting Aqua Fish v", VERSION, sep="")
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
