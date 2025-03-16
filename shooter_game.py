#Create your own shooter
from random import randint
from pygame import *

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")


img_back = "6467671.jpg"
img_hero = "rocket.png"
img_bullet = "bullet.png"

score = 0
lost = 0
goal = 3
max_lost = 3

font.init()

font1 = font.SysFont('Arial', 80)
win = font1.render("YOU WIN!", True, (0,200,0))
lose = font1.render("YOU LOSE!", True, (200,0,0))

font2 = font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)



win_width = 700
win_height = 500
display.set_caption("Game Shooter by Adiba")
window = display. set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost = lost + 1

monsters = sprite.Group()
bullets = sprite.Group()
img_enemy = 'ufo.png'
for i in range(1, 8):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

finish = False

run = True
while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:

        window.blit(background,(0,0))
        text = font2.render("Score: " + str(score), 1,
                            (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Missed: " + str(lost), 1,
                                 (255, 255, 255))
        window.blit(text_lose, (10, 50))
        



        ship.update()
        monsters.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        ship.reset()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
            time.delay(500)
            run = False

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            time.delay(500)
            run = False

        

        display.update()



    time.delay(50)