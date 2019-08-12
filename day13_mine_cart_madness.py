"""
Advent of code, 2018
Day 13: Mine Cart Madness
"""

from typing import List, Dict, Tuple


# Possible cart symbols (at specific location, indicating the direction of the cart)
CART_SYMBOLS = {"<", ">", "^", "v"}  # left, right, up, down

# Dict to get the where the cart will turn at the next crossroads (cycles left-ahead-right)
NEXT_TURN_MAP = {"left": "ahead", "ahead": "right", "right": "left"}

# Dict. Given current cart direction, turn direction at the crossroads  --> new cart direction after the crossroads
XROADS_TURNS = {("<", "left"): "v", (">", "left"): "^", ("^", "left"): "<", ("v", "left"): ">",
                ("<", "ahead"): "<", (">", "ahead"): ">", ("^", "ahead"): "^", ("v", "ahead"): "v",
                ("<", "right"): "^", (">", "right"): "v", ("^", "right"): ">", ("v", "right"): "<"}

# Dict. Given current cart direction and type of curve --> new cart direction
NEW_DIR_AFTER_CURVE = {("<", "/"): "v", ("<", "\\"): "^",
                        (">", "/"): "^", (">", "\\"): "v",
                        ("^", "/"): ">", ("^", "\\"): "<",
                        ("v", "/"): "<", ("v", "\\"): ">"}

# Dict giving the coordinate delta (delta_x, delta_y) based on the direction the cart is going
DIRECTION_TO_COORD_DELTA_MAP = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v":(0, 1)}   # direction x, y

# Part A:
# After following their respective paths for a while, the carts eventually crash. 
# To help prevent crashes, you'd like to know the location of the first crash. 
# Locations are given in X,Y coordinates, where the furthest left column is X=0 and the furthest top row is Y=0


class Cart():
    def __init__(self, id: int, x: int, y: int, direction: str, next_turn: str = "left"):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = next_turn
        
    def step(self):
        self.x, self.y = self.get_next_coords()
          
    def get_next_coords(self):
        delta_x, delta_y = DIRECTION_TO_COORD_DELTA_MAP[self.direction]
        new_x, new_y = self.x + delta_x, self.y + delta_y
        
        return (new_x, new_y)
      


class CartTrack():
    def __init__(self, track: Dict[Tuple[int, int], str,], carts: List[Cart]):
        self.tick = 0
        self.track = track  # dict giving the track. (x,y) as key, track character as value
        self.carts = carts  # list of carts
        self.cart_pos = {(cart.x, cart.y) for cart in carts}
        print(f"Started with {len(self.carts)} carts")
        
        
    def print_track_only(self, x_max: int = 150, y_max: int = 150):
        """
        just for debug purposes. Print out the parsed track (with the carts replaced by the track pieces under them)
        """
        for y in range(y_max):
            line = ""
            for x in range(x_max):
                line += self.track.get((x,y), " ")
            print(line)
        
        
    def step(self, num_ticks: int = 1):
        """
        Update num_ticks steps of the simulation. 
        Used to step until the first crash (part A). Does not remove and handle destroyed carts
        """
        for _ in range(num_ticks):
            self.tick += 1
            print("tick:", self.tick)
            
            # determine the order to move
            self.carts.sort(key = lambda cart: (cart.y, cart.x)) 
            
            # move carts
            for cart in self.carts:
                self.cart_pos.remove((cart.x, cart.y))
                cart.step()
                
                # did I collide?
                if (cart.x, cart.y) in self.cart_pos:
                    print("COLLISION at:", (cart.x, cart.y), "tick:", self.tick)
                    return True
                else:  # update cart location set
                    self.cart_pos.add((cart.x, cart.y))
                    
                # update direction etc
                trackpart = self.track[(cart.x, cart.y)]
                
                if trackpart == "+":  # crossroads
                    cart.direction = XROADS_TURNS[(cart.direction, cart.next_turn)]
                    cart.next_turn = NEXT_TURN_MAP[cart.next_turn]
                    
                elif trackpart in ("/", "\\"):  ## curves... escape backslashes...
                    cart.direction = NEW_DIR_AFTER_CURVE[(cart.direction, trackpart)]       
                
                #else:  # nothing to do
                
                
    def step_until_one_cart(self):
        """
        Update one tick of the cart simulation
        Used to step until there are just one cart remaining (part B). Does remove and handle destroyed carts
        """
        num_ticks = 1
        for _ in range(num_ticks):
            ids_destroyed = set()  # cart ids for the destroyed carts
            self.tick += 1
            
            if self.tick % 100 == 0:
                print("tick:", self.tick)
            
            
            # determine the order to move
            self.carts.sort(key = lambda cart: (cart.y, cart.x))  # ascending
            
            # move
            for cart in self.carts:
                if cart.id in ids_destroyed:
                    continue  # to next cart
                self.cart_pos.remove((cart.x, cart.y))  # kept for the "collided_to" carts -> further cols during the same tick are accounted for
                cart.step()
                             
                # did I collide?
                if (cart.x, cart.y) in self.cart_pos:
                    print("COLLISION at:", (cart.x, cart.y), "tick:", self.tick)
                    # remove both carts
                    for cart_b in self.carts:
                        if cart_b.x == cart.x and cart_b.y == cart.y:  # collided
                            ids_destroyed.add(cart_b.id)
                    continue  # to the next cart
                    
                else:  # update cart location set
                    self.cart_pos.add((cart.x, cart.y))
                    
                # update direction etc
                trackpart = self.track[(cart.x, cart.y)]
                
                if trackpart == "+":  # crossroads
                    cart.direction = XROADS_TURNS[(cart.direction, cart.next_turn)]
                    cart.next_turn = NEXT_TURN_MAP[cart.next_turn]
                    
                elif trackpart in ("/", "\\"):  ## curves... backslashes...
                    cart.direction = NEW_DIR_AFTER_CURVE[(cart.direction, trackpart)]       
                
                #else:  # nothing to do
            
            # end of tick:
            
            # Rebuild carts list and the cart positions set (without the destroyed ones)
            self.carts = [cart for cart in self.carts if cart.id not in ids_destroyed]
            self.cart_pos = {(cart.x, cart.y) for cart in self.carts}
            if len(ids_destroyed) > 0:
                print(f"After cart destruction, there are {len(self.carts)} carts left!")
            
            if len(self.carts) == 1:
                print("Only on cart remains! Location:", self.carts[0].x, self.carts[0].y)
                return True

       
    @staticmethod
    def parse_from_input(input: str) -> 'CartTrack':
        """
        given the input string (without splitting it in any way), get the CartTrack object
        """
        lines = input.split("\n")

        num_carts = 0
        carts = []
        track = {}
        
        for y, line in enumerate(lines):
            for x, elem in enumerate(line):
                if elem.isspace():  # no track, no cart
                    continue
                elif elem in CART_SYMBOLS:  # track and cart
                    # get the cart
                    carts.append(Cart(id=num_carts, x=x, y=y, direction=elem))
                    num_carts += 1
                    
                    # get the underlying piece of track
                    trackpart = "|" if elem in ("^", "v") else "-"
                    track[(x,y)] = trackpart
                    
                else:  # just piece of track
                    track[(x,y)] = elem
    
        return CartTrack(track, carts)


# Get the input data
with open ("data/day13.txt") as f:
    input = f.read()  # .split("\n")
 

ct = CartTrack.parse_from_input(input)
#ct.print_track_only()
#ct.step()

while True:
    collision = ct.step()
    if collision:
        break
# 100,21 is the right answer



#########################
# PART B
# What is the location of the last cart at the end of the first tick where it is the only cart left?
ct_b = CartTrack.parse_from_input(input)

while True:
    one_remains = ct_b.step_until_one_cart()
    if one_remains:
        break
# 113,109 is the right answer
