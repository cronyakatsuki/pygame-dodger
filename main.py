import pygame, random, sys, time

# global variables
WIDTH = 800
HEIGHT = 800
FPS = 60
TEXT_COLOR = (255,255,255)

# initialize pygame and create a window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Dodger")
pygame.mouse.set_visible(False)

class Game:
    def __init__(self):
        self.timer = 0
        self.run = True
        self.lost = False
    
    def play(self, keys, baddies, baddies_spawn_rate, player):
        if self.timer % baddies_spawn_rate == 0:
            baddies.append(enemy())
        
        for baddie in baddies:
            baddie.move()
            
            if player.hitbox.colliderect(baddie.hitbox):
                self.lost = True
            
            if baddie.y + baddie.height + 10 > HEIGHT:
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

# player class
class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_alive = True
        self.move_speed = 5
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, window):
        pygame.draw.rect(window, (0,255,0), (self.x, self.y, self.width, self.height))
        
    def move(self, keys):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width - 50:
            self.x += self.move_speed
        if keys[pygame.K_LEFT] and self.x > 0 + 50:
            self.x -= self.move_speed
        if keys[pygame.K_UP] and self.y > 0 + WIDTH / 2:
            self.y -= self.move_speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height - 50:
            self.y += self.move_speed

# enemy class
class enemy:
    def __init__(self):
        self.start_line = 100
        self.end_line = 700
        self.min_size = 10
        self.max_size = 40
        self.min_speed = 1
        self.max_speed = 8
        self.y = 10
        self.x = random.randint(self.start_line, self.end_line)
        self.width = self.height = random.randint(self.min_size, self.max_size)
        self.vel = random.randint(self.min_speed, self.max_speed)
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def draw(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y, self.width, self.height))
    
    def move(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.y += self.vel

# create a quit function
def terminate():
    pygame.quit()
    sys.exit()
    
def draw_text(text, font, window, x,y):
    textObj = font.render(text, 1, TEXT_COLOR)
    textRect = textObj.get_rect()
    textRect.topleft = (x - textObj.get_width() // 2, y - textObj.get_height() // 2)
    window.blit(textObj, textRect)

def wait_for_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    dodger.run = False
                    dodger.retry = True
                return

def reset_game(player, baddies, game_logic):
    player.x = 100
    player.y = 700
    
    baddies.clear()
    
    game_logic.timer = 0
    
def ask_for_retry(keys, game_logic):
    window.fill((0,0,0))
    draw_text("Wanna try again? y/n", font, window, HEIGHT / 2, WIDTH / 2)
    pygame.display.update()
    
    if keys[pygame.K_y]:
        game_logic.lost = False
    if keys[pygame.K_n]:
        game_logic.run = False

man = Player(100, 700, 30, 30)
baddies = []
BADDIE_SPAWN_RATE = 40
font = pygame.font.SysFont(None, 48)
dodger = Game()

draw_text('Dodger', font, window, (WIDTH / 2), (HEIGHT / 2 - 30))
draw_text('Press a key to start.', font, window, (WIDTH / 2), (HEIGHT / 2 + 30))
    
pygame.display.update()
    
wait_for_key_press()

# main loop
while dodger.run:
    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()
    
    if dodger.lost:
        if dodger.timer > 0:
            reset_game(man, baddies, dodger)
        ask_for_retry(keys, dodger)
    else :
        dodger.play(keys, baddies, BADDIE_SPAWN_RATE, man)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        
    if keys[pygame.K_ESCAPE]:
        dodger.run = False

window.fill((0,0,0))
draw_text('Goodbye', font, window, (WIDTH / 2 ), (HEIGHT / 2))
pygame.display.update()
time.sleep(1)
terminate()