import pygame
import sys
import random

# Инициализация pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)


# FPS
clock = pygame.time.Clock()
FPS = 60

# Загрузка ресурсов
bird_img = pygame.image.load("assets/bird.png")  # Изображение птицы
pipe_img = pygame.image.load("assets/pipe.png")  # Изображение трубы
pipe_img = pygame.transform.scale(pipe_img, (60, 400))  # Масштабирование трубы
background_img = pygame.image.load("assets/ background.png")  # Фон

# Масштабирование и настройка
bird_img = pygame.transform.scale(bird_img, (40, 40))
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

# Параметры игры
gravity = 0.25
bird_movement = 0
score = 0
font = pygame.font.Font(None, 40)

# Звуки
flap_sound = pygame.mixer.Sound("flap.wav")
collision_sound = pygame.mixer.Sound("collision.wav")
point_sound = pygame.mixer.Sound("point.wav")

# Параметры труб
pipe_gap = 150
pipe_speed = 4
pipe_list = []

def create_pipe():
    """Создает верхнюю и нижнюю трубы с зазором."""
    pipe_height = random.randint(200, 400)
    top_pipe = pipe_img.get_rect(midbottom=(WIDTH + 60, pipe_height - pipe_gap // 2))
    bottom_pipe = pipe_img.get_rect(midtop=(WIDTH + 60, pipe_height + pipe_gap // 2))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    """Двигает трубы влево."""
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

def draw_pipes(pipes):
    """Рисует трубы на экране."""
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_img, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)

def check_collision(pipes):
    """Проверяет столкновения птицы с трубами или краями экрана."""
    global running
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.Sound.play(collision_sound)
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        pygame.mixer.Sound.play(collision_sound)
        return False

    return True

def display_score(score):
    """Отображает текущий счет."""
    score_surface = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_surface, (10, 10))

# Таймер для создания труб
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Основной игровой цикл
running = True
while running:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6
                pygame.mixer.Sound.play(flap_sound)  # Исправил сюда правильную переменную

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Птичка
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_img, bird_rect)

    # Трубы
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # Столкновения
    if not check_collision(pipe_list):
        running = False

    # Счет
    for pipe in pipe_list:
        if 95 < pipe.centerx < 105:
            score += 1
            pygame.mixer.Sound.play(point_sound)

    display_score(score)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
