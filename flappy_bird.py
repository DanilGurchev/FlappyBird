import pygame
import sys
import random

# Инициализация pygame
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

# Загрузка ресурсов
bird_img = pygame.image.load("assets/bird.png")  
pipe_img = pygame.image.load("assets/pipe.png")  
pipe_img = pygame.transform.scale(pipe_img, (100, 300))  
background_img = pygame.image.load("assets/background.png") 
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Фон для игры
gear_img = pygame.image.load("assets/gear.png")  # Изображение шестеренки для настроек
gear_img = pygame.transform.scale(gear_img, (40, 40))  # Масштабируем шестеренку

# Масштабирование птички
bird_img = pygame.transform.scale(bird_img, (40, 40))
bird_rect = bird_img.get_rect(center=(50, HEIGHT // 2))

# Параметры игры
gravity = 0.25
bird_movement = 0
score = 0
font = pygame.font.Font(None, 40)

# Звуки
flap_sound = pygame.mixer.Sound("flap.wav")
collision_sound = pygame.mixer.Sound("collision.wav")
point_sound = pygame.mixer.Sound("point.wav")

pipe_gap = 150
pipe_speed = 4
pipe_list = []

# Уровни сложности
level = 1
level_up_score = 5  # Очки для повышения уровня сложности

def create_pipe():
    """Создает трубы с зазором."""
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
        if pipe.bottom >= HEIGHT:  # Верхняя труба
            screen.blit(pipe_img, pipe)
        else:  # Нижняя труба
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)

def check_collision(pipes):
    """Проверка столкновений с трубами и краем экрана."""
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.Sound.play(collision_sound)
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        pygame.mixer.Sound.play(collision_sound)
        return False
    return True

def display_score(score, level):
    """Отображение счета и уровня сложности."""
    score_surface = font.render(f"Счет: {score}", True, BLACK)
    level_surface = font.render(f"Уровень: {level}", True, BLACK)
    screen.blit(score_surface, (10, 10))
    screen.blit(level_surface, (10, 50))

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

def game_loop():
    """Основной игровой цикл."""
    global bird_movement
    global score
    global pipe_speed
    global level
    pipe_list = []
    passed_pipes = []  

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
                    pygame.mixer.Sound.play(flap_sound)

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

        # Счетчик
        for pipe in pipe_list:
            if pipe.top < HEIGHT // 2 and pipe.centerx < 100 and pipe.centerx > 95 and pipe not in passed_pipes:
                passed_pipes.append(pipe)  
                score += 1 
                pygame.mixer.Sound.play(point_sound)

        # Изменение уровня сложности
        if score >= level * level_up_score:
            level += 1
            pipe_speed += 1  # Увеличиваем скорость
            pygame.time.set_timer(SPAWNPIPE, max(1000 - level * 50, 600))  # Уменьшаем интервал спауна труб

        display_score(score, level)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

def settings_menu():
    """Меню настроек для выбора сложности."""
    global pipe_speed, level_up_score
    settings_running = True
    while settings_running:
        screen.blit(background_img, (0, 0))  # Фон для меню настроек

        font = pygame.font.Font(None, 60)
        text = font.render("Настройки сложности", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))

        # Кнопки сложности
        easy_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        medium_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
        hard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)

        pygame.draw.rect(screen, BLACK, easy_button)
        pygame.draw.rect(screen, BLACK, medium_button)
        pygame.draw.rect(screen, BLACK, hard_button)

        easy_text = pygame.font.Font(None, 40).render("Легкий", True, WHITE)
        medium_text = pygame.font.Font(None, 40).render("Средний", True, WHITE)
        hard_text = pygame.font.Font(None, 40).render("Сложный", True, WHITE)

        screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 70))
        screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 130))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(event.pos):
                    pipe_speed = 3
                    level_up_score = 7
                    settings_running = False
                    game_loop()
                if medium_button.collidepoint(event.pos):
                    pipe_speed = 4
                    level_up_score = 5
                    settings_running = False
                    game_loop()
                if hard_button.collidepoint(event.pos):
                    pipe_speed = 5
                    level_up_score = 3
                    settings_running = False
                    game_loop()

def main_menu():
    """Главное меню игры с фоном и кнопкой настроек."""
    menu_running = True
    while menu_running:
        screen.blit(background_img, (0, 0))  # Рисуем фон

        font = pygame.font.Font(None, 60)
        text = font.render("Flappy Bird", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3))
        
        font_small = pygame.font.Font(None, 30)
        start_text = font_small.render("Нажмите ПРОБЕЛ, чтобы начать", True, BLACK)
        settings_text = font_small.render("Нажмите 'S' для настроек", True, BLACK)
        
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 100))
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 150))
        
        # Кнопка настроек (шестеренка)
        screen.blit(gear_img, (WIDTH - 50, 10))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False
                    game_loop()
                if event.key == pygame.K_s:
                    settings_menu()

# Запуск главного меню
main_menu()
