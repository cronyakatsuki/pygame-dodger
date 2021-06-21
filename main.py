import pygame, random, sys

# global variables
windowWidth = 800
windowHeight = 800
fps = 60

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

def redrawGameWindow():
    window.fill((0,0,0))
    
    for baddie in baddies:
        baddie.draw(window)
    man.draw(window)
    
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
timer = 0

# main loop
run = True
while run:
    if timer % baddieSpawnRate == 0:
        baddies.append(enemy())
    
    for baddie in baddies:
        baddie.move()
        
        if man.hitbox.colliderect(baddie.hitbox):
            run = False
        
        if baddie.y + baddie.height + 10 > windowHeight:
            baddies.pop(baddies.index(baddie))
    
    keys = pygame.key.get_pressed()
    
    clock.tick(fps)
    
    man.move(keys)
    
    redrawGameWindow()
    
    timer += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    if keys[pygame.K_ESCAPE]:
        run = False

terminate()