# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
SCREEN_SIZE = (800,600)
WIDTH, HEIGHT = SCREEN_SIZE[0], SCREEN_SIZE[1]
score = 0
lives = 3
time = 0
started = False
is_shooting = False

missile_group = set()
rock_group = set()
explosion_group = set()

SHIP_ACC = 15
SHIP_ANGLE_V = math.pi
FRICTION = 0.98
MISSILE_SPEED = 5
ROCK_V = 5


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 80)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.8)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


class Sprite:
    def __init__(self, pos, vel, angle, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = angle
        self.angle_v = ang_vel
        self.image = image
        self.image_center = [info.get_center()[0], info.get_center()[1]]
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()        
        self.age = info.lifespan        
        self.disappear = False
        self.animated = info.animated
        if sound:
            sound.rewind()
            sound.play()
   
    def collide(self, other_obj):
        juli = dist(self.pos, other_obj.pos)
        r_he = self.radius + other_obj.radius 
        if juli < r_he :
            if not self.disappear :
                self.disappear = True   
                return True
        
    def draw(self, canvas):        
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        if self.animated :
            self.image_center[0] += self.image_size[0]
        self.angle += self.angle_v
        self.pos = [(self.vel[n] + self.pos[n])%SCREEN_SIZE[n] for n in range(2)] 
        self.age -= 1
        if self.age < 0 :
            self.disappear = True
        

class Ship(Sprite):
    def __init__(self, pos, vel, angle, image, info):
        Sprite.__init__(self, pos, vel, angle, 0, image, info)              
        self.acc = 0     
        self.Vector = angle_to_vector(self.angle)
        
    def set_angle_v(self, v):
        self.angle_v = v
    
    def set_acc(self, thrust):
        self.acc = thrust*SHIP_ACC/60.
        if thrust:
            ship_thrust_sound.play()
            self.image_center = [self.image_center[0] + self.image_size[0], self.image_center[1]]
        else :
            ship_thrust_sound.rewind()
            self.image_center = [self.image_center[0] - self.image_size[0], self.image_center[1]]
    
    def shoot(self):        
        missile_pos = [(self.Vector[n]*self.radius + self.pos[n])%SCREEN_SIZE[n] for n in range(2)]
        missile_vel = [self.vel[n] + self.Vector[n]*MISSILE_SPEED for n in range(2)]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
                    
    def update(self):
        Sprite.update(self)
        self.Vector = angle_to_vector(self.angle)
        self.vel = [self.vel[n]*FRICTION + self.Vector[n]*self.acc for n in range(2)]
        

    
def rock_spawner():    
    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    hard = score / 15.
    vel = [(random.random()*.6 - .3 +hard) * random.choice([1,-1]), 
           (random.random()*.6 - .3 +hard) * random.choice([1,-1])]
    ang = random.randrange(-round(math.pi,2)*100, round(math.pi,2)*100) / 100.    
    ang_vel = random.randrange(-ROCK_V, ROCK_V)/60.
    
    juli = dist(pos, my_ship.pos)
    safe_r = asteroid_info.get_radius() + my_ship.radius + 50
    if juli > safe_r :
        a_rock = Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
      
def missile_spawner(switch):    
    global missile_time, is_shooting 
    if switch :
        missile_time = time
        is_shooting = True        
    else :
        is_shooting = False
        
def make_boom(pos) :          
    explosion = Sprite(pos, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
    explosion_group.add(explosion)
    
def group_collide(one, group, is_ship = False):  
    global score, lives, started, rock_group
    for other in group :
        boom = other.collide(one)
        if boom :
            score += 1
            make_boom(other.pos)
            one.disappear = True
            if is_ship :
                lives -= 1
                make_boom(one.pos)
                if lives <= 0 :
                    started = False
                    rock_group = set()
                    return
        
def process_sprite_group(canvas, group):
    "update and draw obj"
    removes = set()
    for obj in group :
        obj.draw(canvas)    
        obj.update()    
        if obj.disappear :
            removes.add(obj)
    group.difference_update(removes)
        
    
def key_down(key):     
    right_key = key_auto.get(key)
    if right_key :
        right_key[0](right_key[1])        
def key_up(key): 
    right_key = key_auto.get(key)
    if right_key :
        right_key[0](0)
        
def click(pos):
    global started, lives, score    
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True  
        lives = 3
        score = 0
        soundtrack.rewind()
        soundtrack.play()
    
def draw(canvas):
    global time, started, rock_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    my_ship.draw(canvas)
    my_ship.update()     
    
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)        
    process_sprite_group(canvas, explosion_group)
    
   
    # draw text
    canvas.draw_text('score: ' + str(score), (SCREEN_SIZE[0] - 95, 30), 20, 'white')
    canvas.draw_text('life: ' + str(lives), (20, 30), 20, 'white')
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    else :
        # shoot and get new rock
        if len(rock_group) < 12 :       
            if time%50 == 0 :
                rock_spawner()
        if is_shooting :
            if (time - missile_time) % 5 == 0 :
                my_ship.shoot()    
                
        # update sprites
        for missile in missile_group :
            group_collide(missile, rock_group)
        group_collide(my_ship, rock_group, is_ship = True)
        
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

key_auto = {simplegui.KEY_MAP['left']:[my_ship.set_angle_v, -SHIP_ANGLE_V/60.], 
            simplegui.KEY_MAP['right']:[my_ship.set_angle_v, SHIP_ANGLE_V/60.], 
            simplegui.KEY_MAP['up']:[my_ship.set_acc, True], 
            simplegui.KEY_MAP['space']:[missile_spawner, True]}


# register handlers
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
soundtrack.play()
