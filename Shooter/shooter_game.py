from pygame import *
from random import *
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

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
                
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0            
kost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y < 0:
            self.kill()

#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

#Персонажи игры:

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy( 'ufo.png' , randint(80, win_width - 80), 0, 60,60,randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()


player = Player('rocket.png', 2, 400,80,80, 50)
#final = GameSprite('treasure.png', win_width - 120, win_height - 80, 0)

game = True
clock = time.Clock()
FPS = 60
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
shoot = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 36)

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        #событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                shoot.play()
                player.fire()

    if not finish:
        window.blit(background,(0, 0))
        player.update()
        monsters.update()
        bullets.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            kost = kost + 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5)) 
            monsters.add(monster)
        if kost >= 10:
            finish = True
            text_win2 = font2.render('ТЫ ВЫЙГРАЛ!',1, (255, 255, 255))
            window.blit(text_win2,(270,230))
        if lost >= 3 or sprite.spritecollide(player, monsters,False):
            finish = True
            text_lose2 = font2.render('ТЫ ПРОИГРАЛ!',1, (255, 255, 255))
            window.blit(text_lose2,(270,230))
        text_win = font1.render('Очков: ' + str(kost),1, (255, 255, 255))
        text_lose = font2.render('Пропущено: ' + str(lost),1, (255, 255, 255))
        window.blit(text_lose,(10,50))
        window.blit(text_win,(10,100))
    display.update()
    clock.tick(FPS)