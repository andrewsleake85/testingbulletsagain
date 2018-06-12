import random
import math
import sys
import pygame as pg

BLACK = (0, 0, 0)
PI = math.pi
pg.init()


DEFAULTFONT = pg.font.SysFont("Arial", 15)


BG_COLOR = pg.Color('gray12')
ENEMY_IMG = pg.Surface((50, 30))
ENEMY_IMG.fill(pg.Color('white'))
BULLET_IMG = pg.Surface((9, 15))
BULLET_IMG.fill(pg.Color('aquamarine2'))
HERO_IMG = pg.Surface((75, 50))
HERO_IMG.fill(pg.Color('blue2'))



class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, shooter, *sprite_groups):
        super().__init__(*sprite_groups)
        self.maxspeed = 450
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(center=pos)
        #set intial position to whatever we pass as pos
        self.pos = pg.math.Vector2(pos)

        #find intial bullet speed and direction
        x, y = pg.mouse.get_pos() - shooter.pos
        total_speed =  math.sqrt(x**2 + y**2)
        #set max speed based on contants
        if total_speed != self.maxspeed:
            div_factor =  math.sqrt(x**2 + y**2) / self.maxspeed
            new_x = int(x / div_factor)
            new_y = int(y / div_factor)
            self.vel = pg.math.Vector2(new_x,new_y)

        #lets adjust the surface so it goes the right direction
        # verticals are already given
        # horizontal rotates are easy here


        if abs(new_x) < abs(self.maxspeed *.80) and abs(new_x) > abs(self.maxspeed *.20):
            self.image = pg.transform.rotozoom(self.image, -45, .8)
            print("x less than 80 and more than 20")
            if (x < 0 and y < 0) or ( x > 0 and y > 0):
                self.image = BULLET_IMG
                self.image = pg.transform.rotozoom(self.image, -135, .8)


        elif abs(new_x) > abs(self.maxspeed * .80):
            self.image = pg.transform.rotate(self.image, -90)




        # adjust max speed given the shooters vector  at time of shooting with a modifier
        # the bullet inherits 1/5 of the shooters velocity in this case
        self.vel = pg.math.Vector2(new_x,new_y) + ( shooter.vel / 5)


        print(" x old speed : ", x , "y old speed : ", y, "total old speed", math.sqrt(x**2 + y**2))
        print(" x new speed : ", new_x, "y new speed : ", new_y, "total new speed", math.sqrt(new_x ** 2 + new_y ** 2))


        self.damage = 10

    def update(self, dt):
        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos  # Update the rect pos.

        if self.rect.bottom <= 0 or self.rect.bottom >= 1000 :
            self.kill()



class Heroes(pg.sprite.Sprite):

    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = HERO_IMG
        self.rect = self.image.get_rect(center=pos)
        self.health=100
        self.textSurf = DEFAULTFONT.render(str(self.health), 1, pg.Color('white'))
        self.pos = pg.math.Vector2(pos)
        self.vel = pg.math.Vector2(0, 0)
        self.shooting = False
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [HERO_IMG.get_width() / 2 - W / 2, HERO_IMG.get_height() / 2 - H / 2])

  # def fire_bullet(self, main_group, sub_group):
   #    Bullet(self.pos,main_group,sub_group)

    def update(self, dt):

        if self.health < 100:
            self.image.fill(pg.Color('blue2'))
            self.textSurf = DEFAULTFONT.render(str(self.health), 1, pg.Color('white'))
            W = self.textSurf.get_width()
            H = self.textSurf.get_height()
            self.image.blit(self.textSurf, [HERO_IMG.get_width() / 2 - W / 2, HERO_IMG.get_height() / 2 - H / 2])

        if self.health <= 0:
            self.kill()
            # if you die its gg, mostly for testing purposes
            pg.quit()
            sys.exit()

         # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel * dt
        self.rect.center = self.pos  # Update the rect pos.


class Enemy(pg.sprite.Sprite):



    def __init__(self, pos, spawn_health, *sprite_groups):
        super().__init__(*sprite_groups)
        self.image = pg.Surface((50, 30))
        self.image.fill(pg.Color('white'))
        self.rect = self.image.get_rect(center=pos)
        self.MAX_HEALTH = spawn_health
        self.health = spawn_health
        self.DEFAULTFONT = pg.font.SysFont("Arial", 15)
        self.textSurf = self.DEFAULTFONT.render(str(self.health), 1, BLACK)
        self.W = self.textSurf.get_width()
        self.H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [self.image.get_width() / 2 - self.W / 2, self.image.get_height() / 2 - self.H / 2])
        r = min(255, 255 - (255 * ((self.health - (self.MAX_HEALTH - self.health)) / self.MAX_HEALTH)))
        g = min(255, 255 * (self.health / (self.MAX_HEALTH / 2)))
        color = (r, g, 0)
        width = int(self.rect.width * self.health / self.MAX_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        pg.draw.rect(self.image, color, self.health_bar)


        self.damage = 10




    def update_health_bar_and_text(self):
        if self.health < self.MAX_HEALTH:
            textSurf = pg.Surface((self.W,self.H))
            textSurf = self.DEFAULTFONT.render(str(self.health), 1, BLACK)
            self.image.fill((pg.Color('white')))
            self.image.blit(textSurf, [self.image.get_width() / 2 - self.W / 2, self.image.get_height() / 2 - self.H / 2])
            if self.health >= 1 :
                r = min(255, 255 - (255 * ((self.health - (self.MAX_HEALTH - self.health)) / self.MAX_HEALTH)))
                g = min(255, 255 * (self.health / (self.MAX_HEALTH / 2)))
                color = (r, g, 0)
                width = int(self.rect.width * self.health / self.MAX_HEALTH)
                self.health_bar = pg.Rect(0, 0, width, 7)
                pg.draw.rect(self.image, color, self.health_bar)


    def update(self, dt):


        if self.health <= 0:

            self.kill()

        self.update_health_bar_and_text()


class ScoreBoard(pg.sprite.Sprite) :

    def __init__(self, pos, *sprite_groups):
        super().__init__(*sprite_groups)

        self.image = pg.Surface((60, 60))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect(center=pos)
        self.score = 0
        self.textSurf = DEFAULTFONT.render(str(self.score), 1, pg.Color('white'))
        self.W = self.textSurf.get_width()
        self.H = self.textSurf.get_height()
        self.image.blit(self.textSurf,[self.image.get_width() / 2 - self.W / 2, self.image.get_height() / 2 - self.H / 2])

    def increaseScore(self):

        self.score += 1


    def updateScore(self):
        textSurf = DEFAULTFONT.render(str(self.score), 1, pg.Color('white'))
        self.image.fill(BLACK)
        self.image.blit(textSurf, [self.image.get_width() / 2 - self.W / 2, self.image.get_height() / 2 - self.H / 2])

    def update(self, dt):

        self.updateScore()

class Game:


    def __init__(self):
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((800, 600))
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.heroes = pg.sprite.Group()
        self.hero1 = Heroes([400,400], self.all_sprites, self.heroes)
        self.score = ScoreBoard([50,550],self.all_sprites)





        #create i  enemies randomly placed with random health amount  -- Enemy(postion, health, groups)
        for i in range(15):
            pos = (random.randrange(30, 750), random.randrange(500))
            Enemy(pos,random.randrange(250,550), self.all_sprites, self.enemies)






        #how fast you take damage
        self.damage_timer = .2
        #how fast you can shoot
        self.bullet_timer = .05
        self.done = False

    def run(self):
        while not self.done:
            # dt = time since last tick in milliseconds.
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.run_logic(dt)
            self.draw(dt)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN:

                # Figure out if it was an movement key. If so
                # adjust speed.
                if event.key == pg.K_a:
                    self.hero1.vel+= pg.math.Vector2(-300, 0)
                elif event.key == pg.K_d:
                    self.hero1.vel += pg.math.Vector2(300,0 )
                elif event.key == pg.K_w:
                    self.hero1.vel += pg.math.Vector2(0, -300)
                elif event.key == pg.K_s:
                    self.hero1.vel += pg.math.Vector2(0, 300)
                elif event.key == pg.K_SPACE:

                    self.hero1.shooting = True


            elif event.type == pg.KEYUP:

                # if the user stopped pressing a direction, reduce that velocity
                if event.key == pg.K_a:
                    self.hero1.vel-= pg.math.Vector2(-300, 0)
                elif event.key == pg.K_d:
                    self.hero1.vel -= pg.math.Vector2(300,0 )
                elif event.key == pg.K_w:
                    self.hero1.vel -= pg.math.Vector2(0, -300)
                elif event.key == pg.K_s:
                    self.hero1.vel -= pg.math.Vector2(0, 300)
                elif event.key == pg.K_SPACE:
                    self.hero1.shooting = False




    def run_logic(self, dt):

        mouse_pressed = pg.mouse.get_pressed()

        self.bullet_timer -= dt  # Subtract the time since the last tick.
        self.damage_timer -= dt

        if self.bullet_timer <= 0:
            self.bullet_timer = 0  # Bullet ready.
            #if mouse_pressed[0]:  # Left mouse button.
            #    # Create a new bullet instance and add it to the groups.
            #    Bullet(pg.mouse.get_pos(), self.all_sprites, self.bullets)
            #    self.bullet_timer = .05  # Reset the timer.
            if self.hero1.shooting == True:
                Bullet(self.hero1.pos, self.hero1, self.all_sprites,self.bullets)
                self.bullet_timer= .05 # reset the timer

        # hits is a dict. The enemies are the keys and bullets the values.
        hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.health -= bullet.damage
                if enemy.health <= 0:
                    self.score.increaseScore()







        #if the hero collides with an enemy he also takes damage
        if self.damage_timer <= 0:
            self.damage_timer = 0 #Can take damage
            struck = pg.sprite.groupcollide(self.enemies, self.heroes, False, False)
            for enemy, hero_list in struck.items():
                for hero in hero_list:
                    hero.health -= enemy.damage
                    self.damage_timer = 1

        #counts the enemies and spawns more if there is less than 1

        while len(self.enemies) < 15:

            pos = (random.randrange(30, 750), random.randrange(500))
            Enemy(pos, random.randrange(300, 600), self.all_sprites, self.enemies)






    def draw(self, dt):

        self.all_sprites.update(dt)
        self.screen.fill(BG_COLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


if __name__ == '__main__':
    Game().run()
    pg.quit()
    sys.exit()


