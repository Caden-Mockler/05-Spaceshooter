import sys, logging, os, random, math, arcade, open_color

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 20
SCREEN_TITLE = "Invasion"

NUM_ENEMIES = 8
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
BULLET_SPEED = 1
ENEMY_HP = 10
HIT_SCORE = 10
KILL_SCORE = 100
Initial_Velocity = 5



class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/laserRed.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy


    
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION
       
class Enemy(arcade.Sprite):
    def __init__(self, position, velocity):
        super().__init__("assets/enemyShip.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x,self.center_y) = position
        (self.dx, self.dy) = velocity
      

        


class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        

    def setup(self):
        
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            dx = random.uniform(-Initial_Velocity, Initial_Velocity)
            dy = random.uniform(-Initial_Velocity, Initial_Velocity)
            enemy = Enemy((x,y), (dx,dy))
            self.enemy_list.append(enemy)    
      

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:
            missle = arcade.check_for_collision_with_list(e,self.bullet_list)
            for b in missle:
                e.hp = e.hp - b.damage
                b.kill()
                if e.hp <=0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE

        self.enemy_list.update()
        for e in self.enemy_list:
            e.center_x = e.center_x + e.dx
            e.center_y = e.center_x + e.dy
            if e.center_x <= 200:
                e.dx = abs(e.dx)
            if e.center_x >= SCREEN_WIDTH:
                e.draw_text = abs(e.dx) * 1
            if e.center_y <= 200:
                e.dy = abs(e.dy)
            if e.center_y >= SCREEN_HEIGHT:
                e.draw_text = abs(e.dy) * 1

                    

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
  
          

    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
             x = self.player.center_x
             y = self.player.center_y + 15
             bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
             self.bullet_list.append(bullet)
             
            #fire a bullet
            #the pass statement is a placeholder. Remove line 97 when you add your code
             pass

def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()