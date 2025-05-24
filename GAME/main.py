import pygame
import random

# إعدادات اللعبة الأساسية
WIDTH, HEIGHT = 800, 600
FPS = 60

# ألوان
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic Spaceships")
clock = pygame.time.Clock()

# تحميل الصور (هنعملهم كصور بسيطة بلون هنا بدل ملفات خارجية)
def create_spaceship_image():
    image = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.polygon(image, BLUE, [(30, 0), (60, 60), (0, 60)])
    return image

def create_enemy_image():
    image = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(image, RED, image.get_rect())
    return image

# كائن السفينة الفضائية
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = create_spaceship_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 100
    
    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -7
        if keys[pygame.K_RIGHT]:
            self.speedx = 7
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# كائن الطلقات
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# كائن الأعداء
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = create_enemy_image()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)

# إعداد المجموعات
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Spaceship()
all_sprites.add(player)

for _ in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

score = 0
running = True

# حلقة اللعبة الأساسية
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    all_sprites.update()
    
    # التحقق من التصادمات
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.health -= 10
        if player.health <= 0:
            running = False
    
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # عرض النتيجة والطاقة
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 50))
    
    pygame.display.flip()

pygame.quit()
