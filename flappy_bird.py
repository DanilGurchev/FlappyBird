import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

WHITE, BLACK, YELLOW, RED = (255, 255, 255), (0, 0, 0), (255, 255, 0), (255, 0, 0)
clock = pygame.time.Clock()
FPS = 60

#загрузка ресурсов
def load_assets():
    try:
        bird_img = pygame.image.load("assets/bird.png")
        pipe_img = pygame.image.load("assets/pipe.png")
        pipe_img = pygame.transform.scale(pipe_img, (100, 300))
        background_img = pygame.image.load("assets/background.png")
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        flap_sound = pygame.mixer.Sound("assets/flap.wav")
        collision_sound = pygame.mixer.Sound("assets/collision.wav")
        point_sound = pygame.mixer.Sound("assets/point.wav")
    except pygame.error as e:
        print(f"Ошибка загрузки ресурсов: {e}")
        sys.exit()
    return bird_img, pipe_img, background_img, flap_sound, collision_sound, point_sound

bird_img, pipe_img, background_img, flap_sound, collision_sound, point_sound = load_assets()

bird_img = pygame.transform.scale(bird_img, (40, 40))
bird_rect = bird_img.get_rect(center=(50, HEIGHT // 2))

difficulties = {
    "easy": {"gravity": 0.25, "pipe_speed": 3, "pipe_gap": 200, "pipe_frequency": 2200}, 
    "medium": {"gravity": 0.35, "pipe_speed": 4, "pipe_gap": 150, "pipe_frequency": 1200},
    "hard": {"gravity": 0.5, "pipe_speed": 6, "pipe_gap": 100, "pipe_frequency": 900},
}
current_difficulty = "easy"

gravity = difficulties[current_difficulty]["gravity"]
pipe_speed = difficulties[current_difficulty]["pipe_speed"]
pipe_gap = difficulties[current_difficulty]["pipe_gap"]
pipe_frequency = difficulties[current_difficulty]["pipe_frequency"]
bird_movement = 0
score = 0
font = pygame.font.Font(None, 40)

pipe_list = []
passed_pipes = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, pipe_frequency)

#создание труб
def create_pipe():
    pipe_height = random.randint(200, 400)
    top_pipe = pipe_img.get_rect(midbottom=(WIDTH + 60, pipe_height - pipe_gap // 2))
    bottom_pipe = pipe_img.get_rect(midtop=(WIDTH + 60, pipe_height + pipe_gap // 2))
    return top_pipe, bottom_pipe

#движение труб
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return [pipe for pipe in pipes if pipe.right > 0]

#отрисовка труб
def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_img if pipe.bottom >= HEIGHT else pygame.transform.flip(pipe_img, False, True), pipe)

#проверка на столкновение
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.Sound.play(collision_sound)
            return False
    return bird_rect.top > 0 and bird_rect.bottom < HEIGHT

#отображение счета
def display_score(score):
    text = font.render(f"Счет: {round(score)}", True, BLACK)  # Округляем score перед отображением
    text_rect = text.get_rect()
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20), 2)
    screen.blit(text, (text_rect.x + 10, text_rect.y + 10))

#отображение главного меню
def display_menu():
    screen.blit(background_img, (0, 0))
    menu_font = pygame.font.Font(None, 60)
    options = [("FLAPPY BIRD", (WIDTH // 2, HEIGHT // 4)), 
               ("Начать игру (SPACE)", (WIDTH // 2, HEIGHT // 2)), 
               ("Настройки (S)", (WIDTH // 2, HEIGHT * 5 // 8)), 
               ("Выход (ESC)", (WIDTH // 2, HEIGHT * 3 // 4))]
    
    for text, pos in options:
        render_text(text, pos)

    pygame.display.update()

#рендеринг текста
def render_text(text, pos):
    menu_font = pygame.font.Font(None, 40)
    text_surf = menu_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=pos)
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20), 2)
    screen.blit(text_surf, text_rect)

#отображение настроек
def display_settings():
    global current_difficulty
    settings_running = True
    while settings_running:
        screen.blit(background_img, (0, 0))
        settings_text = pygame.font.Font(None, 40).render("Настройки сложности", True, BLACK)
        options = [("Легкий (S)", "easy"), ("Средний (D)", "medium"), ("Сложный (F)", "hard")]
        
        for i, (text, difficulty) in enumerate(options):
            color = YELLOW if current_difficulty == difficulty else BLACK
            render_text_with_color(text, (WIDTH // 2, 150 + i * 100), color)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    current_difficulty = "easy"
                elif event.key == pygame.K_d:
                    current_difficulty = "medium"
                elif event.key == pygame.K_f:
                    current_difficulty = "hard"
                elif event.key == pygame.K_ESCAPE:
                    settings_running = False
                    show_menu()

#рендеринг текста с цветом
def render_text_with_color(text, pos, color):
    settings_font = pygame.font.Font(None, 40)
    text_surf = settings_font.render(text, True, color)
    text_rect = text_surf.get_rect(center=pos)
    pygame.draw.rect(screen, WHITE, text_rect.inflate(20, 20), 2)
    screen.blit(text_surf, text_rect)

#игровой цикл
def game_loop():
    global bird_movement, bird_rect, pipe_list, passed_pipes, score, gravity, pipe_speed, pipe_gap, pipe_frequency

    gravity = difficulties[current_difficulty]["gravity"]
    pipe_speed = difficulties[current_difficulty]["pipe_speed"]
    pipe_gap = difficulties[current_difficulty]["pipe_gap"]
    pipe_frequency = difficulties[current_difficulty]["pipe_frequency"]

    bird_movement = 0
    bird_rect.center = (50, HEIGHT // 2)
    pipe_list.clear()
    passed_pipes.clear()
    score = 0

    running = True
    while running:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = -6
                    pygame.mixer.Sound.play(flap_sound)

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_img, bird_rect)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        if not check_collision(pipe_list):
            running = False

        passed_this_pair = False
        for pipe in pipe_list:
            if pipe.centerx < 50 and pipe not in passed_pipes:
                if not passed_this_pair:
                    score += 0.5
                    passed_pipes.append(pipe)
                    pygame.mixer.Sound.play(point_sound)
                    passed_this_pair = True

        display_score(score)  
        pygame.display.update()
        clock.tick(FPS)

#отображение главного меню
def show_menu():
    menu_running = True
    while menu_running:
        display_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_s:
                    display_settings()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

show_menu()
