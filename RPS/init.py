import pygame
import random
import math
from typing import List

pygame.init()

WIDTH: int = 480
HEIGHT: int = 480
FPS: int = 144
NUM_OBJECTS: int = 25
OBJECT_SIZE: int = 50

WHITE = (255, 255, 255)

screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

rock_img: pygame.Surface = pygame.transform.scale(pygame.image.load("rock.png"), (OBJECT_SIZE, OBJECT_SIZE))
paper_img: pygame.Surface = pygame.transform.scale(pygame.image.load("paper.png"), (OBJECT_SIZE, OBJECT_SIZE))
scissors_img: pygame.Surface = pygame.transform.scale(pygame.image.load("scissors.png"), (OBJECT_SIZE, OBJECT_SIZE))

class GameObject:
    def __init__(self, x: int, y: int, img: pygame.Surface, type: str) -> None:
        self.x: float = x
        self.y: float = y
        self.img: pygame.Surface = img
        self.type: str = type
        self.width: int = img.get_width()
        self.height: int = img.get_height()
        self.speed: float = random.uniform(0.8, 1.5)
        self.vx: float = self.speed * math.cos(random.uniform(1, 1 * math.pi))
        self.vy: float = self.speed * math.sin(random.uniform(1, 1 * math.pi))
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = (self.x, self.y)

        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.vx = -self.vx
        if self.y <= 0 or self.y + self.height >= HEIGHT:
            self.vy = -self.vy

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.img, (self.x, self.y))

    def check_collision(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)

    def resolve_collision(self, other: 'GameObject') -> None:
        overlap_x: float = min(self.rect.right, other.rect.right) - max(self.rect.left, other.rect.left)
        overlap_y: float = min(self.rect.bottom, other.rect.bottom) - max(self.rect.top, other.rect.top)

        if overlap_x < overlap_y:
            if self.rect.centerx < other.rect.centerx:
                self.x -= overlap_x / 2
                other.x += overlap_x / 2
            else:
                self.x += overlap_x / 2
                other.x -= overlap_x / 2
            self.vx, other.vx = -self.vx, -other.vx
        else:
            if self.rect.centery < other.rect.centery:
                self.y -= overlap_y / 2
                other.y += overlap_y / 2
            else:
                self.y += overlap_y / 2
                other.y -= overlap_y / 2
            self.vy, other.vy = -self.vy, -other.vy

        self.rect.topleft = (self.x, self.y)
        other.rect.topleft = (other.x, other.y)

    def handle_interaction(self, other: 'GameObject') -> None:
        if self.type == "Rock" and other.type == "Scissors":
            other.type = "Rock"
            other.img = rock_img
        elif self.type == "Scissors" and other.type == "Paper":
            other.type = "Scissors"
            other.img = scissors_img
        elif self.type == "Paper" and other.type == "Rock":
            other.type = "Paper"
            other.img = paper_img
        elif other.type == "Rock" and self.type == "Scissors":
            self.type = "Rock"
            self.img = rock_img
        elif other.type == "Scissors" and self.type == "Paper":
            self.type = "Scissors"
            self.img = scissors_img
        elif other.type == "Paper" and self.type == "Rock":
            self.type = "Paper"
            self.img = paper_img

def is_overlapping(new_obj: GameObject, objects: List[GameObject]) -> bool:
    for obj in objects:
        if new_obj.check_collision(obj):
            return True
    return False

def create_objects() -> List[GameObject]:
    objects: List[GameObject] = []
    for _ in range(NUM_OBJECTS):
        while True:
            x: int = random.randint(0, WIDTH - OBJECT_SIZE)
            y: int = random.randint(0, HEIGHT - OBJECT_SIZE)
            type: str = random.choice(["Rock", "Paper", "Scissors"])
            img: pygame.Surface = rock_img if type == "Rock" else paper_img if type == "Paper" else scissors_img
            new_obj: GameObject = GameObject(x, y, img, type)
            if not is_overlapping(new_obj, objects):
                objects.append(new_obj)
                break
    return objects

def run() -> bool:
    objects: List[GameObject] = create_objects()
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for obj in objects:
            obj.move()
            obj.draw(screen)

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if objects[i].check_collision(objects[j]):
                    objects[i].resolve_collision(objects[j])
                    objects[i].handle_interaction(objects[j])

        pygame.display.flip()

        first_type: str = objects[0].type
        if all(obj.type == first_type for obj in objects):
            running = False

    return False

if __name__ == "__main__":
    run()
