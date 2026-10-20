import pygame
import random
import os
import sys

# ============================================================
# SPACE SHOOTER 2D
# PYTHON + PYGAME
# ============================================================

# ============================================================
# 1. INISIALISASI
# ============================================================

pygame.init()

AUDIO_AVAILABLE = True

try:
    pygame.mixer.init()
except pygame.error:
    AUDIO_AVAILABLE = False
    print("[INFO] Audio tidak tersedia.")


# ============================================================
# 2. KONFIGURASI
# ============================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "Space Shooter 2D - Python"
)

clock = pygame.time.Clock()


# ============================================================
# 3. WARNA
# ============================================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 60, 60)
GREEN = (60, 255, 100)
YELLOW = (255, 220, 50)

BLUE = (60, 150, 255)
PURPLE = (180, 50, 255)


# ============================================================
# 4. FONT
# ============================================================

font = pygame.font.SysFont(
    "arial",
    24,
    bold=True
)

small_font = pygame.font.SysFont(
    "arial",
    20
)

big_font = pygame.font.SysFont(
    "arial",
    55,
    bold=True
)


# ============================================================
# 5. FOLDER PROGRAM
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 6. BACKGROUND CADANGAN
# ============================================================

def create_fallback_background():

    background = pygame.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )
    )

    background.fill(
        (5, 10, 30)
    )

    # Membuat bintang
    for i in range(150):

        x = random.randint(
            0,
            SCREEN_WIDTH - 1
        )

        y = random.randint(
            0,
            SCREEN_HEIGHT - 1
        )

        size = random.choice(
            [1, 1, 1, 2]
        )

        pygame.draw.circle(
            background,
            WHITE,
            (x, y),
            size
        )

    return background


# ============================================================
# 7. LOAD IMAGE
# ============================================================

def load_image(
    filename,
    size,
    alpha=True
):

    path = os.path.join(
        BASE_DIR,
        filename
    )

    try:

        image = pygame.image.load(
            path
        )

        if alpha:

            image = image.convert_alpha()

        else:

            image = image.convert()

        image = pygame.transform.scale(
            image,
            size
        )

        return image

    except (
        pygame.error,
        FileNotFoundError
    ):

        print(
            f"[PERINGATAN] File gambar tidak ditemukan: {filename}"
        )

        # ====================================================
        # BACKGROUND
        # ====================================================

        if filename == "background.png":

            return create_fallback_background()


        # ====================================================
        # PLAYER
        # ====================================================

        if filename == "player.png":

            image = pygame.Surface(
                size,
                pygame.SRCALPHA
            )

            pygame.draw.polygon(
                image,
                BLUE,
                [
                    (
                        size[0] // 2,
                        0
                    ),
                    (
                        0,
                        size[1]
                    ),
                    (
                        size[0] // 2,
                        size[1] - 10
                    ),
                    (
                        size[0],
                        size[1]
                    )
                ]
            )

            pygame.draw.rect(
                image,
                WHITE,
                (
                    size[0] // 2 - 5,
                    15,
                    10,
                    15
                )
            )

            return image


        # ====================================================
        # ENEMY
        # ====================================================

        if filename == "enemy.png":

            image = pygame.Surface(
                size,
                pygame.SRCALPHA
            )

            pygame.draw.ellipse(
                image,
                RED,
                (
                    0,
                    5,
                    size[0],
                    size[1] - 10
                )
            )

            pygame.draw.circle(
                image,
                WHITE,
                (
                    size[0] // 3,
                    size[1] // 2
                ),
                4
            )

            pygame.draw.circle(
                image,
                WHITE,
                (
                    size[0] * 2 // 3,
                    size[1] // 2
                ),
                4
            )

            return image


        # ====================================================
        # BULLET
        # ====================================================

        if filename == "bullet.png":

            image = pygame.Surface(
                size,
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                image,
                YELLOW,
                (
                    0,
                    0,
                    size[0],
                    size[1]
                )
            )

            return image


        # ====================================================
        # BOSS
        # ====================================================

        if filename == "boss.png":

            image = pygame.Surface(
                size,
                pygame.SRCALPHA
            )

            # Badan Boss
            pygame.draw.ellipse(
                image,
                PURPLE,
                (
                    0,
                    15,
                    size[0],
                    size[1] - 20
                )
            )

            # Mata kiri
            pygame.draw.circle(
                image,
                RED,
                (
                    size[0] // 3,
                    size[1] // 2
                ),
                10
            )

            # Mata kanan
            pygame.draw.circle(
                image,
                RED,
                (
                    size[0] * 2 // 3,
                    size[1] // 2
                ),
                10
            )

            # Tengah
            pygame.draw.rect(
                image,
                WHITE,
                (
                    size[0] // 2 - 8,
                    size[1] // 2 - 5,
                    16,
                    10
                )
            )

            return image


        # ====================================================
        # DEFAULT
        # ====================================================

        image = pygame.Surface(
            size
        )

        image.fill(
            BLACK
        )

        return image


# ============================================================
# 8. LOAD ASSET
# ============================================================

BACKGROUND_IMG = load_image(
    "background.png",
    (
        SCREEN_WIDTH,
        SCREEN_HEIGHT
    ),
    False
)

PLAYER_IMG = load_image(
    "player.png",
    (50, 50),
    True
)

ENEMY_IMG = load_image(
    "enemy.png",
    (40, 40),
    True
)

BULLET_IMG = load_image(
    "bullet.png",
    (10, 30),
    True
)

BOSS_IMG = load_image(
    "boss.png",
    (130, 100),
    True
)


# ============================================================
# 9. LOAD SOUND
# ============================================================

def load_sound(filename):

    if not AUDIO_AVAILABLE:

        return None

    path = os.path.join(
        BASE_DIR,
        filename
    )

    try:

        return pygame.mixer.Sound(
            path
        )

    except (
        pygame.error,
        FileNotFoundError
    ):

        print(
            f"[PERINGATAN] File suara tidak ditemukan: {filename}"
        )

        return None


shoot_sound = load_sound(
    "shoot.ogg"
)

explosion_sound = load_sound(
    "explosion.ogg"
)


# ============================================================
# 10. BACKGROUND MUSIC
# ============================================================

music_path = os.path.join(
    BASE_DIR,
    "background.ogg"
)

if AUDIO_AVAILABLE:

    try:

        pygame.mixer.music.load(
            music_path
        )

        pygame.mixer.music.set_volume(
            0.3
        )

        pygame.mixer.music.play(
            -1
        )

    except (
        pygame.error,
        FileNotFoundError
    ):

        print(
            "[PERINGATAN] background.mp3 tidak ditemukan."
        )


# ============================================================
# 11. SPRITE GROUP
# ============================================================

all_sprites = pygame.sprite.Group()

enemies = pygame.sprite.Group()

bullets = pygame.sprite.Group()

boss_group = pygame.sprite.Group()

boss_bullets = pygame.sprite.Group()


# ============================================================
# 12. DATA GAME
# ============================================================

score = 0

game_over = False

# Status Boss
boss_active = False

boss_defeated = False

# ============================================================
# KONTROL MOBILE
# ============================================================

mobile_controls = {
    "left": False,
    "right": False,
    "up": False,
    "down": False,
    "shoot": False
}

# Ukuran tombol
CONTROL_SIZE = 64
CONTROL_MARGIN = 18

# Transparansi tombol
CONTROL_ALPHA = 85

# Warna Tombol
CONTROL_COLOR = (255, 255, 255)
SHOOT_COLOR = (255, 255, 255)

# Posisi tombol pada layar game 800 x 700
CONTROL_RECTS = {
    "up": pygame.Rect(90, 510, 64, 64),
    "left": pygame.Rect(20, 575, 64, 64),
    "down": pygame.Rect(90, 575, 64, 64),
    "right": pygame.Rect(160, 575, 64, 64),
    "shoot": pygame.Rect(680, 570, 95, 95)
}

# Menyimpan tombol yang sedang ditekan
active_pointers = {}


def get_control_at_position(pos):
    for name, rect in CONTROL_RECTS.items():
        if rect.collidepoint(pos):
            return name

    return None


def update_mobile_control_states():
    for name in mobile_controls:
        mobile_controls[name] = (
            name in active_pointers.values()
        )


# ============================================================
# 13. CLASS PLAYER
# ============================================================

class Player(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = PLAYER_IMG

        self.rect = self.image.get_rect()

        # Posisi awal
        self.rect.centerx = (
            SCREEN_WIDTH // 2
        )

        self.rect.bottom = (
            SCREEN_HEIGHT - 25
        )

        # Kecepatan
        self.speed = 7

        # HP
        self.lives = 5

        # Cooldown tembakan
        self.shoot_delay = 250

        self.last_shot = 0

        # Kebal setelah terkena
        self.invincible_until = 0


    # ========================================================
    # GERAK
    # ========================================================

    def update(self):

        keys = pygame.key.get_pressed()

        # KIRI
        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        ):

            self.rect.x -= self.speed


        # KANAN
        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):

            self.rect.x += self.speed
        # ATAS
        if mobile_controls["up"]:
            self.rect.y -= self.speed

        # BAWAH
        if mobile_controls["down"]:
            self.rect.y += self.speed

        # Batas atas
        if self.rect.top < 0:
            self.rect.top = 0

        # Batas bawah
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Batas kiri
        if self.rect.left < 0:

            self.rect.left = 0


        # Batas kanan
        if self.rect.right > SCREEN_WIDTH:

            self.rect.right = SCREEN_WIDTH


    # ========================================================
    # TEMBAK
    # ========================================================

    def shoot(self):

        current_time = (
            pygame.time.get_ticks()
        )

        if (
            current_time
            - self.last_shot
            >= self.shoot_delay
        ):

            bullet = Bullet(
                self.rect.centerx,
                self.rect.top
            )

            all_sprites.add(
                bullet
            )

            bullets.add(
                bullet
            )

            self.last_shot = (
                current_time
            )

            if shoot_sound:

                shoot_sound.play()


# ============================================================
# 14. CLASS ENEMY
# ============================================================

class Enemy(pygame.sprite.Sprite):

    def __init__(
        self,
        speed_bonus=0
    ):

        super().__init__()

        self.image = ENEMY_IMG

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(
            0,
            SCREEN_WIDTH
            - self.rect.width
        )

        self.rect.y = random.randint(
            -150,
            -40
        )

        # Kecepatan berdasarkan score
        self.speed = (
            random.randint(2, 5)
            + speed_bonus
        )


    def update(self):

        self.rect.y += self.speed

        # Jika keluar layar
        if self.rect.top > SCREEN_HEIGHT:

            self.reset_position()


    def reset_position(self):

        self.rect.x = random.randint(
            0,
            SCREEN_WIDTH
            - self.rect.width
        )

        self.rect.y = random.randint(
            -150,
            -40
        )


# ============================================================
# 15. CLASS BULLET PLAYER
# ============================================================

class Bullet(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y
    ):

        super().__init__()

        self.image = BULLET_IMG

        self.rect = self.image.get_rect()

        self.rect.centerx = x

        self.rect.bottom = y

        self.speed = -10


    def update(self):

        self.rect.y += self.speed

        # Hapus jika keluar layar
        if self.rect.bottom < 0:

            self.kill()


# ============================================================
# 16. CLASS BOSS
# ============================================================

class Boss(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = BOSS_IMG

        self.rect = self.image.get_rect()

        # Posisi awal Boss
        self.rect.centerx = (
            SCREEN_WIDTH // 2
        )

        self.rect.top = 40

        # HP Boss
        self.max_hp = 30

        self.hp = 30

        # Gerakan
        self.speed_x = 4

        # Tembakan Boss
        self.shoot_delay = 900

        self.last_shot = 0


    # ========================================================
    # UPDATE BOSS
    # ========================================================

    def update(self):

        # Gerak kiri-kanan
        self.rect.x += self.speed_x


        # Batas kiri
        if self.rect.left <= 0:

            self.rect.left = 0

            self.speed_x *= -1


        # Batas kanan
        if self.rect.right >= SCREEN_WIDTH:

            self.rect.right = SCREEN_WIDTH

            self.speed_x *= -1


        # Tembak
        current_time = (
            pygame.time.get_ticks()
        )

        if (
            current_time
            - self.last_shot
            >= self.shoot_delay
        ):

            self.shoot()

            self.last_shot = (
                current_time
            )


    # ========================================================
    # TEMBAK BOSS
    # ========================================================

    def shoot(self):

        bullet = BossBullet(
            self.rect.centerx,
            self.rect.bottom
        )

        all_sprites.add(
            bullet
        )

        boss_bullets.add(
            bullet
        )


# ============================================================
# 17. CLASS BOSS BULLET
# ============================================================

class BossBullet(pygame.sprite.Sprite):

    def __init__(
        self,
        x,
        y
    ):

        super().__init__()

        self.image = pygame.Surface(
            (14, 28),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.image,
            PURPLE,
            (
                0,
                0,
                14,
                28
            )
        )

        pygame.draw.circle(
            self.image,
            RED,
            (
                7,
                14
            ),
            5
        )

        self.rect = self.image.get_rect()

        self.rect.centerx = x

        self.rect.top = y

        self.speed = 7


    def update(self):

        self.rect.y += self.speed

        # Hapus jika keluar layar
        if self.rect.top > SCREEN_HEIGHT:

            self.kill()


# ============================================================
# 18. KECEPATAN MUSUH
# ============================================================

def get_speed_bonus():

    # Setiap 50 score,
    # kecepatan bertambah 1

    return score // 50


# ============================================================
# 19. CREATE ENEMY
# ============================================================

def create_enemy():

    enemy = Enemy(
        get_speed_bonus()
    )

    all_sprites.add(
        enemy
    )

    enemies.add(
        enemy
    )


# ============================================================
# 20. SPAWN BOSS
# ============================================================

def spawn_boss():

    global boss_active

    # Jangan buat Boss kedua
    if boss_active:

        return


    boss = Boss()

    all_sprites.add(
        boss
    )

    boss_group.add(
        boss
    )

    boss_active = True

    print(
        "================================"
    )

    print(
        "       BOSS MUNCUL!"
    )

    print(
        "       BOSS HP: 30"
    )

    print(
        "================================"
    )


# ============================================================
# 21. PLAYER
# ============================================================

player = Player()

all_sprites.add(
    player
)


# ============================================================
# 22. MUSUH AWAL
# ============================================================

for i in range(8):

    create_enemy()


# ============================================================
# 23. HUD
# ============================================================

def draw_hud():

    # SCORE
    score_text = font.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (15, 15)
    )


    # HP PLAYER
    hp_color = GREEN

    if player.lives <= 2:

        hp_color = RED

    hp_text = font.render(
        f"HP: {player.lives}",
        True,
        hp_color
    )

    screen.blit(
        hp_text,
        (15, 45)
    )


# ============================================================
# 24. BOSS HP BAR
# ============================================================

def draw_boss_hp():

    if not boss_active:

        return


    if len(boss_group) == 0:

        return


    boss = boss_group.sprites()[0]


    # Ukuran bar
    bar_width = 400

    bar_height = 25


    # Posisi
    x = (
        SCREEN_WIDTH
        - bar_width
    ) // 2

    y = 15


    # Background bar
    pygame.draw.rect(
        screen,
        RED,
        (
            x,
            y,
            bar_width,
            bar_height
        )
    )


    # Hitung HP
    hp_width = int(
        bar_width
        * boss.hp
        / boss.max_hp
    )


    # HP aktif
    pygame.draw.rect(
        screen,
        GREEN,
        (
            x,
            y,
            hp_width,
            bar_height
        )
    )


    # Border
    pygame.draw.rect(
        screen,
        WHITE,
        (
            x,
            y,
            bar_width,
            bar_height
        ),
        2
    )


    # Tulisan
    boss_text = small_font.render(
        f"BOSS HP: {boss.hp}/{boss.max_hp}",
        True,
        WHITE
    )

    screen.blit(
        boss_text,
        (
            x + 120,
            y + 2
        )
    )


# ============================================================
# 25. GAME OVER
# ============================================================

def draw_game_over():

    overlay = pygame.Surface(
        (
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        ),
        pygame.SRCALPHA
    )

    overlay.fill(
        (
            0,
            0,
            0,
            190
        )
    )

    screen.blit(
        overlay,
        (0, 0)
    )


    # GAME OVER
    game_over_text = big_font.render(
        "GAME OVER",
        True,
        RED
    )

    screen.blit(
        game_over_text,
        game_over_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                280
            )
        )
    )


    # SCORE
    score_text = font.render(
        f"Skor Akhir: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        score_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                350
            )
        )
    )


    # RESTART
    restart_text = small_font.render(
        "Tekan R untuk bermain lagi",
        True,
        WHITE
    )

    screen.blit(
        restart_text,
        restart_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                410
            )
        )
    )


    # EXIT
    quit_text = small_font.render(
        "Tekan ESC untuk keluar",
        True,
        WHITE
    )

    screen.blit(
        quit_text,
        quit_text.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                445
            )
        )
    )


# ============================================================
# 26. BOSS DEFEATED MESSAGE
# ============================================================

def draw_boss_defeated():

    if boss_defeated:

        text = small_font.render(
            "BOSS DIKALAHKAN! +100 SCORE",
            True,
            YELLOW
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    SCREEN_WIDTH // 2,
                    80
                )
            )
        )


# ============================================================
# 27. RESET GAME
# ============================================================

def reset_game():

    global player
    global score
    global game_over
    global boss_active
    global boss_defeated


    # Hapus semua sprite
    all_sprites.empty()

    enemies.empty()

    bullets.empty()

    boss_group.empty()

    boss_bullets.empty()


    # Reset score
    score = 0


    # Reset game
    game_over = False


    # Reset Boss
    boss_active = False

    boss_defeated = False


    # Player baru
    player = Player()

    all_sprites.add(
        player
    )


    # Musuh baru
    for i in range(8):

        create_enemy()
def draw_mobile_controls():
    labels = {
        "up": "ATAS",
        "left": "KIRI",
        "down": "BAWAH",
        "right": "KANAN",
        "shoot": "TEMBAK"
    }

    for name, rect in CONTROL_RECTS.items():
        color = (
            SHOOT_COLOR
            if name == "shoot"
            else CONTROL_COLOR
        )

        surface = pygame.Surface(
            rect.size,
            pygame.SRCALPHA
        )

        surface.fill((*color, CONTROL_ALPHA))

        screen.blit(surface, rect.topleft)

        # Garis putih transparan
        border_surface = pygame.Surface(
            rect.size,
            pygame.SRCALPHA
        )
        
        pygame.draw.rect(
            border_surface,
            (255, 255, 255, 150),
            border_surface.get_rect(),
            2,
            border_radius=10
        )

        screen.blit(
            border_surface,
            rect.topleft
        )

        label = small_font.render(
            labels[name],
            True,
            WHITE
        )

        screen.blit(
            label,
            label.get_rect(center=rect.center)
        )

# ============================================================
# 28. MAIN LOOP
# ============================================================

import asyncio


async def main():
    global running, score, game_over, boss_active, boss_defeated, player

    running = True


    while running:

        # FPS
        clock.tick(FPS)


        # ========================================================
        # EVENT
        # ========================================================

        for event in pygame.event.get():

                        # SENTUHAN / MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    active_pointers["mouse"] = (
                        get_control_at_position(event.pos)
                    )

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    active_pointers.pop("mouse", None)

            # LAYAR SENTUH
            elif event.type == pygame.FINGERDOWN:
                pos = (
                    int(event.x * SCREEN_WIDTH),
                    int(event.y * SCREEN_HEIGHT)
                )

                active_pointers[event.finger_id] = (
                    get_control_at_position(pos)
                )

            elif event.type == pygame.FINGERUP:
                active_pointers.pop(event.finger_id, None)

            update_mobile_control_states()


            # CLOSE WINDOW
            if event.type == pygame.QUIT:

                running = False


            # KEYBOARD
            if event.type == pygame.KEYDOWN:


                # ESC
                if event.key == pygame.K_ESCAPE:

                    running = False


                # SPACE
                if (
                    event.key == pygame.K_SPACE
                    and not game_over
                ):

                    player.shoot()


                # RESTART
                if (
                    event.key == pygame.K_r
                    and game_over
                ):

                    reset_game()


        # ========================================================
        # UPDATE
        # ========================================================

        if not game_over:


            # Update semua sprite
            all_sprites.update()

            # Tembak terus selama tombol mobile ditahan
            if mobile_controls["shoot"]:
                player.shoot()


            # ====================================================
            # BOSS MUNCUL SAAT SCORE 200
            # ====================================================

            if (
                score >= 200
                and not boss_active
                and not boss_defeated
            ):

                spawn_boss()


            # ====================================================
            # BULLET PLAYER VS ENEMY
            # ====================================================

            hits = pygame.sprite.groupcollide(
                enemies,
                bullets,
                True,
                True
            )


            for enemy in hits:

                # Score +10
                score += 10


                # Suara ledakan
                if explosion_sound:

                    explosion_sound.play()


                # Buat musuh baru
                create_enemy()


            # ====================================================
            # BULLET PLAYER VS BOSS
            # ====================================================

            if boss_active:

                boss_hits = pygame.sprite.groupcollide(
                    boss_group,
                    bullets,
                    False,
                    True
                )


                for boss in boss_hits:

                    # Setiap peluru = -1 HP
                    damage = len(
                        boss_hits[boss]
                    )

                    boss.hp -= damage


                    # Jika Boss mati
                    if boss.hp <= 0:

                        # Hapus Boss
                        boss.kill()

                        boss_group.empty()

                        # Status
                        boss_active = False

                        boss_defeated = True

                        # Bonus score
                        score += 100


                        # Hapus peluru Boss
                        for bullet in boss_bullets:

                            bullet.kill()


                        if explosion_sound:

                            explosion_sound.play()


                        print(
                            "================================"
                        )

                        print(
                            "       BOSS DIKALAHKAN!"
                        )

                        print(
                            "       BONUS +100 SCORE"
                        )

                        print(
                            "================================"
                        )


            # ====================================================
            # BOSS BULLET VS PLAYER
            # ====================================================

            boss_bullet_hits = pygame.sprite.spritecollide(
                player,
                boss_bullets,
                True
            )


            if boss_bullet_hits:

                # Setiap peluru Boss
                # mengurangi 1 HP
                damage = len(
                    boss_bullet_hits
                )

                player.lives -= damage


                # Cegah HP negatif
                if player.lives < 0:

                    player.lives = 0


                # Suara
                if explosion_sound:

                    explosion_sound.play()


                # Game Over
                if player.lives <= 0:

                    game_over = True


            # ====================================================
            # PLAYER VS ENEMY
            # ====================================================

            current_time = (
                pygame.time.get_ticks()
            )


            # Player tidak sedang kebal
            if (
                current_time
                >= player.invincible_until
            ):

                hit_enemies = pygame.sprite.spritecollide(
                    player,
                    enemies,
                    True
                )


                if hit_enemies:

                    # Kurangi HP
                    player.lives -= len(
                        hit_enemies
                    )


                    # Cegah HP negatif
                    if player.lives < 0:

                        player.lives = 0


                    # Kebal 1 detik
                    player.invincible_until = (
                        current_time + 1000
                    )


                    # Suara
                    if explosion_sound:

                        explosion_sound.play()


                    # Ganti musuh
                    for enemy in hit_enemies:

                        create_enemy()


                    # Game Over
                    if player.lives <= 0:

                        game_over = True


        # ========================================================
        # DRAW BACKGROUND
        # ========================================================

        screen.blit(
            BACKGROUND_IMG,
            (0, 0)
        )


        # ========================================================
        # DRAW SPRITE
        # ========================================================

        all_sprites.draw(
            screen
        )


        # ========================================================
        # HUD
        # ========================================================

        draw_hud()


        # ========================================================
        # BOSS HP
        # ========================================================

        draw_boss_hp()


        # ========================================================
        # BOSS DEFEATED
        # ========================================================

        draw_boss_defeated()


        # ========================================================
        # GAME OVER
        # ========================================================

        if game_over:

            draw_game_over()


        # ========================================================
        # DISPLAY
        # ========================================================
        # TOMBOL MOBILE
        draw_mobile_controls()

        pygame.display.flip()
        await asyncio.sleep(0)


    # ============================================================
    # 29. KELUAR
    # ============================================================

    if AUDIO_AVAILABLE:
        pygame.mixer.music.stop()
    pygame.quit()


asyncio.run(main())
