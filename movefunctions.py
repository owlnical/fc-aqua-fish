
import arcade,random

# Rörelsemönster för pfish
def pfishbehaviour(list,sw,sh):
    # Stega igenom alla fiskar
    for fish in list:
        # De blir lugna av att befinna sig i mitter av akvariet
        if 0.10*sw < fish.center_x < 0.90*sw:
            fish.relaxed[0] = True
        if 0.10*sh < fish.center_y< 0.90*sh:
            fish.relaxed[1] = True

        if fish.relaxed == [True,True]:
            # Om de är lugna så rör de sig normalt
            if fish.pathcounter > 200:
                fish.change_x = random.random() * 2 - 1
                fish.change_y = random.random() * 2 - 1
                fish.pathcounter = random.random()*50
            # Slumpfaktor som gör att de stannar upp och funderar
            if random.random() < 0.001:
                fish.change_x = 0
                fish.change_y = 0
                fish.pathcounter = 0
        # Alla dessa if kollar kanter, styr in dem mot mitten och stressar upp dem
        if fish.center_x > sw * 0.95:
            fish.change_x = -2
            fish.pathcounter = 100
            fish.relaxed[0] = False
        if fish.center_x < sw * 0.05:
            fish.change_x = 2
            fish.pathcounter = 100
            fish.relaxed[0] = False
        if fish.center_y > sh * 0.95:
            fish.change_y = -2
            fish.pathcounter = 100
            fish.relaxed[1] = False
        if fish.center_y < sh * 0.05:
            fish.change_y = 2
            fish.pathcounter = 100
            fish.relaxed[1] = False
        # Stega upp variabeln som styr hur länge de gör saker
        fish.pathcounter += 1
