from pygame import *
from random import *
font.init()

class Player():
    def __init__(self, x, y, w, h, imgname):
        self.rect = rect.Rect(x, y, w, h)
        self.img = transform.scale(image.load(imgname), (w, h))
    def showplayer(self):
        w.blit(self.img, (self.rect.x, self.rect.y))

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
        if (yadd > 0 and (bomber.rect.y < (700 - yadd))) or (yadd < 0 and (bomber.rect.y > ((-(yadd)) - 50))):
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
        bullets.append(rect.Rect(1050, (bomber.rect.y + 50), 20, 5))
    for i in bullets:
        i.x -= 50
        draw.rect(w, (0, 0, 0), i)
        if i.colliderect(player.rect):
            playerhitpoints -= 5

def draw_bullets():
    for i in bullets:
        draw.rect(w, (0, 0, 0), i)
        if i.x < -20:
            bullets.remove(i)

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
            missile = Player(200, bomber.rect.y, 50, 25, "missile.png")
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
            missile.rect.x += 10
            missile.rect.y = bomber.rect.y
        if missile.rect.colliderect(bomber.rect):
            score += 1
            missile = None
        missile.showplayer()
    except:
        pass

def calclock():
    global wait2
    wait2 += 1
    if wait2 == 120:
        wait2 = 0

def showlock():
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

def pause():
    global keys
    global pausevar
    global pausewait
    pausewait += 1
    if pausewait > 29:
        if keys[K_1]:
            if pausevar:
                pausevar = False
                pausewait = 0
            else:
                pausevar = True
                pausewait = 0

closeall = False
while closeall != True:
    w = display.set_mode((1500, 750))
    display.set_caption('dogfight')
    player = Player(100, 100, 90, 50, 'fighter_img.png')
    bomber = Player(1100, 500, 140, 100, 'bomber_img.jpg')
    playerhitpoints = 100
    lock = 0
    missileready = False
    missilefired = False
    pausevar = False
    wait2 = 0
    score = 0
    missile = None
    players = [player, bomber]
    bullets = []
    pausewait = 0
    clock = time.Clock()
    wait = 0
    close = False
    while close != True:
        keys = key.get_pressed()
        w.fill((255, 255, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
        if closeall:
            close = True
        pause()
        if not pausevar:
            move_player()
            move_bomber()
            shoot_bomber()
            movemissile()
            checklose()
            fighterlock()
            calclock()
        display_players()
        draw_bullets()
        showlock()
        showscore()
        showhitpoints()
        display.update()
        clock.tick(60)
    close = False
    while close != True:
        w.fill((255, 255, 255))
        for i in event.get():
            if i.type == QUIT:
                close = True
                closeall = True
            if i.type == KEYDOWN:
                if i.key == K_1:
                    close = True
        if closeall:
            close = True
        w.blit(font.SysFont('Arial', 30).render('score: ' + str(score) + (" (1-try again)"), True, (0, 0, 0)), (50, 130))
        display.update()
        clock.tick(60)