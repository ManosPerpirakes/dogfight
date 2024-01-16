from pygame import *
from random import *
font.init()

class Player():
    def __init__(self, x, y, w, h, imgname):
        self.rect = rect.Rect(x, y, w, h)
        self.img = transform.scale(image.load(imgname), (w, h))
    def showplayer(self):
        w.blit(self.img, (self.rect.x, self.rect.y))

class Rocket():
    def __init__(self, x, y, w, h, imgname):
        self.rect = rect.Rect(x, y, w, h)
        self.img = transform.scale(image.load(imgname), (w, h))
    def move(self):
        global playerhitpoints
        self.rect.x -= 8
        if player.rect.y > self.rect.y:
            self.rect.y += 1
        if player.rect.y < self.rect.y:
            self.rect.y -= 1
        if self.rect.colliderect(player.rect):
            self.rect.x = 1500
            self.rect.y = 750/2
            playerhitpoints -= 20
        if self.rect.x < -50:
            self.rect.x = 1500
            self.rect.y = 750/2
    def show(self):
        w.blit(self.img, (self.rect.x, self.rect.y))

def move_player():
    global keys
    if (keys[K_w] or keys[K_UP]) and player.rect.y > 0:
        player.rect.y -= 5
    if (keys[K_s] or keys[K_DOWN]) and player.rect.y < 700:
        player.rect.y += 5

def move_bomber():
    global wait
    if wait == 5:
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
        bullets.append(rect.Rect(1050, (bomber.rect.y + 50), 10, 2))
    for i in bullets:
        i.x -= 50
        draw.rect(w, (0, 0, 0), i)
        if i.colliderect(player.rect):
            playerhitpoints -= 0.5

def draw_bullets():
    for i in bullets:
        draw.rect(w, (0, 0, 0), i)
        if i.x < -20:
            bullets.remove(i)

def showhitpoints():
    w.blit(font.SysFont('Arial', 30).render('hitpoints: ' + str(round(playerhitpoints)), True, (0, 0, 0)), (50, 50))

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
            missile = Player(200, player.rect.y + 70, 50, 25, "missile.png")
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
        if bomber.rect.y > missile.rect.y:
            missile.rect.y += 2
        if bomber.rect.y < missile.rect.y:
            missile.rect.y -= 2
        if missile.rect.colliderect(bomber.rect):
            score += 1
            missile = None
        if missile.rect.x > 1600:
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
    player = Player(100, 300, 150, 35, 'fighter_img.png')
    bomber = Player(1100, 500, 300, 104, 'bomber_img.jpg')
    rocket = Rocket(1500, 750/2, 50, 25, "missile2.png")
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
        if playerhitpoints < 1:
            playerhitpoints = 0
        fps = int(clock.get_fps())
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
            rocket.move()
        rocket.show()
        display_players()
        draw_bullets()
        showlock()
        showscore()
        showhitpoints()
        w.blit(font.SysFont('Arial', 30).render("FPS: " + str(fps), True, (0, 0, 0)), (50, 180))
        display.update()
        clock.tick(60)
    close = False
    while close != True:
        fps = int(clock.get_fps())
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
        w.blit(font.SysFont('Arial', 30).render("FPS: " + str(fps), True, (0, 0, 0)), (50, 180))
        display.update()
        clock.tick(60)