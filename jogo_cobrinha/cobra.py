import pygame
import random

# Definindo constantes
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ROSA = (255, 192, 203)
AMARELO = (255, 255, 0)
VIOLETA = (95, 0, 196)
SNAKE_SPEED = 10

# Inicialização do Pygame
pygame.init()
pygame.display.set_caption("O jogo do FELIPÂO")  # Definindo o título da janela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


# Função para desenhar a grade
def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GREEN, (0, y), (WIDTH, y))


# Classe para representar a cobra
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head = self.body[0]
        dx, dy = self.direction
        new_head = ((head[0] + dx) % GRID_WIDTH, (head[1] + dy) % GRID_HEIGHT)

        if new_head in self.body[1:] or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            # A cobra colidiu consigo mesma ou tocou na borda
            return False

        self.body.insert(0, new_head)
        self.body.pop()
        return True

    def change_direction(self, dx, dy):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)

    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, ROSA, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def grow(self):
        tail = self.body[-1]
        dx, dy = self.direction
        new_segment = ((tail[0] - dx) % GRID_WIDTH, (tail[1] - dy) % GRID_HEIGHT)
        self.body.append(new_segment)

    def check_collision(self):
        head = self.body[0]
        return head in self.body[1:]

    def check_food_collision(self, food):
        head = self.body[0]
        return head == food.position


# Classe para representar a comida
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self):
        x, y = self.position
        pygame.draw.rect(screen, VIOLETA, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Função principal do jogo
def game():
    snake = Snake()
    food = Food()
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1, 0)

        if not snake.move():
            # A cobra colidiu consigo mesma ou tocou na borda
            running = False

        if snake.check_food_collision(food):
            snake.grow()
            food = Food()
            score += 1
            if score % 5 == 0:
                global SNAKE_SPEED
                SNAKE_SPEED += 1

        screen.fill(BLACK)
        draw_grid()
        snake.draw()
        food.draw()

        # Este é o placar do jogo
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Pontos: {score}", True, AMARELO)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    return score


# Função para exibir a tela de início
def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    title_text = font.render("O jogo", True, WHITE)
    instructions_text = font.render("Toque para começar", True, AMARELO)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height()))
    screen.blit(instructions_text,
                (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + instructions_text.get_height()))
    pygame.display.update()
    pygame.event.wait()


# Função para exibir a tela de fim de jogo
def show_game_over_screen(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Fim da linha", True, WHITE)
    score_text = font.render(f"Pontos: {score}", True, AMARELO)
    instructions_text = font.render("Você morreu meu amigo, tente novamente", True, WHITE)
    screen.blit(game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height()))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(instructions_text,
                (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 2 + instructions_text.get_height()))
    pygame.display.update()
    pygame.event.wait()


# Loop principal do jogo
running = True
while running:
    show_start_screen()
    score = game()
    show_game_over_screen(score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
