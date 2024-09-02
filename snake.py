import pygame
import random
import time
from collections import deque
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

def bfs(start, goal, obstacles):
    queue = deque([[start]])
    seen = set([tuple(start)])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if [x, y] == goal:
            return path
        for x2, y2 in ((x+snake_block, y), (x-snake_block, y), (x, y+snake_block), (x, y-snake_block)):
            if (0 <= x2 < width and 0 <= y2 < height and 
                [x2, y2] not in obstacles and 
                (x2, y2) not in seen):
                queue.append(path + [[x2, y2]])
                seen.add((x2, y2))
    return None

def auto_move():
    global snake_direction
    head = snake[0]
    food = food_pos

    obstacles = snake[1:]

    path_to_food = bfs(head, food, obstacles)

    if path_to_food:
        simulated_snake = snake.copy()
        for step in path_to_food[1:]:
            simulated_snake.insert(0, step)
            simulated_snake.pop()
            
            if not bfs(step, simulated_snake[-1], simulated_snake[:-1]):
                path_to_food = None
                break

    if path_to_food:
        next_move = path_to_food[1]
        if next_move[0] > head[0]:
            return "RIGHT"
        elif next_move[0] < head[0]:
            return "LEFT"
        elif next_move[1] < head[1]:
            return "UP"
        elif next_move[1] > head[1]:
            return "DOWN"
    
    path_to_tail = bfs(head, snake[-1], obstacles[:-1])
    if path_to_tail and len(path_to_tail) > 1:
        next_move = path_to_tail[1]
        if next_move[0] > head[0]:
            return "RIGHT"
        elif next_move[0] < head[0]:
            return "LEFT"
        elif next_move[1] < head[1]:
            return "UP"
        elif next_move[1] > head[1]:
            return "DOWN"

    for direction in ["RIGHT", "LEFT", "UP", "DOWN"]:
        if direction == "RIGHT" and [head[0] + snake_block, head[1]] not in obstacles:
            return "RIGHT"
        elif direction == "LEFT" and [head[0] - snake_block, head[1]] not in obstacles:
            return "LEFT"
        elif direction == "UP" and [head[0], head[1] - snake_block] not in obstacles:
            return "UP"
        elif direction == "DOWN" and [head[0], head[1] + snake_block] not in obstacles:
            return "DOWN"

    return snake_direction

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
