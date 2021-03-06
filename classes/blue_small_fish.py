
import arcade, random, math
from classes.fish import FishSprite
from fish_vars import SPRITE_SCALING_BFISH, bfish_eager, bfish_hungry, bfish_conformity, bfish_daydream, bfish_kiss_will, bfish_finforce, bfish_mass, bfish_size, bfish_findelay

# Klass för små blå fiskar (blue_fish)
class BfishSprite(FishSprite):
    def __init__(self, textures_bfish, textures_bfish_kid, carrot_list, blueberry_list, popcorn_list, bfish_list, hunter_list, eager=None, hungry=None, conformity=None, daydream=None, finforce=None,
                 size=None, mass=None, color=None, setpos_x=None, setpos_y=None, setspeed_y=None):
        # Anropa Sprite konstruktor
        super().__init__()

        # Fiskarnas personlighet
        self.eager = eager or bfish_eager           # Hur ofta byter fiskarna riktning
        self.hungry = hungry or bfish_hungry        # Hur intresserade är de av mat
        self.base_hungry = self.hungry
        self.conformity = conformity or bfish_conformity
        self.daydream = daydream or bfish_daydream
        self.kiss_will = bfish_kiss_will

        # Fiskarnas fysiska egenskaper
        self.finforce = finforce or bfish_finforce
        self.size = size or bfish_size
        self.base_size = bfish_size
        self.scaling = SPRITE_SCALING_BFISH
        self.mass = mass or bfish_mass
        self.fish_color = color or "blue"
        self.type = "bfish"

        self.findelay = bfish_findelay  # Hur ofta viftar de med fenorna
        self.findelay_base = self.findelay
        self.eat_speed = 5

        self.food_objects_c = carrot_list
        self.food_objects_b = blueberry_list
        self.food_objects_p = popcorn_list
        self.food_objects = self.food_objects_b
        self.bfish_list = bfish_list
        self.hunter_fish_list = hunter_list

        # Ladda in texturer
        self.textures_grown = textures_bfish
        self.textures_kid = textures_bfish_kid
        if self.size < self.base_size:
            self.textures = self.textures_kid
        else:
            self.textures = self.textures_grown
        # Slumpa fiskarna höger/vänster
        if random.random() > 0.5:
            self.set_texture(0)
            self.whichtexture = 11  # 11 = left1
        else:
            self.set_texture(2)
            self.whichtexture = 21  # 21 = right1

        # Placera ut fiskarna
        self.center_x = setpos_x or random.randrange(int(self.sw * 0.7)) + int(self.sw * 0.1)
        self.center_y = setpos_y or random.randrange(int(self.sh * 0.7)) + int(self.sh * 0.1)
        self.change_y = setspeed_y or 0

    def update(self):

        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.15 * self.sw < self.center_x < 0.85 * self.sw:
            self.relaxed[0] = True
        if 0.15 * self.sh < self.center_y < 0.85 * self.sh:
            self.relaxed[1] = True

        # Kolla om de är vuxna
        if self.size < self.base_size:
            self.grown_up = False
        else:
            self.grown_up = True

        # Håll koll ifall fisken störs av någonting
        if not self.isalive or not self.relaxed == [True, True] or self.pregnant or self.partner or self.is_hooked:
            self.disturbed = True
        else:
            self.disturbed = False

        # Om de är lugna kan de vilja ändra riktning
        if random.randrange(1000) < self.eager and not self.disturbed:
            self.random_move()

        # Om de inte är störda kommer de att vilja simma i stim
        if random.randrange(1000) < self.conformity and not self.disturbed:
            self.shoal_move()

        # Om de inte är störda kan de vilja jaga morötter
        if random.randrange(1000) < self.hungry and not self.disturbed:
            self.food_objects = self.food_objects_c
            self.chase_food()

        # Men de prioriterar blåbär
        if random.randrange(1000) < self.hungry and not self.disturbed:
            self.food_objects = self.food_objects_p
            self.chase_food()

        # Men de prioriterar blåbär
        if random.randrange(1000) < self.hungry and not self.disturbed:
            self.food_objects = self.food_objects_b
            self.chase_food()

        # ifall fisken är mätt och pilsk och inte störd kan den bli sugen att pussas
        if self.health > self.base_health and random.randrange(1000) < self.kiss_will and not self.disturbed and self.grown_up:
            self.kiss_spirit = 1000

        # Om de är sugna att pussas och inte störda letar de efter en partner
        if self.kiss_spirit > 0 and not self.disturbed and self.iseating == 0:
            self.find_partner(self.bfish_list)

        # De tröttnas ifall de inte hittar någon
        if self.kiss_spirit > 0:
            self.kiss_spirit -= 1

        # Finns det en partner och fisken lever så flyttar den sig mot den
        if self.partner and self.isalive:
            self.move_to_partner_kiss(self.partner)

        # om fisken är gravid så flyttar den sig mot en bra plats att lägga äggen på
        if self.pregnant and self.isalive:
            self.move_lay_egg_position()

        # Om de är lugna kan de börja dagdrömma
        if random.randrange(1000) < self.daydream and not self.disturbed:
            self.acc_x = 0
            self.acc_y = 0

        self.flee_from_close_fish()

        if self.size < self.base_size:
            self.check_grow_up()

        if self.health <= 0:
            self.die()

        # Ta bort döda fisken som flutit upp
        if self.bottom > self.sh and self.health <= 0:
            self.kill()

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
        if self.isalive and self.iseating == 0 and not self.is_hooked:
            if self.partner:
                self.animate_love()
            else:
                self.animate()

        # Anropa huvudklassen
        super().update()
