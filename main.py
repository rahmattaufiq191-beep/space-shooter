import pygame
import random
import os
import asyncio

# ============================================================
# SPACE SHOOTER 2D - VERSI MOBILE + PC
# Gameplay asli dipertahankan: skor, musuh, HP, boss, suara.
# Kontrol mobile: tombol putih transparan + input sentuh.
# ============================================================

pygame.init()

AUDIO_AVAILABLE = True
try:
    pygame.mixer.init()
except pygame.error:
    AUDIO_AVAILABLE = False
    print("[INFO] Audio tidak tersedia.")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter 2D - Python")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 60, 60)
GREEN = (60, 255, 100)
YELLOW = (255, 220, 50)
BLUE = (60, 150, 255)
PURPLE = (180, 50, 255)

font = pygame.font.SysFont("arial", 24, bold=True)
small_font = pygame.font.SysFont("arial", 20)
big_font = pygame.font.SysFont("arial", 55, bold=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# BACKGROUND CADANGAN DAN LOAD GAMBAR
# ============================================================

def create_fallback_background():
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((5, 10, 30))
    for _ in range(150):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        size = random.choice([1, 1, 1, 2])
        pygame.draw.circle(background, WHITE, (x, y), size)
    return background


def load_image(filename, size, alpha=True):
    path = os.path.join(BASE_DIR, filename)
    try:
        image = pygame.image.load(path)
        image = image.convert_alpha() if alpha else image.convert()
        return pygame.transform.scale(image, size)
    except (pygame.error, FileNotFoundError):
        print(f"[PERINGATAN] Gambar tidak ditemukan: {filename}")

        if filename == "background.png":
            return create_fallback_background()

        image = pygame.Surface(size, pygame.SRCALPHA)

        if filename == "player.png":
            pygame.draw.polygon(
                image, BLUE,
                [(size[0] // 2, 0), (0, size[1]),
                 (size[0] // 2, size[1] - 10), (size[0], size[1])]
            )
            pygame.draw.rect(
                image, WHITE,
                (size[0] // 2 - 5, 15, 10, 15)
            )

        elif filename == "enemy.png":
            pygame.draw.ellipse(
                image, RED, (0, 5, size[0], size[1] - 10)
            )
            pygame.draw.circle(
                image, WHITE, (size[0] // 3, size[1] // 2), 4
            )
            pygame.draw.circle(
                image, WHITE, (size[0] * 2 // 3, size[1] // 2), 4
            )

        elif filename == "bullet.png":
            pygame.draw.rect(image, YELLOW, (0, 0, size[0], size[1]))

        elif filename == "boss.png":
            pygame.draw.ellipse(
                image, PURPLE, (0, 15, size[0], size[1] - 20)
            )
            pygame.draw.circle(
                image, RED, (size[0] // 3, size[1] // 2), 10
            )
            pygame.draw.circle(
                image, RED, (size[0] * 2 // 3, size[1] // 2), 10
            )
            pygame.draw.rect(
                image, WHITE,
                (size[0] // 2 - 8, size[1] // 2 - 5, 16, 10)
            )
        else:
            image.fill(BLACK)

        return image


BACKGROUND_IMG = load_image(
    "background.png", (SCREEN_WIDTH, SCREEN_HEIGHT), False
)
PLAYER_IMG = load_image("player.png", (50, 50), True)
ENEMY_IMG = load_image("enemy.png", (40, 40), True)
BULLET_IMG = load_image("bullet.png", (10, 30), True)
BOSS_IMG = load_image("boss.png", (130, 100), True)


# ============================================================
# SUARA
# ============================================================

def load_sound(filename):
    if not AUDIO_AVAILABLE:
        return None
    try:
        return pygame.mixer.Sound(os.path.join(BASE_DIR, filename))
    except (pygame.error, FileNotFoundError):
        print(f"[PERINGATAN] File suara tidak ditemukan: {filename}")
        return None


shoot_sound = load_sound("shoot.ogg")
explosion_sound = load_sound("explosion.ogg")

music_path = os.path.join(BASE_DIR, "background.ogg")
if AUDIO_AVAILABLE:
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError):
        print("[PERINGATAN] background.ogg tidak ditemukan.")


# ============================================================
# KONTROL MOBILE
# ============================================================

CONTROL_SIZE = 64
CONTROL_RECTS = {
    "up": pygame.Rect(90, 510, CONTROL_SIZE, CONTROL_SIZE),
    "left": pygame.Rect(20, 575, CONTROL_SIZE, CONTROL_SIZE),
    "down": pygame.Rect(90, 575, CONTROL_SIZE, CONTROL_SIZE),
    "right": pygame.Rect(160, 575, CONTROL_SIZE, CONTROL_SIZE),
    "shoot": pygame.Rect(680, 565, 100, 100),
}

CONTROL_LABELS = {
    "up": "↑",
    "left": "←",
    "down": "↓",
    "right": "→",
    "shoot": "TEMBAK",
}

# Nilai True berarti tombol sedang ditahan.
mobile_controls = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "shoot": False,
}

# Setiap pointer (jari atau mouse) menyimpan tombol yang disentuh.
active_pointers = {}


def get_control_at_position(pos):
    for name, rect in CONTROL_RECTS.items():
        if rect.collidepoint(pos):
            return name
    return None


def update_mobile_control_states():
    for name in mobile_controls:
        mobile_controls[name] = name in active_pointers.values()


def draw_mobile_controls():
    """Gambar tombol putih transparan di atas gameplay."""
    for name, rect in CONTROL_RECTS.items():
        button_surface = pygame.Surface(rect.size, pygame.SRCALPHA)

        # Isi putih sangat transparan.
        pygame.draw.rect(
            button_surface,
            (255, 255, 255, 38),
            button_surface.get_rect(),
            border_radius=16,
        )
        screen.blit(button_surface, rect.topleft)

        # Bingkai putih transparan.
        border_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            border_surface,
            (255, 255, 255, 175),
            border_surface.get_rect(),
            width=2,
            border_radius=16,
        )
        screen.blit(border_surface, rect.topleft)

        label = small_font.render(CONTROL_LABELS[name], True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))


# ============================================================
# SPRITE GROUP DAN DATA GAME
# ============================================================

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_bullets = pygame.sprite.Group()

score = 0
game_over = False
boss_active = False
boss_defeated = False


# ============================================================
# PLAYER
# ============================================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 25
        self.speed = 7
        self.lives = 5
        self.shoot_delay = 250
        self.last_shot = 0
        self.invincible_until = 0

    def update(self):
        keys = pygame.key.get_pressed()

        # Keyboard PC tetap berfungsi.
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or mobile_controls["left"]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or mobile_controls["right"]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w] or mobile_controls["up"]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or mobile_controls["down"]:
            self.rect.y += self.speed

        # Batas area permainan.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot = current_time
            if shoot_sound:
                shoot_sound.play()


# ============================================================
# ENEMY
# ============================================================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_bonus=0):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed = random.randint(2, 5) + speed_bonus

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)


# ============================================================
# PELURU PEMAIN
# ============================================================

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BULLET_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


# ============================================================
# BOSS
# ============================================================

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = BOSS_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.top = 40
        self.max_hp = 30
        self.hp = 30
        self.speed_x = 4
        self.shoot_delay = 900
        self.last_shot = 0

    def update(self):
        self.rect.x += self.speed_x

        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x *= -1

        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_delay:
            self.shoot()
            self.last_shot = current_time

    def shoot(self):
        bullet = BossBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        boss_bullets.add(bullet)


class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((14, 28), pygame.SRCALPHA)
        pygame.draw.rect(self.image, PURPLE, (0, 0, 14, 28))
        pygame.draw.circle(self.image, RED, (7, 14), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# ============================================================
# PEMBUAT MUSUH DAN BOSS
# ============================================================

def get_speed_bonus():
    return score // 50


def create_enemy():
    enemy = Enemy(get_speed_bonus())
    all_sprites.add(enemy)
    enemies.add(enemy)


def spawn_boss():
    global boss_active
    if boss_active:
        return
    boss = Boss()
    all_sprites.add(boss)
    boss_group.add(boss)
    boss_active = True
    print("BOSS MUNCUL! BOSS HP: 30")


# ============================================================
# PEMAIN DAN MUSUH AWAL
# ============================================================

player = Player()
all_sprites.add(player)

for _ in range(8):
    create_enemy()


# ============================================================
# HUD
# ============================================================

def draw_hud():
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (15, 15))

    hp_color = RED if player.lives <= 2 else GREEN
    hp_text = font.render(f"HP: {player.lives}", True, hp_color)
    screen.blit(hp_text, (15, 45))


def draw_boss_hp():
    if not boss_active or len(boss_group) == 0:
        return

    boss = boss_group.sprites()[0]
    bar_width = 400
    bar_height = 25
    x = (SCREEN_WIDTH - bar_width) // 2
    y = 15

    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    hp_width = int(bar_width * max(0, boss.hp) / boss.max_hp)
    pygame.draw.rect(screen, GREEN, (x, y, hp_width, bar_height))
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)

    boss_text = small_font.render(
        f"BOSS HP: {boss.hp}/{boss.max_hp}", True, WHITE
    )
    screen.blit(boss_text, (x + 120, y + 2))


def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    title = big_font.render("GAME OVER", True, RED)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 280)))

    final_score = font.render(f"Skor Akhir: {score}", True, WHITE)
    screen.blit(final_score, final_score.get_rect(center=(SCREEN_WIDTH // 2, 350)))

    restart = small_font.render("Tekan R untuk bermain lagi", True, WHITE)
    screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, 410)))

    exit_text = small_font.render("Tekan ESC untuk keluar", True, WHITE)
    screen.blit(exit_text, exit_text.get_rect(center=(SCREEN_WIDTH // 2, 445)))


def draw_boss_defeated():
    if boss_defeated:
        text = small_font.render("BOSS DIKALAHKAN! +100 SCORE", True, YELLOW)
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, 80)))


# ============================================================
# RESET GAME
# ============================================================

def reset_game():
    global player, score, game_over, boss_active, boss_defeated

    all_sprites.empty()
    enemies.empty()
    bullets.empty()
    boss_group.empty()
    boss_bullets.empty()

    active_pointers.clear()
    for name in mobile_controls:
        mobile_controls[name] = False

    score = 0
    game_over = False
    boss_active = False
    boss_defeated = False

    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        create_enemy()


# ============================================================
# MAIN LOOP
# ============================================================

async def main():
    global score, game_over, boss_active, boss_defeated

    running = True

    while running:
        clock.tick(FPS)

        # ----------------------------------------------------
        # INPUT KEYBOARD, MOUSE, DAN LAYAR SENTUH
        # ----------------------------------------------------
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()

                if event.key == pygame.K_r and game_over:
                    reset_game()

            # Mouse: berguna untuk pengujian tombol di komputer.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    active_pointers["mouse"] = get_control_at_position(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_pointers.pop("mouse", None)

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0] and "mouse" in active_pointers:
                    active_pointers["mouse"] = get_control_at_position(event.pos)

            # Sentuhan HP: koordinat FINGER memakai nilai normalisasi 0.0–1.0.
            elif event.type == pygame.FINGERDOWN:
                pos = (
                    int(event.x * SCREEN_WIDTH),
                    int(event.y * SCREEN_HEIGHT),
                )
                active_pointers[event.finger_id] = get_control_at_position(pos)

            elif event.type == pygame.FINGERMOTION:
                pos = (
                    int(event.x * SCREEN_WIDTH),
                    int(event.y * SCREEN_HEIGHT),
                )
                if event.finger_id in active_pointers:
                    active_pointers[event.finger_id] = get_control_at_position(pos)

            elif event.type == pygame.FINGERUP:
                active_pointers.pop(event.finger_id, None)

        update_mobile_control_states()

        # ----------------------------------------------------
        # UPDATE GAME
        # ----------------------------------------------------
        if not game_over:
            all_sprites.update()

            # Menembak terus selama tombol TEMBAK ditahan.
            if mobile_controls["shoot"]:
                player.shoot()

            if score >= 200 and not boss_active and not boss_defeated:
                spawn_boss()

            # Peluru pemain mengenai musuh.
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for enemy in hits:
                score += 10
                if explosion_sound:
                    explosion_sound.play()
                create_enemy()

            # Peluru pemain mengenai boss.
            if boss_active:
                boss_hits = pygame.sprite.groupcollide(
                    boss_group, bullets, False, True
                )
                for boss, hit_bullets in boss_hits.items():
                    boss.hp -= len(hit_bullets)

                    if boss.hp <= 0:
                        boss.kill()
                        boss_group.empty()
                        boss_active = False
                        boss_defeated = True
                        score += 100

                        for bullet in list(boss_bullets):
                            bullet.kill()

                        if explosion_sound:
                            explosion_sound.play()

                        print("BOSS DIKALAHKAN! BONUS +100 SCORE")

            # Peluru boss mengenai pemain.
            boss_bullet_hits = pygame.sprite.spritecollide(
                player, boss_bullets, True
            )
            if boss_bullet_hits:
                player.lives -= len(boss_bullet_hits)
                player.lives = max(0, player.lives)

                if explosion_sound:
                    explosion_sound.play()

                if player.lives <= 0:
                    game_over = True

            # Pemain bertabrakan dengan musuh.
            current_time = pygame.time.get_ticks()
            if current_time >= player.invincible_until:
                hit_enemies = pygame.sprite.spritecollide(
                    player, enemies, True
                )

                if hit_enemies:
                    player.lives -= len(hit_enemies)
                    player.lives = max(0, player.lives)
                    player.invincible_until = current_time + 1000

                    if explosion_sound:
                        explosion_sound.play()

                    for _ in hit_enemies:
                        create_enemy()

                    if player.lives <= 0:
                        game_over = True

        # ----------------------------------------------------
        # GAMBAR LAYAR
        # ----------------------------------------------------
        screen.blit(BACKGROUND_IMG, (0, 0))
        all_sprites.draw(screen)
        draw_hud()
        draw_boss_hp()
        draw_boss_defeated()

        if game_over:
            draw_game_over()

        # Tombol selalu digambar setelah background dan sprite,
        # supaya tidak tertutup oleh gambar game.
        draw_mobile_controls()

        pygame.display.flip()
        await asyncio.sleep(0)

    if AUDIO_AVAILABLE:
        pygame.mixer.music.stop()
    pygame.quit()


asyncio.run(main())
