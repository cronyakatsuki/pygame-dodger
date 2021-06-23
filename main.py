import pygame, random, sys, time

# global variables
windowWidth = 800
windowHeight = 800
fps = 60
textColor = (255,255,255)

# initialize pygame and create a window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Pygame Dodger")
pygame.mouse.set_visible(False)

# create a quit function
def terminate():
    pygame.quit()
    sys.exit()
    
def drawText(text, font, window, x,y):
    textObj = font.render(text, 1, textColor)
    textRect = textObj.get_rect()
    textRect.topleft = (x - textObj.get_width() // 2,y - textObj.get_height() // 2)
    window.blit(textObj, textRect)

def waitForKeyPress():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dodger.run = False
                    dodger.retry = True
                return

def resetGame(player, baddies, gameLogic):
    player.x = 100
    player.y = 700
    
    baddies.clear()
    
    gameLogic.timer = 0
    
def askForRetry(keys, gameLogic):
    window.fill((0,0,0))
    drawText("Wanna try again? y/n", font, window, windowHeight / 2, windowWidth / 2)
    pygame.display.update()
    
    if keys[pygame.K_y]:
        gameLogic.lost = False
    if keys[pygame.K_n]:
        gameLogic.run = False

class game(object):
    def __init__(self):
        self.timer = 0
        self.run = True
        self.lost = False
        pass
    
    def play(self, keys, baddies, baddiesSpawnRate, player):
        if self.timer % baddiesSpawnRate == 0:
            baddies.append(enemy())
        
        for baddie in baddies:
            baddie.move()
            
            if player.hitbox.colliderect(baddie.hitbox):
                self.lost = True
            
            if baddie.y + baddie.height + 10 > windowHeight:
                baddies.pop(baddies.index(baddie))
        
        player.move(keys)
        
        self.timer += 1
        
        self.draw(baddies, player)
    def draw(self, baddies, player):
        window.fill((0,0,0))
        for baddie in baddies:
            baddie.draw(window)
        player.draw(window)
        pygame.display.update()

# enemy class
class enemy(object):
    def __init__(self):
        self.startLine = 100
        self.endLine = 700
        self.minSize = 10
        self.maxSize = 40
        self.minSpeed = 1
        self.maxSpeed = 8
        self.y = 10
        self.x = random.randint(self.startLine, self.endLine)
        self.width = self.height = random.randint(self.minSize, self.maxSize)
        self.vel = random.randint(self.minSpeed, self.maxSpeed)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.y += self.vel

# player class
class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isAlive = True
        self.moveSpeed = 5
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, window):
        pygame.draw.rect(window, (0,255,0), (self.x, self.y, self.width, self.height))
        
    def move(self, keys):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if keys[pygame.K_RIGHT] and self.x < windowWidth - self.width - 50:
            self.x += self.moveSpeed
        if keys[pygame.K_LEFT] and self.x > 0 + 50:
            self.x -= self.moveSpeed
        if keys[pygame.K_UP] and self.y > 0 + windowWidth / 2:
            self.y -= self.moveSpeed
        if keys[pygame.K_DOWN] and self.y < windowHeight - self.height - 50:
            self.y += self.moveSpeed

man = player(100, 700, 30, 30)
baddies = []
baddieSpawnRate = 40
font = pygame.font.SysFont(None, 48)
dodger = game()

drawText('Dodger', font, window, (windowWidth / 2), (windowHeight / 2 - 30))
drawText('Press a key to start.', font, window, (windowWidth / 2), (windowHeight / 2 + 30))
    
pygame.display.update()
    
waitForKeyPress()

# main loop
while dodger.run:
    clock.tick(fps)
    
    keys = pygame.key.get_pressed()
    
    if dodger.lost:
        if dodger.timer > 0:
            resetGame(man, baddies, dodger)
        askForRetry(keys, dodger)
    else :
        dodger.play(keys, baddies, baddieSpawnRate, man)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        
    if keys[pygame.K_ESCAPE]:
        dodger.run = False

window.fill((0,0,0))
drawText('Goodbye', font, window, (windowWidth / 2 ), (windowHeight / 2))
pygame.display.update()
time.sleep(1)
terminate()