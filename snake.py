import pygame
import random
import time

pygame.init()

width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

snake_block = 20
snake_speed = 50

snake = [[width // 2, height // 2]]
snake_direction = "RIGHT"

food_pos = [random.randrange(1, (width // snake_block)) * snake_block,
            random.randrange(1, (height // snake_block)) * snake_block]

clock = pygame.time.Clock()

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(window, GREEN, [x[0], x[1], snake_block, snake_block])

def generate_food():
    while True:
        pos = [random.randrange(1, (width // snake_block)) * snake_block,
               random.randrange(1, (height // snake_block)) * snake_block]
        if pos not in snake:
            return pos

def auto_move():
    global snake_direction
    head = snake[0]
    food = food_pos

    moves = {
        "RIGHT": (snake_block, 0),
        "LEFT": (-snake_block, 0),
        "UP": (0, -snake_block),
        "DOWN": (0, snake_block)
    }

    def is_safe_move(move):
        new_head = [head[0] + move[0], head[1] + move[1]]
        return (0 <= new_head[0] < width and
                0 <= new_head[1] < height and
                new_head not in snake[1:])

    safe_moves = {}
    for direction, move in moves.items():
        if is_safe_move(move) and direction != opposite_direction(snake_direction):
            new_head = [head[0] + move[0], head[1] + move[1]]
            distance = ((new_head[0] - food[0])**2 + (new_head[1] - food[1])**2)**0.5
            safe_moves[direction] = distance

    if safe_moves:
        return min(safe_moves, key=safe_moves.get)
    
    for direction, move in moves.items():
        if is_safe_move(move):
            return direction

    return snake_direction

def opposite_direction(direction):
    opposites = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
    return opposites.get(direction, direction)

def game_loop():
    global snake_direction, food_pos

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        snake_direction = auto_move()

        if snake_direction == "RIGHT":
            snake.insert(0, [snake[0][0] + snake_block, snake[0][1]])
        elif snake_direction == "LEFT":
            snake.insert(0, [snake[0][0] - snake_block, snake[0][1]])
        elif snake_direction == "UP":
            snake.insert(0, [snake[0][0], snake[0][1] - snake_block])
        elif snake_direction == "DOWN":
            snake.insert(0, [snake[0][0], snake[0][1] + snake_block])

        if snake[0] == food_pos:
            food_pos = generate_food()
        else:
            snake.pop()

        if (snake[0][0] >= width or snake[0][0] < 0 or
            snake[0][1] >= height or snake[0][1] < 0 or
            snake[0] in snake[1:]):
            game_over = True

        if len(snake) == (width // snake_block) * (height // snake_block):
            game_over = True

        window.fill(BLACK)
        pygame.draw.rect(window, RED, [food_pos[0], food_pos[1], snake_block, snake_block])
        draw_snake(snake)
        pygame.display.update()

        clock.tick(snake_speed)

    window.fill(BLACK)
    font = pygame.font.SysFont(None, 50)
    if len(snake) == (width // snake_block) * (height // snake_block):
        text = font.render("You Win!", True, WHITE)
    else:
        text = font.render("Game Over!", True, WHITE)
    window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
if __name__ == "__main__":
    game_loop()
