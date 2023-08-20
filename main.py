from pygame import *
from random import *
font.init()

class Player():
    def __init__(self, x, y, w, h, text, colour):
        self.rect = rect.Rect(x, y, w, h)
        self.text = font.SysFont('Arial', 40).render(text, True, (0, 0, 0))
        self.colour = colour
    def showplayer(self):
        draw.rect(w, self.colour, self.rect)
        w.blit(self.text, (self.rect.x, self.rect.y))

def move_player():
    global keys
    if (keys[K_w] or keys[K_UP]) and player.rect.y > 0:
        player.rect.y -= 5
    if (keys[K_s] or keys[K_DOWN]) and player.rect.y < 700:
        player.rect.y += 5

def move_bomber():
    global wait
    if wait == 10:
        yadd = randint(-50, 50)
        if (yadd > 0 and (bomber.rect.y < (650 - yadd))) or (yadd < 0 and (bomber.rect.y > (50 + yadd))):
            bomber.rect.y += yadd
        wait = 0
    else:
        wait += 1

def display_players():
    for i in players:
        i.showplayer()

def shoot_bomber():
    global playerhitpoints
    if wait == 0:
        bullets.append(rect.Rect(1050, (bomber.rect.y + 30), 20, 5))
    for i in bullets:
        i.x -= 50
        draw.rect(w, (0, 0, 0), i)
        if i.colliderect(player.rect):
            playerhitpoints -= 5

def showhitpoints():
    w.blit(font.SysFont('Arial', 30).render('hitpoints: ' + str(playerhitpoints), True, (0, 0, 0)), (50, 50))

def checklose():
    global close
    global playerhitpoints
    if playerhitpoints <= 0:
        close = True

def fighterlock():
    global lock
    global missileready
    global missile
    global missilefired
    if ((player.rect.y - bomber.rect.y) < 200) and ((player.rect.y - bomber.rect.y) > (-200)):
        lock += 1
    elif lock < 255:
        lock = 0
    if lock == 255:
        missileready = True
    if missileready:
        if keys[K_SPACE]:
            missile = rect.Rect(200, bomber.rect.y, 50, 20)
            missilefired = True 
            lock = 0
            missileready = False

def movemissile():
    global missile
    global missilefired
    global close
    global score
    try:
        if missilefired:
            missile.x += 10
            missile.y = bomber.rect.y
        if missile.colliderect(bomber.rect):
            score += 1
            missile = None
        draw.rect(w, (255, 0, 0), missile)
    except:
        pass

def showlock():
    global lock
    global wait2
    w.blit(font.SysFont('Arial', 30).render('lock: ', True, (0, 0, 0)), (50, 90))
    if lock < 255:
        draw.rect(w, ((255 - lock), lock, 0), rect.Rect(110, 90, 30, 30))
    else:
        draw.rect(w, (0, 255, 0), rect.Rect(100, 90, 30, 30))
        if wait2 <= 60:
            w.blit(font.SysFont('Arial', 70).render('FIRE MISSILE', True, (255, 0, 0)), (300, 200))

def showscore():
    global score
    w.blit(font.SysFont('Arial', 30).render('score: ' + str(score), True, (0, 0, 0)), (50, 130))

closeall = False
while closeall != True:
    w = display.set_mode((1500, 750))
    display.set_caption('dogfight')
    player = Player(100, 100, 100, 50, 'fighter', (0, 255, 0))
    bomber = Player(1100, 500, 200, 50, 'bomber', (255, 0, 0))
    playerhitpoints = 100
    lock = 0
    missileready = False
    missilefired = False
    wait2 = 0
    score = 0
    players = [player, bomber]
    bullets = []
    clock = time.Clock()
    wait = 0
    close = False
    while close != True:
        wait2 += 1
        if wait2 == 120:
            wait2 = 0
        keys = key.get_pressed()
        w.fill((0, 0, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
        if closeall:
            close = True
        move_player()
        move_bomber()
        shoot_bomber()
        movemissile()
        display_players()
        checklose()
        showhitpoints()
        showlock()
        showscore()
        fighterlock()
        display.update()
        clock.tick(60)
    close = False
    while close != True:
        w.fill((0, 0, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
        if closeall:
            close = True
        showscore()
        display.update()
        clock.tick(60)