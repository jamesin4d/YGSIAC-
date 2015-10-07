# Created by a human
# when:
#8/22/2015
#6:19 AM
#
#
#--------------------------------------------------------------------
from entities import *
from projectiles import *

# ---------------------------------------------------------------------------------------------------
# so the idea here is: subclass the Base class so that we have an
# Enemy type, then use the Enemy class as a parent to the different types
# of enemy. the parent enemy class will have a 'behavioural tree' of methods
# for the child class to inherit from, deciding what to do based on state
# ------------------------------------------------------------------------
class Enemy(Base):
    aggressive = False
    aggression = 0

    alerted = False
    alerts = 0

    scared = False
    fear = 0

    idle = False
    boredom = 0

    target_in_range = False
    target_x_range = False
    target_y_range = False
    horizontal_speed = 0
    vertical_speed = 0

    target = None
    barriers = None
    state = None
    dx = ()
    dy = ()
    boundsL = None
    boundsR = None
    damage = 0
    has_hit_player = False
    hit_timer = 0
    bullets = []
    walk_speed = 0


    def __init__(self, x, y , left, right):
        Base.__init__(self)
        self.boundsL = left
        self.boundsR = right
        self.set_position((x,y))
        self.aware = False # just in case....


    def check_target(self):
        self.target_x_range = False
        self.target_y_range = False
        self.aim(self.target)
        target_position = self.target.get_position()
        position = self.get_position()
        tp = target_position
        sp = position
        dx = tp[0] - sp[0]
        dy = tp[1] - sp[1]
        diff = (dx, dy)
        self.dx = dx
        self.dy = dy
        if 150 > diff[0] > -150:
            self.target_x_range = True
        if 48 > diff[1] > -48:
            self.target_y_range = True
        if self.target_x_range and self.target_y_range:
            self.target_in_range = True
        else: self.target_in_range = False

        contact = pygame.sprite.collide_rect(self, self.target)
        if contact:
            if self.target.attacking:
                self.has_hit_player = True
                if self.target.melee:
                    self.take_damage(self.target.melee_damage)
            elif not self.target.attacking:
                if self.hit_timer == 0:
                    self.has_hit_player = True
                    self.target.take_damage(self.damage)
        if self.has_hit_player:
            self.hit_timer += 1
            if self.hit_timer >= 20:
                self.has_hit_player = False
                self.hit_timer = 0
        return diff




    def get_started(self):
        if self.xvelocity == 0:
            self.xvelocity += 2
            if self.xvelocity > self.walk_speed:
                self.xvelocity = self.walk_speed

    def roam(self):
        if self.rect.x >= self.boundsR:
            self.walk_left()
        if self.rect.x <= self.boundsL:
            self.walk_right()
        if self.collide_right or self.collide_left:
            self.jump(-7)





class Rat(Enemy):
    def __init__(self, x, y , left, right):
        self.rat_frames()
        self.walking_frames_left = []
        self.walking_frames_right = []
        Enemy.__init__(self, x, y , left, right)
        self.health = random.randint(3,6)
        self.max_health = 6.0
        self.walk_speed = 2
        self.damage = 1
        self.gravity = 1
        self.get_started()

    def rat_frames(self):
        rat_left = SpriteSheet.strip_sheet('img/enemies/rat/ratLeft.png',128,32,32,32)
        rat_right = SpriteSheet.strip_sheet('img/enemies/rat/ratRight.png',128,32,32,32)
        self.walking_frames_left = rat_left
        self.walking_frames_right = rat_right
        self.image = self.walking_frames_right[0]
        self.rect = pygame.Rect((0,0,32,32))

    def animate(self):
        if self.direction == "left":
            frame = (self.rect.x//15) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        if self.direction == "right":
            frame = (self.rect.x//15) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]


    def update(self, objects):
        self.move_and_check(objects)
        self.animate()
        self.check_target()
        self.roam()

class Bat(Enemy):
    def __init__(self, x, y , left, right):
        self.walking_frames_left = []
        self.walking_frames_right = []
        self.bat_frames()
        Enemy.__init__(self, x, y , left, right)
        self.health = random.randint(3,6)
        self.max_health = 6.0
        self.walk_speed = 4
        self.damage = 1
        self.gravity = 0
        self.get_started()

    def bat_frames(self):
        bat_left = SpriteSheet.strip_sheet('img/enemies/bat/bat.png',112,20,28,20)
        bat_right = SpriteSheet.strip_sheet('img/enemies/bat/bat.png',112,20,28,20)
        self.walking_frames_left = bat_left
        self.walking_frames_right = bat_right
        self.image = self.walking_frames_right[0]
        self.rect = pygame.Rect((0,0,32,32))

    def animate(self):
        if self.direction == "left":
            frame = (self.rect.x//15) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        if self.direction == "right":
            frame = (self.rect.x//15) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]


    def update(self, objects):
        self.move_and_check(objects)
        self.animate()
        self.check_target()
        self.roam()









