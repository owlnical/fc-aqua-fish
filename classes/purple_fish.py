
import arcade, random, math
from classes.fish import FishSprite
from vars import SCREEN_WIDTH, SCREEN_HEIGHT
from fish_vars import SPRITE_SCALING_PFISH, pfish_eager, pfish_hungry, pfish_daydream, pfish_finforce, pfish_mass, pfish_size, pfish_findelay

# Klass för lila fiskar (Purple_fish)
class PfishSprite(FishSprite):
    def __init__(self, carrot_list, pfish_list, eager=None, hungry=None, daydream=None, finforce=None, size=None, mass=None,
                 color=None, setpos_x=None, setpos_y=None, setspeed_y=None):
        # Anropa Sprite konstruktor
        super().__init__()

        # Fiskarnas personlighet
        self.eager = eager or pfish_eager                # Hur ofta byter fiskarna riktning
        self.hungry = hungry or pfish_hungry              # Hur intresserade är de av mat
        self.base_hungry = self.hungry
        self.daydream = daydream or pfish_daydream

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or pfish_finforce
        self.size = size or pfish_size
        self.mass = mass or pfish_mass
        self.color = color or "purple"
        self.type = "pfish"
        self.pfish_list = pfish_list

        self.findelay = pfish_findelay          # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 8                      # Denna variabel styr hur intensivt de äter

        self.relaxed = [True, True]             # Pfish blir nervös nära kanter
        self.frame_count = 0

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT
        self.food_objects = carrot_list

        # texture 1 & 2 för höger och vänster
        scale_factor = SPRITE_SCALING_PFISH*self.size/8
        self.texture_left1 = arcade.load_texture(f"images/{self.color}_fish1.png", mirrored=True, scale=scale_factor)
        self.texture_left2 = arcade.load_texture(f"images/{self.color}_fish2.png", mirrored=True, scale=scale_factor)
        self.texture_left8 = arcade.load_texture(f"images/{self.color}_fish_eat.png", mirrored=True, scale=scale_factor)
        self.texture_right1 = arcade.load_texture(f"images/{self.color}_fish1.png", scale=scale_factor)
        self.texture_right2 = arcade.load_texture(f"images/{self.color}_fish2.png", scale=scale_factor)
        self.texture_right8 = arcade.load_texture(f"images/{self.color}_fish_eat.png", scale=scale_factor)

        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.texture = self.texture_left1
            self.whichtexture = 11              # 11 = left1
        else:
            self.texture = self.texture_right1
            self.whichtexture = 21              # 21 = right1

        # Placera ut fiskarna
        self.center_x = setpos_x or random.randrange(int(self.sw * 0.8)) + int(self.sw * 0.1)
        self.center_y = setpos_y or random.randrange(int(self.sh * 0.8)) + int(self.sh * 0.1)
        self.change_y = setspeed_y or 0

    def update(self):

        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * self.sw < self.center_x < 0.85 * self.sw:
            self.relaxed[0] = True
        if 0.15 * self.sh < self.center_y < 0.85 * self.sh:
            self.relaxed[1] = True

        # Om de är lugna kan de vilja ändra riktning
        if self.relaxed == [True, True] and random.randrange(1000) < self.eager and not self.partner and self.isalive:
            self.random_move()

        # Om de är lugna och kan de vilja jaga mat
        if self.relaxed == [True, True] and random.randrange(1000) < self.hungry and not self.partner and self.isalive:
            self.chase_food()

        if self.relaxed == [True, True] and self.health > self.base_health and random.randrange(1000) < 10 and not self.partner and self.isalive:
            self.kiss_spirit = 1000

        if self.kiss_spirit > 0:
            self.find_partner(self.pfish_list)
            self.kiss_spirit -= 1

        if self.partner:
            self.move_to_partner_kiss(self.partner)

        # Om de är lugna kan de börja dagdrömma
        if self.relaxed == [True, True] and random.randrange(1000) < self.daydream and not self.partner and self.isalive:
            self.acc_x = 0
            self.acc_y = 0

        if self.health <= 0:
            self.die()

        # Kolla om fisken är nära kansten och styr in den mot mitten
        # Stressa även upp den
        self.check_edge()

        # Beräkna vattnets motstånd
        self.water_res()

        # Gör beräkningar för acceleration
        self.move_calc()

        # Gör beräkningar för hälsa
        self.health_calc()

        # Updatera animationen
        if self.isalive:
            self.animate()

        # Anropa huvudklassen
        super().update()


