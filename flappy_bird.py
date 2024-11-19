import pygame
import sys
import random

# Инициализация pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Попытка загрузить изображения и звуки с обработкой ошибок
try:
    bird_img = pygame.image.load("assets/bird.png")  # Изображение птицы
    pipe_img = pygame.image.load("assets/pipe.png")  # Изображение трубы
    pipe_img = pygame.transform.scale(pipe_img, (100, 300))  # Масштабирование трубы
    background_img = pygame.image.load("assets/background.png")  # Фон
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Растягиваем фон на весь экран
    flap_sound = pygame.mixer.Sound("assets/flap.wav")
    collision_sound = pygame.mixer.Sound("assets/collision.wav")
    point_sound = pygame.mixer.Sound("assets/point.wav")
except pygame.error as e:
    print(f"Ошибка при загрузке ресурсов: {e}")
    sys.exit()

# Масштабирование и настройка
bird_img = pygame.transform.scale(bird_img, (40, 40))
bird_rect = bird_img.get_rect(center=(50, HEIGHT // 2))

# Параметры игры
gravity = 0.25
bird_movement = 0
score = 0
font = pygame.font.Font(None, 40)

# Параметры труб
pipe_gap = 150
pipe_speed = 4
pipe_list = []

# Список пройденных труб
passed_pipes = []

def create_pipe():
    """Создает верхнюю и нижнюю трубы с зазором."""
    pipe_height = random.randint(200, 400)
    top_pipe = pipe_img.get_rect(midbottom=(WIDTH + 60, pipe_height - pipe_gap // 2))
    bottom_pipe = pipe_img.get_rect(midtop=(WIDTH + 60, pipe_height + pipe_gap // 2))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    """Двигает трубы влево и удаляет пройденные."""
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
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            pygame.mixer.Sound.play(collision_sound)
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        pygame.mixer.Sound.play(collision_sound)
        return False

    return True

def draw_text_with_shadow(text, font, color, x, y, shadow_offset=(2, 2), shadow_color=BLACK):
    """Функция рисования текста с тенью и контуром."""
    # Рисуем тень
    text_shadow = font.render(text, True, shadow_color)
    screen.blit(text_shadow, (x + shadow_offset[0], y + shadow_offset[1]))
    
    # Рисуем основной текст
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def display_score(score):
    """Отображает текущий счет с тенью и контуром для текста."""
    draw_text_with_shadow(f"Счет: {score}", font, YELLOW, 10, 10)

def display_menu():
    """Отображает главное меню с фоном."""
    screen.blit(background_img, (0, 0)) 
    menu_font = pygame.font.Font(None, 60)
    title = menu_font.render("Flappy Bird", True, BLACK)
    start_text = pygame.font.Font(None, 40).render("НАЧАТЬ ИГРУ (SPACE)", True, BLACK)
    quit_text = pygame.font.Font(None, 40).render("ВЫХОД (ESC)", True, BLACK)

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))

    screen.blit(title, title_rect)
    screen.blit(start_text, start_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.update()

# Таймер для создания труб
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Основной игровой цикл
def game_loop():
    global bird_movement, bird_rect, pipe_list, passed_pipes, score 
   
    bird_movement = 0
    bird_rect.center = (50, HEIGHT // 2)
    
    pipe_list.clear()
    passed_pipes.clear()
    
    score = 0
    
    running = True
    
    while running:
        screen.blit(background_img,(0 ,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement=-6  
                    pygame.mixer.Sound.play(flap_sound)

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

        # Птичка 
        bird_movement += gravity 
        bird_rect.centery += bird_movement 
        screen.blit(bird_img,bird_rect)

        # Трубы 
        pipe_list=move_pipes(pipe_list) 
        draw_pipes(pipe_list)

        # Проверка на столкновение 
        if not check_collision(pipe_list):
            running=False 

        # Проверка прохождения труб и начисление очков 
        for pipe in pipe_list:
            if pipe.centerx < 50 and pipe not in passed_pipes:  
                score +=1 
                passed_pipes.append(pipe)  
                pygame.mixer.Sound.play(point_sound)

        # Отображаем счет 
        display_score(score) 
        pygame.display.update() 
        clock.tick(FPS)

# Меню игры 
def show_menu():
    
   menu_running=True
   
   while menu_running: 
       display_menu()

       for event in pygame.event.get():
           if event.type ==pygame.QUIT: 
               pygame.quit() 
               sys.exit() 
           if event.type ==pygame.KEYDOWN: 
               if event.key==pygame.K_SPACE: 
                   game_loop()  
               if event.key==pygame.K_ESCAPE: 
                   pygame.quit() 
                   sys.exit()

# Запуск меню 
show_menu()
