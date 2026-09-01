import pygame
import random

# game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

# bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img

# pipe class
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

# game images
background_image = pygame.image.load("flappybirdbg.png")
bird_image_raw = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image_raw, (bird_width, bird_height))
top_pipe_image_raw = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image_raw, (pipe_width, pipe_height))
bottom_pipe_image_raw = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image_raw, (pipe_width, pipe_height))

# game logic
bird = Bird(bird_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0
game_over = False
start_screen = True

start_button = pygame.Rect(0, 0, 180, 54)
start_button.center = (GAME_WIDTH/2, GAME_HEIGHT/2 + 80)

try_again_button = pygame.Rect(0, 0, 190, 54)
try_again_button.center = (GAME_WIDTH/2, GAME_HEIGHT/2 + 90)

def draw_centered_text(text, font_size, y, color="white"):
    text_font = pygame.font.SysFont("Comic Sans MS", font_size)
    text_render = text_font.render(text, True, color)
    text_rect = text_render.get_rect(center=(GAME_WIDTH/2, y))
    window.blit(text_render, text_rect)

def draw_button(rect, text):
    pygame.draw.rect(window, "white", rect, border_radius=8)
    pygame.draw.rect(window, "black", rect, 3, border_radius=8)

    text_font = pygame.font.SysFont("Comic Sans MS", 28)
    text_render = text_font.render(text, True, "black")
    text_rect = text_render.get_rect(center=rect.center)
    window.blit(text_render, text_rect)

def draw():
    window.blit(background_image, (0, 0))
    angle = max(min(-velocity_y * 5, 25), -90)
    rotated_bird = pygame.transform.rotate(bird.img, angle)
    rotated_rect = rotated_bird.get_rect(center=bird.center)
    window.blit(rotated_bird, rotated_rect)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))

def draw_start_screen():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)
    draw_centered_text("Flappy Bird", 48, GAME_HEIGHT/2 - 80)
    draw_centered_text("Press Space or click Start", 22, GAME_HEIGHT/2 - 20)
    draw_button(start_button, "Start")

def draw_game_over_screen():
    draw()
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    window.blit(overlay, (0, 0))

    draw_centered_text("Game Over", 46, GAME_HEIGHT/2 - 80)
    draw_centered_text("Score: " + str(int(score)), 30, GAME_HEIGHT/2 - 25)
    draw_button(try_again_button, "Try Again")

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True

        if bird.colliderect(pipe):
            game_over = True
            return

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/4 - random.random()*(pipe_height/2)
    opening_space = GAME_HEIGHT/4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

    print(len(pipes))

def reset_game():
    global velocity_y, score, game_over
    bird.y = bird_y
    pipes.clear()
    velocity_y = 0
    score = 0
    game_over = False

def start_game():
    global start_screen
    reset_game()
    pygame.event.clear(create_pipes_timer)
    pygame.time.set_timer(create_pipes_timer, 1500)
    start_screen = False

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer and not start_screen and not game_over:
            create_pipes()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_screen and start_button.collidepoint(event.pos):
                start_game()
            elif game_over and try_again_button.collidepoint(event.pos):
                start_game()

        if event.type == pygame.KEYDOWN:
            if start_screen and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                start_game()
            elif game_over and event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN):
                start_game()
            elif event.key in (pygame.K_SPACE, pygame.K_UP):
                velocity_y = -6

    if start_screen:
        draw_start_screen()
    elif game_over:
        draw_game_over_screen()
    else:
        move()
        if game_over:
            draw_game_over_screen()
        else:
            draw()

    pygame.display.update()
    clock.tick(60)
